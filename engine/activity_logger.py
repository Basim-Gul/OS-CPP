"""Activity Logger for OS simulation."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class EventType(Enum):
    """Types of events in the simulation."""
    PROCESS_CREATED = "process_created"
    PROCESS_TERMINATED = "process_terminated"
    STATE_TRANSITION = "state_transition"
    RESOURCE_ALLOCATED = "resource_allocated"
    RESOURCE_RELEASED = "resource_released"
    RESOURCE_REQUESTED = "resource_requested"
    DEADLOCK_DETECTED = "deadlock_detected"
    DEADLOCK_RESOLVED = "deadlock_resolved"
    MUTEX_ACQUIRED = "mutex_acquired"
    MUTEX_RELEASED = "mutex_released"
    SEMAPHORE_WAIT = "semaphore_wait"
    SEMAPHORE_SIGNAL = "semaphore_signal"
    PAGE_FAULT = "page_fault"
    PAGE_LOADED = "page_loaded"
    PAGE_EVICTED = "page_evicted"
    SCHEDULING_DECISION = "scheduling_decision"
    CONTEXT_SWITCH = "context_switch"
    SIMULATION_START = "simulation_start"
    SIMULATION_END = "simulation_end"


@dataclass
class LogEvent:
    """A single log event."""
    timestamp: int  # Simulation time in ms
    event_type: EventType
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    real_time: datetime = field(default_factory=datetime.now)
    
    def to_string(self) -> str:
        """Format the event as a string."""
        emoji = self._get_emoji()
        return f"[{self.timestamp:06d}ms] {emoji} {self.description}"
    
    def _get_emoji(self) -> str:
        """Get an emoji for the event type."""
        emoji_map = {
            EventType.PROCESS_CREATED: "🆕",
            EventType.PROCESS_TERMINATED: "✅",
            EventType.STATE_TRANSITION: "➡️",
            EventType.RESOURCE_ALLOCATED: "📦",
            EventType.RESOURCE_RELEASED: "📤",
            EventType.RESOURCE_REQUESTED: "🔄",
            EventType.DEADLOCK_DETECTED: "⚠️",
            EventType.DEADLOCK_RESOLVED: "🔓",
            EventType.MUTEX_ACQUIRED: "🔒",
            EventType.MUTEX_RELEASED: "🔓",
            EventType.SEMAPHORE_WAIT: "⏳",
            EventType.SEMAPHORE_SIGNAL: "📣",
            EventType.PAGE_FAULT: "💥",
            EventType.PAGE_LOADED: "📄",
            EventType.PAGE_EVICTED: "🗑️",
            EventType.SCHEDULING_DECISION: "🎯",
            EventType.CONTEXT_SWITCH: "🔀",
            EventType.SIMULATION_START: "🚀",
            EventType.SIMULATION_END: "🏁"
        }
        return emoji_map.get(self.event_type, "📝")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON export."""
        return {
            'timestamp': self.timestamp,
            'event_type': self.event_type.value,
            'description': self.description,
            'details': self.details,
            'real_time': self.real_time.isoformat()
        }


class ActivityLogger:
    """Logs all activities during simulation."""
    
    def __init__(self):
        self.events: List[LogEvent] = []
        self.current_time: int = 0
        self.enabled: bool = True
    
    def log(self, event_type: EventType, description: str, 
            details: Dict[str, Any] = None) -> None:
        """Log an event."""
        if not self.enabled:
            return
        
        event = LogEvent(
            timestamp=self.current_time,
            event_type=event_type,
            description=description,
            details=details or {}
        )
        self.events.append(event)
    
    def log_process_created(self, pid: int, name: str, burst: int, priority: int) -> None:
        """Log process creation."""
        self.log(
            EventType.PROCESS_CREATED,
            f"Process P{pid} ({name}) created - Burst: {burst}ms, Priority: {priority}",
            {'pid': pid, 'name': name, 'burst_time': burst, 'priority': priority}
        )
    
    def log_process_terminated(self, pid: int, name: str, 
                                turnaround: int, waiting: int) -> None:
        """Log process termination."""
        self.log(
            EventType.PROCESS_TERMINATED,
            f"Process P{pid} ({name}) terminated - TAT: {turnaround}ms, WT: {waiting}ms",
            {'pid': pid, 'name': name, 'turnaround_time': turnaround, 'waiting_time': waiting}
        )
    
    def log_state_transition(self, pid: int, from_state: str, to_state: str) -> None:
        """Log process state transition."""
        self.log(
            EventType.STATE_TRANSITION,
            f"P{pid}: {from_state} → {to_state}",
            {'pid': pid, 'from_state': from_state, 'to_state': to_state}
        )
    
    def log_resource_allocated(self, pid: int, resource: str, count: int) -> None:
        """Log resource allocation."""
        self.log(
            EventType.RESOURCE_ALLOCATED,
            f"Allocated {count} {resource} to P{pid}",
            {'pid': pid, 'resource': resource, 'count': count}
        )
    
    def log_resource_released(self, pid: int, resource: str, count: int) -> None:
        """Log resource release."""
        self.log(
            EventType.RESOURCE_RELEASED,
            f"P{pid} released {count} {resource}",
            {'pid': pid, 'resource': resource, 'count': count}
        )
    
    def log_deadlock_detected(self, processes: List[int], resources: List[int],
                               cycle: List[str]) -> None:
        """Log deadlock detection."""
        cycle_str = " → ".join(cycle)
        self.log(
            EventType.DEADLOCK_DETECTED,
            f"DEADLOCK DETECTED! Chain: {cycle_str}",
            {'processes': processes, 'resources': resources, 'cycle': cycle}
        )
    
    def log_deadlock_resolved(self, method: str, victim: int) -> None:
        """Log deadlock resolution."""
        self.log(
            EventType.DEADLOCK_RESOLVED,
            f"Deadlock resolved by {method} - Victim: P{victim}",
            {'method': method, 'victim_pid': victim}
        )
    
    def log_mutex_acquired(self, pid: int, mutex_name: str) -> None:
        """Log mutex acquisition."""
        self.log(
            EventType.MUTEX_ACQUIRED,
            f"P{pid} acquired mutex '{mutex_name}'",
            {'pid': pid, 'mutex': mutex_name}
        )
    
    def log_mutex_released(self, pid: int, mutex_name: str) -> None:
        """Log mutex release."""
        self.log(
            EventType.MUTEX_RELEASED,
            f"P{pid} released mutex '{mutex_name}'",
            {'pid': pid, 'mutex': mutex_name}
        )
    
    def log_page_fault(self, pid: int, page_id: int, fault_type: str) -> None:
        """Log page fault."""
        self.log(
            EventType.PAGE_FAULT,
            f"Page fault for P{pid} page {page_id} ({fault_type})",
            {'pid': pid, 'page_id': page_id, 'fault_type': fault_type}
        )
    
    def log_scheduling_decision(self, algorithm: str, selected_pid: int,
                                 reason: str = "") -> None:
        """Log scheduling decision."""
        msg = f"Scheduler ({algorithm}) selected P{selected_pid}"
        if reason:
            msg += f" - {reason}"
        self.log(
            EventType.SCHEDULING_DECISION,
            msg,
            {'algorithm': algorithm, 'selected_pid': selected_pid, 'reason': reason}
        )
    
    def log_context_switch(self, from_pid: Optional[int], to_pid: int) -> None:
        """Log context switch."""
        if from_pid:
            self.log(
                EventType.CONTEXT_SWITCH,
                f"Context switch: P{from_pid} → P{to_pid}",
                {'from_pid': from_pid, 'to_pid': to_pid}
            )
        else:
            self.log(
                EventType.CONTEXT_SWITCH,
                f"Context switch: CPU idle → P{to_pid}",
                {'from_pid': None, 'to_pid': to_pid}
            )
    
    def log_simulation_start(self) -> None:
        """Log simulation start."""
        self.log(
            EventType.SIMULATION_START,
            "Simulation started",
            {}
        )
    
    def log_simulation_end(self, total_time: int) -> None:
        """Log simulation end."""
        self.log(
            EventType.SIMULATION_END,
            f"Simulation completed at {total_time}ms",
            {'total_time': total_time}
        )
    
    def set_time(self, time: int) -> None:
        """Set the current simulation time."""
        self.current_time = time
    
    def get_events(self, event_type: EventType = None) -> List[LogEvent]:
        """Get events, optionally filtered by type."""
        if event_type is None:
            return self.events
        return [e for e in self.events if e.event_type == event_type]
    
    def get_events_by_process(self, pid: int) -> List[LogEvent]:
        """Get all events related to a specific process."""
        return [e for e in self.events 
                if e.details.get('pid') == pid or 
                   e.details.get('from_pid') == pid or
                   e.details.get('to_pid') == pid or
                   pid in e.details.get('processes', [])]
    
    def export_to_file(self, filename: str = "simulation_log.txt") -> None:
        """Export log to a text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("                    OS SIMULATION LOG\n")
            f.write("=" * 70 + "\n\n")
            
            for event in self.events:
                f.write(event.to_string() + "\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write(f"Total events logged: {len(self.events)}\n")
    
    def export_to_json(self, filename: str = "simulation_log.json") -> None:
        """Export log to JSON file."""
        data = {
            'events': [e.to_dict() for e in self.events],
            'total_events': len(self.events)
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def get_summary(self) -> Dict:
        """Get a summary of logged events."""
        summary = {}
        for event in self.events:
            event_type = event.event_type.value
            summary[event_type] = summary.get(event_type, 0) + 1
        return summary
    
    def enable(self) -> None:
        """Enable logging."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable logging."""
        self.enabled = False
    
    def clear(self) -> None:
        """Clear all events."""
        self.events.clear()
        self.current_time = 0
