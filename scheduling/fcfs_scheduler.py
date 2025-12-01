"""First-Come-First-Serve (FCFS) Scheduler."""

from typing import List, Optional
from .base_scheduler import BaseScheduler, SchedulingResult
from models.process import Process, ProcessState


class FCFSScheduler(BaseScheduler):
    """First-Come-First-Serve scheduling algorithm.
    
    Non-preemptive algorithm that schedules processes in order of arrival.
    """
    
    def __init__(self):
        super().__init__("FCFS", preemptive=False)
    
    def select_next(self) -> Optional[Process]:
        """Select the first process in the ready queue."""
        if not self.ready_queue:
            return None
        # FCFS: select the process that arrived first
        self.ready_queue.sort(key=lambda p: (p.arrival_time, p.pid))
        return self.ready_queue[0]
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run FCFS scheduling on the given processes."""
        self.reset()
        
        # Reset all processes
        for p in processes:
            p.reset()
        
        # Sort by arrival time
        remaining = sorted(processes.copy(), key=lambda p: (p.arrival_time, p.pid))
        completed = []
        
        while remaining or self.ready_queue:
            # Add arrived processes to ready queue
            while remaining and remaining[0].arrival_time <= self.current_time:
                process = remaining.pop(0)
                self.add_to_ready_queue(process)
            
            # If no process is ready, jump to next arrival
            if not self.ready_queue:
                if remaining:
                    self.current_time = remaining[0].arrival_time
                    continue
                else:
                    break
            
            # Select next process (first in queue)
            process = self.select_next()
            if not process:
                break
            
            self.remove_from_ready_queue(process)
            
            # Record response time (first time process starts running)
            if process.response_time == -1:
                process.response_time = self.current_time - process.arrival_time
            
            # Set process as running
            process.state = ProcessState.RUNNING
            process.start_time = self.current_time
            self.running_process = process
            self.log(f"Process P{process.pid} started executing")
            
            # Execute for full burst time (non-preemptive)
            start_time = self.current_time
            self.current_time += process.burst_time
            process.remaining_time = 0
            
            # Record in Gantt chart
            self.gantt_chart.append((process.pid, start_time, self.current_time))
            
            # Process completed
            process.completion_time = self.current_time
            process.state = ProcessState.TERMINATED
            self.calculate_process_metrics(process)
            completed.append(process)
            self.log(f"Process P{process.pid} completed")
            
            # Context switch (if there are more processes)
            if remaining or self.ready_queue:
                self.context_switches += 1
            
            self.running_process = None
        
        return self.create_result(processes)
