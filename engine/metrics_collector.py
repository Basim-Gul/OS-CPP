"""Metrics Collector for OS simulation."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from models.process import Process


@dataclass
class ProcessMetrics:
    """Metrics for a single process."""
    pid: int
    name: str
    arrival_time: int
    burst_time: int
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = 0


@dataclass
class SimulationMetrics:
    """Aggregated metrics for a simulation."""
    algorithm: str
    total_processes: int
    total_time: int
    
    # Process metrics
    avg_waiting_time: float = 0.0
    avg_turnaround_time: float = 0.0
    avg_response_time: float = 0.0
    avg_completion_time: float = 0.0
    max_waiting_time: int = 0
    min_waiting_time: int = 0
    
    # System metrics
    cpu_utilization: float = 0.0
    throughput: float = 0.0
    context_switches: int = 0
    
    # Deadlock metrics
    deadlock_count: int = 0
    deadlocks_resolved: int = 0
    
    # Memory metrics
    page_fault_count: int = 0
    page_fault_rate: float = 0.0
    total_memory_accesses: int = 0


class MetricsCollector:
    """Collects and calculates simulation metrics."""
    
    def __init__(self):
        self.process_metrics: Dict[int, ProcessMetrics] = {}
        self.simulation_metrics: Optional[SimulationMetrics] = None
        
        # Counters
        self.context_switches = 0
        self.deadlock_count = 0
        self.deadlocks_resolved = 0
        self.page_faults = 0
        self.memory_accesses = 0
        
        # Time tracking
        self.cpu_busy_time = 0
        self.total_time = 0
        self.algorithm_name = ""
    
    def record_process(self, process: Process) -> None:
        """Record metrics for a process."""
        metrics = ProcessMetrics(
            pid=process.pid,
            name=process.name,
            arrival_time=process.arrival_time,
            burst_time=process.burst_time,
            completion_time=process.completion_time,
            turnaround_time=process.turnaround_time,
            waiting_time=process.waiting_time,
            response_time=process.response_time if process.response_time >= 0 else 0
        )
        self.process_metrics[process.pid] = metrics
    
    def record_processes(self, processes: List[Process]) -> None:
        """Record metrics for multiple processes."""
        for process in processes:
            self.record_process(process)
    
    def record_context_switch(self) -> None:
        """Record a context switch."""
        self.context_switches += 1
    
    def record_deadlock(self, resolved: bool = False) -> None:
        """Record a deadlock event."""
        self.deadlock_count += 1
        if resolved:
            self.deadlocks_resolved += 1
    
    def record_page_fault(self) -> None:
        """Record a page fault."""
        self.page_faults += 1
    
    def record_memory_access(self) -> None:
        """Record a memory access."""
        self.memory_accesses += 1
    
    def set_cpu_busy_time(self, time: int) -> None:
        """Set the total CPU busy time."""
        self.cpu_busy_time = time
    
    def set_total_time(self, time: int) -> None:
        """Set the total simulation time."""
        self.total_time = time
    
    def set_algorithm(self, name: str) -> None:
        """Set the scheduling algorithm name."""
        self.algorithm_name = name
    
    def calculate_metrics(self) -> SimulationMetrics:
        """Calculate all simulation metrics."""
        n = len(self.process_metrics)
        
        if n == 0:
            return SimulationMetrics(
                algorithm=self.algorithm_name,
                total_processes=0,
                total_time=self.total_time
            )
        
        # Calculate averages
        total_waiting = sum(m.waiting_time for m in self.process_metrics.values())
        total_turnaround = sum(m.turnaround_time for m in self.process_metrics.values())
        total_response = sum(m.response_time for m in self.process_metrics.values())
        total_completion = sum(m.completion_time for m in self.process_metrics.values())
        
        waiting_times = [m.waiting_time for m in self.process_metrics.values()]
        
        # CPU utilization
        if self.total_time > 0:
            if self.cpu_busy_time == 0:
                # Calculate from burst times
                self.cpu_busy_time = sum(m.burst_time for m in self.process_metrics.values())
            cpu_util = (self.cpu_busy_time / self.total_time) * 100
        else:
            cpu_util = 0
        
        # Throughput (processes per second)
        throughput = (n / (self.total_time / 1000)) if self.total_time > 0 else 0
        
        # Page fault rate
        fault_rate = (self.page_faults / self.memory_accesses * 100) if self.memory_accesses > 0 else 0
        
        self.simulation_metrics = SimulationMetrics(
            algorithm=self.algorithm_name,
            total_processes=n,
            total_time=self.total_time,
            avg_waiting_time=total_waiting / n,
            avg_turnaround_time=total_turnaround / n,
            avg_response_time=total_response / n,
            avg_completion_time=total_completion / n,
            max_waiting_time=max(waiting_times) if waiting_times else 0,
            min_waiting_time=min(waiting_times) if waiting_times else 0,
            cpu_utilization=cpu_util,
            throughput=throughput,
            context_switches=self.context_switches,
            deadlock_count=self.deadlock_count,
            deadlocks_resolved=self.deadlocks_resolved,
            page_fault_count=self.page_faults,
            page_fault_rate=fault_rate,
            total_memory_accesses=self.memory_accesses
        )
        
        return self.simulation_metrics
    
    def get_process_table(self) -> List[Dict]:
        """Get process metrics as a table-friendly list."""
        return [
            {
                'PID': f"P{m.pid}",
                'Name': m.name,
                'Arrival': m.arrival_time,
                'Burst': m.burst_time,
                'Completion': m.completion_time,
                'Turnaround': m.turnaround_time,
                'Waiting': m.waiting_time,
                'Response': m.response_time
            }
            for m in sorted(self.process_metrics.values(), key=lambda x: x.pid)
        ]
    
    def get_summary_string(self) -> str:
        """Get a formatted summary string."""
        if not self.simulation_metrics:
            self.calculate_metrics()
        
        m = self.simulation_metrics
        lines = [
            "=" * 60,
            "                  SIMULATION METRICS",
            "=" * 60,
            f"Algorithm: {m.algorithm}",
            f"Total Processes: {m.total_processes}",
            f"Total Time: {m.total_time}ms",
            "",
            "Process Metrics:",
            f"  Average Waiting Time:    {m.avg_waiting_time:.2f}ms",
            f"  Average Turnaround Time: {m.avg_turnaround_time:.2f}ms",
            f"  Average Response Time:   {m.avg_response_time:.2f}ms",
            f"  Average Completion Time: {m.avg_completion_time:.2f}ms",
            f"  Max Waiting Time:        {m.max_waiting_time}ms",
            f"  Min Waiting Time:        {m.min_waiting_time}ms",
            "",
            "System Metrics:",
            f"  CPU Utilization:         {m.cpu_utilization:.2f}%",
            f"  Throughput:              {m.throughput:.2f} processes/sec",
            f"  Context Switches:        {m.context_switches}",
            "",
            "Deadlock Metrics:",
            f"  Deadlocks Detected:      {m.deadlock_count}",
            f"  Deadlocks Resolved:      {m.deadlocks_resolved}",
            "",
            "Memory Metrics:",
            f"  Page Faults:             {m.page_fault_count}",
            f"  Page Fault Rate:         {m.page_fault_rate:.2f}%",
            f"  Total Memory Accesses:   {m.total_memory_accesses}",
            "=" * 60
        ]
        return "\n".join(lines)
    
    def compare_with(self, other: 'MetricsCollector') -> Dict:
        """Compare metrics with another collector."""
        if not self.simulation_metrics:
            self.calculate_metrics()
        if not other.simulation_metrics:
            other.calculate_metrics()
        
        m1 = self.simulation_metrics
        m2 = other.simulation_metrics
        
        return {
            'algorithms': [m1.algorithm, m2.algorithm],
            'avg_waiting_time': [m1.avg_waiting_time, m2.avg_waiting_time],
            'avg_turnaround_time': [m1.avg_turnaround_time, m2.avg_turnaround_time],
            'avg_response_time': [m1.avg_response_time, m2.avg_response_time],
            'cpu_utilization': [m1.cpu_utilization, m2.cpu_utilization],
            'throughput': [m1.throughput, m2.throughput],
            'context_switches': [m1.context_switches, m2.context_switches]
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.process_metrics.clear()
        self.simulation_metrics = None
        self.context_switches = 0
        self.deadlock_count = 0
        self.deadlocks_resolved = 0
        self.page_faults = 0
        self.memory_accesses = 0
        self.cpu_busy_time = 0
        self.total_time = 0
