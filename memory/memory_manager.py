"""Memory Manager for OS simulation."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from models.memory_page import Page, Frame
from models.process import Process


@dataclass
class PageFaultEvent:
    """Record of a page fault event."""
    timestamp: int
    process_id: int
    page_id: int
    frame_id: Optional[int]  # Frame where page was loaded
    evicted_page: Optional[Tuple[int, int]]  # (process_id, page_id) of evicted page
    fault_type: str  # 'compulsory', 'capacity', 'conflict'


class MemoryManager:
    """Manages virtual memory with paging."""
    
    def __init__(self, num_frames: int = 50, page_size: int = 4096):
        self.num_frames = num_frames
        self.page_size = page_size
        
        # Physical memory frames
        self.frames: List[Frame] = [Frame(i, page_size) for i in range(num_frames)]
        self.free_frames: List[int] = list(range(num_frames))
        
        # Process page tables
        self.page_tables: Dict[int, Dict[int, Optional[int]]] = {}  # pid -> {page_id -> frame_id}
        
        # Page tracking
        self.pages: Dict[Tuple[int, int], Page] = {}  # (pid, page_id) -> Page
        
        # Event logging
        self.page_faults: List[PageFaultEvent] = []
        self.current_time: int = 0
        
        # Statistics
        self.total_accesses: int = 0
        self.fault_count: int = 0
        
        # Replacement algorithm (set externally)
        self.replacement_algorithm = None
    
    def register_process(self, process: Process) -> None:
        """Register a process and create its page table."""
        pid = process.pid
        self.page_tables[pid] = {}
        
        # Create pages for the process
        for page_id in range(process.memory_pages):
            self.pages[(pid, page_id)] = Page(page_id, pid, self.page_size)
            self.page_tables[pid][page_id] = None  # Not loaded yet
    
    def unregister_process(self, pid: int) -> None:
        """Unregister a process and free its frames."""
        if pid not in self.page_tables:
            return
        
        # Free all frames used by this process
        for page_id, frame_id in self.page_tables[pid].items():
            if frame_id is not None:
                self.free_frame(frame_id)
        
        # Remove page table
        del self.page_tables[pid]
        
        # Remove pages
        keys_to_remove = [key for key in self.pages if key[0] == pid]
        for key in keys_to_remove:
            del self.pages[key]
    
    def access_page(self, pid: int, page_id: int, write: bool = False) -> Tuple[bool, Optional[int]]:
        """Access a page, handling page faults if necessary.
        
        Returns: (fault_occurred, frame_id)
        """
        self.total_accesses += 1
        
        if pid not in self.page_tables:
            return True, None  # Process not registered
        
        if page_id not in self.page_tables[pid]:
            return True, None  # Invalid page
        
        frame_id = self.page_tables[pid][page_id]
        
        if frame_id is not None:
            # Page is in memory - hit
            page = self.pages.get((pid, page_id))
            if page:
                page.access(write)
            return False, frame_id
        
        # Page fault - need to load page
        self.fault_count += 1
        frame_id, evicted = self._handle_page_fault(pid, page_id)
        
        if frame_id is not None:
            page = self.pages.get((pid, page_id))
            if page:
                page.access(write)
        
        return True, frame_id
    
    def _handle_page_fault(self, pid: int, page_id: int) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Handle a page fault by loading the page into a frame.
        
        Returns: (frame_id, evicted_page or None)
        """
        evicted = None
        
        # Try to get a free frame
        if self.free_frames:
            frame_id = self.free_frames.pop(0)
            fault_type = 'compulsory'
        else:
            # Need to evict a page
            frame_id, evicted = self._select_victim()
            if frame_id is None:
                return None, None
            fault_type = 'capacity'
        
        # Load the page into the frame
        self._load_page(pid, page_id, frame_id)
        
        # Log the event
        event = PageFaultEvent(
            timestamp=self.current_time,
            process_id=pid,
            page_id=page_id,
            frame_id=frame_id,
            evicted_page=evicted,
            fault_type=fault_type
        )
        self.page_faults.append(event)
        
        return frame_id, evicted
    
    def _select_victim(self) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page to evict using the replacement algorithm.
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        if self.replacement_algorithm is None:
            # Default: FIFO based on frame allocation order
            for frame in self.frames:
                if not frame.is_free and frame.page:
                    victim_page = frame.page
                    return frame.frame_id, (victim_page.process_id, victim_page.page_id)
            return None, None
        
        # Use the replacement algorithm
        return self.replacement_algorithm.select_victim(
            self.frames, self.pages, self.page_tables
        )
    
    def _load_page(self, pid: int, page_id: int, frame_id: int) -> None:
        """Load a page into a frame."""
        frame = self.frames[frame_id]
        
        # If frame has a page, unmap it first
        if frame.page is not None:
            old_page = frame.page
            old_pid = old_page.process_id
            old_page_id = old_page.page_id
            if old_pid in self.page_tables and old_page_id in self.page_tables[old_pid]:
                self.page_tables[old_pid][old_page_id] = None
        
        # Load new page
        page = self.pages.get((pid, page_id))
        if page:
            frame.allocate(page)
            self.page_tables[pid][page_id] = frame_id
    
    def free_frame(self, frame_id: int) -> None:
        """Free a frame."""
        if 0 <= frame_id < len(self.frames):
            frame = self.frames[frame_id]
            if frame.page:
                pid = frame.page.process_id
                page_id = frame.page.page_id
                if pid in self.page_tables and page_id in self.page_tables[pid]:
                    self.page_tables[pid][page_id] = None
            frame.deallocate()
            if frame_id not in self.free_frames:
                self.free_frames.append(frame_id)
    
    def get_page_fault_rate(self) -> float:
        """Get the page fault rate."""
        if self.total_accesses == 0:
            return 0.0
        return (self.fault_count / self.total_accesses) * 100
    
    def get_memory_usage(self) -> Dict:
        """Get current memory usage statistics."""
        used_frames = sum(1 for f in self.frames if not f.is_free)
        return {
            'total_frames': self.num_frames,
            'used_frames': used_frames,
            'free_frames': len(self.free_frames),
            'usage_percentage': (used_frames / self.num_frames) * 100,
            'total_accesses': self.total_accesses,
            'page_faults': self.fault_count,
            'fault_rate': self.get_page_fault_rate()
        }
    
    def get_frame_map(self) -> List[Dict]:
        """Get a map of all frames and their contents."""
        return [
            {
                'frame_id': f.frame_id,
                'is_free': f.is_free,
                'process_id': f.page.process_id if f.page else None,
                'page_id': f.page.page_id if f.page else None
            }
            for f in self.frames
        ]
    
    def set_time(self, time: int) -> None:
        """Set the current simulation time."""
        self.current_time = time
    
    def set_replacement_algorithm(self, algorithm) -> None:
        """Set the page replacement algorithm."""
        self.replacement_algorithm = algorithm
    
    def reset(self) -> None:
        """Reset the memory manager."""
        for frame in self.frames:
            frame.deallocate()
        self.free_frames = list(range(self.num_frames))
        self.page_tables.clear()
        self.pages.clear()
        self.page_faults.clear()
        self.total_accesses = 0
        self.fault_count = 0
        self.current_time = 0
