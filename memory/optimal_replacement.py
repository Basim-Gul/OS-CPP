"""Optimal (Belady's) Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from models.memory_page import Page, Frame


class OptimalReplacement:
    """Optimal (Belady's) page replacement algorithm.
    
    Evicts the page that won't be used for the longest time in the future.
    This is an oracle algorithm - requires knowledge of future references.
    """
    
    def __init__(self, future_references: List[Tuple[int, int]] = None):
        self.name = "Optimal (Belady)"
        self.future_references = future_references or []
        self.current_index = 0
        self.fault_count = 0
        self.hit_count = 0
    
    def set_future_references(self, references: List[Tuple[int, int]]) -> None:
        """Set the future reference string."""
        self.future_references = references
        self.current_index = 0
    
    def select_victim(self, frames: List[Frame],
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page to evict (one with furthest future use).
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        # Get all pages currently in memory
        in_memory = []
        for frame in frames:
            if not frame.is_free and frame.page:
                in_memory.append((frame.frame_id, frame.page.process_id, frame.page.page_id))
        
        if not in_memory:
            return None, None
        
        # Find which page won't be used for the longest time
        future = self.future_references[self.current_index:] if self.future_references else []
        
        best_victim = None
        max_distance = -1
        
        for frame_id, pid, page_id in in_memory:
            key = (pid, page_id)
            
            # Find next use of this page
            try:
                distance = future.index(key)
            except ValueError:
                # Page won't be used again - perfect victim
                return frame_id, key
            
            if distance > max_distance:
                max_distance = distance
                best_victim = (frame_id, key)
        
        if best_victim:
            return best_victim[0], best_victim[1]
        
        # Fallback: first occupied frame
        return in_memory[0][0], (in_memory[0][1], in_memory[0][2])
    
    def advance_reference(self) -> None:
        """Advance the current reference index."""
        self.current_index += 1
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        pass  # Optimal doesn't need to track this
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed."""
        self.advance_reference()
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        pass  # Optimal doesn't need to track this
    
    def simulate(self, reference_string: List[Tuple[int, int]],
                 num_frames: int) -> Dict:
        """Simulate Optimal on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        faults = 0
        hits = 0
        history = []
        
        # Precompute next use positions for each page at each index for O(n) lookup
        next_use = {}  # {page: [list of indices where it appears]}
        for idx, ref in enumerate(reference_string):
            if ref not in next_use:
                next_use[ref] = []
            next_use[ref].append(idx)
        
        for i, ref in enumerate(reference_string):
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
                    # Find optimal victim using precomputed positions
                    best_idx = 0
                    max_distance = -1
                    
                    for j, page in enumerate(frames):
                        # Find next use of this page after current position
                        positions = next_use.get(page, [])
                        # Binary search for next position > i
                        next_pos = None
                        for pos in positions:
                            if pos > i:
                                next_pos = pos
                                break
                        
                        if next_pos is None:
                            # Page not used again - evict it
                            best_idx = j
                            break
                        
                        distance = next_pos - i
                        if distance > max_distance:
                            max_distance = distance
                            best_idx = j
                    
                    frames[best_idx] = ref
                
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
        self.current_index = 0
        self.fault_count = 0
        self.hit_count = 0
