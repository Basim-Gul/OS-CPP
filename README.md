# OS Simulation System

A comprehensive **Python-based OS simulation** for Ubuntu terminal. This is a **PURE CONSOLE APPLICATION** with beautiful text-based UI using the Rich library.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Ubuntu/Linux-orange.svg)

## Features

### CPU Scheduling (7 Algorithms)
- **FCFS** (First-Come-First-Serve)
- **SJF** (Shortest Job First)
- **SRTF** (Shortest Remaining Time First)
- **Round Robin** (configurable time quantum)
- **Priority Scheduling** (Non-Preemptive)
- **Preemptive Priority with Aging**
- **MLFQ** (Multi-Level Feedback Queue)
- **Adaptive Scheduler** - Automatically selects best algorithm

### Resource Management & Deadlock Handling
- Resource Allocation Graph (RAG)
- DFS-based cycle detection
- Banker's Algorithm for prevention
- Process termination and resource preemption for recovery

### Synchronization
- Mutex implementation
- Counting semaphores
- Race condition demonstration (with/without mutex)
- Producer-Consumer problem

### Memory Management (4 Page Replacement Algorithms)
- FIFO (First-In-First-Out)
- LRU (Least Recently Used)
- Optimal (Belady's Algorithm)
- Clock (Second Chance)

### Logging & Metrics
- Complete activity logging
- Gantt chart generation
- Waiting time, turnaround time, response time
- CPU utilization, throughput
- Export to files

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/Basim-Gul/OS-CPP.git
cd OS-CPP

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python3 main.py
```

This launches the interactive console UI with menus for:
- Creating processes manually or auto-generating
- Running simulations with different scheduling algorithms
- Viewing Gantt charts and logs
- Demonstrating race conditions
- Managing memory and resources
- Exporting reports

### Run Test Scenarios

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

### Run Individual Test Modules

```bash
python3 -m tests.test_scenario_1  # CPU-bound batch
python3 -m tests.test_scenario_2  # Interactive mixed
python3 -m tests.test_scenario_3  # Deadlock demo
python3 -m tests.test_scenario_4  # Race condition
python3 -m tests.test_scenario_5  # Memory thrashing
```

## Project Structure

```
OS-CPP/
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── models/                          # Data models
│   ├── process.py                   # Process class
│   ├── resource.py                  # Resource class
│   ├── memory_page.py               # Page/Frame classes
│   ├── mutex.py                     # Mutex implementation
│   └── semaphore.py                 # Semaphore implementation
│
├── scheduling/                      # Scheduling algorithms
│   ├── base_scheduler.py            # Abstract base
│   ├── fcfs_scheduler.py
│   ├── sjf_scheduler.py
│   ├── srtf_scheduler.py
│   ├── round_robin_scheduler.py
│   ├── priority_scheduler.py
│   ├── mlfq_scheduler.py
│   └── adaptive_selector.py
│
├── resources/                       # Resource management
│   ├── resource_manager.py
│   ├── rag.py                       # Resource Allocation Graph
│   ├── deadlock_detector.py
│   ├── bankers_algorithm.py
│   └── deadlock_resolver.py
│
├── synchronization/                 # Synchronization
│   ├── sync_manager.py
│   ├── critical_section.py
│   └── race_detector.py
│
├── memory/                          # Memory management
│   ├── memory_manager.py
│   ├── page_table.py
│   ├── fifo_replacement.py
│   ├── lru_replacement.py
│   ├── optimal_replacement.py
│   └── clock_replacement.py
│
├── engine/                          # Simulation engine
│   ├── simulation_engine.py
│   ├── activity_logger.py
│   └── metrics_collector.py
│
├── ui/                              # Console UI
│   ├── console_ui.py
│   ├── gantt_chart.py
│   └── menu_system.py
│
├── tests/                           # Test scenarios
│   ├── test_scenario_1.py           # CPU-bound batch
│   ├── test_scenario_2.py           # Interactive mixed
│   ├── test_scenario_3.py           # Deadlock demo
│   ├── test_scenario_4.py           # Race condition
│   └── test_scenario_5.py           # Memory thrashing
│
└── docs/
    ├── report_generator.py
    └── ANALYSIS_REPORT.md           # Comprehensive documentation
```

## Test Scenarios

### Scenario 1: CPU-Bound Batch
- 10 processes with burst times 100-500ms
- Expected: SJF/SRTF selection by adaptive scheduler

### Scenario 2: Interactive Mixed
- 20 processes with burst times 10-50ms
- Expected: Round Robin/MLFQ selection

### Scenario 3: Deadlock Demo
- 4 processes, 4 resources, circular dependency
- Demonstrates detection and resolution

### Scenario 4: Race Condition
- 5 threads incrementing shared counter
- Shows results WITH and WITHOUT mutex

### Scenario 5: Memory Thrashing
- 20 processes, 10 pages each, 50 frames
- Demonstrates high page fault rate

## Screenshots

### Main Menu
```
╔════════════════════════════════════╗
║   OS SIMULATION SYSTEM - v1.0      ║
╠════════════════════════════════════╣
║ 1. Create Process Manually         ║
║ 2. Auto-Generate Processes         ║
║ 3. Start Simulation                ║
║ 4. View Gantt Chart                ║
║ 5. View Detailed Logs              ║
║ 6. Compare Scheduling Algorithms   ║
║ 7. Demo Race Condition             ║
║ 8. Export Reports                  ║
║ 0. Exit                            ║
╚════════════════════════════════════╝
```

### Process States
- 🔵 NEW: Cyan
- 🟢 READY: Green
- 🟡 RUNNING: Yellow
- 🔴 BLOCKED: Red
- ⚪ TERMINATED: White

## Documentation

See [docs/ANALYSIS_REPORT.md](docs/ANALYSIS_REPORT.md) for comprehensive documentation including:
- Algorithm comparisons
- Deadlock handling mechanisms
- Synchronization analysis
- Memory management analysis
- Test results
- Design decisions

## Requirements

```
rich>=13.0.0
colorama>=0.4.6
```

## License

MIT License

## Author

OS Simulation Team

---

**This is a PURE PYTHON CONSOLE APPLICATION for Ubuntu Terminal - NO GUI**