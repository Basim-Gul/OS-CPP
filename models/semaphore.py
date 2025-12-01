"""Semaphore implementation for OS simulation."""

from dataclasses import dataclass, field
from typing import List
import threading
import time


@dataclass
class Semaphore:
    """Counting semaphore implementation."""
    name: str
    initial_count: int = 1
    
    # Runtime attributes
    count: int = field(default=0, init=False)
    waiting_queue: List[int] = field(default_factory=list, init=False)
    
    # Internal threading primitives
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _condition: threading.Condition = field(default=None, init=False, repr=False)
    
    # Statistics
    wait_count: int = field(default=0, init=False)
    signal_count: int = field(default=0, init=False)
    
    def __post_init__(self):
        """Initialize count and condition variable."""
        self.count = self.initial_count
        self._condition = threading.Condition(self._lock)
    
    def wait(self, pid: int, blocking: bool = True, timeout: float = None) -> bool:
        """Decrement semaphore (P operation).
        
        Args:
            pid: Process ID performing the wait
            blocking: If True, block until count > 0
            timeout: Maximum time to wait (None = infinite)
            
        Returns:
            True if semaphore was decremented, False otherwise
        """
        with self._condition:
            self.wait_count += 1
            
            if self.count > 0:
                self.count -= 1
                return True
            
            if not blocking:
                return False
            
            # Add to waiting queue
            if pid not in self.waiting_queue:
                self.waiting_queue.append(pid)
            
            # Wait for signal
            start_time = time.time()
            while self.count <= 0:
                if timeout is not None:
                    remaining = timeout - (time.time() - start_time)
                    if remaining <= 0:
                        if pid in self.waiting_queue:
                            self.waiting_queue.remove(pid)
                        return False
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()
            
            # Semaphore now available
            self.count -= 1
            if pid in self.waiting_queue:
                self.waiting_queue.remove(pid)
            return True
    
    def signal(self, pid: int = None) -> None:
        """Increment semaphore (V operation).
        
        Args:
            pid: Process ID performing the signal (optional, for logging)
        """
        with self._condition:
            self.count += 1
            self.signal_count += 1
            self._condition.notify()
    
    # Aliases for P and V operations
    def P(self, pid: int, blocking: bool = True, timeout: float = None) -> bool:
        """P operation (alias for wait)."""
        return self.wait(pid, blocking, timeout)
    
    def V(self, pid: int = None) -> None:
        """V operation (alias for signal)."""
        self.signal(pid)
    
    def get_count(self) -> int:
        """Get current semaphore count."""
        return self.count
    
    def get_waiting_count(self) -> int:
        """Get number of processes waiting."""
        return len(self.waiting_queue)
    
    def reset(self) -> None:
        """Reset semaphore to initial state."""
        with self._lock:
            self.count = self.initial_count
            self.waiting_queue.clear()
            self.wait_count = 0
            self.signal_count = 0
    
    def __repr__(self) -> str:
        return f"Semaphore(name={self.name}, count={self.count}, waiting={len(self.waiting_queue)})"
