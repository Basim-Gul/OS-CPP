"""Shortest Remaining Time First (SRTF) Scheduler."""

from typing import List, Optional
from .base_scheduler import BaseScheduler, SchedulingResult
from models.process import Process, ProcessState


class SRTFScheduler(BaseScheduler):
    """Shortest Remaining Time First scheduling algorithm.
    
    Preemptive version of SJF. Preempts running process if a new process
    arrives with shorter remaining time.
    """
    
    def __init__(self):
        super().__init__("SRTF", preemptive=True)
    
    def select_next(self) -> Optional[Process]:
        """Select the process with shortest remaining time."""
        if not self.ready_queue:
            return None
        # SRTF: select process with shortest remaining time
        # Tie-breaker: earlier arrival time, then lower PID
        self.ready_queue.sort(key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
        return self.ready_queue[0]
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run SRTF scheduling on the given processes."""
        self.reset()
        
        # Reset all processes
        for p in processes:
            p.reset()
        
        n = len(processes)
        completed_count = 0
        
        # Add all processes to consideration
        all_processes = {p.pid: p for p in processes}
        
        while completed_count < n:
            # Add arrived processes to ready queue
            for process in processes:
                if (process.arrival_time <= self.current_time and 
                    process.state == ProcessState.NEW):
                    self.add_to_ready_queue(process)
            
            # If no process is ready, jump to next arrival
            if not self.ready_queue:
                next_arrival = min(
                    (p.arrival_time for p in processes if p.state == ProcessState.NEW),
                    default=None
                )
                if next_arrival is not None:
                    self.current_time = next_arrival
                    continue
                else:
                    break
            
            # Select process with shortest remaining time
            process = self.select_next()
            if not process:
                break
            
            # Record response time
            if process.response_time == -1:
                process.response_time = self.current_time - process.arrival_time
            
            # Set process as running
            if self.running_process != process:
                if self.running_process is not None:
                    # Preemption occurred
                    self.log(f"Process P{self.running_process.pid} preempted by P{process.pid}")
                    self.context_switches += 1
                
                process.state = ProcessState.RUNNING
                self.running_process = process
                self.remove_from_ready_queue(process)
            
            # Find next event time (next arrival or completion)
            next_arrival = min(
                (p.arrival_time for p in processes 
                 if p.state == ProcessState.NEW and p.arrival_time > self.current_time),
                default=float('inf')
            )
            
            completion_time = self.current_time + process.remaining_time
            
            # Determine how long to run
            if next_arrival < completion_time:
                # Run until next arrival
                run_time = next_arrival - self.current_time
                start_time = self.current_time
                process.remaining_time -= run_time
                self.current_time = next_arrival
                
                # Record in Gantt chart
                self.gantt_chart.append((process.pid, start_time, self.current_time))
                
                # Put process back in ready queue for re-evaluation
                process.state = ProcessState.READY
                self.ready_queue.append(process)
                self.running_process = None
            else:
                # Run to completion
                start_time = self.current_time
                self.current_time += process.remaining_time
                process.remaining_time = 0
                
                # Record in Gantt chart
                self.gantt_chart.append((process.pid, start_time, self.current_time))
                
                # Process completed
                process.completion_time = self.current_time
                process.state = ProcessState.TERMINATED
                self.calculate_process_metrics(process)
                completed_count += 1
                self.log(f"Process P{process.pid} completed")
                self.running_process = None
        
        return self.create_result(processes)
