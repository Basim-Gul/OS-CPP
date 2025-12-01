"""Process model for OS simulation."""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import time


class ProcessState(Enum):
    """Process states in the OS."""
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    TERMINATED = "TERMINATED"


@dataclass
class Process:
    """Represents a process in the OS simulation."""
    pid: int
    name: str
    burst_time: int  # in milliseconds
    priority: int = 0  # Lower value = higher priority
    arrival_time: int = 0  # in milliseconds
    io_bound: bool = False  # True if I/O bound, False if CPU bound
    memory_pages: int = 5  # Number of pages required
    
    # Runtime attributes
    state: ProcessState = field(default=ProcessState.NEW)
    remaining_time: int = field(default=0, init=False)
    waiting_time: int = field(default=0, init=False)
    turnaround_time: int = field(default=0, init=False)
    response_time: int = field(default=-1, init=False)  # -1 indicates not started
    completion_time: int = field(default=0, init=False)
    start_time: int = field(default=-1, init=False)  # -1 indicates not started
    
    # Resource tracking
    allocated_resources: Dict[str, int] = field(default_factory=dict)
    requested_resources: Dict[str, int] = field(default_factory=dict)
    
    # MLFQ queue level (0 = highest priority)
    queue_level: int = field(default=0, init=False)
    
    # Aging counter for priority scheduling
    aging_counter: int = field(default=0, init=False)
    
    # Page table for memory management
    page_table: List[Optional[int]] = field(default_factory=list, init=False)
    
    # Creation timestamp
    created_at: float = field(default_factory=time.time, init=False)
    
    def __post_init__(self):
        """Initialize remaining time after creation."""
        self.remaining_time = self.burst_time
        self.page_table = [None] * self.memory_pages
    
    def execute(self, time_slice: int) -> int:
        """Execute the process for a given time slice.
        
        Returns the actual time executed.
        """
        if self.start_time == -1:
            self.start_time = 0  # Will be set by scheduler
        
        actual_time = min(time_slice, self.remaining_time)
        self.remaining_time -= actual_time
        
        if self.remaining_time == 0:
            self.state = ProcessState.TERMINATED
        
        return actual_time
    
    def is_complete(self) -> bool:
        """Check if the process has completed execution."""
        return self.remaining_time == 0
    
    def reset(self) -> None:
        """Reset process for re-simulation."""
        self.remaining_time = self.burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        self.completion_time = 0
        self.start_time = -1
        self.state = ProcessState.NEW
        self.queue_level = 0
        self.aging_counter = 0
        self.allocated_resources.clear()
        self.requested_resources.clear()
        self.page_table = [None] * self.memory_pages
    
    def get_state_color(self) -> str:
        """Get the Rich color for the current state."""
        color_map = {
            ProcessState.NEW: "cyan",
            ProcessState.READY: "green",
            ProcessState.RUNNING: "yellow",
            ProcessState.BLOCKED: "red",
            ProcessState.TERMINATED: "white"
        }
        return color_map.get(self.state, "white")
    
    def get_state_emoji(self) -> str:
        """Get emoji for the current state."""
        emoji_map = {
            ProcessState.NEW: "🔵",
            ProcessState.READY: "🟢",
            ProcessState.RUNNING: "🟡",
            ProcessState.BLOCKED: "🔴",
            ProcessState.TERMINATED: "⚪"
        }
        return emoji_map.get(self.state, "⚪")
    
    def __repr__(self) -> str:
        return f"Process(pid={self.pid}, name={self.name}, state={self.state.value})"
