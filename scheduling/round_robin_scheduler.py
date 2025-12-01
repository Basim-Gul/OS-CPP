"""Round Robin Scheduler."""

from typing import List, Optional
from collections import deque
from .base_scheduler import BaseScheduler, SchedulingResult
from models.process import Process, ProcessState


class RoundRobinScheduler(BaseScheduler):
    """Round Robin scheduling algorithm.
    
    Preemptive algorithm that gives each process a fixed time quantum.
    """
    
    def __init__(self, time_quantum: int = 10):
        super().__init__(f"Round Robin (q={time_quantum})", preemptive=True)
        self.time_quantum = time_quantum
        self.circular_queue: deque = deque()
    
    def select_next(self) -> Optional[Process]:
        """Select the next process from the circular queue."""
        if not self.circular_queue:
            return None
        return self.circular_queue[0]
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run Round Robin scheduling on the given processes."""
        self.reset()
        self.circular_queue.clear()
        
        # Reset all processes
        for p in processes:
            p.reset()
        
        # Sort by arrival time
        remaining = sorted(processes.copy(), key=lambda p: (p.arrival_time, p.pid))
        n = len(processes)
        completed_count = 0
        
        while completed_count < n:
            # Add arrived processes to circular queue
            while remaining and remaining[0].arrival_time <= self.current_time:
                process = remaining.pop(0)
                process.state = ProcessState.READY
                self.circular_queue.append(process)
                self.log(f"Process P{process.pid} added to queue")
            
            # If no process is ready, jump to next arrival
            if not self.circular_queue:
                if remaining:
                    self.current_time = remaining[0].arrival_time
                    continue
                else:
                    break
            
            # Select next process from front of queue
            process = self.circular_queue.popleft()
            
            # Record response time
            if process.response_time == -1:
                process.response_time = self.current_time - process.arrival_time
            
            # Set process as running
            process.state = ProcessState.RUNNING
            self.running_process = process
            
            # Determine run time (minimum of quantum and remaining time)
            run_time = min(self.time_quantum, process.remaining_time)
            start_time = self.current_time
            
            self.log(f"Process P{process.pid} running for {run_time}ms")
            
            # Execute for run_time
            process.remaining_time -= run_time
            self.current_time += run_time
            
            # Record in Gantt chart
            self.gantt_chart.append((process.pid, start_time, self.current_time))
            
            # Add newly arrived processes to queue (before re-adding current if not complete)
            while remaining and remaining[0].arrival_time <= self.current_time:
                new_process = remaining.pop(0)
                new_process.state = ProcessState.READY
                self.circular_queue.append(new_process)
                self.log(f"Process P{new_process.pid} added to queue")
            
            if process.remaining_time > 0:
                # Process not complete, add to back of queue
                process.state = ProcessState.READY
                self.circular_queue.append(process)
                self.log(f"Process P{process.pid} quantum expired, re-queued")
            else:
                # Process completed
                process.completion_time = self.current_time
                process.state = ProcessState.TERMINATED
                self.calculate_process_metrics(process)
                completed_count += 1
                self.log(f"Process P{process.pid} completed")
            
            # Context switch
            if self.circular_queue or remaining:
                self.context_switches += 1
            
            self.running_process = None
        
        return self.create_result(processes)
