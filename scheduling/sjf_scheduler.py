"""Shortest Job First (SJF) Scheduler."""

from typing import List, Optional
from .base_scheduler import BaseScheduler, SchedulingResult
from models.process import Process, ProcessState


class SJFScheduler(BaseScheduler):
    """Shortest Job First scheduling algorithm.
    
    Non-preemptive algorithm that schedules the process with shortest burst time.
    """
    
    def __init__(self):
        super().__init__("SJF", preemptive=False)
    
    def select_next(self) -> Optional[Process]:
        """Select the process with shortest burst time."""
        if not self.ready_queue:
            return None
        # SJF: select process with shortest burst time
        # Tie-breaker: earlier arrival time, then lower PID
        self.ready_queue.sort(key=lambda p: (p.burst_time, p.arrival_time, p.pid))
        return self.ready_queue[0]
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run SJF scheduling on the given processes."""
        self.reset()
        
        # Reset all processes
        for p in processes:
            p.reset()
        
        # Sort by arrival time initially
        remaining = sorted(processes.copy(), key=lambda p: (p.arrival_time, p.pid))
        completed = []
        
        while remaining or self.ready_queue:
            # Add arrived processes to ready queue
            arrived = [p for p in remaining if p.arrival_time <= self.current_time]
            for process in arrived:
                remaining.remove(process)
                self.add_to_ready_queue(process)
            
            # If no process is ready, jump to next arrival
            if not self.ready_queue:
                if remaining:
                    self.current_time = remaining[0].arrival_time
                    continue
                else:
                    break
            
            # Select next process (shortest burst time)
            process = self.select_next()
            if not process:
                break
            
            self.remove_from_ready_queue(process)
            
            # Record response time
            if process.response_time == -1:
                process.response_time = self.current_time - process.arrival_time
            
            # Set process as running
            process.state = ProcessState.RUNNING
            process.start_time = self.current_time
            self.running_process = process
            self.log(f"Process P{process.pid} started executing (burst={process.burst_time}ms)")
            
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
            
            # Context switch
            if remaining or self.ready_queue:
                self.context_switches += 1
            
            self.running_process = None
        
        return self.create_result(processes)
