"""LRU Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from collections import OrderedDict
from models.memory_page import Page, Frame


class LRUReplacement:
    """Least Recently Used page replacement algorithm.
    
    Evicts the page that hasn't been used for the longest time.
    """
    
    def __init__(self):
        self.name = "LRU"
        # OrderedDict maintains order of access (most recent at end)
        self.access_order: OrderedDict = OrderedDict()
        self.fault_count = 0
        self.hit_count = 0
    
    def select_victim(self, frames: List[Frame],
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page to evict (least recently used).
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        # Find the least recently used page that's still in memory
        for victim_key in self.access_order.keys():
            pid, page_id = victim_key
            
            if pid in page_tables and page_id in page_tables[pid]:
                frame_id = page_tables[pid][page_id]
                if frame_id is not None:
                    del self.access_order[victim_key]
                    return frame_id, victim_key
        
        # Fallback: find page with oldest access time
        oldest_time = float('inf')
        victim_frame = None
        victim_key = None
        
        for frame in frames:
            if not frame.is_free and frame.page:
                if frame.page.last_access_time < oldest_time:
                    oldest_time = frame.page.last_access_time
                    victim_frame = frame.frame_id
                    victim_key = (frame.page.process_id, frame.page.page_id)
        
        return victim_frame, victim_key
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        key = (pid, page_id)
        # Remove if exists and add to end (most recent)
        if key in self.access_order:
            del self.access_order[key]
        self.access_order[key] = True
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed (update LRU order)."""
        key = (pid, page_id)
        # Move to end (most recent)
        if key in self.access_order:
            del self.access_order[key]
        self.access_order[key] = True
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        key = (pid, page_id)
        if key in self.access_order:
            del self.access_order[key]
    
    def simulate(self, reference_string: List[Tuple[int, int]],
                 num_frames: int) -> Dict:
        """Simulate LRU on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        access_order: OrderedDict = OrderedDict()
        faults = 0
        hits = 0
        history = []
        
        for ref in reference_string:
            if ref in frames:
                # Hit - update access order
                hits += 1
                del access_order[ref]
                access_order[ref] = True
                history.append({'ref': ref, 'fault': False, 'frames': list(frames)})
            else:
                # Fault
                faults += 1
                
                if None in frames:
                    # Free frame available
                    idx = frames.index(None)
                    frames[idx] = ref
                else:
                    # Evict LRU page
                    victim = next(iter(access_order))
                    del access_order[victim]
                    idx = frames.index(victim)
                    frames[idx] = ref
                
                access_order[ref] = True
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
        self.access_order.clear()
        self.fault_count = 0
        self.hit_count = 0
