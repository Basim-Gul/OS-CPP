"""Priority Scheduler (both Non-Preemptive and Preemptive with Aging)."""

from typing import List, Optional
from .base_scheduler import BaseScheduler, SchedulingResult
from models.process import Process, ProcessState


class PriorityScheduler(BaseScheduler):
    """Non-preemptive Priority scheduling algorithm.
    
    Schedules processes based on priority (lower value = higher priority).
    """
    
    def __init__(self):
        super().__init__("Priority (Non-Preemptive)", preemptive=False)
    
    def select_next(self) -> Optional[Process]:
        """Select the highest priority process."""
        if not self.ready_queue:
            return None
        # Priority: select process with lowest priority value (highest priority)
        # Tie-breaker: earlier arrival time, then lower PID
        self.ready_queue.sort(key=lambda p: (p.priority, p.arrival_time, p.pid))
        return self.ready_queue[0]
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run Priority scheduling on the given processes."""
        self.reset()
        
        # Reset all processes
        for p in processes:
            p.reset()
        
        # Sort by arrival time initially
        remaining = sorted(processes.copy(), key=lambda p: (p.arrival_time, p.pid))
        
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
            
            # Select highest priority process
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
            self.log(f"Process P{process.pid} started (priority={process.priority})")
            
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
            self.log(f"Process P{process.pid} completed")
            
            # Context switch
            if remaining or self.ready_queue:
                self.context_switches += 1
            
            self.running_process = None
        
        return self.create_result(processes)


class PreemptivePriorityScheduler(BaseScheduler):
    """Preemptive Priority scheduling with aging.
    
    Higher priority process can preempt lower priority.
    Aging prevents starvation by increasing priority of waiting processes.
    """
    
    def __init__(self, aging_interval: int = 50, aging_amount: int = 1):
        super().__init__("Priority (Preemptive with Aging)", preemptive=True)
        self.aging_interval = aging_interval  # Time interval for aging
        self.aging_amount = aging_amount  # Priority increase per aging interval
    
    def select_next(self) -> Optional[Process]:
        """Select the highest priority process considering aging."""
        if not self.ready_queue:
            return None
        # Calculate effective priority (original - aging_counter)
        # Lower effective priority = higher actual priority
        self.ready_queue.sort(
            key=lambda p: (p.priority - p.aging_counter, p.arrival_time, p.pid)
        )
        return self.ready_queue[0]
    
    def apply_aging(self) -> None:
        """Apply aging to all waiting processes."""
        for process in self.ready_queue:
            process.aging_counter += self.aging_amount
            if process.aging_counter > 0:
                self.log(f"Process P{process.pid} aged (effective priority: {process.priority - process.aging_counter})")
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run Preemptive Priority scheduling with aging."""
        self.reset()
        
        # Reset all processes
        for p in processes:
            p.reset()
        
        n = len(processes)
        completed_count = 0
        last_aging_time = 0
        
        while completed_count < n:
            # Add arrived processes to ready queue
            for process in processes:
                if (process.arrival_time <= self.current_time and 
                    process.state == ProcessState.NEW):
                    self.add_to_ready_queue(process)
            
            # Apply aging periodically
            if self.current_time - last_aging_time >= self.aging_interval:
                self.apply_aging()
                last_aging_time = self.current_time
            
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
            
            # Select highest priority process
            process = self.select_next()
            if not process:
                break
            
            # Record response time
            if process.response_time == -1:
                process.response_time = self.current_time - process.arrival_time
            
            # Check for preemption
            if self.running_process != process:
                if self.running_process is not None:
                    self.log(f"Process P{self.running_process.pid} preempted by P{process.pid}")
                    self.context_switches += 1
                
                process.state = ProcessState.RUNNING
                self.running_process = process
                self.remove_from_ready_queue(process)
            
            # Find next event time
            next_arrival = min(
                (p.arrival_time for p in processes 
                 if p.state == ProcessState.NEW and p.arrival_time > self.current_time),
                default=float('inf')
            )
            next_aging = last_aging_time + self.aging_interval
            completion_time = self.current_time + process.remaining_time
            
            next_event = min(next_arrival, next_aging, completion_time)
            run_time = next_event - self.current_time
            
            start_time = self.current_time
            process.remaining_time -= run_time
            self.current_time = next_event
            
            # Record in Gantt chart
            if run_time > 0:
                self.gantt_chart.append((process.pid, start_time, self.current_time))
            
            if process.remaining_time <= 0:
                # Process completed
                process.remaining_time = 0
                process.completion_time = self.current_time
                process.state = ProcessState.TERMINATED
                self.calculate_process_metrics(process)
                completed_count += 1
                self.log(f"Process P{process.pid} completed")
                self.running_process = None
            elif next_event == next_arrival or next_event == next_aging:
                # Put back in ready queue for re-evaluation
                process.state = ProcessState.READY
                self.ready_queue.append(process)
                self.running_process = None
        
        return self.create_result(processes)
