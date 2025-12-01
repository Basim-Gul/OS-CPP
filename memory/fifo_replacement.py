"""FIFO Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from collections import deque
from models.memory_page import Page, Frame


class FIFOReplacement:
    """First-In-First-Out page replacement algorithm.
    
    Evicts the page that has been in memory the longest.
    """
    
    def __init__(self):
        self.name = "FIFO"
        self.page_queue: deque = deque()  # (pid, page_id) in order of arrival
        self.fault_count = 0
        self.hit_count = 0
    
    def select_victim(self, frames: List[Frame], 
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page to evict.
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        while self.page_queue:
            victim_key = self.page_queue.popleft()
            pid, page_id = victim_key
            
            # Check if this page is still in memory
            if pid in page_tables and page_id in page_tables[pid]:
                frame_id = page_tables[pid][page_id]
                if frame_id is not None:
                    return frame_id, victim_key
        
        # Fallback: find any occupied frame
        for frame in frames:
            if not frame.is_free and frame.page:
                return frame.frame_id, (frame.page.process_id, frame.page.page_id)
        
        return None, None
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        self.page_queue.append((pid, page_id))
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed (no-op for FIFO)."""
        pass  # FIFO doesn't update on access
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        try:
            self.page_queue.remove((pid, page_id))
        except ValueError:
            pass  # Page wasn't in queue
    
    def simulate(self, reference_string: List[Tuple[int, int]], 
                 num_frames: int) -> Dict:
        """Simulate FIFO on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        page_queue: deque = deque()
        faults = 0
        hits = 0
        history = []
        
        for ref in reference_string:
            if ref in frames:
                # Hit
                hits += 1
                history.append({'ref': ref, 'fault': False, 'frames': list(frames)})
            else:
                # Fault
                faults += 1
                
                if None in frames:
                    # Free frame available
                    idx = frames.index(None)
                    frames[idx] = ref
                else:
                    # Evict oldest page
                    victim = page_queue.popleft()
                    idx = frames.index(victim)
                    frames[idx] = ref
                
                page_queue.append(ref)
                history.append({'ref': ref, 'fault': True, 'frames': list(frames)})
        
        return {
            'algorithm': self.name,
            'faults': faults,
            'hits': hits,
            'fault_rate': faults / len(reference_string) * 100 if reference_string else 0,
            'history': history
        }
    
    def reset(self) -> None:
        """Reset the algorithm state."""
        self.page_queue.clear()
        self.fault_count = 0
        self.hit_count = 0
