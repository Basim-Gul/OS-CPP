"""Page Table implementation for OS simulation."""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from models.memory_page import PageTableEntry


@dataclass
class PageTable:
    """Page table for a process."""
    process_id: int
    num_pages: int
    
    # Page table entries
    entries: Dict[int, PageTableEntry] = field(default_factory=dict)
    
    # Statistics
    hit_count: int = field(default=0, init=False)
    miss_count: int = field(default=0, init=False)
    
    def __post_init__(self):
        """Initialize page table entries."""
        for i in range(self.num_pages):
            self.entries[i] = PageTableEntry(page_id=i)
    
    def lookup(self, page_id: int) -> Optional[int]:
        """Look up a page and return the frame number if valid.
        
        Returns: frame_id if page is in memory, None otherwise
        """
        if page_id not in self.entries:
            self.miss_count += 1
            return None
        
        entry = self.entries[page_id]
        if entry.valid:
            self.hit_count += 1
            entry.access()
            return entry.frame_id
        else:
            self.miss_count += 1
            return None
    
    def map_page(self, page_id: int, frame_id: int) -> bool:
        """Map a virtual page to a physical frame.
        
        Returns: True if mapping was successful
        """
        if page_id not in self.entries:
            return False
        
        self.entries[page_id].set_frame(frame_id)
        return True
    
    def unmap_page(self, page_id: int) -> Optional[int]:
        """Unmap a page and return the frame it was using.
        
        Returns: frame_id if page was mapped, None otherwise
        """
        if page_id not in self.entries:
            return None
        
        entry = self.entries[page_id]
        frame_id = entry.frame_id
        entry.invalidate()
        return frame_id
    
    def is_valid(self, page_id: int) -> bool:
        """Check if a page is currently in memory."""
        if page_id not in self.entries:
            return False
        return self.entries[page_id].valid
    
    def get_frame(self, page_id: int) -> Optional[int]:
        """Get the frame number for a page without recording access."""
        if page_id not in self.entries:
            return None
        entry = self.entries[page_id]
        return entry.frame_id if entry.valid else None
    
    def get_valid_pages(self) -> List[int]:
        """Get list of page IDs that are currently in memory."""
        return [pid for pid, entry in self.entries.items() if entry.valid]
    
    def get_hit_rate(self) -> float:
        """Get the page table hit rate."""
        total = self.hit_count + self.miss_count
        if total == 0:
            return 0.0
        return (self.hit_count / total) * 100
    
    def clear_reference_bits(self) -> None:
        """Clear all reference bits (used by Clock algorithm)."""
        for entry in self.entries.values():
            entry.clear_reference()
    
    def get_referenced_pages(self) -> List[int]:
        """Get list of page IDs that have been recently referenced."""
        return [pid for pid, entry in self.entries.items() 
                if entry.valid and entry.referenced]
    
    def get_modified_pages(self) -> List[int]:
        """Get list of page IDs that have been modified."""
        return [pid for pid, entry in self.entries.items() 
                if entry.valid and entry.modified]
    
    def to_string(self) -> str:
        """Get string representation of the page table."""
        lines = [f"Page Table for Process {self.process_id}",
                 "-" * 50,
                 f"{'Page':<8} {'Frame':<8} {'Valid':<8} {'Ref':<8} {'Mod':<8}"]
        
        for page_id, entry in sorted(self.entries.items()):
            frame = str(entry.frame_id) if entry.frame_id is not None else "-"
            lines.append(f"{page_id:<8} {frame:<8} {entry.valid!s:<8} "
                        f"{entry.referenced!s:<8} {entry.modified!s:<8}")
        
        return "\n".join(lines)
    
    def reset(self) -> None:
        """Reset the page table."""
        for entry in self.entries.values():
            entry.invalidate()
        self.hit_count = 0
        self.miss_count = 0
