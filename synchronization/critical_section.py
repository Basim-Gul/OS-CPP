"""Critical Section simulation for OS simulation."""

from typing import List, Callable, Any
from dataclasses import dataclass, field
import threading
import time

from models.mutex import Mutex


@dataclass
class CriticalSectionEvent:
    """Event in a critical section execution."""
    timestamp: float
    thread_id: int
    action: str  # 'enter', 'exit', 'wait'
    message: str = ""


class CriticalSection:
    """Simulates critical section access with mutex protection."""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.mutex = Mutex(f"cs_{name}")
        self.events: List[CriticalSectionEvent] = []
        self.in_section: bool = False
        self.current_thread: int = -1
        self._lock = threading.Lock()
    
    def enter(self, thread_id: int, blocking: bool = True) -> bool:
        """Try to enter the critical section."""
        start_time = time.time()
        
        if self.mutex.acquire(thread_id, blocking):
            with self._lock:
                self.in_section = True
                self.current_thread = thread_id
                self._log_event(thread_id, 'enter', "Entered critical section")
            return True
        else:
            self._log_event(thread_id, 'wait', "Waiting for critical section")
            return False
    
    def exit(self, thread_id: int) -> bool:
        """Exit the critical section."""
        with self._lock:
            if self.current_thread != thread_id:
                self._log_event(thread_id, 'error', "Not in critical section")
                return False
            
            self.in_section = False
            self.current_thread = -1
        
        self.mutex.release(thread_id)
        self._log_event(thread_id, 'exit', "Exited critical section")
        return True
    
    def execute_with_protection(self, thread_id: int, 
                                 operation: Callable[[], Any]) -> Any:
        """Execute an operation within the critical section."""
        self.enter(thread_id)
        try:
            return operation()
        finally:
            self.exit(thread_id)
    
    def _log_event(self, thread_id: int, action: str, message: str) -> None:
        """Log a critical section event."""
        event = CriticalSectionEvent(
            timestamp=time.time(),
            thread_id=thread_id,
            action=action,
            message=message
        )
        self.events.append(event)
    
    def is_in_use(self) -> bool:
        """Check if the critical section is currently in use."""
        return self.in_section
    
    def get_current_thread(self) -> int:
        """Get the thread currently in the critical section."""
        return self.current_thread
    
    def get_events(self) -> List[CriticalSectionEvent]:
        """Get all critical section events."""
        return self.events
    
    def reset(self) -> None:
        """Reset the critical section."""
        self.mutex.reset()
        self.events.clear()
        self.in_section = False
        self.current_thread = -1


class ProducerConsumerProblem:
    """Implementation of the Producer-Consumer problem using semaphores."""
    
    def __init__(self, buffer_size: int = 5):
        self.buffer_size = buffer_size
        self.buffer: List[Any] = []
        
        # Semaphores
        self.empty_count = threading.Semaphore(buffer_size)  # Empty slots
        self.full_count = threading.Semaphore(0)  # Full slots
        self.mutex = threading.Lock()  # Buffer access
        
        # Tracking
        self.produced_count = 0
        self.consumed_count = 0
        self.events: List[str] = []
    
    def produce(self, producer_id: int, item: Any) -> bool:
        """Produce an item and add to buffer."""
        # Wait for empty slot
        acquired = self.empty_count.acquire(timeout=1.0)
        if not acquired:
            self._log(f"Producer {producer_id}: Buffer full, waiting...")
            return False
        
        # Access buffer
        with self.mutex:
            self.buffer.append(item)
            self.produced_count += 1
            self._log(f"Producer {producer_id}: Produced item {item} (buffer: {len(self.buffer)}/{self.buffer_size})")
        
        # Signal that buffer has item
        self.full_count.release()
        return True
    
    def consume(self, consumer_id: int) -> Any:
        """Consume an item from the buffer."""
        # Wait for full slot
        acquired = self.full_count.acquire(timeout=1.0)
        if not acquired:
            self._log(f"Consumer {consumer_id}: Buffer empty, waiting...")
            return None
        
        # Access buffer
        with self.mutex:
            if not self.buffer:
                return None
            item = self.buffer.pop(0)
            self.consumed_count += 1
            self._log(f"Consumer {consumer_id}: Consumed item {item} (buffer: {len(self.buffer)}/{self.buffer_size})")
        
        # Signal that buffer has empty slot
        self.empty_count.release()
        return item
    
    def _log(self, message: str) -> None:
        """Log an event."""
        self.events.append(f"[{time.time():.3f}] {message}")
    
    def get_buffer_status(self) -> dict:
        """Get current buffer status."""
        return {
            'buffer_size': self.buffer_size,
            'items_in_buffer': len(self.buffer),
            'total_produced': self.produced_count,
            'total_consumed': self.consumed_count
        }
    
    def get_events(self) -> List[str]:
        """Get all events."""
        return self.events
    
    def reset(self) -> None:
        """Reset the producer-consumer."""
        self.buffer.clear()
        self.produced_count = 0
        self.consumed_count = 0
        self.events.clear()
        self.empty_count = threading.Semaphore(self.buffer_size)
        self.full_count = threading.Semaphore(0)
