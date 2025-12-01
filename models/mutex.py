"""Mutex implementation for OS simulation."""

from dataclasses import dataclass, field
from typing import Optional, List
import threading
import time


@dataclass
class Mutex:
    """Mutual exclusion lock implementation."""
    name: str
    
    # Runtime attributes
    locked: bool = field(default=False, init=False)
    owner_pid: Optional[int] = field(default=None, init=False)
    waiting_queue: List[int] = field(default_factory=list, init=False)
    lock_time: float = field(default=0, init=False)
    
    # Internal threading lock for thread-safe operations
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _condition: threading.Condition = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """Initialize condition variable."""
        self._condition = threading.Condition(self._lock)
    
    def acquire(self, pid: int, blocking: bool = True, timeout: float = None) -> bool:
        """Acquire the mutex.
        
        Args:
            pid: Process ID requesting the lock
            blocking: If True, block until lock is available
            timeout: Maximum time to wait (None = infinite)
            
        Returns:
            True if lock was acquired, False otherwise
        """
        with self._condition:
            if not self.locked:
                # Lock is free, acquire it
                self.locked = True
                self.owner_pid = pid
                self.lock_time = time.time()
                return True
            
            if not blocking:
                return False
            
            # Add to waiting queue
            if pid not in self.waiting_queue:
                self.waiting_queue.append(pid)
            
            # Wait for lock
            start_time = time.time()
            while self.locked:
                if timeout is not None:
                    remaining = timeout - (time.time() - start_time)
                    if remaining <= 0:
                        if pid in self.waiting_queue:
                            self.waiting_queue.remove(pid)
                        return False
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()
            
            # Lock is now free, acquire it
            self.locked = True
            self.owner_pid = pid
            self.lock_time = time.time()
            if pid in self.waiting_queue:
                self.waiting_queue.remove(pid)
            return True
    
    def release(self, pid: int) -> bool:
        """Release the mutex.
        
        Args:
            pid: Process ID releasing the lock
            
        Returns:
            True if lock was released, False if caller is not owner
        """
        with self._condition:
            if self.owner_pid != pid:
                return False
            
            self.locked = False
            self.owner_pid = None
            self._condition.notify()
            return True
    
    def is_locked(self) -> bool:
        """Check if mutex is locked."""
        return self.locked
    
    def get_owner(self) -> Optional[int]:
        """Get the owner process ID."""
        return self.owner_pid
    
    def get_waiting_count(self) -> int:
        """Get number of processes waiting for the lock."""
        return len(self.waiting_queue)
    
    def reset(self) -> None:
        """Reset mutex to initial state."""
        with self._lock:
            self.locked = False
            self.owner_pid = None
            self.waiting_queue.clear()
            self.lock_time = 0
    
    def __repr__(self) -> str:
        status = f"locked by P{self.owner_pid}" if self.locked else "unlocked"
        return f"Mutex(name={self.name}, {status}, waiting={len(self.waiting_queue)})"
