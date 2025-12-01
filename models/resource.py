"""Resource model for OS simulation."""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional


class ResourceType(Enum):
    """Types of resources in the system."""
    CPU = "CPU"
    MEMORY = "Memory"
    PRINTER = "Printer"
    DISK = "Disk"


@dataclass
class Resource:
    """Represents a resource in the OS simulation."""
    rid: int
    name: str
    resource_type: ResourceType
    total_instances: int = 1
    
    # Runtime attributes
    available_instances: int = field(default=0, init=False)
    allocated_to: Dict[int, int] = field(default_factory=dict)  # pid -> count
    waiting_queue: List[int] = field(default_factory=list)  # List of waiting PIDs
    
    def __post_init__(self):
        """Initialize available instances after creation."""
        self.available_instances = self.total_instances
    
    def allocate(self, pid: int, count: int = 1) -> bool:
        """Allocate resource instances to a process.
        
        Returns True if allocation was successful, False otherwise.
        """
        if count <= self.available_instances:
            self.available_instances -= count
            if pid in self.allocated_to:
                self.allocated_to[pid] += count
            else:
                self.allocated_to[pid] = count
            # Remove from waiting queue if present
            if pid in self.waiting_queue:
                self.waiting_queue.remove(pid)
            return True
        return False
    
    def release(self, pid: int, count: Optional[int] = None) -> int:
        """Release resource instances from a process.
        
        If count is None, releases all instances held by the process.
        Returns the number of instances released.
        """
        if pid not in self.allocated_to:
            return 0
        
        if count is None:
            count = self.allocated_to[pid]
        
        actual_release = min(count, self.allocated_to[pid])
        self.allocated_to[pid] -= actual_release
        self.available_instances += actual_release
        
        if self.allocated_to[pid] == 0:
            del self.allocated_to[pid]
        
        return actual_release
    
    def request(self, pid: int) -> None:
        """Add a process to the waiting queue."""
        if pid not in self.waiting_queue:
            self.waiting_queue.append(pid)
    
    def get_allocated_count(self, pid: int) -> int:
        """Get the number of instances allocated to a process."""
        return self.allocated_to.get(pid, 0)
    
    def is_available(self, count: int = 1) -> bool:
        """Check if the requested instances are available."""
        return self.available_instances >= count
    
    def reset(self) -> None:
        """Reset resource to initial state."""
        self.available_instances = self.total_instances
        self.allocated_to.clear()
        self.waiting_queue.clear()
    
    def __repr__(self) -> str:
        return (f"Resource(rid={self.rid}, name={self.name}, "
                f"available={self.available_instances}/{self.total_instances})")
