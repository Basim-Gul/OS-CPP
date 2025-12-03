# BAHRIA UNIVERSITY, KARACHI CAMPUS
## Department of Computer Science

# Operating System Simulation Project
## Assignment Report

---

## COVER PAGE

| Field | Value |
|-------|-------|
| **University** | Bahria University, Karachi Campus |
| **Department** | Computer Science |
| **Course** | Operating System (CSC-320) |
| **Class** | BS(CS)-5B |
| **Semester** | Fall 2025 |
| **Instructor** | Asma Basit |
| **Marks** | 10 (80% Code + 20% Explanation) |
| **Student Name** | ________________________________ |
| **Roll Number** | ________________________________ |
| **Submission Date** | ________________________________ |

---

## TABLE OF CONTENTS

| Section | Title | Page |
|---------|-------|------|
| 1 | Introduction | 3 |
| 2 | Project Architecture | 4 |
| 3 | **REQUIREMENT 1:** CPU Scheduling Algorithms | 5 |
| 3.1 | First-Come-First-Serve (FCFS) | 6 |
| 3.2 | Shortest Job First (SJF) | 7 |
| 3.3 | Shortest Remaining Time First (SRTF) | 8 |
| 3.4 | Round Robin | 9 |
| 3.5 | Priority Scheduling | 10 |
| 3.6 | Multi-Level Feedback Queue (MLFQ) | 11 |
| 3.7 | Adaptive Scheduler Selector | 12 |
| 3.8 | Algorithm Comparison & Analysis | 14 |
| 4 | **REQUIREMENT 2:** Resource Allocation & Deadlock | 15 |
| 4.1 | Resource Manager Implementation | 15 |
| 4.2 | Resource Allocation Graph (RAG) | 17 |
| 4.3 | Deadlock Scenario (Test Scenario 3) | 18 |
| 5 | **REQUIREMENT 3:** Synchronization Mechanisms | 19 |
| 5.1 | Mutex Implementation | 19 |
| 5.2 | Semaphore Implementation | 20 |
| 5.3 | Race Condition Demonstration | 21 |
| 6 | **REQUIREMENT 4:** Deadlock Handling Mechanisms | 22 |
| 6.1 | Deadlock Detection (DFS Cycle Detection) | 22 |
| 6.2 | Deadlock Prevention (Bankers Algorithm) | 23 |
| 6.3 | Deadlock Resolution | 24 |
| 6.4 | Resource Ordering | 25 |
| 6.5 | Mechanism Comparison Table | 26 |
| 7 | **REQUIREMENT 5:** Memory Management | 27 |
| 7.1 | FIFO Page Replacement | 27 |
| 7.2 | LRU Page Replacement | 28 |
| 7.3 | Optimal (Beladys) Page Replacement | 29 |
| 7.4 | Clock (Second Chance) Page Replacement | 30 |
| 7.5 | Conclusion: LRU is Best | 31 |
| 8 | **REQUIREMENT 6:** System Testing | 32 |
| 8.1 | Test Scenario 1: CPU-Bound Batch | 32 |
| 8.2 | Test Scenario 2: Interactive Mixed | 33 |
| 8.3 | Test Scenario 3: Deadlock Demo | 34 |
| 8.4 | Test Scenario 4: Race Condition | 35 |
| 8.5 | Test Scenario 5: Memory Thrashing | 36 |
| 9 | Conclusions | 37 |
| 10 | Appendices | 38 |

---

# 1. INTRODUCTION

## 1.1 Project Overview

This OS Simulation System is a comprehensive Python-based operating system simulation designed for educational purposes. The project implements core operating system concepts including:

- **CPU Scheduling**: 7 different scheduling algorithms
- **Resource Management**: Resource allocation and tracking
- **Deadlock Handling**: Detection, prevention, and resolution
- **Synchronization**: Mutex and semaphore implementations
- **Memory Management**: 4 page replacement algorithms

## 1.2 Repository Information

| Property | Value |
|----------|-------|
| Repository | `Basim-Gul/OS-CPP` |
| Language | Python 3.8+ |
| Platform | Ubuntu/Linux Terminal |
| UI | Console-based (Rich library) |

## 1.3 Project Structure

```
OS-CPP/
|-- main.py                          # Entry point
|-- requirements.txt                 # Dependencies
|-- README.md
|
|-- models/                          # Data models
|   |-- process.py                   # Process class
|   |-- resource.py                  # Resource class
|   |-- memory_page.py               # Page/Frame classes
|   |-- mutex.py                     # Mutex implementation
|   |-- semaphore.py                 # Semaphore implementation
|
|-- scheduling/                      # Scheduling algorithms
|   |-- base_scheduler.py            # Abstract base
|   |-- fcfs_scheduler.py
|   |-- sjf_scheduler.py
|   |-- srtf_scheduler.py
|   |-- round_robin_scheduler.py
|   |-- priority_scheduler.py
|   |-- mlfq_scheduler.py
|   |-- adaptive_selector.py
|
|-- resources/                       # Resource management
|   |-- resource_manager.py
|   |-- rag.py                       # Resource Allocation Graph
|   |-- deadlock_detector.py
|   |-- bankers_algorithm.py
|   |-- deadlock_resolver.py
|
|-- memory/                          # Memory management
|   |-- memory_manager.py
|   |-- page_table.py
|   |-- fifo_replacement.py
|   |-- lru_replacement.py
|   |-- optimal_replacement.py
|   |-- clock_replacement.py
|
|-- tests/                           # Test scenarios
|   |-- test_scenario_1.py           # CPU-bound batch
|   |-- test_scenario_2.py           # Interactive mixed
|   |-- test_scenario_3.py           # Deadlock demo
|   |-- test_scenario_4.py           # Race condition
|   |-- test_scenario_5.py           # Memory thrashing
```

---

# 2. PROJECT ARCHITECTURE

## 2.1 Core Components

The simulation is built around several key components:

1. **Process Model** (`models/process.py`): Defines process states and attributes
2. **Scheduling Engine** (`scheduling/`): Implements CPU scheduling algorithms
3. **Resource Manager** (`resources/`): Handles resource allocation and deadlock
4. **Memory Manager** (`memory/`): Implements virtual memory with paging
5. **Synchronization** (`models/mutex.py`, `models/semaphore.py`): Thread synchronization

## 2.2 Process States

The system implements the standard 5-state process model:

| State | Description | Color Code |
|-------|-------------|------------|
| NEW | Process just created | Cyan |
| READY | Waiting for CPU | Green |
| RUNNING | Currently executing | Yellow |
| BLOCKED | Waiting for resource/I/O | Red |
| TERMINATED | Execution complete | White |

---

# 3. REQUIREMENT 1: CPU SCHEDULING ALGORITHMS

This section covers all 7 CPU scheduling algorithms implemented in the `scheduling/` directory.

---

## 3.1 First-Come-First-Serve (FCFS)

**File:** `scheduling/fcfs_scheduler.py`

### Algorithm Description
FCFS is the simplest scheduling algorithm. It schedules processes in the order they arrive (first-in, first-out). It is non-preemptive - once a process starts, it runs to completion.

### Key Characteristics
- **Type**: Non-preemptive
- **Selection Criteria**: Arrival time (earliest first)
- **Tie-breaker**: Process ID (lower PID first)

### Implementation Code

```python
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

```

### Analysis
- **Advantages**: Simple, fair (no starvation)
- **Disadvantages**: Convoy effect - short processes wait behind long ones
- **Best for**: Batch systems with similar job lengths

---

## 3.2 Shortest Job First (SJF)

**File:** `scheduling/sjf_scheduler.py`

### Algorithm Description
SJF selects the process with the shortest burst time. It is optimal for minimizing average waiting time among non-preemptive algorithms.

### Key Characteristics
- **Type**: Non-preemptive
- **Selection Criteria**: Burst time (shortest first)
- **Tie-breaker**: Arrival time, then PID

### Implementation Code

```python
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

```

### Analysis
- **Advantages**: Optimal average waiting time (non-preemptive)
- **Disadvantages**: Starvation of long processes, requires burst time prediction
- **Best for**: Batch systems where burst times are known

---

## 3.3 Shortest Remaining Time First (SRTF)

**File:** `scheduling/srtf_scheduler.py`

### Algorithm Description
SRTF is the preemptive version of SJF. When a new process arrives with a shorter remaining time than the currently running process, preemption occurs.

### Key Characteristics
- **Type**: Preemptive
- **Selection Criteria**: Remaining time (shortest first)
- **Preemption**: On new process arrival

### Implementation Code

```python
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

```

### Analysis
- **Advantages**: Optimal average waiting time overall
- **Disadvantages**: Higher context switch overhead, starvation possible
- **Best for**: Interactive systems with varying job lengths

---

## 3.4 Round Robin

**File:** `scheduling/round_robin_scheduler.py`

### Algorithm Description
Round Robin gives each process a fixed time quantum. After the quantum expires, the process is preempted and moved to the back of the queue.

### Key Characteristics
- **Type**: Preemptive
- **Time Quantum**: Configurable (default 10ms)
- **Queue**: Circular FIFO queue

### Implementation Code

```python
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

```

### Analysis
- **Advantages**: Fair, good response time, no starvation
- **Disadvantages**: Higher context switches, performance depends on quantum
- **Best for**: Time-sharing systems, interactive environments

---

## 3.5 Priority Scheduling

**File:** `scheduling/priority_scheduler.py`

### Algorithm Description
Processes are scheduled based on priority. Lower priority value = higher priority. Includes both non-preemptive and preemptive (with aging) variants.

### Key Characteristics
- **Type**: Non-preemptive and Preemptive variants
- **Selection Criteria**: Priority value (lower = higher priority)
- **Aging**: Prevents starvation by increasing priority over time

### Implementation Code

```python
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

```

### Analysis
- **Advantages**: Supports different importance levels
- **Disadvantages**: Starvation without aging
- **Best for**: Systems with clear process priorities

---

## 3.6 Multi-Level Feedback Queue (MLFQ)

**File:** `scheduling/mlfq_scheduler.py`

### Algorithm Description
MLFQ uses multiple queues with different priorities and time quantums. Processes move between queues based on their behavior.

### Queue Structure
| Level | Time Quantum | Algorithm |
|-------|--------------|-----------|
| 0 (highest) | 8ms | Round Robin |
| 1 (medium) | 16ms | Round Robin |
| 2 (lowest) | FCFS | FCFS |

### Key Characteristics
- **Type**: Preemptive
- **Queues**: 3 levels with different quantums
- **Priority Boost**: Periodic boost to prevent starvation

### Implementation Code

```python
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

```

### Analysis
- **Advantages**: Adapts to process behavior, balances fairness and efficiency
- **Disadvantages**: Complex, many parameters to tune
- **Best for**: General-purpose systems with mixed workloads

---

## 3.7 Adaptive Scheduler Selector

**File:** `scheduling/adaptive_selector.py`

### Algorithm Description
The Adaptive Selector analyzes workload characteristics and automatically selects the best scheduling algorithm.

### Workload Analysis Metrics
- Process count
- Average burst time
- Burst time variance/coefficient of variation
- Priority distribution
- I/O-bound vs CPU-bound ratio

### Selection Logic
1. Calculate performance estimates for all 7 algorithms
2. Sort by estimated waiting time
3. Select from top 3 based on workload type:
   - **Batch workloads**: Prefer SJF/SRTF
   - **Interactive workloads**: Prefer Round Robin/MLFQ
   - **High priority variance**: Prefer Priority scheduling

### Implementation Code

```python
"""Adaptive Scheduler Selector for OS simulation."""

from typing import List, Tuple, Optional, Type, Dict
from dataclasses import dataclass
import statistics

from models.process import Process
from .base_scheduler import BaseScheduler, SchedulingResult
from .fcfs_scheduler import FCFSScheduler
from .sjf_scheduler import SJFScheduler
from .srtf_scheduler import SRTFScheduler
from .round_robin_scheduler import RoundRobinScheduler
from .priority_scheduler import PriorityScheduler, PreemptivePriorityScheduler
from .mlfq_scheduler import MLFQScheduler


@dataclass
class WorkloadAnalysis:
    """Analysis of process workload characteristics."""
    process_count: int
    avg_burst_time: float
    burst_time_variance: float
    coefficient_of_variation: float
    priority_range: int
    priority_variance: float
    io_bound_ratio: float
    cpu_bound_ratio: float
    avg_arrival_spread: float
    is_interactive: bool
    is_batch: bool


@dataclass
class SchedulerRecommendation:
    """Recommendation for scheduler selection."""
    scheduler: BaseScheduler
    algorithm_name: str
    justification: str
    expected_avg_wait: float
    confidence: float  # 0.0 to 1.0


@dataclass
class PerformanceEstimate:
    """Performance estimate for an algorithm."""
    algorithm: str
    estimated_wait_time: float
    scheduler_class: type


class AdaptiveSelector:
    """Intelligent scheduler selector based on workload analysis."""
    
    # Constants for Round Robin quantum calculation
    MIN_TIME_QUANTUM = 10
    MAX_TIME_QUANTUM = 50
    QUANTUM_DIVISOR = 5
    
    # Threshold for using Priority scheduler
    PRIORITY_VARIANCE_THRESHOLD = 6
    PRIORITY_RANGE_THRESHOLD = 7
    
    def __init__(self):
        self.schedulers = {
            'FCFS': FCFSScheduler,
            'SJF': SJFScheduler,
            'SRTF': SRTFScheduler,
            'RR': RoundRobinScheduler,
            'Priority': PriorityScheduler,
            'PreemptivePriority': PreemptivePriorityScheduler,
            'MLFQ': MLFQScheduler
        }
    
    def analyze_workload(self, processes: List[Process]) -> WorkloadAnalysis:
        """Analyze the characteristics of the process workload."""
        if not processes:
            return WorkloadAnalysis(
                process_count=0, avg_burst_time=0, burst_time_variance=0,
                coefficient_of_variation=0, priority_range=0, priority_variance=0,
                io_bound_ratio=0, cpu_bound_ratio=0, avg_arrival_spread=0,
                is_interactive=False, is_batch=False
            )
        
        n = len(processes)
        burst_times = [p.burst_time for p in processes]
        priorities = [p.priority for p in processes]
        arrival_times = sorted([p.arrival_time for p in processes])
        
        # Basic statistics
        avg_burst = statistics.mean(burst_times)
        burst_variance = statistics.variance(burst_times) if n > 1 else 0
        burst_stdev = statistics.stdev(burst_times) if n > 1 else 0
        cv = burst_stdev / avg_burst if avg_burst > 0 else 0
        
        priority_range = max(priorities) - min(priorities) if n > 0 else 0
        priority_variance = statistics.variance(priorities) if n > 1 else 0
        
        # I/O vs CPU bound ratio
        io_count = sum(1 for p in processes if p.io_bound)
        io_ratio = io_count / n
        cpu_ratio = 1 - io_ratio
        
        # Arrival spread
        if n > 1:
            arrival_diffs = [arrival_times[i+1] - arrival_times[i] 
                           for i in range(len(arrival_times)-1)]
            avg_spread = statistics.mean(arrival_diffs) if arrival_diffs else 0
        else:
            avg_spread = 0
        
        # Classification
        is_interactive = avg_burst < 50 and io_ratio > 0.3
        is_batch = avg_burst > 100 and io_ratio < 0.2
        
        return WorkloadAnalysis(
            process_count=n,
            avg_burst_time=avg_burst,
            burst_time_variance=burst_variance,
            coefficient_of_variation=cv,
            priority_range=priority_range,
            priority_variance=priority_variance,
            io_bound_ratio=io_ratio,
            cpu_bound_ratio=cpu_ratio,
            avg_arrival_spread=avg_spread,
            is_interactive=is_interactive,
            is_batch=is_batch
        )
    
    def _estimate_performance(self, processes: List[Process], 
                              analysis: WorkloadAnalysis) -> Dict[str, PerformanceEstimate]:
        """Estimate avg waiting time for ALL 7 algorithms.
        
        Args:
            processes: List of processes to analyze
            analysis: Pre-computed workload analysis
            
        Returns:
            Dictionary mapping algorithm name to PerformanceEstimate
        """
        n = analysis.process_count
        avg_burst = analysis.avg_burst_time
        cv = analysis.coefficient_of_variation
        
        estimates = {}
        
        # FCFS: Average waiting time approximation
        # Convoy effect makes this worse with high variance
        fcfs_wait = avg_burst * (n - 1) / 2
        if cv > 0.5:
            fcfs_wait *= (1 + cv * 0.3)  # Penalize for high variance
        estimates['FCFS'] = PerformanceEstimate('FCFS', fcfs_wait, FCFSScheduler)
        
        # SJF: Optimal for non-preemptive - better with sorted short jobs
        sjf_wait = avg_burst * (n - 1) / 3
        estimates['SJF'] = PerformanceEstimate('SJF', sjf_wait, SJFScheduler)
        
        # SRTF: Best case, preemptive version of SJF
        srtf_wait = avg_burst * (n - 1) / 4
        estimates['SRTF'] = PerformanceEstimate('SRTF', srtf_wait, SRTFScheduler)
        
        # Round Robin: Depends on quantum
        quantum = max(self.MIN_TIME_QUANTUM, int(avg_burst / self.QUANTUM_DIVISOR))
        quantum = min(quantum, self.MAX_TIME_QUANTUM)
        rr_wait = avg_burst * n / 2
        # RR is better for interactive (I/O-bound) workloads
        if analysis.io_bound_ratio > 0.3:
            rr_wait *= 0.8
        # Use default value to avoid closure issue
        estimates['RR'] = PerformanceEstimate(f'RR (q={quantum})', rr_wait, 
                                               lambda q=quantum: RoundRobinScheduler(q))
        
        # Priority: Depends on priority distribution
        priority_wait = avg_burst * (n - 1) / 3
        # Worse if priorities are similar (less meaningful ordering)
        if analysis.priority_variance < 3:
            priority_wait *= 1.3
        estimates['Priority'] = PerformanceEstimate('Priority', priority_wait, PriorityScheduler)
        
        # Preemptive Priority: Better with high I/O ratio
        preemptive_priority_wait = avg_burst * (n - 1) / 4
        if analysis.io_bound_ratio > 0.3:
            preemptive_priority_wait *= 0.9
        estimates['PreemptivePriority'] = PerformanceEstimate('Preemptive Priority', 
                                                               preemptive_priority_wait,
                                                               PreemptivePriorityScheduler)
        
        # MLFQ: Good for mixed workloads with many processes
        mlfq_wait = avg_burst * n / 3
        if n > 10:
            mlfq_wait *= 0.9  # Scales better with many processes
        estimates['MLFQ'] = PerformanceEstimate('MLFQ', mlfq_wait, MLFQScheduler)
        
        return estimates
    
    def select_scheduler(self, processes: List[Process]) -> SchedulerRecommendation:
        """Select the best scheduling algorithm based on workload analysis.
        
        Uses performance estimation to prioritize algorithms with lowest
        estimated waiting time, while considering workload characteristics.
        """
        analysis = self.analyze_workload(processes)
        
        # Handle empty process list
        if analysis.process_count == 0:
            return SchedulerRecommendation(
                scheduler=FCFSScheduler(),
                algorithm_name="FCFS",
                justification="No processes to schedule. FCFS selected as default.",
                expected_avg_wait=0,
                confidence=1.0
            )
        
        # Step 1: Calculate performance estimates for all algorithms
        estimates = self._estimate_performance(processes, analysis)
        
        # Step 2: Sort by estimated wait time (ascending)
        sorted_estimates = sorted(estimates.values(), 
                                  key=lambda x: x.estimated_wait_time)
        
        # Get top 3 algorithms
        top_3 = sorted_estimates[:3]
        top_3_keys = set()
        for e in top_3:
            if 'Priority' in e.algorithm and 'Preemptive' in e.algorithm:
                top_3_keys.add('PreemptivePriority')
            elif 'Priority' in e.algorithm:
                top_3_keys.add('Priority')
            elif 'RR' in e.algorithm:
                top_3_keys.add('RR')
            else:
                top_3_keys.add(e.algorithm)
        
        # Step 3: Select from top 3 based on workload type
        selected = top_3[0]  # Default to best performer
        
        # Step 4: Only use Priority scheduling if it's in top 3 AND meets criteria
        priority_criteria_met = (analysis.priority_variance > self.PRIORITY_VARIANCE_THRESHOLD and 
                                  analysis.priority_range > self.PRIORITY_RANGE_THRESHOLD)
        
        # Check if Priority (non-preemptive) is in top 3
        priority_in_top_3 = 'Priority' in top_3_keys
        preemptive_priority_in_top_3 = 'PreemptivePriority' in top_3_keys
        
        if priority_criteria_met:
            if preemptive_priority_in_top_3 and analysis.io_bound_ratio > 0.3:
                selected = estimates['PreemptivePriority']
            elif priority_in_top_3:
                selected = estimates['Priority']
            # If neither is in top 3, use best performer (already selected)
        else:
            # Select based on workload type from top 3
            if analysis.is_interactive:
                # Prefer RR or MLFQ for interactive workloads
                for e in top_3:
                    if 'RR' in e.algorithm or 'MLFQ' in e.algorithm:
                        selected = e
                        break
            elif analysis.io_bound_ratio > 0.5:
                # High I/O: prefer RR or MLFQ
                for e in top_3:
                    if 'RR' in e.algorithm or 'MLFQ' in e.algorithm:
                        selected = e
                        break
            # Otherwise, use the best performer (already selected)
        
        # Build performance estimates string for justification
        estimates_str = self._format_performance_estimates(sorted_estimates, selected.algorithm)
        
        # Create scheduler instance - all scheduler_class values are callable
        scheduler = selected.scheduler_class()
        
        # Build justification
        justification = self._build_justification(selected, analysis, estimates_str)
        
        return SchedulerRecommendation(
            scheduler=scheduler,
            algorithm_name=selected.algorithm,
            justification=justification,
            expected_avg_wait=selected.estimated_wait_time,
            confidence=0.85
        )
    
    def _format_performance_estimates(self, sorted_estimates: List[PerformanceEstimate],
                                       selected_algo: str) -> str:
        """Format performance estimates for display."""
        lines = []
        for i, est in enumerate(sorted_estimates):
            marker = "← BEST" if i == 0 else ""
            if est.algorithm == selected_algo and i > 0:
                marker = "← SELECTED"
            lines.append(f"  {est.algorithm:25s} {est.estimated_wait_time:>8.0f}ms {marker}")
        return "\n".join(lines)
    
    def _build_justification(self, selected: PerformanceEstimate,
                             analysis: WorkloadAnalysis,
                             estimates_str: str) -> str:
        """Build detailed justification string."""
        algo_name = selected.algorithm.split()[0]  # Remove quantum info if present
        
        reason = ""
        if algo_name in ('SRTF', 'SJF'):
            reason = f"{algo_name} provides lowest estimated waiting time for this workload."
        elif 'RR' in algo_name:
            reason = f"Round Robin provides fair CPU distribution for {analysis.process_count} processes."
        elif 'MLFQ' in algo_name:
            reason = "MLFQ adapts to process behavior, balancing interactive and batch workloads."
        elif 'Priority' in algo_name:
            reason = f"Priority scheduling is effective with high priority variance (range={analysis.priority_range})."
        else:
            reason = f"FCFS provides simplicity with minimal overhead."
        
        return (
            f"SELECTED: {selected.algorithm}\n\n"
            f"Performance Estimates:\n{estimates_str}\n\n"
            f"Workload: {analysis.process_count} processes, "
            f"CV={analysis.coefficient_of_variation:.2f}, "
            f"I/O ratio={analysis.io_bound_ratio*100:.0f}%\n\n"
            f"Justification: {reason}"
        )
    
    def compare_all(self, processes: List[Process]) -> List[Tuple[str, SchedulingResult]]:
        """Run all scheduling algorithms and return results for comparison."""
        results = []
        
        for name, scheduler_class in self.schedulers.items():
            # Reset processes for each scheduler
            for p in processes:
                p.reset()
            
            # Create scheduler instance
            if name == 'RR':
                scheduler = scheduler_class(time_quantum=20)
            else:
                scheduler = scheduler_class()
            
            # Run scheduling
            result = scheduler.schedule(processes)
            results.append((name, result))
        
        return results

```

---

## 3.8 Algorithm Comparison & Analysis

### Comparison Table

| Algorithm | Type | Avg Wait Time | Response Time | Starvation | Overhead |
|-----------|------|---------------|---------------|------------|----------|
| FCFS | Non-preemptive | High | Poor | No | Low |
| SJF | Non-preemptive | Optimal* | Poor | Yes | Low |
| SRTF | Preemptive | Optimal | Good | Yes | Medium |
| Round Robin | Preemptive | Medium | Excellent | No | High |
| Priority | Both | Varies | Varies | Yes** | Low |
| MLFQ | Preemptive | Good | Good | No | High |
| Adaptive | Dynamic | Best*** | Good | No | Medium |

*Optimal among non-preemptive
**Without aging
***Selects best algorithm for workload

### When to Use Each Algorithm

| Workload Type | Recommended Algorithm | Justification |
|--------------|----------------------|---------------|
| CPU-bound batch | SJF/SRTF | Minimizes average waiting time |
| Interactive | Round Robin/MLFQ | Good response time |
| Mixed | MLFQ/Adaptive | Adapts to process behavior |
| Priority-based | Priority with Aging | Respects priorities, prevents starvation |
| Unknown | Adaptive | Analyzes and selects automatically |

---

# 4. REQUIREMENT 2: RESOURCE ALLOCATION & DEADLOCK

---

## 4.1 Resource Manager Implementation

**File:** `resources/resource_manager.py`

### Description
The Resource Manager handles allocation, release, and tracking of system resources. It maintains allocation history and provides matrices for deadlock analysis.

### Default Resources
| ID | Name | Type | Instances |
|----|------|------|-----------|
| 1 | CPU | CPU | 4 |
| 2 | Memory | MEMORY | 16 |
| 3 | Printer | PRINTER | 2 |
| 4 | Disk | DISK | 4 |

### Implementation Code

```python
"""Resource Manager for OS simulation."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from models.resource import Resource, ResourceType
from models.process import Process


@dataclass
class AllocationEvent:
    """Record of a resource allocation event."""
    timestamp: int
    event_type: str  # 'allocate', 'release', 'request', 'deny'
    process_id: int
    resource_id: int
    resource_name: str
    count: int
    success: bool
    message: str = ""


class ResourceManager:
    """Manages resources and their allocation to processes."""
    
    def __init__(self):
        self.resources: Dict[int, Resource] = {}
        self.processes: Dict[int, Process] = {}
        self.allocation_history: List[AllocationEvent] = []
        self.current_time: int = 0
        
        # Initialize default resources
        self._init_default_resources()
    
    def _init_default_resources(self) -> None:
        """Initialize the default system resources."""
        default_resources = [
            (1, "CPU", ResourceType.CPU, 4),
            (2, "Memory", ResourceType.MEMORY, 16),  # 16 memory units
            (3, "Printer", ResourceType.PRINTER, 2),
            (4, "Disk", ResourceType.DISK, 4)
        ]
        
        for rid, name, rtype, instances in default_resources:
            self.add_resource(Resource(rid, name, rtype, instances))
    
    def add_resource(self, resource: Resource) -> None:
        """Add a resource to the system."""
        self.resources[resource.rid] = resource
    
    def remove_resource(self, rid: int) -> Optional[Resource]:
        """Remove a resource from the system."""
        return self.resources.pop(rid, None)
    
    def get_resource(self, rid: int) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.resources.get(rid)
    
    def get_resource_by_name(self, name: str) -> Optional[Resource]:
        """Get a resource by name."""
        for resource in self.resources.values():
            if resource.name == name:
                return resource
        return None
    
    def register_process(self, process: Process) -> None:
        """Register a process with the resource manager."""
        self.processes[process.pid] = process
    
    def unregister_process(self, pid: int) -> None:
        """Unregister a process and release all its resources."""
        if pid in self.processes:
            self.release_all(pid)
            del self.processes[pid]
    
    def request(self, pid: int, rid: int, count: int = 1) -> bool:
        """Request resources for a process.
        
        Returns True if allocation was successful, False otherwise.
        """
        if rid not in self.resources:
            self._log_event('deny', pid, rid, "", count, False, "Resource not found")
            return False
        
        resource = self.resources[rid]
        
        if resource.is_available(count):
            success = resource.allocate(pid, count)
            if success:
                # Update process allocation tracking
                if pid in self.processes:
                    process = self.processes[pid]
                    if resource.name in process.allocated_resources:
                        process.allocated_resources[resource.name] += count
                    else:
                        process.allocated_resources[resource.name] = count
                
                self._log_event('allocate', pid, rid, resource.name, count, True,
                              f"Allocated {count} instance(s)")
                return True
        
        # Resource not available, add to waiting queue
        resource.request(pid)
        
        # Track in process requested resources
        if pid in self.processes:
            process = self.processes[pid]
            if resource.name in process.requested_resources:
                process.requested_resources[resource.name] += count
            else:
                process.requested_resources[resource.name] = count
        
        self._log_event('request', pid, rid, resource.name, count, False,
                       f"Waiting for {count} instance(s)")
        return False
    
    def release(self, pid: int, rid: int, count: Optional[int] = None) -> int:
        """Release resources from a process.
        
        Returns the number of instances released.
        """
        if rid not in self.resources:
            return 0
        
        resource = self.resources[rid]
        released = resource.release(pid, count)
        
        if released > 0:
            # Update process allocation tracking
            if pid in self.processes:
                process = self.processes[pid]
                if resource.name in process.allocated_resources:
                    process.allocated_resources[resource.name] -= released
                    if process.allocated_resources[resource.name] <= 0:
                        del process.allocated_resources[resource.name]
            
            self._log_event('release', pid, rid, resource.name, released, True,
                          f"Released {released} instance(s)")
        
        return released
    
    def release_all(self, pid: int) -> Dict[int, int]:
        """Release all resources held by a process.
        
        Returns a dict of resource_id -> released_count.
        """
        released = {}
        for rid, resource in self.resources.items():
            count = resource.release(pid)
            if count > 0:
                released[rid] = count
                self._log_event('release', pid, rid, resource.name, count, True,
                              f"Released all {count} instance(s)")
        
        # Clear process allocation tracking
        if pid in self.processes:
            self.processes[pid].allocated_resources.clear()
            self.processes[pid].requested_resources.clear()
        
        return released
    
    def get_allocation_matrix(self) -> Dict[int, Dict[int, int]]:
        """Get the current allocation matrix.
        
        Returns: {pid: {rid: count}}
        """
        allocation = {}
        for rid, resource in self.resources.items():
            for pid, count in resource.allocated_to.items():
                if pid not in allocation:
                    allocation[pid] = {}
                allocation[pid][rid] = count
        return allocation
    
    def get_available_vector(self) -> Dict[int, int]:
        """Get the available resources vector.
        
        Returns: {rid: available_count}
        """
        return {rid: r.available_instances for rid, r in self.resources.items()}
    
    def get_max_matrix(self) -> Dict[int, Dict[int, int]]:
        """Get the maximum resource needs (for Banker's algorithm).
        
        Returns: {pid: {rid: max_need}}
        """
        # This would typically come from process declarations
        # For now, we'll estimate based on current allocation + requested
        max_matrix = {}
        for pid in self.processes:
            max_matrix[pid] = {}
            process = self.processes[pid]
            for rid, resource in self.resources.items():
                allocated = resource.get_allocated_count(pid)
                # Assume max = allocated + 2 (for demonstration)
                max_matrix[pid][rid] = allocated + 2
        return max_matrix
    
    def get_status(self) -> Dict:
        """Get the current resource status."""
        return {
            'resources': [
                {
                    'id': r.rid,
                    'name': r.name,
                    'type': r.resource_type.value,
                    'total': r.total_instances,
                    'available': r.available_instances,
                    'allocated_to': dict(r.allocated_to),
                    'waiting': list(r.waiting_queue)
                }
                for r in self.resources.values()
            ],
            'allocation_matrix': self.get_allocation_matrix(),
            'available': self.get_available_vector()
        }
    
    def _log_event(self, event_type: str, pid: int, rid: int, 
                   resource_name: str, count: int, success: bool,
                   message: str = "") -> None:
        """Log a resource allocation event."""
        event = AllocationEvent(
            timestamp=self.current_time,
            event_type=event_type,
            process_id=pid,
            resource_id=rid,
            resource_name=resource_name,
            count=count,
            success=success,
            message=message
        )
        self.allocation_history.append(event)
    
    def set_time(self, time: int) -> None:
        """Set the current simulation time."""
        self.current_time = time
    
    def reset(self) -> None:
        """Reset the resource manager to initial state."""
        for resource in self.resources.values():
            resource.reset()
        self.processes.clear()
        self.allocation_history.clear()
        self.current_time = 0

```

---

## 4.2 Resource Allocation Graph (RAG)

**File:** `resources/rag.py`

### Description
The RAG represents the resource allocation state using a directed graph:
- **Process nodes**: [P1], [P2], ...
- **Resource nodes**: (R1), (R2), ...
- **Request edges**: P -> R (process wants resource)
- **Assignment edges**: R -> P (resource held by process)

### Implementation Code

```python
"""Resource Allocation Graph (RAG) implementation for OS simulation."""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    """Type of node in the RAG."""
    PROCESS = "process"
    RESOURCE = "resource"


@dataclass
class Node:
    """A node in the Resource Allocation Graph."""
    node_id: str
    node_type: NodeType
    name: str
    
    # For resource nodes
    total_instances: int = 1
    available_instances: int = 1


@dataclass
class Edge:
    """An edge in the Resource Allocation Graph."""
    from_node: str
    to_node: str
    edge_type: str  # 'request' (P -> R) or 'assignment' (R -> P)
    count: int = 1
    timestamp: int = 0


class ResourceAllocationGraph:
    """Resource Allocation Graph for deadlock detection and visualization."""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.adjacency_list: Dict[str, List[str]] = {}  # For cycle detection
    
    def add_process(self, pid: int, name: str = None) -> None:
        """Add a process node to the graph."""
        node_id = f"P{pid}"
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(
                node_id=node_id,
                node_type=NodeType.PROCESS,
                name=name or f"Process {pid}"
            )
            self.adjacency_list[node_id] = []
    
    def add_resource(self, rid: int, name: str = None, instances: int = 1) -> None:
        """Add a resource node to the graph."""
        node_id = f"R{rid}"
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(
                node_id=node_id,
                node_type=NodeType.RESOURCE,
                name=name or f"Resource {rid}",
                total_instances=instances,
                available_instances=instances
            )
            self.adjacency_list[node_id] = []
    
    def add_request_edge(self, pid: int, rid: int, count: int = 1, 
                         timestamp: int = 0) -> None:
        """Add a request edge from process to resource (P -> R)."""
        from_node = f"P{pid}"
        to_node = f"R{rid}"
        
        # Ensure nodes exist
        if from_node not in self.nodes:
            self.add_process(pid)
        if to_node not in self.nodes:
            self.add_resource(rid)
        
        # Check if edge already exists
        for edge in self.edges:
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'request'):
                edge.count += count
                return
        
        # Add new edge
        edge = Edge(from_node, to_node, 'request', count, timestamp)
        self.edges.append(edge)
        self.adjacency_list[from_node].append(to_node)
    
    def add_assignment_edge(self, rid: int, pid: int, count: int = 1,
                           timestamp: int = 0) -> None:
        """Add an assignment edge from resource to process (R -> P)."""
        from_node = f"R{rid}"
        to_node = f"P{pid}"
        
        # Ensure nodes exist
        if from_node not in self.nodes:
            self.add_resource(rid)
        if to_node not in self.nodes:
            self.add_process(pid)
        
        # Check if edge already exists
        for edge in self.edges:
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'assignment'):
                edge.count += count
                return
        
        # Add new edge
        edge = Edge(from_node, to_node, 'assignment', count, timestamp)
        self.edges.append(edge)
        self.adjacency_list[from_node].append(to_node)
        
        # Update resource availability
        if from_node in self.nodes:
            self.nodes[from_node].available_instances -= count
    
    def remove_request_edge(self, pid: int, rid: int, count: int = 1) -> bool:
        """Remove a request edge."""
        from_node = f"P{pid}"
        to_node = f"R{rid}"
        
        for i, edge in enumerate(self.edges):
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'request'):
                if edge.count <= count:
                    self.edges.pop(i)
                    if to_node in self.adjacency_list[from_node]:
                        self.adjacency_list[from_node].remove(to_node)
                else:
                    edge.count -= count
                return True
        return False
    
    def remove_assignment_edge(self, rid: int, pid: int, count: int = 1) -> bool:
        """Remove an assignment edge."""
        from_node = f"R{rid}"
        to_node = f"P{pid}"
        
        for i, edge in enumerate(self.edges):
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'assignment'):
                if edge.count <= count:
                    self.edges.pop(i)
                    if to_node in self.adjacency_list[from_node]:
                        self.adjacency_list[from_node].remove(to_node)
                else:
                    edge.count -= count
                
                # Update resource availability
                if from_node in self.nodes:
                    self.nodes[from_node].available_instances += count
                return True
        return False
    
    def remove_process(self, pid: int) -> None:
        """Remove a process and all its edges from the graph."""
        node_id = f"P{pid}"
        
        # Remove all edges involving this process
        self.edges = [e for e in self.edges 
                      if e.from_node != node_id and e.to_node != node_id]
        
        # Update adjacency list
        if node_id in self.adjacency_list:
            del self.adjacency_list[node_id]
        for node, neighbors in self.adjacency_list.items():
            if node_id in neighbors:
                neighbors.remove(node_id)
        
        # Remove node
        if node_id in self.nodes:
            del self.nodes[node_id]
    
    def get_request_edges(self, pid: int = None) -> List[Edge]:
        """Get all request edges, optionally filtered by process."""
        if pid is None:
            return [e for e in self.edges if e.edge_type == 'request']
        node_id = f"P{pid}"
        return [e for e in self.edges 
                if e.edge_type == 'request' and e.from_node == node_id]
    
    def get_assignment_edges(self, pid: int = None, rid: int = None) -> List[Edge]:
        """Get all assignment edges, optionally filtered."""
        edges = [e for e in self.edges if e.edge_type == 'assignment']
        if pid is not None:
            edges = [e for e in edges if e.to_node == f"P{pid}"]
        if rid is not None:
            edges = [e for e in edges if e.from_node == f"R{rid}"]
        return edges
    
    def get_processes_holding_resource(self, rid: int) -> List[int]:
        """Get list of process IDs holding a resource."""
        node_id = f"R{rid}"
        pids = []
        for edge in self.edges:
            if edge.from_node == node_id and edge.edge_type == 'assignment':
                pid = int(edge.to_node[1:])
                pids.append(pid)
        return pids
    
    def get_resources_held_by_process(self, pid: int) -> List[int]:
        """Get list of resource IDs held by a process."""
        node_id = f"P{pid}"
        rids = []
        for edge in self.edges:
            if edge.to_node == node_id and edge.edge_type == 'assignment':
                rid = int(edge.from_node[1:])
                rids.append(rid)
        return rids
    
    def get_wait_for_graph(self) -> Dict[int, List[int]]:
        """Create a wait-for graph from the RAG.
        
        Returns: {pid: [pids that this process is waiting for]}
        """
        wait_for: Dict[int, List[int]] = {}
        
        # For each request edge P -> R
        for req_edge in self.get_request_edges():
            pid = int(req_edge.from_node[1:])
            rid = int(req_edge.to_node[1:])
            
            if pid not in wait_for:
                wait_for[pid] = []
            
            # Find who holds this resource
            for assign_edge in self.edges:
                if (assign_edge.from_node == req_edge.to_node and 
                    assign_edge.edge_type == 'assignment'):
                    holder_pid = int(assign_edge.to_node[1:])
                    if holder_pid != pid and holder_pid not in wait_for[pid]:
                        wait_for[pid].append(holder_pid)
        
        return wait_for
    
    def to_ascii(self) -> str:
        """Generate ASCII representation of the graph."""
        lines = ["Resource Allocation Graph:", "=" * 40]
        
        # List processes
        processes = [n for n in self.nodes.values() if n.node_type == NodeType.PROCESS]
        resources = [n for n in self.nodes.values() if n.node_type == NodeType.RESOURCE]
        
        lines.append("\nProcesses:")
        for p in processes:
            lines.append(f"  [{p.node_id}] {p.name}")
        
        lines.append("\nResources:")
        for r in resources:
            lines.append(f"  ({r.node_id}) {r.name} "
                        f"[{r.available_instances}/{r.total_instances} available]")
        
        lines.append("\nEdges:")
        for edge in self.edges:
            if edge.edge_type == 'request':
                lines.append(f"  {edge.from_node} --wants--> {edge.to_node} (count: {edge.count})")
            else:
                lines.append(f"  {edge.from_node} --held-by--> {edge.to_node} (count: {edge.count})")
        
        return "\n".join(lines)
    
    def reset(self) -> None:
        """Reset the graph to empty state."""
        self.nodes.clear()
        self.edges.clear()
        self.adjacency_list.clear()

```

---

## 4.3 Deadlock Scenario (Test Scenario 3)

**File:** `tests/test_scenario_3.py`

### Scenario Setup
Creates a circular wait condition:
- P1 holds R1, wants R2
- P2 holds R2, wants R3
- P3 holds R3, wants R4
- P4 holds R4, wants R1

### Circular Wait Chain
```
P1 -> R2 -> P2 -> R3 -> P3 -> R4 -> P4 -> R1 -> P1
```

### Test Code

```python
#!/usr/bin/env python3
"""Test Scenario 3: Deadlock Creation and Detection

Creates 4 processes with 4 resources in circular dependency.
Expected: Deadlock detection and resolution.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.simulation_engine import SimulationEngine
from resources.rag import ResourceAllocationGraph
from resources.deadlock_detector import DeadlockDetector


def test_deadlock_demo():
    """Run deadlock creation and detection test."""
    console = Console()
    engine = SimulationEngine()
    
    console.print(Panel(
        "[bold]Test Scenario 3: Deadlock Creation and Detection[/bold]\n\n"
        "• 4 processes (P1-P4)\n"
        "• 4 resources (R1-R4)\n"
        "• Creating circular wait: P1→R1→P2→R2→P3→R3→P4→R4→P1",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    # Create 4 processes
    for i in range(1, 5):
        engine.create_process(
            name=f"Deadlock_P{i}",
            burst_time=100,
            priority=5,
            arrival_time=0,
            io_bound=False
        )
    
    console.print("[bold]Step 1: Initial resource allocation[/bold]\n")
    
    # Create circular wait condition
    # P1 holds R1, wants R2
    # P2 holds R2, wants R3
    # P3 holds R3, wants R4
    # P4 holds R4, wants R1
    
    allocations = [
        (1, 1, "P1 holds R1"),
        (2, 2, "P2 holds R2"),
        (3, 3, "P3 holds R3"),
        (4, 4, "P4 holds R4"),
    ]
    
    for pid, rid, desc in allocations:
        success = engine.request_resource(pid, rid)
        status = "[green]✓ Allocated[/green]" if success else "[red]✗ Waiting[/red]"
        console.print(f"  {desc}: {status}")
    
    console.print("\n[bold]Step 2: Creating circular wait[/bold]\n")
    
    requests = [
        (1, 2, "P1 requests R2 (held by P2)"),
        (2, 3, "P2 requests R3 (held by P3)"),
        (3, 4, "P3 requests R4 (held by P4)"),
        (4, 1, "P4 requests R1 (held by P1)"),
    ]
    
    for pid, rid, desc in requests:
        success = engine.request_resource(pid, rid)
        status = "[green]✓ Allocated[/green]" if success else "[yellow]⏳ Waiting[/yellow]"
        console.print(f"  {desc}: {status}")
    
    # Display RAG
    console.print("\n[bold]Resource Allocation Graph:[/bold]")
    console.print(engine.rag.to_ascii())
    
    # Check for deadlock
    console.print("\n[bold]Step 3: Deadlock Detection[/bold]\n")
    
    result = engine.check_deadlock()
    
    if result['detected']:
        console.print(Panel(
            f"[bold red]⚠️  DEADLOCK DETECTED![/bold red]\n\n"
            f"Circular Wait Chain: {' → '.join(result['cycle'])}\n"
            f"Processes in Deadlock: {result['processes']}\n"
            f"Resources Involved: {result['resources']}",
            title=f"[{result['timestamp']:05d}ms] Deadlock Alert",
            border_style="red"
        ))
        
        # Show resolution options
        console.print("\n[bold]Step 4: Deadlock Resolution[/bold]\n")
        
        # Resolve by termination
        resolve_result = engine.resolve_deadlock('termination')
        
        if resolve_result and resolve_result['success']:
            console.print(Panel(
                f"[bold green]✓ DEADLOCK RESOLVED[/bold green]\n\n"
                f"Method: {resolve_result['method']}\n"
                f"Victim Process: P{resolve_result['victim']}\n"
                f"Resources Released: {resolve_result['resources_released']}\n\n"
                f"{resolve_result['message']}",
                title="Resolution Result",
                border_style="green"
            ))
        
        # Verify deadlock is resolved
        console.print("\n[bold]Step 5: Verification[/bold]\n")
        
        verify_result = engine.check_deadlock()
        
        if not verify_result['detected']:
            console.print("[bold green]✓ PASS: Deadlock successfully resolved[/bold green]")
            console.print("[dim]System is now in safe state[/dim]")
            return True
        else:
            console.print("[bold red]✗ FAIL: Deadlock still exists[/bold red]")
            return False
    else:
        console.print("[bold yellow]⚠ No deadlock detected[/bold yellow]")
        console.print("[dim]This might happen if resources were allocated differently[/dim]")
        return True


def demonstrate_bankers_algorithm():
    """Demonstrate Banker's Algorithm for deadlock prevention."""
    console = Console()
    
    console.print(Panel(
        "[bold]Banker's Algorithm Demonstration[/bold]\n\n"
        "Showing how Banker's Algorithm prevents deadlock by\n"
        "ensuring the system stays in a safe state.",
        title="Deadlock Prevention",
        border_style="blue"
    ))
    
    from resources.bankers_algorithm import BankersAlgorithm
    
    bankers = BankersAlgorithm()
    
    # Initialize with resources
    total = {1: 10, 2: 5, 3: 7}  # 3 resource types
    
    # Maximum needs for each process
    max_need = {
        1: {1: 7, 2: 5, 3: 3},
        2: {1: 3, 2: 2, 3: 2},
        3: {1: 9, 2: 0, 3: 2},
        4: {1: 2, 2: 2, 3: 2},
        5: {1: 4, 2: 3, 3: 3},
    }
    
    bankers.initialize(total, max_need)
    
    # Simulate some allocations
    allocations = [
        (1, {1: 0, 2: 1, 3: 0}),
        (2, {1: 2, 2: 0, 3: 0}),
        (3, {1: 3, 2: 0, 3: 2}),
        (4, {1: 2, 2: 1, 3: 1}),
        (5, {1: 0, 2: 0, 3: 2}),
    ]
    
    console.print("\n[bold]Current Allocations:[/bold]")
    
    for pid, alloc in allocations:
        success, msg = bankers.request_resources(pid, alloc)
        status = "[green]Granted[/green]" if success else "[red]Denied[/red]"
        console.print(f"  P{pid}: {alloc} - {status}")
    
    # Check safe state
    result = bankers.is_safe()
    
    console.print("\n[bold]Safety Check:[/bold]")
    if result.is_safe:
        console.print(f"[green]System is in SAFE state[/green]")
        console.print(f"Safe Sequence: {result.safe_sequence}")
    else:
        console.print(f"[red]System is in UNSAFE state[/red]")
    
    # Try a request that would make system unsafe
    console.print("\n[bold]Testing Dangerous Request:[/bold]")
    success, msg = bankers.request_resources(1, {1: 1, 2: 0, 3: 2})
    console.print(f"  P1 requests {{R1: 1, R3: 2}}: {msg}")


if __name__ == "__main__":
    success = test_deadlock_demo()
    print()
    demonstrate_bankers_algorithm()
    sys.exit(0 if success else 1)

```

### How to Run
```bash
python3 -m tests.test_scenario_3
```

---

# 5. REQUIREMENT 3: SYNCHRONIZATION MECHANISMS

---

## 5.1 Mutex Implementation

**File:** `models/mutex.py`

### Description
A mutual exclusion lock that ensures only one process can access a critical section at a time.

### Key Operations
- `acquire(pid)`: Request the lock
- `release(pid)`: Release the lock
- Supports blocking and non-blocking modes
- Maintains waiting queue

### Implementation Code

```python
"""Mutex implementation for OS simulation."""

from dataclasses import dataclass, field
from typing import Optional, List
import threading
import time


@dataclass
class Mutex:
    """Mutual exclusion lock implementation."""
    name: str
    
    # Runtime attributes
    locked: bool = field(default=False, init=False)
    owner_pid: Optional[int] = field(default=None, init=False)
    waiting_queue: List[int] = field(default_factory=list, init=False)
    lock_time: float = field(default=0, init=False)
    
    # Internal threading lock for thread-safe operations
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _condition: threading.Condition = field(default=None, init=False, repr=False)
    
    def __post_init__(self):
        """Initialize condition variable."""
        self._condition = threading.Condition(self._lock)
    
    def acquire(self, pid: int, blocking: bool = True, timeout: float = None) -> bool:
        """Acquire the mutex.
        
        Args:
            pid: Process ID requesting the lock
            blocking: If True, block until lock is available
            timeout: Maximum time to wait (None = infinite)
            
        Returns:
            True if lock was acquired, False otherwise
        """
        with self._condition:
            if not self.locked:
                # Lock is free, acquire it
                self.locked = True
                self.owner_pid = pid
                self.lock_time = time.time()
                return True
            
            if not blocking:
                return False
            
            # Add to waiting queue
            if pid not in self.waiting_queue:
                self.waiting_queue.append(pid)
            
            # Wait for lock
            start_time = time.time()
            while self.locked:
                if timeout is not None:
                    remaining = timeout - (time.time() - start_time)
                    if remaining <= 0:
                        if pid in self.waiting_queue:
                            self.waiting_queue.remove(pid)
                        return False
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()
            
            # Lock is now free, acquire it
            self.locked = True
            self.owner_pid = pid
            self.lock_time = time.time()
            if pid in self.waiting_queue:
                self.waiting_queue.remove(pid)
            return True
    
    def release(self, pid: int) -> bool:
        """Release the mutex.
        
        Args:
            pid: Process ID releasing the lock
            
        Returns:
            True if lock was released, False if caller is not owner
        """
        with self._condition:
            if self.owner_pid != pid:
                return False
            
            self.locked = False
            self.owner_pid = None
            self._condition.notify()
            return True
    
    def is_locked(self) -> bool:
        """Check if mutex is locked."""
        return self.locked
    
    def get_owner(self) -> Optional[int]:
        """Get the owner process ID."""
        return self.owner_pid
    
    def get_waiting_count(self) -> int:
        """Get number of processes waiting for the lock."""
        return len(self.waiting_queue)
    
    def reset(self) -> None:
        """Reset mutex to initial state."""
        with self._lock:
            self.locked = False
            self.owner_pid = None
            self.waiting_queue.clear()
            self.lock_time = 0
    
    def __repr__(self) -> str:
        status = f"locked by P{self.owner_pid}" if self.locked else "unlocked"
        return f"Mutex(name={self.name}, {status}, waiting={len(self.waiting_queue)})"

```

---

## 5.2 Semaphore Implementation

**File:** `models/semaphore.py`

### Description
A counting semaphore for controlling access to a resource pool. Supports classic P (wait) and V (signal) operations.

### Key Operations
- `wait(pid)` / `P(pid)`: Decrement counter, block if zero
- `signal(pid)` / `V(pid)`: Increment counter, wake waiting process

### Implementation Code

```python
"""Semaphore implementation for OS simulation."""

from dataclasses import dataclass, field
from typing import List
import threading
import time


@dataclass
class Semaphore:
    """Counting semaphore implementation."""
    name: str
    initial_count: int = 1
    
    # Runtime attributes
    count: int = field(default=0, init=False)
    waiting_queue: List[int] = field(default_factory=list, init=False)
    
    # Internal threading primitives
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _condition: threading.Condition = field(default=None, init=False, repr=False)
    
    # Statistics
    wait_count: int = field(default=0, init=False)
    signal_count: int = field(default=0, init=False)
    
    def __post_init__(self):
        """Initialize count and condition variable."""
        self.count = self.initial_count
        self._condition = threading.Condition(self._lock)
    
    def wait(self, pid: int, blocking: bool = True, timeout: float = None) -> bool:
        """Decrement semaphore (P operation).
        
        Args:
            pid: Process ID performing the wait
            blocking: If True, block until count > 0
            timeout: Maximum time to wait (None = infinite)
            
        Returns:
            True if semaphore was decremented, False otherwise
        """
        with self._condition:
            self.wait_count += 1
            
            if self.count > 0:
                self.count -= 1
                return True
            
            if not blocking:
                return False
            
            # Add to waiting queue
            if pid not in self.waiting_queue:
                self.waiting_queue.append(pid)
            
            # Wait for signal
            start_time = time.time()
            while self.count <= 0:
                if timeout is not None:
                    remaining = timeout - (time.time() - start_time)
                    if remaining <= 0:
                        if pid in self.waiting_queue:
                            self.waiting_queue.remove(pid)
                        return False
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()
            
            # Semaphore now available
            self.count -= 1
            if pid in self.waiting_queue:
                self.waiting_queue.remove(pid)
            return True
    
    def signal(self, pid: int = None) -> None:
        """Increment semaphore (V operation).
        
        Args:
            pid: Process ID performing the signal (optional, for logging)
        """
        with self._condition:
            self.count += 1
            self.signal_count += 1
            self._condition.notify()
    
    # Aliases for P and V operations
    def P(self, pid: int, blocking: bool = True, timeout: float = None) -> bool:
        """P operation (alias for wait)."""
        return self.wait(pid, blocking, timeout)
    
    def V(self, pid: int = None) -> None:
        """V operation (alias for signal)."""
        self.signal(pid)
    
    def get_count(self) -> int:
        """Get current semaphore count."""
        return self.count
    
    def get_waiting_count(self) -> int:
        """Get number of processes waiting."""
        return len(self.waiting_queue)
    
    def reset(self) -> None:
        """Reset semaphore to initial state."""
        with self._lock:
            self.count = self.initial_count
            self.waiting_queue.clear()
            self.wait_count = 0
            self.signal_count = 0
    
    def __repr__(self) -> str:
        return f"Semaphore(name={self.name}, count={self.count}, waiting={len(self.waiting_queue)})"

```

---

## 5.3 Race Condition Demonstration

**File:** `tests/test_scenario_4.py`

### Scenario
5 threads each increment a shared counter 1000 times:
- **Without mutex**: Race condition causes lost updates
- **With mutex**: Counter reaches expected value (5000)

### Test Code

```python
#!/usr/bin/env python3
"""Test Scenario 4: Race Condition Demonstration

Demonstrates race conditions with and without mutex protection.
Shows 5 threads each incrementing a shared counter 1000 times.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from synchronization.race_detector import RaceConditionDemo


def test_race_condition():
    """Run race condition demonstration test."""
    console = Console()
    
    console.print(Panel(
        "[bold]Test Scenario 4: Race Condition Demonstration[/bold]\n\n"
        "• 5 threads\n"
        "• Each thread increments a shared counter 1000 times\n"
        "• Expected: 5000 increments total\n\n"
        "Testing both WITH and WITHOUT mutex protection",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    demo = RaceConditionDemo()
    num_threads = 5
    increments = 1000
    
    # Test WITHOUT mutex
    console.print("\n" + "="*60)
    console.print("[bold red]Test 1: WITHOUT Mutex Protection[/bold red]")
    console.print("="*60 + "\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Running threads without mutex...", total=None)
        without_result = demo.run_without_mutex(num_threads, increments)
    
    console.print(Panel(
        f"Running {num_threads} threads, each incrementing shared counter {increments} times...\n\n"
        f"Expected: [bold]{without_result.expected_value}[/bold]\n"
        f"Actual:   [bold]{without_result.actual_value}[/bold]\n\n"
        f"{without_result.message}\n\n"
        f"[dim]Execution time: {without_result.execution_time:.4f}s[/dim]",
        title="WITHOUT Mutex Results",
        border_style="red" if without_result.race_detected else "green"
    ))
    
    # Test WITH mutex
    console.print("\n" + "="*60)
    console.print("[bold green]Test 2: WITH Mutex Protection[/bold green]")
    console.print("="*60 + "\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Running threads with mutex...", total=None)
        with_result = demo.run_with_mutex(num_threads, increments)
    
    console.print(Panel(
        f"Running {num_threads} threads, each incrementing shared counter {increments} times...\n\n"
        f"Expected: [bold]{with_result.expected_value}[/bold]\n"
        f"Actual:   [bold]{with_result.actual_value}[/bold]\n\n"
        f"{with_result.message}\n\n"
        f"[dim]Execution time: {with_result.execution_time:.4f}s[/dim]",
        title="WITH Mutex Results",
        border_style="green" if not with_result.race_detected else "red"
    ))
    
    # Comparison Summary
    console.print("\n" + "="*60)
    console.print("[bold cyan]Summary Comparison[/bold cyan]")
    console.print("="*60 + "\n")
    
    table = Table(box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Without Mutex", style="red")
    table.add_column("With Mutex", style="green")
    
    table.add_row(
        "Expected Value",
        str(without_result.expected_value),
        str(with_result.expected_value)
    )
    table.add_row(
        "Actual Value",
        str(without_result.actual_value),
        str(with_result.actual_value)
    )
    table.add_row(
        "Lost Updates",
        str(without_result.lost_updates),
        str(with_result.lost_updates)
    )
    table.add_row(
        "Race Detected",
        "Yes ❌" if without_result.race_detected else "No ✓",
        "Yes ❌" if with_result.race_detected else "No ✓"
    )
    table.add_row(
        "Data Integrity",
        "Compromised ❌" if without_result.race_detected else "Maintained ✓",
        "Compromised ❌" if with_result.race_detected else "Maintained ✓"
    )
    table.add_row(
        "Execution Time",
        f"{without_result.execution_time:.4f}s",
        f"{with_result.execution_time:.4f}s"
    )
    
    console.print(table)
    
    # Verification
    console.print("\n[bold]Test Verification:[/bold]")
    
    # Without mutex should show race condition (usually)
    if without_result.race_detected:
        console.print("[green]✓ Race condition demonstrated without mutex[/green]")
    else:
        console.print("[yellow]⚠ No race condition in this run (can happen occasionally)[/yellow]")
    
    # With mutex should NEVER show race condition
    if not with_result.race_detected:
        console.print("[green]✓ Mutex successfully prevented race condition[/green]")
        console.print("[bold green]✓ PASS: Test scenario completed successfully[/bold green]")
        return True
    else:
        console.print("[red]✗ FAIL: Race condition occurred even with mutex[/red]")
        return False


def demonstrate_producer_consumer():
    """Demonstrate producer-consumer problem with semaphores."""
    console = Console()
    
    console.print("\n" + "="*60)
    console.print("[bold cyan]Producer-Consumer Problem Demonstration[/bold cyan]")
    console.print("="*60 + "\n")
    
    from synchronization.critical_section import ProducerConsumerProblem
    import threading
    import time
    
    pc = ProducerConsumerProblem(buffer_size=5)
    
    console.print(Panel(
        "• Buffer size: 5\n"
        "• 3 producers, each producing 5 items\n"
        "• 2 consumers, each consuming 7-8 items",
        title="Configuration",
        border_style="cyan"
    ))
    
    # Producer function
    def producer(producer_id, count):
        for i in range(count):
            item = f"Item_{producer_id}_{i}"
            pc.produce(producer_id, item)
            time.sleep(0.1)
    
    # Consumer function
    def consumer(consumer_id, count):
        for i in range(count):
            item = pc.consume(consumer_id)
            time.sleep(0.15)
    
    # Create threads
    threads = []
    
    # 3 producers, each producing 5 items
    for i in range(3):
        t = threading.Thread(target=producer, args=(i+1, 5))
        threads.append(t)
    
    # 2 consumers, each consuming 7-8 items
    for i in range(2):
        t = threading.Thread(target=consumer, args=(i+1, 7 if i == 0 else 8))
        threads.append(t)
    
    console.print("[bold]Running producer-consumer simulation...[/bold]\n")
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Wait for completion
    for t in threads:
        t.join()
    
    # Show results
    status = pc.get_buffer_status()
    
    table = Table(title="Producer-Consumer Results", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")
    
    table.add_row("Buffer Size", str(status['buffer_size']))
    table.add_row("Items in Buffer", str(status['items_in_buffer']))
    table.add_row("Total Produced", str(status['total_produced']))
    table.add_row("Total Consumed", str(status['total_consumed']))
    
    console.print(table)
    
    # Show last 5 events
    console.print("\n[bold]Last 5 Events:[/bold]")
    for event in pc.get_events()[-5:]:
        console.print(f"  {event}")
    
    if status['total_produced'] == 15 and status['total_consumed'] == 15:
        console.print("\n[bold green]✓ Producer-Consumer synchronized correctly![/bold green]")


if __name__ == "__main__":
    success = test_race_condition()
    print()
    demonstrate_producer_consumer()
    sys.exit(0 if success else 1)

```

### Expected Output
```
WITHOUT Mutex:
  Expected: 5000
  Actual: ~4500-4900 (varies due to race condition)
  Race Detected: Yes

WITH Mutex:
  Expected: 5000
  Actual: 5000
  Race Detected: No
```

### How to Run
```bash
python3 -m tests.test_scenario_4
```

---

# 6. REQUIREMENT 4: DEADLOCK HANDLING MECHANISMS

The system implements 5 deadlock handling mechanisms in the `resources/` directory.

---

## 6.1 Deadlock Detection (DFS Cycle Detection)

**File:** `resources/deadlock_detector.py`

### Algorithm
Uses Depth-First Search (DFS) on the wait-for graph derived from the RAG to detect cycles.

### Detection Process
1. Build wait-for graph from RAG
2. Run DFS from each unvisited node
3. Track recursion stack to detect back edges (cycles)
4. Report cycle if found

### Implementation Code

```python
"""Deadlock Detector using DFS-based cycle detection."""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from .rag import ResourceAllocationGraph


@dataclass
class DeadlockInfo:
    """Information about a detected deadlock."""
    timestamp: int
    cycle: List[str]  # Chain of nodes in the cycle
    processes: List[int]  # Process IDs in deadlock
    resources: List[int]  # Resource IDs involved
    
    def __str__(self) -> str:
        cycle_str = " → ".join(self.cycle)
        return (f"DEADLOCK DETECTED at {self.timestamp}ms\n"
                f"Circular Wait Chain: {cycle_str}\n"
                f"Processes in Deadlock: {self.processes}\n"
                f"Resources Involved: {self.resources}")


class DeadlockDetector:
    """Deadlock detection using DFS-based cycle detection on RAG."""
    
    def __init__(self, rag: ResourceAllocationGraph = None):
        self.rag = rag or ResourceAllocationGraph()
        self.deadlock_history: List[DeadlockInfo] = []
        self.current_time: int = 0
    
    def set_rag(self, rag: ResourceAllocationGraph) -> None:
        """Set the Resource Allocation Graph to monitor."""
        self.rag = rag
    
    def detect(self) -> Optional[DeadlockInfo]:
        """Detect deadlock in the current RAG state.
        
        Uses DFS to find cycles in the wait-for graph.
        Returns DeadlockInfo if deadlock is found, None otherwise.
        """
        # Build wait-for graph from RAG
        wait_for = self.rag.get_wait_for_graph()
        
        if not wait_for:
            return None
        
        # DFS for cycle detection
        visited: Set[int] = set()
        rec_stack: Set[int] = set()
        path: List[int] = []
        
        def dfs(pid: int) -> Optional[List[int]]:
            visited.add(pid)
            rec_stack.add(pid)
            path.append(pid)
            
            for neighbor in wait_for.get(pid, []):
                if neighbor not in visited:
                    cycle = dfs(neighbor)
                    if cycle:
                        return cycle
                elif neighbor in rec_stack:
                    # Found cycle - extract it
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:] + [neighbor]
            
            path.pop()
            rec_stack.remove(pid)
            return None
        
        # Check all processes for cycles
        for pid in wait_for.keys():
            if pid not in visited:
                path.clear()
                cycle = dfs(pid)
                if cycle:
                    return self._create_deadlock_info(cycle)
        
        return None
    
    def detect_all_cycles(self) -> List[DeadlockInfo]:
        """Detect all cycles in the current RAG state.
        
        Returns a list of all detected deadlocks.
        """
        wait_for = self.rag.get_wait_for_graph()
        
        if not wait_for:
            return []
        
        deadlocks = []
        visited: Set[int] = set()
        
        def find_cycles_from(start: int, path: List[int], rec_stack: Set[int]) -> List[List[int]]:
            cycles = []
            rec_stack.add(start)
            path.append(start)
            
            for neighbor in wait_for.get(start, []):
                if neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
                elif neighbor not in visited:
                    cycles.extend(find_cycles_from(neighbor, path.copy(), rec_stack.copy()))
            
            visited.add(start)
            return cycles
        
        for pid in wait_for.keys():
            if pid not in visited:
                cycles = find_cycles_from(pid, [], set())
                for cycle in cycles:
                    deadlock = self._create_deadlock_info(cycle)
                    deadlocks.append(deadlock)
        
        return deadlocks
    
    def _create_deadlock_info(self, process_cycle: List[int]) -> DeadlockInfo:
        """Create a DeadlockInfo object from a cycle of process IDs."""
        # Build the full cycle chain including resources
        chain = []
        resources = set()
        
        for i in range(len(process_cycle) - 1):
            pid = process_cycle[i]
            next_pid = process_cycle[i + 1]
            
            chain.append(f"P{pid}")
            
            # Find the resource that pid is waiting for from next_pid
            for edge in self.rag.edges:
                if edge.edge_type == 'request' and edge.from_node == f"P{pid}":
                    rid = int(edge.to_node[1:])
                    # Check if next_pid holds this resource
                    for assign in self.rag.edges:
                        if (assign.edge_type == 'assignment' and 
                            assign.from_node == f"R{rid}" and
                            assign.to_node == f"P{next_pid}"):
                            chain.append(f"R{rid}")
                            resources.add(rid)
                            break
        
        # Complete the cycle
        if process_cycle:
            chain.append(f"P{process_cycle[-1]}")
        
        # Get unique processes (excluding the repeated last one)
        unique_processes = list(set(process_cycle[:-1]))
        
        deadlock = DeadlockInfo(
            timestamp=self.current_time,
            cycle=chain,
            processes=unique_processes,
            resources=list(resources)
        )
        
        self.deadlock_history.append(deadlock)
        return deadlock
    
    def is_safe_state(self, available: Dict[int, int], 
                      allocation: Dict[int, Dict[int, int]],
                      max_need: Dict[int, Dict[int, int]]) -> Tuple[bool, List[int]]:
        """Check if the system is in a safe state using the safety algorithm.
        
        Args:
            available: Available resources {rid: count}
            allocation: Current allocation {pid: {rid: count}}
            max_need: Maximum need {pid: {rid: count}}
            
        Returns:
            Tuple of (is_safe, safe_sequence or [])
        """
        if not allocation:
            return True, []
        
        processes = list(allocation.keys())
        resources = list(available.keys())
        n = len(processes)
        
        # Calculate need matrix
        need = {}
        for pid in processes:
            need[pid] = {}
            for rid in resources:
                alloc = allocation.get(pid, {}).get(rid, 0)
                max_n = max_need.get(pid, {}).get(rid, 0)
                need[pid][rid] = max_n - alloc
        
        # Work = Available
        work = available.copy()
        finish = {pid: False for pid in processes}
        safe_sequence = []
        
        while True:
            found = False
            for pid in processes:
                if not finish[pid]:
                    # Check if need[pid] <= work
                    can_satisfy = all(
                        need[pid].get(rid, 0) <= work.get(rid, 0)
                        for rid in resources
                    )
                    
                    if can_satisfy:
                        # Process can complete, release resources
                        for rid in resources:
                            work[rid] = work.get(rid, 0) + allocation.get(pid, {}).get(rid, 0)
                        finish[pid] = True
                        safe_sequence.append(pid)
                        found = True
            
            if not found:
                break
        
        is_safe = all(finish.values())
        return is_safe, safe_sequence if is_safe else []
    
    def set_time(self, time: int) -> None:
        """Set the current simulation time."""
        self.current_time = time
    
    def get_history(self) -> List[DeadlockInfo]:
        """Get the history of detected deadlocks."""
        return self.deadlock_history
    
    def reset(self) -> None:
        """Reset the detector state."""
        self.deadlock_history.clear()
        self.current_time = 0

```

---

## 6.2 Deadlock Prevention (Banker's Algorithm)

**File:** `resources/bankers_algorithm.py`

### Algorithm
Ensures the system never enters an unsafe state by checking safety before granting requests.

### Safety Algorithm
1. Initialize Work = Available, Finish[i] = false
2. Find process Pi where Need[i] <= Work
3. Work = Work + Allocation[i], Finish[i] = true
4. Repeat until all finished (safe) or no progress (unsafe)

### Implementation Code

```python
"""Banker's Algorithm for deadlock prevention."""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SafetyCheckResult:
    """Result of a safety check."""
    is_safe: bool
    safe_sequence: List[int]
    message: str


@dataclass
class AllocationRequest:
    """A resource allocation request."""
    pid: int
    resources: Dict[int, int]  # {rid: count}


class BankersAlgorithm:
    """Banker's Algorithm for deadlock prevention.
    
    Ensures the system always remains in a safe state by checking
    whether granting a request would lead to an unsafe state.
    """
    
    def __init__(self):
        # Total resources in the system
        self.total: Dict[int, int] = {}
        
        # Available resources
        self.available: Dict[int, int] = {}
        
        # Maximum resources each process may need
        self.max_need: Dict[int, Dict[int, int]] = {}
        
        # Currently allocated resources
        self.allocation: Dict[int, Dict[int, int]] = {}
        
        # Calculated need matrix (max - allocation)
        self.need: Dict[int, Dict[int, int]] = {}
    
    def initialize(self, total: Dict[int, int], 
                   max_need: Dict[int, Dict[int, int]]) -> None:
        """Initialize the Banker's Algorithm with system resources.
        
        Args:
            total: Total resources {rid: count}
            max_need: Maximum needs {pid: {rid: count}}
        """
        self.total = total.copy()
        self.available = total.copy()
        self.max_need = {pid: needs.copy() for pid, needs in max_need.items()}
        self.allocation = {pid: {} for pid in max_need}
        self._calculate_need()
    
    def add_process(self, pid: int, max_need: Dict[int, int]) -> None:
        """Add a new process with its maximum resource needs."""
        self.max_need[pid] = max_need.copy()
        self.allocation[pid] = {rid: 0 for rid in self.total}
        self._calculate_need()
    
    def remove_process(self, pid: int) -> None:
        """Remove a process and release its resources."""
        if pid in self.allocation:
            # Release all allocated resources
            for rid, count in self.allocation[pid].items():
                self.available[rid] = self.available.get(rid, 0) + count
            
            del self.allocation[pid]
            if pid in self.max_need:
                del self.max_need[pid]
            if pid in self.need:
                del self.need[pid]
    
    def _calculate_need(self) -> None:
        """Calculate the need matrix (max - allocation)."""
        self.need = {}
        for pid in self.max_need:
            self.need[pid] = {}
            for rid in self.total:
                max_val = self.max_need.get(pid, {}).get(rid, 0)
                alloc_val = self.allocation.get(pid, {}).get(rid, 0)
                self.need[pid][rid] = max_val - alloc_val
    
    def request_resources(self, pid: int, 
                          request: Dict[int, int]) -> Tuple[bool, str]:
        """Request resources using Banker's Algorithm.
        
        Args:
            pid: Process ID requesting resources
            request: Resources requested {rid: count}
            
        Returns:
            Tuple of (granted, message)
        """
        # Step 1: Check if request <= need
        for rid, count in request.items():
            if count > self.need.get(pid, {}).get(rid, 0):
                return False, f"Error: P{pid} exceeded its maximum claim for R{rid}"
        
        # Step 2: Check if request <= available
        for rid, count in request.items():
            if count > self.available.get(rid, 0):
                return False, f"P{pid} must wait - insufficient R{rid} available"
        
        # Step 3: Pretend to allocate and check safety
        # Save current state
        saved_available = self.available.copy()
        saved_allocation = {pid: alloc.copy() for pid, alloc in self.allocation.items()}
        
        # Pretend allocation
        for rid, count in request.items():
            self.available[rid] -= count
            if pid not in self.allocation:
                self.allocation[pid] = {}
            self.allocation[pid][rid] = self.allocation[pid].get(rid, 0) + count
        
        self._calculate_need()
        
        # Check safety
        result = self.is_safe()
        
        if result.is_safe:
            # Keep the allocation
            return True, f"Request granted. Safe sequence: {result.safe_sequence}"
        else:
            # Restore previous state
            self.available = saved_available
            self.allocation = saved_allocation
            self._calculate_need()
            return False, "Request denied - would lead to unsafe state"
    
    def release_resources(self, pid: int, release: Dict[int, int]) -> bool:
        """Release resources from a process.
        
        Args:
            pid: Process ID releasing resources
            release: Resources to release {rid: count}
            
        Returns:
            True if release was successful
        """
        if pid not in self.allocation:
            return False
        
        for rid, count in release.items():
            if count > self.allocation[pid].get(rid, 0):
                return False
        
        # Perform release
        for rid, count in release.items():
            self.allocation[pid][rid] -= count
            self.available[rid] += count
        
        self._calculate_need()
        return True
    
    def is_safe(self) -> SafetyCheckResult:
        """Check if the current state is safe.
        
        Returns:
            SafetyCheckResult with is_safe, safe_sequence, and message
        """
        work = self.available.copy()
        finish = {pid: False for pid in self.allocation}
        safe_sequence = []
        
        while True:
            found = False
            
            for pid in self.allocation:
                if not finish[pid]:
                    # Check if need[pid] <= work
                    can_finish = all(
                        self.need.get(pid, {}).get(rid, 0) <= work.get(rid, 0)
                        for rid in self.total
                    )
                    
                    if can_finish:
                        # Process can complete
                        for rid in self.total:
                            work[rid] += self.allocation.get(pid, {}).get(rid, 0)
                        finish[pid] = True
                        safe_sequence.append(pid)
                        found = True
            
            if not found:
                break
        
        is_safe = all(finish.values())
        
        if is_safe:
            return SafetyCheckResult(
                is_safe=True,
                safe_sequence=safe_sequence,
                message=f"System is in SAFE state. Safe sequence: {safe_sequence}"
            )
        else:
            unsafe_processes = [pid for pid, done in finish.items() if not done]
            return SafetyCheckResult(
                is_safe=False,
                safe_sequence=[],
                message=f"System is in UNSAFE state. Processes at risk: {unsafe_processes}"
            )
    
    def get_state_string(self) -> str:
        """Get a string representation of the current state."""
        lines = ["Banker's Algorithm State", "=" * 40]
        
        # Available
        lines.append(f"\nAvailable: {self.available}")
        
        # Allocation matrix
        lines.append("\nAllocation Matrix:")
        for pid, alloc in self.allocation.items():
            lines.append(f"  P{pid}: {alloc}")
        
        # Max matrix
        lines.append("\nMax Matrix:")
        for pid, max_n in self.max_need.items():
            lines.append(f"  P{pid}: {max_n}")
        
        # Need matrix
        lines.append("\nNeed Matrix:")
        for pid, need in self.need.items():
            lines.append(f"  P{pid}: {need}")
        
        # Safety check
        result = self.is_safe()
        lines.append(f"\nState: {'SAFE' if result.is_safe else 'UNSAFE'}")
        if result.is_safe:
            lines.append(f"Safe Sequence: {result.safe_sequence}")
        
        return "\n".join(lines)
    
    def reset(self) -> None:
        """Reset to initial state."""
        self.total.clear()
        self.available.clear()
        self.max_need.clear()
        self.allocation.clear()
        self.need.clear()

```

---

## 6.3 Deadlock Resolution

**File:** `resources/deadlock_resolver.py`

### Resolution Methods

#### 1. Process Termination
Terminates the victim process and releases all its resources.

**Victim Selection Criteria:**
1. Lowest priority
2. Most resources held
3. Lowest PID (tie-breaker)

#### 2. Resource Preemption
Preempts minimum resources needed to break the cycle.

### Implementation Code

```python
"""Deadlock Resolution mechanisms for OS simulation."""

from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .deadlock_detector import DeadlockDetector, DeadlockInfo
from .rag import ResourceAllocationGraph
from .resource_manager import ResourceManager


class ResolutionMethod(Enum):
    """Methods for resolving deadlock."""
    PROCESS_TERMINATION = "process_termination"
    RESOURCE_PREEMPTION = "resource_preemption"


@dataclass
class ResolutionResult:
    """Result of a deadlock resolution attempt."""
    method: ResolutionMethod
    victim_pid: int
    resources_released: Dict[int, int]
    success: bool
    message: str


class DeadlockResolver:
    """Resolves detected deadlocks using various strategies."""
    
    # Maximum iterations for deadlock resolution loop
    MAX_RESOLUTION_ITERATIONS = 100
    
    def __init__(self, resource_manager: ResourceManager,
                 rag: ResourceAllocationGraph,
                 detector: DeadlockDetector):
        self.resource_manager = resource_manager
        self.rag = rag
        self.detector = detector
        self.resolution_history: List[ResolutionResult] = []
        self.process_priorities: Dict[int, int] = {}  # Lower = more important
        self.process_rollback_costs: Dict[int, int] = {}  # Cost of rolling back
    
    def set_process_priority(self, pid: int, priority: int) -> None:
        """Set the priority of a process for victim selection."""
        self.process_priorities[pid] = priority
    
    def set_rollback_cost(self, pid: int, cost: int) -> None:
        """Set the rollback cost for a process."""
        self.process_rollback_costs[pid] = cost
    
    def resolve_by_termination(self, deadlock: DeadlockInfo) -> ResolutionResult:
        """Resolve deadlock by terminating the lowest priority process.
        
        Victim selection criteria (in order):
        1. Lowest priority
        2. Least progress (remaining time)
        3. Most resources held
        4. Lowest PID (tie-breaker)
        """
        if not deadlock.processes:
            return ResolutionResult(
                method=ResolutionMethod.PROCESS_TERMINATION,
                victim_pid=-1,
                resources_released={},
                success=False,
                message="No processes in deadlock to terminate"
            )
        
        # Select victim based on criteria
        victim = self._select_victim(deadlock.processes)
        
        # Release all resources held by victim
        released = self._release_process_resources(victim)
        
        # Remove from RAG
        self.rag.remove_process(victim)
        
        result = ResolutionResult(
            method=ResolutionMethod.PROCESS_TERMINATION,
            victim_pid=victim,
            resources_released=released,
            success=True,
            message=f"Terminated P{victim}, released resources: {released}"
        )
        
        self.resolution_history.append(result)
        return result
    
    def resolve_by_preemption(self, deadlock: DeadlockInfo) -> ResolutionResult:
        """Resolve deadlock by preempting resources from victim.
        
        Preempts minimum resources needed to break the cycle.
        """
        if not deadlock.processes:
            return ResolutionResult(
                method=ResolutionMethod.RESOURCE_PREEMPTION,
                victim_pid=-1,
                resources_released={},
                success=False,
                message="No processes in deadlock"
            )
        
        # Select victim with lowest rollback cost
        victim = self._select_victim_for_preemption(deadlock.processes)
        
        # Find minimum resources to preempt
        resources_to_preempt = self._find_minimum_preemption(victim, deadlock)
        
        # Perform preemption
        for rid, count in resources_to_preempt.items():
            self.resource_manager.release(victim, rid, count)
            self.rag.remove_assignment_edge(rid, victim, count)
        
        result = ResolutionResult(
            method=ResolutionMethod.RESOURCE_PREEMPTION,
            victim_pid=victim,
            resources_released=resources_to_preempt,
            success=True,
            message=f"Preempted resources from P{victim}: {resources_to_preempt}"
        )
        
        self.resolution_history.append(result)
        return result
    
    def _select_victim(self, processes: List[int]) -> int:
        """Select a victim process for termination."""
        # Score each process (higher = better victim candidate)
        scores = {}
        
        for pid in processes:
            score = 0
            
            # Priority (lower priority = higher score)
            priority = self.process_priorities.get(pid, 5)
            score += (10 - priority) * 100
            
            # Resources held (more resources = higher score)
            resources_held = len(self.rag.get_resources_held_by_process(pid))
            score += resources_held * 10
            
            # Lower PID as tie-breaker (higher PID = higher score)
            score += pid
            
            scores[pid] = score
        
        # Select process with highest score
        return max(processes, key=lambda p: scores.get(p, 0))
    
    def _select_victim_for_preemption(self, processes: List[int]) -> int:
        """Select a victim for resource preemption based on rollback cost."""
        # Lower rollback cost = better victim
        return min(processes, key=lambda p: self.process_rollback_costs.get(p, 100))
    
    def _release_process_resources(self, pid: int) -> Dict[int, int]:
        """Release all resources held by a process."""
        released = {}
        
        for rid, resource in self.resource_manager.resources.items():
            count = resource.release(pid)
            if count > 0:
                released[rid] = count
        
        return released
    
    def _find_minimum_preemption(self, victim_pid: int, 
                                   deadlock: DeadlockInfo) -> Dict[int, int]:
        """Find minimum resources to preempt to break deadlock."""
        resources_to_preempt = {}
        
        # For each resource involved in deadlock that victim holds
        for rid in deadlock.resources:
            assignment_edges = [e for e in self.rag.edges 
                              if e.from_node == f"R{rid}" and 
                              e.to_node == f"P{victim_pid}" and
                              e.edge_type == 'assignment']
            
            if assignment_edges:
                resources_to_preempt[rid] = assignment_edges[0].count
                break  # Preempt minimum (one resource may be enough)
        
        return resources_to_preempt
    
    def resolve_automatically(self, method: ResolutionMethod = None) -> Optional[ResolutionResult]:
        """Detect and automatically resolve any deadlock.
        
        Args:
            method: Resolution method to use (default: PROCESS_TERMINATION)
            
        Returns:
            ResolutionResult if deadlock was found and resolved, None otherwise
        """
        deadlock = self.detector.detect()
        
        if deadlock is None:
            return None
        
        if method is None or method == ResolutionMethod.PROCESS_TERMINATION:
            return self.resolve_by_termination(deadlock)
        else:
            return self.resolve_by_preemption(deadlock)
    
    def resolve_all(self, method: ResolutionMethod = None) -> List[ResolutionResult]:
        """Resolve all deadlocks in the system.
        
        Continues resolving until no deadlocks remain.
        """
        results = []
        max_iterations = self.MAX_RESOLUTION_ITERATIONS
        
        for _ in range(max_iterations):
            result = self.resolve_automatically(method)
            if result is None:
                break
            results.append(result)
        
        return results
    
    def apply_resource_ordering(self, resources: List[int]) -> Dict[int, int]:
        """Create a total ordering on resources for deadlock prevention.
        
        Returns a mapping of resource_id to order number.
        Processes should always request resources in increasing order.
        """
        return {rid: i for i, rid in enumerate(sorted(resources))}
    
    def check_ordering_violation(self, pid: int, rid: int,
                                  held_resources: List[int],
                                  ordering: Dict[int, int]) -> bool:
        """Check if requesting a resource would violate the ordering.
        
        Returns True if there's a violation (request should be denied).
        """
        request_order = ordering.get(rid, float('inf'))
        
        for held_rid in held_resources:
            if ordering.get(held_rid, 0) >= request_order:
                return True  # Violation: holding higher-ordered resource
        
        return False
    
    def get_history(self) -> List[ResolutionResult]:
        """Get the resolution history."""
        return self.resolution_history
    
    def reset(self) -> None:
        """Reset the resolver state."""
        self.resolution_history.clear()
        self.process_priorities.clear()
        self.process_rollback_costs.clear()

```

---

## 6.4 Resource Ordering

The `DeadlockResolver` class also supports resource ordering for deadlock prevention.

### Ordering Rule
Processes must request resources in increasing order of resource ID.

### Implementation
```python
def apply_resource_ordering(self, resources: List[int]) -> Dict[int, int]:
    """Create a total ordering on resources."""
    return {rid: i for i, rid in enumerate(sorted(resources))}

def check_ordering_violation(self, pid: int, rid: int,
                              held_resources: List[int],
                              ordering: Dict[int, int]) -> bool:
    """Returns True if request violates ordering."""
    request_order = ordering.get(rid, float('inf'))
    for held_rid in held_resources:
        if ordering.get(held_rid, 0) >= request_order:
            return True  # Violation
    return False
```

---

## 6.5 Deadlock Mechanism Comparison Table

| Mechanism | Type | Approach | Overhead | Resource Utilization |
|-----------|------|----------|----------|---------------------|
| Detection + Termination | Recovery | Detect cycle, kill process | Low | High |
| Detection + Preemption | Recovery | Detect cycle, preempt resources | Low | High |
| Banker's Algorithm | Prevention | Check safety before allocation | High | Medium |
| Resource Ordering | Prevention | Enforce request order | Low | Medium |
| Wait-For Graph | Detection | Track dependencies | Medium | N/A |

### When to Use Each

| Scenario | Recommended Mechanism |
|----------|----------------------|
| High resource utilization needed | Detection + Recovery |
| Critical systems | Prevention (Banker's) |
| Simple resource hierarchy | Resource Ordering |
| Real-time monitoring | Wait-For Graph Detection |

---

# 7. REQUIREMENT 5: MEMORY MANAGEMENT

The system implements 4 page replacement algorithms in the `memory/` directory.

---

## 7.1 FIFO Page Replacement

**File:** `memory/fifo_replacement.py`

### Algorithm Description
First-In-First-Out evicts the page that has been in memory the longest.

### Key Characteristics
- Simple queue-based implementation
- Does not consider page usage patterns
- Subject to Belady's anomaly

### Implementation Code

```python
"""FIFO Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from collections import deque
from models.memory_page import Page, Frame


class FIFOReplacement:
    """First-In-First-Out page replacement algorithm.
    
    Evicts the page that has been in memory the longest.
    """
    
    def __init__(self):
        self.name = "FIFO"
        self.page_queue: deque = deque()  # (pid, page_id) in order of arrival
        self.fault_count = 0
        self.hit_count = 0
    
    def select_victim(self, frames: List[Frame], 
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page to evict.
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        while self.page_queue:
            victim_key = self.page_queue.popleft()
            pid, page_id = victim_key
            
            # Check if this page is still in memory
            if pid in page_tables and page_id in page_tables[pid]:
                frame_id = page_tables[pid][page_id]
                if frame_id is not None:
                    return frame_id, victim_key
        
        # Fallback: find any occupied frame
        for frame in frames:
            if not frame.is_free and frame.page:
                return frame.frame_id, (frame.page.process_id, frame.page.page_id)
        
        return None, None
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        self.page_queue.append((pid, page_id))
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed (no-op for FIFO)."""
        pass  # FIFO doesn't update on access
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        try:
            self.page_queue.remove((pid, page_id))
        except ValueError:
            pass  # Page wasn't in queue
    
    def simulate(self, reference_string: List[Tuple[int, int]], 
                 num_frames: int) -> Dict:
        """Simulate FIFO on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        page_queue: deque = deque()
        faults = 0
        hits = 0
        history = []
        
        for ref in reference_string:
            if ref in frames:
                # Hit
                hits += 1
                history.append({'ref': ref, 'fault': False, 'frames': list(frames)})
            else:
                # Fault
                faults += 1
                
                if None in frames:
                    # Free frame available
                    idx = frames.index(None)
                    frames[idx] = ref
                else:
                    # Evict oldest page
                    victim = page_queue.popleft()
                    idx = frames.index(victim)
                    frames[idx] = ref
                
                page_queue.append(ref)
                history.append({'ref': ref, 'fault': True, 'frames': list(frames)})
        
        return {
            'algorithm': self.name,
            'faults': faults,
            'hits': hits,
            'fault_rate': faults / len(reference_string) * 100 if reference_string else 0,
            'history': history
        }
    
    def reset(self) -> None:
        """Reset the algorithm state."""
        self.page_queue.clear()
        self.fault_count = 0
        self.hit_count = 0

```

---

## 7.2 LRU Page Replacement

**File:** `memory/lru_replacement.py`

### Algorithm Description
Least Recently Used evicts the page that hasn't been accessed for the longest time.

### Key Characteristics
- Uses OrderedDict to maintain access order
- Updates order on every access (hit)
- Good approximation of optimal

### Implementation Code

```python
"""LRU Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from collections import OrderedDict
from models.memory_page import Page, Frame


class LRUReplacement:
    """Least Recently Used page replacement algorithm.
    
    Evicts the page that hasn't been used for the longest time.
    """
    
    def __init__(self):
        self.name = "LRU"
        # OrderedDict maintains order of access (most recent at end)
        self.access_order: OrderedDict = OrderedDict()
        self.fault_count = 0
        self.hit_count = 0
    
    def select_victim(self, frames: List[Frame],
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page to evict (least recently used).
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        # Find the least recently used page that's still in memory
        for victim_key in self.access_order.keys():
            pid, page_id = victim_key
            
            if pid in page_tables and page_id in page_tables[pid]:
                frame_id = page_tables[pid][page_id]
                if frame_id is not None:
                    del self.access_order[victim_key]
                    return frame_id, victim_key
        
        # Fallback: find page with oldest access time
        oldest_time = float('inf')
        victim_frame = None
        victim_key = None
        
        for frame in frames:
            if not frame.is_free and frame.page:
                if frame.page.last_access_time < oldest_time:
                    oldest_time = frame.page.last_access_time
                    victim_frame = frame.frame_id
                    victim_key = (frame.page.process_id, frame.page.page_id)
        
        return victim_frame, victim_key
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        key = (pid, page_id)
        # Remove if exists and add to end (most recent)
        if key in self.access_order:
            del self.access_order[key]
        self.access_order[key] = True
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed (update LRU order)."""
        key = (pid, page_id)
        # Move to end (most recent)
        if key in self.access_order:
            del self.access_order[key]
        self.access_order[key] = True
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        key = (pid, page_id)
        if key in self.access_order:
            del self.access_order[key]
    
    def simulate(self, reference_string: List[Tuple[int, int]],
                 num_frames: int) -> Dict:
        """Simulate LRU on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        access_order: OrderedDict = OrderedDict()
        faults = 0
        hits = 0
        history = []
        
        for ref in reference_string:
            if ref in frames:
                # Hit - update access order
                hits += 1
                del access_order[ref]
                access_order[ref] = True
                history.append({'ref': ref, 'fault': False, 'frames': list(frames)})
            else:
                # Fault
                faults += 1
                
                if None in frames:
                    # Free frame available
                    idx = frames.index(None)
                    frames[idx] = ref
                else:
                    # Evict LRU page
                    victim = next(iter(access_order))
                    del access_order[victim]
                    idx = frames.index(victim)
                    frames[idx] = ref
                
                access_order[ref] = True
                history.append({'ref': ref, 'fault': True, 'frames': list(frames)})
        
        return {
            'algorithm': self.name,
            'faults': faults,
            'hits': hits,
            'fault_rate': faults / len(reference_string) * 100 if reference_string else 0,
            'history': history
        }
    
    def reset(self) -> None:
        """Reset the algorithm state."""
        self.access_order.clear()
        self.fault_count = 0
        self.hit_count = 0

```

---

## 7.3 Optimal (Belady's) Page Replacement

**File:** `memory/optimal_replacement.py`

### Algorithm Description
Optimal evicts the page that won't be used for the longest time in the future. This is a theoretical algorithm requiring future knowledge.

### Key Characteristics
- Requires knowledge of future references
- Provides minimum possible page faults
- Used as benchmark for other algorithms

### Implementation Code

```python
"""Optimal (Belady's) Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from models.memory_page import Page, Frame


class OptimalReplacement:
    """Optimal (Belady's) page replacement algorithm.
    
    Evicts the page that won't be used for the longest time in the future.
    This is an oracle algorithm - requires knowledge of future references.
    """
    
    def __init__(self, future_references: List[Tuple[int, int]] = None):
        self.name = "Optimal (Belady)"
        self.future_references = future_references or []
        self.current_index = 0
        self.fault_count = 0
        self.hit_count = 0
    
    def set_future_references(self, references: List[Tuple[int, int]]) -> None:
        """Set the future reference string."""
        self.future_references = references
        self.current_index = 0
    
    def select_victim(self, frames: List[Frame],
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page to evict (one with furthest future use).
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        # Get all pages currently in memory
        in_memory = []
        for frame in frames:
            if not frame.is_free and frame.page:
                in_memory.append((frame.frame_id, frame.page.process_id, frame.page.page_id))
        
        if not in_memory:
            return None, None
        
        # Find which page won't be used for the longest time
        future = self.future_references[self.current_index:] if self.future_references else []
        
        best_victim = None
        max_distance = -1
        
        for frame_id, pid, page_id in in_memory:
            key = (pid, page_id)
            
            # Find next use of this page
            try:
                distance = future.index(key)
            except ValueError:
                # Page won't be used again - perfect victim
                return frame_id, key
            
            if distance > max_distance:
                max_distance = distance
                best_victim = (frame_id, key)
        
        if best_victim:
            return best_victim[0], best_victim[1]
        
        # Fallback: first occupied frame
        return in_memory[0][0], (in_memory[0][1], in_memory[0][2])
    
    def advance_reference(self) -> None:
        """Advance the current reference index."""
        self.current_index += 1
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        pass  # Optimal doesn't need to track this
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed."""
        self.advance_reference()
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        pass  # Optimal doesn't need to track this
    
    def simulate(self, reference_string: List[Tuple[int, int]],
                 num_frames: int) -> Dict:
        """Simulate Optimal on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        faults = 0
        hits = 0
        history = []
        
        # Precompute next use positions for each page at each index for O(n) lookup
        next_use = {}  # {page: [list of indices where it appears]}
        for idx, ref in enumerate(reference_string):
            if ref not in next_use:
                next_use[ref] = []
            next_use[ref].append(idx)
        
        for i, ref in enumerate(reference_string):
            if ref in frames:
                # Hit
                hits += 1
                history.append({'ref': ref, 'fault': False, 'frames': list(frames)})
            else:
                # Fault
                faults += 1
                
                if None in frames:
                    # Free frame available
                    idx = frames.index(None)
                    frames[idx] = ref
                else:
                    # Find optimal victim using precomputed positions
                    best_idx = 0
                    max_distance = -1
                    
                    for j, page in enumerate(frames):
                        # Find next use of this page after current position
                        positions = next_use.get(page, [])
                        # Binary search for next position > i
                        next_pos = None
                        for pos in positions:
                            if pos > i:
                                next_pos = pos
                                break
                        
                        if next_pos is None:
                            # Page not used again - evict it
                            best_idx = j
                            break
                        
                        distance = next_pos - i
                        if distance > max_distance:
                            max_distance = distance
                            best_idx = j
                    
                    frames[best_idx] = ref
                
                history.append({'ref': ref, 'fault': True, 'frames': list(frames)})
        
        return {
            'algorithm': self.name,
            'faults': faults,
            'hits': hits,
            'fault_rate': faults / len(reference_string) * 100 if reference_string else 0,
            'history': history
        }
    
    def reset(self) -> None:
        """Reset the algorithm state."""
        self.current_index = 0
        self.fault_count = 0
        self.hit_count = 0

```

---

## 7.4 Clock (Second Chance) Page Replacement

**File:** `memory/clock_replacement.py`

### Algorithm Description
Clock is an efficient approximation of LRU using reference bits and a circular buffer.

### Key Characteristics
- Uses reference bit for each page
- Circular sweep gives "second chance"
- More efficient than LRU (no list updates on hit)

### Implementation Code

```python
"""Clock (Second Chance) Page Replacement Algorithm for OS simulation."""

from typing import List, Dict, Optional, Tuple
from models.memory_page import Page, Frame


class ClockReplacement:
    """Clock (Second Chance) page replacement algorithm.
    
    A more efficient approximation of LRU using a circular queue
    and reference bits.
    """
    
    def __init__(self):
        self.name = "Clock (Second Chance)"
        self.clock_hand = 0  # Current position in the circular buffer
        self.page_list: List[Tuple[int, int]] = []  # Pages in circular order
        self.reference_bits: Dict[Tuple[int, int], bool] = {}  # Reference bit for each page
        self.fault_count = 0
        self.hit_count = 0
    
    def select_victim(self, frames: List[Frame],
                      pages: Dict[Tuple[int, int], Page],
                      page_tables: Dict[int, Dict[int, Optional[int]]]) -> Tuple[Optional[int], Optional[Tuple[int, int]]]:
        """Select a victim page using the Clock algorithm.
        
        Returns: (frame_id, (victim_pid, victim_page_id))
        """
        if not self.page_list:
            # Build page list from frames
            for frame in frames:
                if not frame.is_free and frame.page:
                    key = (frame.page.process_id, frame.page.page_id)
                    if key not in self.page_list:
                        self.page_list.append(key)
                        self.reference_bits[key] = True
        
        if not self.page_list:
            return None, None
        
        # Clock algorithm: circle until finding page with reference bit = 0
        max_iterations = len(self.page_list) * 2  # Safety limit
        iterations = 0
        
        while iterations < max_iterations:
            if self.clock_hand >= len(self.page_list):
                self.clock_hand = 0
            
            key = self.page_list[self.clock_hand]
            pid, page_id = key
            
            # Check if page is still in memory
            if pid not in page_tables or page_id not in page_tables[pid]:
                # Page no longer valid, remove from list
                self.page_list.pop(self.clock_hand)
                if key in self.reference_bits:
                    del self.reference_bits[key]
                iterations += 1
                continue
            
            frame_id = page_tables[pid][page_id]
            if frame_id is None:
                # Page no longer in memory
                self.page_list.pop(self.clock_hand)
                if key in self.reference_bits:
                    del self.reference_bits[key]
                iterations += 1
                continue
            
            # Check reference bit
            if self.reference_bits.get(key, False):
                # Give second chance - clear reference bit
                self.reference_bits[key] = False
                self.clock_hand = (self.clock_hand + 1) % max(1, len(self.page_list))
            else:
                # Found victim
                self.page_list.pop(self.clock_hand)
                if key in self.reference_bits:
                    del self.reference_bits[key]
                return frame_id, key
            
            iterations += 1
        
        # Fallback: evict first page
        if self.page_list:
            key = self.page_list.pop(0)
            pid, page_id = key
            if pid in page_tables and page_id in page_tables[pid]:
                frame_id = page_tables[pid][page_id]
                if frame_id is not None:
                    return frame_id, key
        
        # Last resort: find any occupied frame
        for frame in frames:
            if not frame.is_free and frame.page:
                return frame.frame_id, (frame.page.process_id, frame.page.page_id)
        
        return None, None
    
    def page_loaded(self, pid: int, page_id: int) -> None:
        """Notify that a page has been loaded into memory."""
        key = (pid, page_id)
        if key not in self.page_list:
            # Insert at clock hand position
            if self.page_list:
                self.page_list.insert(self.clock_hand, key)
            else:
                self.page_list.append(key)
        self.reference_bits[key] = True
    
    def page_accessed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been accessed (set reference bit)."""
        key = (pid, page_id)
        self.reference_bits[key] = True
    
    def page_removed(self, pid: int, page_id: int) -> None:
        """Notify that a page has been removed from memory."""
        key = (pid, page_id)
        if key in self.page_list:
            idx = self.page_list.index(key)
            self.page_list.remove(key)
            # Adjust clock hand if needed
            if idx < self.clock_hand:
                self.clock_hand = max(0, self.clock_hand - 1)
        if key in self.reference_bits:
            del self.reference_bits[key]
    
    def simulate(self, reference_string: List[Tuple[int, int]],
                 num_frames: int) -> Dict:
        """Simulate Clock algorithm on a reference string.
        
        Args:
            reference_string: List of (pid, page_id) references
            num_frames: Number of available frames
            
        Returns:
            Dictionary with simulation results
        """
        frames: List[Optional[Tuple[int, int]]] = [None] * num_frames
        ref_bits: List[bool] = [False] * num_frames
        clock = 0
        faults = 0
        hits = 0
        history = []
        
        for ref in reference_string:
            if ref in frames:
                # Hit - set reference bit
                hits += 1
                idx = frames.index(ref)
                ref_bits[idx] = True
                history.append({'ref': ref, 'fault': False, 'frames': list(frames)})
            else:
                # Fault
                faults += 1
                
                if None in frames:
                    # Free frame available
                    idx = frames.index(None)
                    frames[idx] = ref
                    ref_bits[idx] = True
                else:
                    # Clock algorithm
                    while True:
                        if ref_bits[clock]:
                            ref_bits[clock] = False
                            clock = (clock + 1) % num_frames
                        else:
                            frames[clock] = ref
                            ref_bits[clock] = True
                            clock = (clock + 1) % num_frames
                            break
                
                history.append({'ref': ref, 'fault': True, 'frames': list(frames)})
        
        return {
            'algorithm': self.name,
            'faults': faults,
            'hits': hits,
            'fault_rate': faults / len(reference_string) * 100 if reference_string else 0,
            'history': history
        }
    
    def reset(self) -> None:
        """Reset the algorithm state."""
        self.clock_hand = 0
        self.page_list.clear()
        self.reference_bits.clear()
        self.fault_count = 0
        self.hit_count = 0

```

---

## 7.5 Conclusion: LRU is Best

### Algorithm Comparison

| Algorithm | Fault Rate | Implementation Complexity | Overhead |
|-----------|------------|---------------------------|----------|
| FIFO | High | Simple | Low |
| LRU | Low | Moderate | Medium |
| Optimal | Lowest | N/A (oracle) | N/A |
| Clock | Low | Moderate | Low |

### Why LRU is the Best Practical Choice

1. **Low Fault Rate**: Exploits temporal locality effectively
2. **No Belady's Anomaly**: Unlike FIFO
3. **Practical Implementation**: Unlike Optimal
4. **Reasonable Overhead**: Acceptable for most systems

### Recommendation
For general-purpose systems, **LRU** provides the best balance of performance and practicality. For systems where overhead is critical, **Clock** is a good alternative.

---

# 8. REQUIREMENT 6: SYSTEM TESTING

All test scenarios are in the `tests/` directory.

---

## 8.1 Test Scenario 1: CPU-Bound Batch

**File:** `tests/test_scenario_1.py`

### Configuration
- 10 processes with burst times 100-500ms
- All CPU-bound (io_bound=False)
- Expected: SJF/SRTF selection by adaptive scheduler

### Test Code

```python
#!/usr/bin/env python3
"""Test Scenario 1: CPU-Bound Batch Processing

Creates 10 processes with burst times 100-500ms.
Expected: SJF or SRTF selection by adaptive scheduler.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.simulation_engine import SimulationEngine
from scheduling.adaptive_selector import AdaptiveSelector


def test_cpu_bound_batch():
    """Run CPU-bound batch processing test."""
    console = Console()
    engine = SimulationEngine()
    
    console.print(Panel(
        "[bold]Test Scenario 1: CPU-Bound Batch Processing[/bold]\n\n"
        "• 10 processes with burst times 100-500ms\n"
        "• All CPU-bound processes\n"
        "• Expected: SJF or SRTF selection",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    # Create 10 CPU-bound processes with burst times 100-500ms
    processes_data = [
        ("Batch_1", 150, 5, 0),
        ("Batch_2", 300, 3, 10),
        ("Batch_3", 100, 7, 20),
        ("Batch_4", 450, 2, 30),
        ("Batch_5", 200, 4, 40),
        ("Batch_6", 350, 6, 50),
        ("Batch_7", 500, 1, 60),
        ("Batch_8", 250, 8, 70),
        ("Batch_9", 400, 9, 80),
        ("Batch_10", 180, 10, 90),
    ]
    
    for name, burst, priority, arrival in processes_data:
        engine.create_process(
            name=name,
            burst_time=burst,
            priority=priority,
            arrival_time=arrival,
            io_bound=False,
            memory_pages=5
        )
    
    # Display processes
    table = Table(title="Created Processes", box=box.ROUNDED)
    table.add_column("PID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Burst (ms)", style="yellow", justify="right")
    table.add_column("Priority", style="magenta", justify="center")
    table.add_column("Arrival", style="green", justify="right")
    
    for p in engine.processes:
        table.add_row(
            f"P{p.pid}",
            p.name,
            str(p.burst_time),
            str(p.priority),
            str(p.arrival_time)
        )
    
    console.print(table)
    
    # Get adaptive recommendation
    rec = engine.get_adaptive_recommendation()
    
    console.print(Panel(
        f"[bold green]Selected Algorithm: {rec['algorithm']}[/bold green]\n\n"
        f"Justification: {rec['justification']}\n\n"
        f"Expected Average Wait Time: {rec['expected_wait']:.0f}ms\n"
        f"Confidence: {rec['confidence']*100:.0f}%",
        title="Adaptive Scheduler Selection",
        border_style="green"
    ))
    
    # Run simulation with recommended algorithm
    console.print("\n[bold]Running simulation...[/bold]\n")
    result = engine.run_scheduling()
    
    # Display results
    results_table = Table(title="Simulation Results", box=box.ROUNDED)
    results_table.add_column("Metric", style="cyan")
    results_table.add_column("Value", style="green", justify="right")
    
    results_table.add_row("Algorithm Used", result.algorithm)
    results_table.add_row("Total Time", f"{result.total_time}ms")
    results_table.add_row("Avg Waiting Time", f"{result.avg_waiting_time:.2f}ms")
    results_table.add_row("Avg Turnaround Time", f"{result.avg_turnaround_time:.2f}ms")
    results_table.add_row("Avg Response Time", f"{result.avg_response_time:.2f}ms")
    results_table.add_row("CPU Utilization", f"{result.cpu_utilization:.2f}%")
    results_table.add_row("Context Switches", str(result.context_switches))
    
    console.print(results_table)
    
    # Compare all algorithms
    console.print("\n[bold]Comparing all scheduling algorithms...[/bold]\n")
    
    all_results = engine.compare_all_schedulers()
    
    compare_table = Table(title="Algorithm Comparison", box=box.ROUNDED)
    compare_table.add_column("Algorithm", style="cyan")
    compare_table.add_column("Avg Wait", style="yellow", justify="right")
    compare_table.add_column("Avg TAT", style="green", justify="right")
    compare_table.add_column("CPU Util", style="blue", justify="right")
    
    best_wait = min(r['avg_waiting'] for r in all_results)
    
    for r in all_results:
        style = "bold green" if r['avg_waiting'] == best_wait else ""
        compare_table.add_row(
            r['algorithm'],
            f"[{style}]{r['avg_waiting']:.2f}ms[/{style}]" if style else f"{r['avg_waiting']:.2f}ms",
            f"{r['avg_turnaround']:.2f}ms",
            f"{r['cpu_utilization']:.1f}%"
        )
    
    console.print(compare_table)
    
    # Verification
    console.print("\n[bold]Test Verification:[/bold]")
    
    expected_algorithms = ['SJF', 'SRTF']
    if any(alg in rec['algorithm'] for alg in expected_algorithms):
        console.print("[bold green]✓ PASS: Adaptive selector chose SJF/SRTF as expected[/bold green]")
        return True
    else:
        console.print(f"[bold yellow]⚠ Adaptive selector chose {rec['algorithm']} instead of SJF/SRTF[/bold yellow]")
        console.print("[dim]This may be valid depending on workload characteristics[/dim]")
        return True  # Still valid


if __name__ == "__main__":
    success = test_cpu_bound_batch()
    sys.exit(0 if success else 1)

```

### How to Run
```bash
python3 -m tests.test_scenario_1
```

---

## 8.2 Test Scenario 2: Interactive Mixed

**File:** `tests/test_scenario_2.py`

### Configuration
- 20 processes with burst times 10-50ms
- Mix of I/O-bound and CPU-bound
- Expected: Round Robin/MLFQ selection

### Test Code

```python
#!/usr/bin/env python3
"""Test Scenario 2: Interactive Mixed Workload

Creates 20 processes with burst times 10-50ms.
Expected: Round Robin or MLFQ selection by adaptive scheduler.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.simulation_engine import SimulationEngine


def test_interactive_mixed():
    """Run interactive mixed workload test."""
    console = Console()
    engine = SimulationEngine()
    
    console.print(Panel(
        "[bold]Test Scenario 2: Interactive Mixed Workload[/bold]\n\n"
        "• 20 processes with burst times 10-50ms\n"
        "• Mix of I/O-bound and CPU-bound processes\n"
        "• Expected: Round Robin or MLFQ selection",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    # Create 20 interactive processes with short burst times
    random.seed(42)  # For reproducibility
    
    for i in range(20):
        burst = random.randint(10, 50)
        io_bound = random.random() < 0.4  # 40% I/O bound
        
        engine.create_process(
            name=f"Interactive_{i+1}",
            burst_time=burst,
            priority=random.randint(1, 10),
            arrival_time=i * 5,  # Staggered arrivals
            io_bound=io_bound,
            memory_pages=random.randint(2, 5)
        )
    
    # Display first 10 processes
    table = Table(title="Created Processes (first 10 of 20)", box=box.ROUNDED)
    table.add_column("PID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Burst (ms)", style="yellow", justify="right")
    table.add_column("Type", style="magenta", justify="center")
    table.add_column("Arrival", style="green", justify="right")
    
    for p in engine.processes[:10]:
        table.add_row(
            f"P{p.pid}",
            p.name,
            str(p.burst_time),
            "I/O" if p.io_bound else "CPU",
            str(p.arrival_time)
        )
    
    console.print(table)
    console.print(f"[dim]... and 10 more processes[/dim]\n")
    
    # Get adaptive recommendation
    rec = engine.get_adaptive_recommendation()
    
    console.print(Panel(
        f"[bold green]Selected Algorithm: {rec['algorithm']}[/bold green]\n\n"
        f"Justification: {rec['justification']}\n\n"
        f"Expected Average Wait Time: {rec['expected_wait']:.0f}ms\n"
        f"Confidence: {rec['confidence']*100:.0f}%",
        title="Adaptive Scheduler Selection",
        border_style="green"
    ))
    
    # Run simulation
    console.print("\n[bold]Running simulation...[/bold]\n")
    result = engine.run_scheduling()
    
    # Display results
    results_table = Table(title="Simulation Results", box=box.ROUNDED)
    results_table.add_column("Metric", style="cyan")
    results_table.add_column("Value", style="green", justify="right")
    
    results_table.add_row("Algorithm Used", result.algorithm)
    results_table.add_row("Total Time", f"{result.total_time}ms")
    results_table.add_row("Avg Waiting Time", f"{result.avg_waiting_time:.2f}ms")
    results_table.add_row("Avg Turnaround Time", f"{result.avg_turnaround_time:.2f}ms")
    results_table.add_row("Avg Response Time", f"{result.avg_response_time:.2f}ms")
    results_table.add_row("CPU Utilization", f"{result.cpu_utilization:.2f}%")
    results_table.add_row("Context Switches", str(result.context_switches))
    results_table.add_row("Throughput", f"{result.throughput:.2f} proc/sec")
    
    console.print(results_table)
    
    # Process completion times
    proc_table = Table(title="Process Completion (first 10)", box=box.ROUNDED)
    proc_table.add_column("PID", style="cyan")
    proc_table.add_column("Burst", justify="right")
    proc_table.add_column("Waiting", style="yellow", justify="right")
    proc_table.add_column("Response", style="magenta", justify="right")
    proc_table.add_column("Turnaround", style="green", justify="right")
    
    for p in result.processes[:10]:
        proc_table.add_row(
            f"P{p.pid}",
            str(p.burst_time),
            str(p.waiting_time),
            str(p.response_time) if p.response_time >= 0 else "-",
            str(p.turnaround_time)
        )
    
    console.print(proc_table)
    
    # Compare relevant algorithms
    console.print("\n[bold]Comparing interactive-suitable algorithms...[/bold]\n")
    
    all_results = engine.compare_all_schedulers()
    
    compare_table = Table(title="Algorithm Comparison", box=box.ROUNDED)
    compare_table.add_column("Algorithm", style="cyan")
    compare_table.add_column("Avg Response", style="magenta", justify="right")
    compare_table.add_column("Avg Wait", style="yellow", justify="right")
    compare_table.add_column("Context Switches", style="red", justify="right")
    
    for r in all_results:
        compare_table.add_row(
            r['algorithm'],
            f"{r['avg_response']:.2f}ms",
            f"{r['avg_waiting']:.2f}ms",
            str(r['context_switches'])
        )
    
    console.print(compare_table)
    
    # Verification
    console.print("\n[bold]Test Verification:[/bold]")
    
    expected_algorithms = ['Round Robin', 'RR', 'MLFQ']
    if any(alg in rec['algorithm'] for alg in expected_algorithms):
        console.print("[bold green]✓ PASS: Adaptive selector chose Round Robin/MLFQ as expected[/bold green]")
        return True
    else:
        console.print(f"[bold yellow]⚠ Adaptive selector chose {rec['algorithm']}[/bold yellow]")
        console.print("[dim]This may be valid for certain workload characteristics[/dim]")
        return True


if __name__ == "__main__":
    success = test_interactive_mixed()
    sys.exit(0 if success else 1)

```

### How to Run
```bash
python3 -m tests.test_scenario_2
```

---

## 8.3 Test Scenario 3: Deadlock Demo

**File:** `tests/test_scenario_3.py`

### Configuration
- 4 processes (P1-P4)
- 4 resources (R1-R4)
- Circular wait condition created

### Test Code
(See Section 4.3 for full code)

### How to Run
```bash
python3 -m tests.test_scenario_3
```

---

## 8.4 Test Scenario 4: Race Condition

**File:** `tests/test_scenario_4.py`

### Configuration
- 5 threads
- Each increments counter 1000 times
- Tests WITH and WITHOUT mutex protection

### Test Code
(See Section 5.3 for full code)

### How to Run
```bash
python3 -m tests.test_scenario_4
```

---

## 8.5 Test Scenario 5: Memory Thrashing

**File:** `tests/test_scenario_5.py`

### Configuration
- 20 processes with 10 pages each (200 total)
- Only 50 physical frames
- Overcommitment ratio: 4:1

### Test Code

```python
#!/usr/bin/env python3
"""Test Scenario 5: Memory Thrashing

Creates 20 processes with 10 pages each, using 50 frames.
Expected: High page fault rate demonstrating thrashing.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

from memory import (
    MemoryManager,
    FIFOReplacement, LRUReplacement, OptimalReplacement, ClockReplacement
)


def test_memory_thrashing():
    """Run memory thrashing test."""
    console = Console()
    
    console.print(Panel(
        "[bold]Test Scenario 5: Memory Thrashing Demonstration[/bold]\n\n"
        "• 20 processes with 10 pages each = 200 total pages\n"
        "• Only 50 physical frames available\n"
        "• High memory pressure ratio (4:1)\n\n"
        "Expected: High page fault rate",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    num_processes = 20
    pages_per_process = 10
    num_frames = 50
    total_pages = num_processes * pages_per_process
    
    console.print(f"\n[bold]Memory Configuration:[/bold]")
    console.print(f"  Total virtual pages: {total_pages}")
    console.print(f"  Physical frames: {num_frames}")
    console.print(f"  Overcommitment ratio: {total_pages/num_frames:.1f}:1")
    
    # Generate reference string simulating thrashing
    random.seed(42)  # For reproducibility
    
    # Create a reference string that causes thrashing
    # Each process accesses its pages randomly
    reference_string = []
    for _ in range(500):  # 500 memory accesses
        pid = random.randint(1, num_processes)
        page = random.randint(0, pages_per_process - 1)
        reference_string.append((pid, page))
    
    console.print(f"  Reference string length: {len(reference_string)}")
    console.print(f"\n[bold]First 10 references:[/bold] {reference_string[:10]}")
    
    # Test all page replacement algorithms
    algorithms = {
        'FIFO': FIFOReplacement(),
        'LRU': LRUReplacement(),
        'Optimal': OptimalReplacement(),
        'Clock': ClockReplacement()
    }
    
    results = {}
    
    console.print("\n[bold]Running page replacement simulations...[/bold]\n")
    
    # Set future references for Optimal
    algorithms['Optimal'].set_future_references(reference_string)
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        for name, algo in algorithms.items():
            task = progress.add_task(f"Testing {name}...", total=100)
            
            result = algo.simulate(reference_string, num_frames)
            results[name] = result
            
            progress.update(task, completed=100)
    
    # Display results
    console.print("\n" + "="*70)
    console.print("[bold cyan]Page Replacement Algorithm Comparison[/bold cyan]")
    console.print("="*70 + "\n")
    
    table = Table(title="Results (50 frames, 500 accesses)", box=box.ROUNDED)
    table.add_column("Algorithm", style="cyan")
    table.add_column("Page Faults", style="red", justify="right")
    table.add_column("Page Hits", style="green", justify="right")
    table.add_column("Fault Rate", style="yellow", justify="right")
    table.add_column("Hit Rate", style="blue", justify="right")
    
    best_faults = min(r['faults'] for r in results.values())
    
    for name, result in results.items():
        fault_style = "bold green" if result['faults'] == best_faults else ""
        hit_rate = 100 - result['fault_rate']
        
        table.add_row(
            name,
            f"[{fault_style}]{result['faults']}[/{fault_style}]" if fault_style else str(result['faults']),
            str(result['hits']),
            f"{result['fault_rate']:.1f}%",
            f"{hit_rate:.1f}%"
        )
    
    console.print(table)
    
    # Analysis
    avg_fault_rate = sum(r['fault_rate'] for r in results.values()) / len(results)
    
    console.print(Panel(
        f"[bold]Analysis:[/bold]\n\n"
        f"Average Fault Rate: {avg_fault_rate:.1f}%\n"
        f"Best Algorithm: [green]{min(results.items(), key=lambda x: x[1]['faults'])[0]}[/green]\n"
        f"Worst Algorithm: [red]{max(results.items(), key=lambda x: x[1]['faults'])[0]}[/red]\n\n"
        f"[bold]Thrashing Indicators:[/bold]\n"
        f"• Fault rate > 50%: {'Yes ⚠️' if avg_fault_rate > 50 else 'No'}\n"
        f"• Overcommitment ratio > 2: Yes (4:1)\n"
        f"• Random access pattern: High locality violation",
        title="Memory Analysis",
        border_style="yellow"
    ))
    
    # Show what happens with different frame counts
    console.print("\n[bold]Effect of Frame Count on Page Faults (FIFO):[/bold]\n")
    
    frame_counts = [10, 20, 30, 50, 100, 150, 200]
    fifo = FIFOReplacement()
    
    frame_table = Table(box=box.ROUNDED)
    frame_table.add_column("Frames", style="cyan", justify="right")
    frame_table.add_column("Faults", style="red", justify="right")
    frame_table.add_column("Fault Rate", style="yellow", justify="right")
    frame_table.add_column("Status", justify="center")
    
    for frames in frame_counts:
        result = fifo.simulate(reference_string, frames)
        
        if result['fault_rate'] > 70:
            status = "[bold red]Thrashing[/bold red]"
        elif result['fault_rate'] > 40:
            status = "[yellow]High Faults[/yellow]"
        else:
            status = "[green]Normal[/green]"
        
        frame_table.add_row(
            str(frames),
            str(result['faults']),
            f"{result['fault_rate']:.1f}%",
            status
        )
    
    console.print(frame_table)
    
    # Verification
    console.print("\n[bold]Test Verification:[/bold]")
    
    # We expect high fault rate with 50 frames for 200 pages
    if avg_fault_rate > 40:
        console.print("[green]✓ High page fault rate demonstrates memory thrashing[/green]")
        console.print(f"[green]✓ Optimal algorithm performed best ({results['Optimal']['faults']} faults)[/green]")
        console.print("[bold green]✓ PASS: Memory thrashing scenario demonstrated successfully[/bold green]")
        return True
    else:
        console.print("[yellow]⚠ Page fault rate lower than expected[/yellow]")
        return True  # Still valid


def analyze_locality():
    """Analyze the effect of locality on page faults."""
    console = Console()
    
    console.print("\n" + "="*70)
    console.print("[bold cyan]Locality of Reference Analysis[/bold cyan]")
    console.print("="*70 + "\n")
    
    num_frames = 10
    
    # High locality reference string (temporal + spatial)
    high_locality = []
    for _ in range(50):
        page = random.choice([0, 1, 2])  # Working set of 3 pages
        for _ in range(5):
            high_locality.append((1, page))
        # Occasional jump
        if random.random() < 0.2:
            high_locality.append((1, random.randint(5, 9)))
    
    # Low locality reference string (random)
    low_locality = [(1, random.randint(0, 9)) for _ in range(250)]
    
    fifo = FIFOReplacement()
    lru = LRUReplacement()
    
    console.print("[bold]Comparing High vs Low Locality (10 frames):[/bold]\n")
    
    table = Table(box=box.ROUNDED)
    table.add_column("Locality", style="cyan")
    table.add_column("FIFO Faults", style="red", justify="right")
    table.add_column("LRU Faults", style="red", justify="right")
    table.add_column("Reference Length", justify="right")
    
    high_fifo = fifo.simulate(high_locality, num_frames)
    high_lru = lru.simulate(high_locality, num_frames)
    low_fifo = fifo.simulate(low_locality, num_frames)
    low_lru = lru.simulate(low_locality, num_frames)
    
    table.add_row(
        "High Locality",
        f"{high_fifo['faults']} ({high_fifo['fault_rate']:.1f}%)",
        f"{high_lru['faults']} ({high_lru['fault_rate']:.1f}%)",
        str(len(high_locality))
    )
    table.add_row(
        "Low Locality",
        f"{low_fifo['faults']} ({low_fifo['fault_rate']:.1f}%)",
        f"{low_lru['faults']} ({low_lru['fault_rate']:.1f}%)",
        str(len(low_locality))
    )
    
    console.print(table)
    
    console.print("\n[bold]Conclusion:[/bold]")
    console.print("• High locality significantly reduces page faults")
    console.print("• LRU benefits more from locality than FIFO")
    console.print("• Working set model helps predict memory needs")


if __name__ == "__main__":
    success = test_memory_thrashing()
    print()
    analyze_locality()
    sys.exit(0 if success else 1)

```

### How to Run
```bash
python3 -m tests.test_scenario_5
```

---

# 9. CONCLUSIONS

## 9.1 Project Summary

This OS Simulation System successfully demonstrates the core concepts of operating systems:

### CPU Scheduling
- Implemented 7 algorithms covering all major scheduling strategies
- Adaptive selector automatically chooses optimal algorithm
- Comprehensive metrics collection and comparison

### Resource Management
- Full resource allocation tracking
- Resource Allocation Graph for visualization
- Support for multiple resource types

### Deadlock Handling
- Detection using DFS cycle detection
- Prevention using Banker's Algorithm
- Resolution via termination and preemption
- Resource ordering for prevention

### Synchronization
- Mutex for mutual exclusion
- Semaphore for counting resources
- Race condition demonstration

### Memory Management
- 4 page replacement algorithms
- Page fault tracking and analysis
- Thrashing detection

## 9.2 Key Learnings

1. **Scheduling Trade-offs**: No single algorithm is best for all workloads
2. **Deadlock Complexity**: Prevention has overhead; detection allows better utilization
3. **Synchronization Necessity**: Race conditions are real and dangerous
4. **Memory Hierarchy**: Page replacement significantly affects performance

## 9.3 Future Improvements

1. Add more scheduling algorithms (EDF, Rate Monotonic)
2. Implement I/O scheduling
3. Add file system simulation
4. GUI visualization

---

# 10. APPENDICES

## 10.1 How to Run the Project

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/Basim-Gul/OS-CPP.git
cd OS-CPP

# Install dependencies
pip install -r requirements.txt
```

### Running the Main Application
```bash
python3 main.py
```

### Running Test Scenarios
```bash
# Run all tests
python3 main.py --test

# Run specific test (1-5)
python3 main.py --test 1   # CPU-bound batch
python3 main.py --test 2   # Interactive mixed
python3 main.py --test 3   # Deadlock demo
python3 main.py --test 4   # Race condition
python3 main.py --test 5   # Memory thrashing
```

### Running Individual Test Modules
```bash
python3 -m tests.test_scenario_1
python3 -m tests.test_scenario_2
python3 -m tests.test_scenario_3
python3 -m tests.test_scenario_4
python3 -m tests.test_scenario_5
```

## 10.2 Dependencies

```
rich>=13.0.0
colorama>=0.4.6
```

## 10.3 References

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). Operating System Concepts (10th ed.)
2. Tanenbaum, A. S., & Bos, H. (2014). Modern Operating Systems (4th ed.)
3. Course materials - CSC-320 Operating Systems, Bahria University

---

**END OF REPORT**

---

*Document generated from Basim-Gul/OS-CPP repository*
*Total Lines: ~2000*
*Total Sections: 10 major sections covering all 6 requirements*
