"""Memory page model for OS simulation."""

from dataclasses import dataclass, field
from typing import Optional
import time


@dataclass
class Page:
    """Represents a virtual memory page."""
    page_id: int
    process_id: int
    size: int = 4096  # Default 4KB
    
    # Runtime attributes
    referenced: bool = field(default=False, init=False)
    modified: bool = field(default=False, init=False)
    last_access_time: float = field(default_factory=time.time, init=False)
    access_count: int = field(default=0, init=False)
    load_time: float = field(default=0, init=False)
    
    def access(self, modify: bool = False) -> None:
        """Record a page access."""
        self.referenced = True
        self.modified = self.modified or modify
        self.last_access_time = time.time()
        self.access_count += 1
    
    def clear_reference(self) -> None:
        """Clear the reference bit (used by Clock algorithm)."""
        self.referenced = False
    
    def __repr__(self) -> str:
        return f"Page(id={self.page_id}, process={self.process_id})"


@dataclass
class Frame:
    """Represents a physical memory frame."""
    frame_id: int
    size: int = 4096  # Default 4KB
    
    # Runtime attributes
    page: Optional[Page] = field(default=None, init=False)
    is_free: bool = field(default=True, init=False)
    allocation_time: float = field(default=0, init=False)
    
    def allocate(self, page: Page) -> None:
        """Allocate a page to this frame."""
        self.page = page
        self.is_free = False
        self.allocation_time = time.time()
        page.load_time = self.allocation_time
    
    def deallocate(self) -> Optional[Page]:
        """Deallocate the page from this frame."""
        old_page = self.page
        self.page = None
        self.is_free = True
        return old_page
    
    def __repr__(self) -> str:
        if self.page:
            return f"Frame({self.frame_id}, page={self.page.page_id})"
        return f"Frame({self.frame_id}, free)"


@dataclass
class PageTableEntry:
    """Represents an entry in a page table."""
    page_id: int
    frame_id: Optional[int] = None
    valid: bool = False
    referenced: bool = False
    modified: bool = False
    protection: str = "rw"  # read-write by default
    
    def set_frame(self, frame_id: int) -> None:
        """Set the frame ID and mark as valid."""
        self.frame_id = frame_id
        self.valid = True
    
    def invalidate(self) -> None:
        """Invalidate the entry."""
        self.frame_id = None
        self.valid = False
        self.referenced = False
        self.modified = False
    
    def access(self, write: bool = False) -> None:
        """Record access to this page."""
        self.referenced = True
        if write:
            self.modified = True
    
    def clear_reference(self) -> None:
        """Clear the reference bit."""
        self.referenced = False
    
    def __repr__(self) -> str:
        if self.valid:
            return f"PTE(page={self.page_id}, frame={self.frame_id}, valid)"
        return f"PTE(page={self.page_id}, invalid)"
