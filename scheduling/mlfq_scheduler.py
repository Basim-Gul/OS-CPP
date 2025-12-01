"""Multi-Level Feedback Queue (MLFQ) Scheduler."""

from typing import List, Optional, Deque
from collections import deque
from .base_scheduler import BaseScheduler, SchedulingResult
from models.process import Process, ProcessState


class MLFQScheduler(BaseScheduler):
    """Multi-Level Feedback Queue scheduling algorithm.
    
    3-level queue with different time quantums:
    - Level 0 (highest): Time quantum = 8ms (Round Robin)
    - Level 1 (medium): Time quantum = 16ms (Round Robin)
    - Level 2 (lowest): FCFS
    
    Processes start at level 0 and move down if they use full quantum.
    Processes move up if they yield CPU voluntarily or after priority boost.
    """
    
    def __init__(self, time_quantums: List[int] = None, boost_interval: int = 500):
        super().__init__("MLFQ", preemptive=True)
        self.time_quantums = time_quantums or [8, 16, 0]  # 0 = FCFS for level 2
        self.num_levels = len(self.time_quantums)
        self.queues: List[Deque[Process]] = [deque() for _ in range(self.num_levels)]
        self.boost_interval = boost_interval  # Time interval for priority boost
        self.last_boost_time = 0
    
    def select_next(self) -> Optional[Process]:
        """Select the next process from the highest priority non-empty queue."""
        for level, queue in enumerate(self.queues):
            if queue:
                return queue[0]
        return None
    
    def get_current_level(self) -> int:
        """Get the level of the highest priority non-empty queue."""
        for level, queue in enumerate(self.queues):
            if queue:
                return level
        return -1
    
    def add_to_queue(self, process: Process, level: int = None) -> None:
        """Add a process to a specific queue level."""
        if level is None:
            level = process.queue_level
        level = max(0, min(level, self.num_levels - 1))
        process.queue_level = level
        process.state = ProcessState.READY
        self.queues[level].append(process)
        self.log(f"Process P{process.pid} added to queue level {level}")
    
    def remove_from_queue(self, process: Process) -> None:
        """Remove a process from its current queue."""
        level = process.queue_level
        if process in self.queues[level]:
            self.queues[level].remove(process)
    
    def priority_boost(self) -> None:
        """Move all processes to the highest priority queue."""
        self.log("Priority boost - moving all processes to level 0")
        for level in range(1, self.num_levels):
            while self.queues[level]:
                process = self.queues[level].popleft()
                process.queue_level = 0
                self.queues[0].append(process)
    
    def schedule(self, processes: List[Process]) -> SchedulingResult:
        """Run MLFQ scheduling on the given processes."""
        self.reset()
        for queue in self.queues:
            queue.clear()
        self.last_boost_time = 0
        
        # Reset all processes
        for p in processes:
            p.reset()
            p.queue_level = 0
        
        # Sort by arrival time
        remaining = sorted(processes.copy(), key=lambda p: (p.arrival_time, p.pid))
        n = len(processes)
        completed_count = 0
        
        while completed_count < n:
            # Add arrived processes to level 0 queue
            while remaining and remaining[0].arrival_time <= self.current_time:
                process = remaining.pop(0)
                self.add_to_queue(process, 0)
            
            # Priority boost check
            if self.current_time - self.last_boost_time >= self.boost_interval:
                self.priority_boost()
                self.last_boost_time = self.current_time
            
            # If no process is ready, jump to next event
            current_level = self.get_current_level()
            if current_level == -1:
                if remaining:
                    self.current_time = remaining[0].arrival_time
                    continue
                else:
                    break
            
            # Select next process from highest priority queue
            process = self.queues[current_level].popleft()
            
            # Record response time
            if process.response_time == -1:
                process.response_time = self.current_time - process.arrival_time
            
            # Set process as running
            process.state = ProcessState.RUNNING
            self.running_process = process
            
            # Determine time quantum for this level
            time_quantum = self.time_quantums[current_level]
            if time_quantum == 0:  # FCFS for lowest level
                time_quantum = process.remaining_time
            
            # Determine actual run time
            run_time = min(time_quantum, process.remaining_time)
            
            # Check for arrivals or boost during execution
            next_arrival = remaining[0].arrival_time if remaining else float('inf')
            next_boost = self.last_boost_time + self.boost_interval
            
            # Find next event
            potential_end = self.current_time + run_time
            
            # For simplicity, we'll run the full quantum unless completion
            start_time = self.current_time
            
            if next_arrival < potential_end and current_level > 0:
                # New arrival might need to preempt (if it goes to higher level)
                run_time = next_arrival - self.current_time
            
            actual_run_time = min(run_time, process.remaining_time)
            process.remaining_time -= actual_run_time
            self.current_time += actual_run_time
            
            # Record in Gantt chart
            self.gantt_chart.append((process.pid, start_time, self.current_time))
            
            self.log(f"Process P{process.pid} ran for {actual_run_time}ms at level {current_level}")
            
            # Add newly arrived processes
            while remaining and remaining[0].arrival_time <= self.current_time:
                new_process = remaining.pop(0)
                self.add_to_queue(new_process, 0)
            
            if process.remaining_time <= 0:
                # Process completed
                process.remaining_time = 0
                process.completion_time = self.current_time
                process.state = ProcessState.TERMINATED
                self.calculate_process_metrics(process)
                completed_count += 1
                self.log(f"Process P{process.pid} completed")
            elif actual_run_time >= time_quantum and current_level < self.num_levels - 1:
                # Used full quantum, demote to lower level
                new_level = min(current_level + 1, self.num_levels - 1)
                self.add_to_queue(process, new_level)
                self.log(f"Process P{process.pid} demoted to level {new_level}")
            else:
                # Re-add to same level (yielded early or preempted)
                self.add_to_queue(process, current_level)
            
            # Context switch
            self.context_switches += 1
            self.running_process = None
        
        return self.create_result(processes)
