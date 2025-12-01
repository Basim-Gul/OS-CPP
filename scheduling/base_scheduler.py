"""Base scheduler abstract class for OS simulation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from models.process import Process, ProcessState


@dataclass
class SchedulingResult:
    """Result of a scheduling simulation."""
    algorithm: str
    processes: List[Process]
    gantt_chart: List[Tuple[int, int, int]]  # (pid, start, end)
    context_switches: int = 0
    total_time: int = 0
    
    # Calculated metrics
    avg_waiting_time: float = 0.0
    avg_turnaround_time: float = 0.0
    avg_response_time: float = 0.0
    avg_completion_time: float = 0.0
    cpu_utilization: float = 0.0
    throughput: float = 0.0
    
    def calculate_metrics(self) -> None:
        """Calculate all scheduling metrics."""
        if not self.processes:
            return
        
        n = len(self.processes)
        total_waiting = sum(p.waiting_time for p in self.processes)
        total_turnaround = sum(p.turnaround_time for p in self.processes)
        total_response = sum(p.response_time for p in self.processes if p.response_time >= 0)
        total_completion = sum(p.completion_time for p in self.processes)
        
        self.avg_waiting_time = total_waiting / n
        self.avg_turnaround_time = total_turnaround / n
        self.avg_response_time = total_response / n if n > 0 else 0
        self.avg_completion_time = total_completion / n
        
        # Calculate CPU utilization
        if self.total_time > 0:
            busy_time = sum(p.burst_time for p in self.processes)
            self.cpu_utilization = (busy_time / self.total_time) * 100
            self.throughput = n / (self.total_time / 1000)  # processes per second


class BaseScheduler(ABC):
    """Abstract base class for all scheduling algorithms."""
    
    def __init__(self, name: str, preemptive: bool = False):
        self.name = name
        self.preemptive = preemptive
        self.ready_queue: List[Process] = []
        self.current_time: int = 0
        self.gantt_chart: List[Tuple[int, int, int]] = []
        self.context_switches: int = 0
        self.running_process: Optional[Process] = None
        self.logs: List[str] = []
    
    @abstractmethod
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run the scheduling algorithm on the given processes.
        
        Args:
            processes: List of processes to schedule
            
        Returns:
            SchedulingResult with metrics and Gantt chart
        """
        pass
    
    @abstractmethod
    def select_next(self) -> Optional[Process]:
        """Select the next process to run from the ready queue.
        
        Returns:
            The selected process, or None if queue is empty
        """
        pass
    
    def add_to_ready_queue(self, process: Process) -> None:
        """Add a process to the ready queue."""
        process.state = ProcessState.READY
        self.ready_queue.append(process)
        self.log(f"Process P{process.pid} added to ready queue")
    
    def remove_from_ready_queue(self, process: Process) -> None:
        """Remove a process from the ready queue."""
        if process in self.ready_queue:
            self.ready_queue.remove(process)
    
    def get_arrived_processes(self, processes: List[Process], time: int) -> List[Process]:
        """Get processes that have arrived by the given time."""
        return [p for p in processes if p.arrival_time <= time and p.state == ProcessState.NEW]
    
    def reset(self) -> None:
        """Reset the scheduler state."""
        self.ready_queue.clear()
        self.current_time = 0
        self.gantt_chart.clear()
        self.context_switches = 0
        self.running_process = None
        self.logs.clear()
    
    def log(self, message: str) -> None:
        """Add a log message with timestamp."""
        self.logs.append(f"[{self.current_time:05d}ms] {message}")
    
    def calculate_process_metrics(self, process: Process) -> None:
        """Calculate metrics for a completed process."""
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    
    def create_result(self, processes: List[Process]) -> SchedulingResult:
        """Create a scheduling result from the simulation."""
        result = SchedulingResult(
            algorithm=self.name,
            processes=processes,
            gantt_chart=self.gantt_chart.copy(),
            context_switches=self.context_switches,
            total_time=self.current_time
        )
        result.calculate_metrics()
        return result
    
    def __repr__(self) -> str:
        mode = "Preemptive" if self.preemptive else "Non-Preemptive"
        return f"{self.name} ({mode})"
