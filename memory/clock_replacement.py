"""Clock (Second Chance) Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from models.memory_page import Page, Frame


class ClockReplacement:
    """Clock (Second Chance) page replacement algorithm.
    
    A more efficient approximation of LRU using a circular queue
    and reference bits.
    """
    
    def __init__(self):
        self.name = "Clock (Second Chance)"
        self.clock_hand = 0  # Current position in the circular buffer
        self.page_list: List[Tuple[int, int]] = []  # Pages in circular order
        self.reference_bits: Dict[Tuple[int, int], bool] = {}  # Reference bit for each page
        self.fault_count = 0
        self.hit_count = 0
    
    def select_victim(self, frames: List[Frame],
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page using the Clock algorithm.
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        if not self.page_list:
            # Build page list from frames
            for frame in frames:
                if not frame.is_free and frame.page:
                    key = (frame.page.process_id, frame.page.page_id)
                    if key not in self.page_list:
                        self.page_list.append(key)
                        self.reference_bits[key] = True
        
        if not self.page_list:
            return None, None
        
        # Clock algorithm: circle until finding page with reference bit = 0
        max_iterations = len(self.page_list) * 2  # Safety limit
        iterations = 0
        
        while iterations < max_iterations:
            if self.clock_hand >= len(self.page_list):
                self.clock_hand = 0
            
            key = self.page_list[self.clock_hand]
            pid, page_id = key
            
            # Check if page is still in memory
            if pid not in page_tables or page_id not in page_tables[pid]:
                # Page no longer valid, remove from list
                self.page_list.pop(self.clock_hand)
                if key in self.reference_bits:
                    del self.reference_bits[key]
                iterations += 1
                continue
            
            frame_id = page_tables[pid][page_id]
            if frame_id is None:
                # Page no longer in memory
                self.page_list.pop(self.clock_hand)
                if key in self.reference_bits:
                    del self.reference_bits[key]
                iterations += 1
                continue
            
            # Check reference bit
            if self.reference_bits.get(key, False):
                # Give second chance - clear reference bit
                self.reference_bits[key] = False
                self.clock_hand = (self.clock_hand + 1) % max(1, len(self.page_list))
            else:
                # Found victim
                self.page_list.pop(self.clock_hand)
                if key in self.reference_bits:
                    del self.reference_bits[key]
                return frame_id, key
            
            iterations += 1
        
        # Fallback: evict first page
        if self.page_list:
            key = self.page_list.pop(0)
            pid, page_id = key
            if pid in page_tables and page_id in page_tables[pid]:
                frame_id = page_tables[pid][page_id]
                if frame_id is not None:
                    return frame_id, key
        
        # Last resort: find any occupied frame
        for frame in frames:
            if not frame.is_free and frame.page:
                return frame.frame_id, (frame.page.process_id, frame.page.page_id)
        
        return None, None
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        key = (pid, page_id)
        if key not in self.page_list:
            # Insert at clock hand position
            if self.page_list:
                self.page_list.insert(self.clock_hand, key)
            else:
                self.page_list.append(key)
        self.reference_bits[key] = True
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed (set reference bit)."""
        key = (pid, page_id)
        self.reference_bits[key] = True
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        key = (pid, page_id)
        if key in self.page_list:
            idx = self.page_list.index(key)
            self.page_list.remove(key)
            # Adjust clock hand if needed
            if idx < self.clock_hand:
                self.clock_hand = max(0, self.clock_hand - 1)
        if key in self.reference_bits:
            del self.reference_bits[key]
    
    def simulate(self, reference_string: List[Tuple[int, int]],
                 num_frames: int) -> Dict:
        """Simulate Clock algorithm on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        ref_bits: List[bool] = [False] * num_frames
        clock = 0
        faults = 0
        hits = 0
        history = []
        
        for ref in reference_string:
            if ref in frames:
                # Hit - set reference bit
                hits += 1
                idx = frames.index(ref)
                ref_bits[idx] = True
                history.append({'ref': ref, 'fault': False, 'frames': list(frames)})
            else:
                # Fault
                faults += 1
                
                if None in frames:
                    # Free frame available
                    idx = frames.index(None)
                    frames[idx] = ref
                    ref_bits[idx] = True
                else:
                    # Clock algorithm
                    while True:
                        if ref_bits[clock]:
                            ref_bits[clock] = False
                            clock = (clock + 1) % num_frames
                        else:
                            frames[clock] = ref
                            ref_bits[clock] = True
                            clock = (clock + 1) % num_frames
                            break
                
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
        self.clock_hand = 0
        self.page_list.clear()
        self.reference_bits.clear()
        self.fault_count = 0
        self.hit_count = 0
