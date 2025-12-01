"""Synchronization Manager for OS simulation."""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from models.mutex import Mutex
from models.semaphore import Semaphore


@dataclass
class SyncEvent:
    """A synchronization event."""
    timestamp: int
    event_type: str  # 'acquire', 'release', 'wait', 'signal'
    sync_object: str  # mutex or semaphore name
    pid: int
    success: bool
    message: str = ""


class SyncManager:
    """Manages synchronization primitives (mutexes and semaphores)."""
    
    def __init__(self):
        self.mutexes: Dict[str, Mutex] = {}
        self.semaphores: Dict[str, Semaphore] = {}
        self.event_history: List[SyncEvent] = []
        self.current_time: int = 0
    
    def create_mutex(self, name: str) -> Mutex:
        """Create a new mutex."""
        if name not in self.mutexes:
            self.mutexes[name] = Mutex(name)
        return self.mutexes[name]
    
    def create_semaphore(self, name: str, initial_count: int = 1) -> Semaphore:
        """Create a new semaphore."""
        if name not in self.semaphores:
            self.semaphores[name] = Semaphore(name, initial_count)
        return self.semaphores[name]
    
    def get_mutex(self, name: str) -> Optional[Mutex]:
        """Get a mutex by name."""
        return self.mutexes.get(name)
    
    def get_semaphore(self, name: str) -> Optional[Semaphore]:
        """Get a semaphore by name."""
        return self.semaphores.get(name)
    
    def acquire_mutex(self, name: str, pid: int, 
                      blocking: bool = True, 
                      timeout: float = None) -> bool:
        """Acquire a mutex for a process."""
        mutex = self.mutexes.get(name)
        if not mutex:
            self._log_event('acquire', name, pid, False, "Mutex not found")
            return False
        
        success = mutex.acquire(pid, blocking, timeout)
        self._log_event('acquire', name, pid, success,
                       "Acquired" if success else "Waiting")
        return success
    
    def release_mutex(self, name: str, pid: int) -> bool:
        """Release a mutex from a process."""
        mutex = self.mutexes.get(name)
        if not mutex:
            self._log_event('release', name, pid, False, "Mutex not found")
            return False
        
        success = mutex.release(pid)
        self._log_event('release', name, pid, success,
                       "Released" if success else "Not owner")
        return success
    
    def wait_semaphore(self, name: str, pid: int,
                       blocking: bool = True,
                       timeout: float = None) -> bool:
        """Wait on a semaphore (P operation)."""
        sem = self.semaphores.get(name)
        if not sem:
            self._log_event('wait', name, pid, False, "Semaphore not found")
            return False
        
        success = sem.wait(pid, blocking, timeout)
        self._log_event('wait', name, pid, success,
                       f"Count now: {sem.count}" if success else "Waiting")
        return success
    
    def signal_semaphore(self, name: str, pid: int = None) -> None:
        """Signal a semaphore (V operation)."""
        sem = self.semaphores.get(name)
        if not sem:
            self._log_event('signal', name, pid or 0, False, "Semaphore not found")
            return
        
        sem.signal(pid)
        self._log_event('signal', name, pid or 0, True, f"Count now: {sem.count}")
    
    def get_mutex_status(self) -> Dict:
        """Get status of all mutexes."""
        return {
            name: {
                'locked': m.locked,
                'owner': m.owner_pid,
                'waiting': len(m.waiting_queue)
            }
            for name, m in self.mutexes.items()
        }
    
    def get_semaphore_status(self) -> Dict:
        """Get status of all semaphores."""
        return {
            name: {
                'count': s.count,
                'initial': s.initial_count,
                'waiting': len(s.waiting_queue)
            }
            for name, s in self.semaphores.items()
        }
    
    def _log_event(self, event_type: str, sync_name: str, 
                   pid: int, success: bool, message: str = "") -> None:
        """Log a synchronization event."""
        event = SyncEvent(
            timestamp=self.current_time,
            event_type=event_type,
            sync_object=sync_name,
            pid=pid,
            success=success,
            message=message
        )
        self.event_history.append(event)
    
    def set_time(self, time: int) -> None:
        """Set the current simulation time."""
        self.current_time = time
    
    def get_events(self) -> List[SyncEvent]:
        """Get all synchronization events."""
        return self.event_history
    
    def reset(self) -> None:
        """Reset all synchronization primitives."""
        for mutex in self.mutexes.values():
            mutex.reset()
        for sem in self.semaphores.values():
            sem.reset()
        self.event_history.clear()
        self.current_time = 0
