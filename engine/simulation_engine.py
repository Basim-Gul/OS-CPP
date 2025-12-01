"""Simulation Engine - Main orchestrator for OS simulation."""

from typing import List, Dict, Optional, Tuple
import random
import time

from models.process import Process, ProcessState
from models.resource import Resource, ResourceType
from scheduling import (
    BaseScheduler, SchedulingResult,
    FCFSScheduler, SJFScheduler, SRTFScheduler, RoundRobinScheduler,
    PriorityScheduler, PreemptivePriorityScheduler, MLFQScheduler,
    AdaptiveSelector
)
from resources import (
    ResourceManager, ResourceAllocationGraph,
    DeadlockDetector, BankersAlgorithm, DeadlockResolver
)
from synchronization import SyncManager, RaceConditionDemo
from memory import (
    MemoryManager,
    FIFOReplacement, LRUReplacement, OptimalReplacement, ClockReplacement
)
from .activity_logger import ActivityLogger, EventType
from .metrics_collector import MetricsCollector
from .simulation_history import SimulationHistory


class SimulationEngine:
    """Main orchestrator for the OS simulation."""
    
    # Constants for process auto-generation
    DEFAULT_ARRIVAL_SPREAD = 20
    DEFAULT_MIN_PAGES = 3
    DEFAULT_MAX_PAGES = 10
    
    def __init__(self, num_frames: int = 50):
        # Process management
        self.processes: List[Process] = []
        self.next_pid = 1
        
        # Scheduling
        self.scheduler: Optional[BaseScheduler] = None
        self.adaptive_selector = AdaptiveSelector()
        self.last_result: Optional[SchedulingResult] = None
        
        # Resource management
        self.resource_manager = ResourceManager()
        self.rag = ResourceAllocationGraph()
        self.deadlock_detector = DeadlockDetector(self.rag)
        self.bankers = BankersAlgorithm()
        self.deadlock_resolver: Optional[DeadlockResolver] = None
        
        # Synchronization
        self.sync_manager = SyncManager()
        self.race_demo = RaceConditionDemo()
        
        # Memory management
        self.memory_manager = MemoryManager(num_frames=num_frames)
        self.replacement_algorithms = {
            'FIFO': FIFOReplacement(),
            'LRU': LRUReplacement(),
            'Optimal': OptimalReplacement(),
            'Clock': ClockReplacement()
        }
        self.current_replacement = 'FIFO'
        
        # Logging and metrics
        self.logger = ActivityLogger()
        self.metrics = MetricsCollector()
        
        # Simulation history tracking
        self.history = SimulationHistory()
        
        # Simulation state
        self.current_time = 0
        self.is_running = False
        
        self._init_resolver()
    
    def _init_resolver(self) -> None:
        """Initialize the deadlock resolver."""
        self.deadlock_resolver = DeadlockResolver(
            self.resource_manager, self.rag, self.deadlock_detector
        )
    
    # ==================== Process Management ====================
    
    def create_process(self, name: str, burst_time: int, priority: int = 0,
                       arrival_time: int = 0, io_bound: bool = False,
                       memory_pages: int = 5) -> Process:
        """Create a new process."""
        process = Process(
            pid=self.next_pid,
            name=name,
            burst_time=burst_time,
            priority=priority,
            arrival_time=arrival_time,
            io_bound=io_bound,
            memory_pages=memory_pages
        )
        self.next_pid += 1
        self.processes.append(process)
        
        # Register with subsystems
        self.resource_manager.register_process(process)
        self.memory_manager.register_process(process)
        self.rag.add_process(process.pid, process.name)
        
        # Log the creation
        self.logger.log_process_created(
            process.pid, process.name, burst_time, priority
        )
        
        return process
    
    def auto_generate_processes(self, count: int, 
                                 burst_range: Tuple[int, int] = (10, 200),
                                 priority_range: Tuple[int, int] = (1, 10),
                                 io_ratio: float = 0.3) -> List[Process]:
        """Auto-generate random processes."""
        processes = []
        current_arrival = 0
        
        for i in range(count):
            name = f"Process_{i+1}"
            burst = random.randint(*burst_range)
            priority = random.randint(*priority_range)
            arrival = current_arrival
            current_arrival += random.randint(0, self.DEFAULT_ARRIVAL_SPREAD)
            io_bound = random.random() < io_ratio
            pages = random.randint(self.DEFAULT_MIN_PAGES, self.DEFAULT_MAX_PAGES)
            
            process = self.create_process(
                name=name,
                burst_time=burst,
                priority=priority,
                arrival_time=arrival,
                io_bound=io_bound,
                memory_pages=pages
            )
            processes.append(process)
        
        return processes
    
    def get_process(self, pid: int) -> Optional[Process]:
        """Get a process by PID."""
        for p in self.processes:
            if p.pid == pid:
                return p
        return None
    
    def remove_process(self, pid: int) -> bool:
        """Remove a process."""
        process = self.get_process(pid)
        if process:
            self.processes.remove(process)
            self.resource_manager.unregister_process(pid)
            self.memory_manager.unregister_process(pid)
            self.rag.remove_process(pid)
            return True
        return False
    
    def clear_processes(self) -> None:
        """Clear all processes."""
        for p in self.processes:
            self.resource_manager.unregister_process(p.pid)
            self.memory_manager.unregister_process(p.pid)
            self.rag.remove_process(p.pid)
        self.processes.clear()
        self.next_pid = 1
    
    # ==================== Scheduling ====================
    
    def set_scheduler(self, scheduler: BaseScheduler) -> None:
        """Set the scheduling algorithm."""
        self.scheduler = scheduler
    
    def get_scheduler_by_name(self, name: str, **kwargs) -> BaseScheduler:
        """Get a scheduler instance by name."""
        schedulers = {
            'FCFS': FCFSScheduler,
            'SJF': SJFScheduler,
            'SRTF': SRTFScheduler,
            'RR': lambda: RoundRobinScheduler(kwargs.get('quantum', 20)),
            'Priority': PriorityScheduler,
            'PreemptivePriority': PreemptivePriorityScheduler,
            'MLFQ': MLFQScheduler
        }
        
        scheduler_class = schedulers.get(name)
        if scheduler_class:
            return scheduler_class()
        return FCFSScheduler()
    
    def run_scheduling(self, algorithm: str = None, **kwargs) -> SchedulingResult:
        """Run scheduling simulation."""
        if not self.processes:
            return SchedulingResult(
                algorithm="None",
                processes=[],
                gantt_chart=[],
                context_switches=0,
                total_time=0
            )
        
        # Reset processes for simulation
        for p in self.processes:
            p.reset()
        
        # Get or create scheduler
        if algorithm:
            self.scheduler = self.get_scheduler_by_name(algorithm, **kwargs)
        elif self.scheduler is None:
            recommendation = self.adaptive_selector.select_scheduler(self.processes)
            self.scheduler = recommendation.scheduler
        
        # Log simulation start
        self.logger.log_simulation_start()
        
        # Run scheduling
        self.last_result = self.scheduler.schedule(self.processes.copy())
        
        # Record metrics
        self.metrics.set_algorithm(self.last_result.algorithm)
        self.metrics.record_processes(self.processes)
        self.metrics.set_total_time(self.last_result.total_time)
        self.metrics.context_switches = self.last_result.context_switches
        
        # Add to simulation history
        self.history.add_run(
            algorithm=self.last_result.algorithm,
            processes=self.last_result.processes,
            gantt_data=self.last_result.gantt_chart,
            metrics={
                'avg_waiting_time': self.last_result.avg_waiting_time,
                'avg_turnaround_time': self.last_result.avg_turnaround_time,
                'avg_response_time': self.last_result.avg_response_time,
                'avg_completion_time': self.last_result.avg_completion_time,
                'cpu_utilization': self.last_result.cpu_utilization,
                'throughput': self.last_result.throughput,
                'context_switches': self.last_result.context_switches,
                'total_time': self.last_result.total_time
            }
        )
        
        # Log simulation end
        self.logger.log_simulation_end(self.last_result.total_time)
        
        return self.last_result
    
    def get_adaptive_recommendation(self) -> Dict:
        """Get adaptive scheduler recommendation."""
        if not self.processes:
            return {'algorithm': 'None', 'justification': 'No processes'}
        
        recommendation = self.adaptive_selector.select_scheduler(self.processes)
        return {
            'algorithm': recommendation.algorithm_name,
            'justification': recommendation.justification,
            'expected_wait': recommendation.expected_avg_wait,
            'confidence': recommendation.confidence
        }
    
    def compare_all_schedulers(self) -> List[Dict]:
        """Compare all scheduling algorithms."""
        results = []
        
        for name, scheduler_class in [
            ('FCFS', FCFSScheduler),
            ('SJF', SJFScheduler),
            ('SRTF', SRTFScheduler),
            ('RR (q=20)', lambda: RoundRobinScheduler(20)),
            ('Priority', PriorityScheduler),
            ('Preemptive Priority', PreemptivePriorityScheduler),
            ('MLFQ', MLFQScheduler)
        ]:
            # Reset processes
            for p in self.processes:
                p.reset()
            
            scheduler = scheduler_class()
            result = scheduler.schedule(self.processes.copy())
            
            results.append({
                'algorithm': name,
                'avg_waiting': result.avg_waiting_time,
                'avg_turnaround': result.avg_turnaround_time,
                'avg_response': result.avg_response_time,
                'cpu_utilization': result.cpu_utilization,
                'context_switches': result.context_switches
            })
        
        return results
    
    # ==================== Resource Management ====================
    
    def request_resource(self, pid: int, rid: int, count: int = 1) -> bool:
        """Request a resource for a process."""
        success = self.resource_manager.request(pid, rid, count)
        
        if success:
            self.rag.add_assignment_edge(rid, pid, count, self.current_time)
        else:
            self.rag.add_request_edge(pid, rid, count, self.current_time)
        
        return success
    
    def release_resource(self, pid: int, rid: int, count: int = None) -> int:
        """Release a resource from a process."""
        released = self.resource_manager.release(pid, rid, count)
        
        if released > 0:
            self.rag.remove_assignment_edge(rid, pid, released)
        
        return released
    
    def check_deadlock(self) -> Optional[Dict]:
        """Check for deadlock and return info if found."""
        self.deadlock_detector.set_time(self.current_time)
        deadlock = self.deadlock_detector.detect()
        
        if deadlock:
            self.logger.log_deadlock_detected(
                deadlock.processes, deadlock.resources, deadlock.cycle
            )
            self.metrics.record_deadlock(resolved=False)
            
            return {
                'detected': True,
                'timestamp': deadlock.timestamp,
                'processes': deadlock.processes,
                'resources': deadlock.resources,
                'cycle': deadlock.cycle
            }
        
        return {'detected': False}
    
    def resolve_deadlock(self, method: str = 'termination') -> Optional[Dict]:
        """Resolve a detected deadlock."""
        deadlock = self.deadlock_detector.detect()
        
        if not deadlock:
            return None
        
        if method == 'termination':
            result = self.deadlock_resolver.resolve_by_termination(deadlock)
        else:
            result = self.deadlock_resolver.resolve_by_preemption(deadlock)
        
        if result.success:
            self.logger.log_deadlock_resolved(method, result.victim_pid)
            self.metrics.record_deadlock(resolved=True)
        
        return {
            'success': result.success,
            'method': result.method.value,
            'victim': result.victim_pid,
            'resources_released': result.resources_released,
            'message': result.message
        }
    
    def check_safe_state(self, pid: int, request: Dict[int, int]) -> Tuple[bool, str]:
        """Check if a request would leave system in safe state (Banker's)."""
        return self.bankers.request_resources(pid, request)
    
    # ==================== Memory Management ====================
    
    def set_replacement_algorithm(self, name: str) -> None:
        """Set the page replacement algorithm."""
        if name in self.replacement_algorithms:
            self.current_replacement = name
            self.memory_manager.set_replacement_algorithm(
                self.replacement_algorithms[name]
            )
    
    def access_memory(self, pid: int, page_id: int, 
                      write: bool = False) -> Tuple[bool, Optional[int]]:
        """Access a memory page."""
        self.memory_manager.set_time(self.current_time)
        fault, frame = self.memory_manager.access_page(pid, page_id, write)
        
        if fault:
            self.metrics.record_page_fault()
        self.metrics.record_memory_access()
        
        return fault, frame
    
    def get_memory_status(self) -> Dict:
        """Get memory status."""
        return self.memory_manager.get_memory_usage()
    
    def compare_replacement_algorithms(self, 
                                        reference_string: List[Tuple[int, int]],
                                        num_frames: int = 10) -> List[Dict]:
        """Compare all page replacement algorithms."""
        results = []
        
        for name, algo in self.replacement_algorithms.items():
            result = algo.simulate(reference_string, num_frames)
            results.append({
                'algorithm': name,
                'faults': result['faults'],
                'hits': result['hits'],
                'fault_rate': result['fault_rate']
            })
        
        return results
    
    # ==================== Synchronization ====================
    
    def run_race_condition_demo(self, threads: int = 5, 
                                 increments: int = 1000) -> Dict:
        """Run race condition demonstration."""
        without, with_mutex = self.race_demo.run_full_demo(threads, increments)
        
        return {
            'without_mutex': {
                'expected': without.expected_value,
                'actual': without.actual_value,
                'race_detected': without.race_detected,
                'lost_updates': without.lost_updates,
                'message': without.message
            },
            'with_mutex': {
                'expected': with_mutex.expected_value,
                'actual': with_mutex.actual_value,
                'race_detected': with_mutex.race_detected,
                'lost_updates': with_mutex.lost_updates,
                'message': with_mutex.message
            }
        }
    
    def create_mutex(self, name: str) -> None:
        """Create a mutex."""
        self.sync_manager.create_mutex(name)
    
    def create_semaphore(self, name: str, count: int = 1) -> None:
        """Create a semaphore."""
        self.sync_manager.create_semaphore(name, count)
    
    # ==================== Utility ====================
    
    def advance_time(self, delta: int) -> None:
        """Advance simulation time."""
        self.current_time += delta
        self.logger.set_time(self.current_time)
        self.sync_manager.set_time(self.current_time)
        self.resource_manager.set_time(self.current_time)
    
    def get_gantt_chart(self) -> List[Tuple[int, int, int]]:
        """Get the Gantt chart from last scheduling run."""
        if self.last_result:
            return self.last_result.gantt_chart
        return []
    
    def export_logs(self, filename: str = "simulation_log.txt") -> None:
        """Export activity logs to file."""
        self.logger.export_to_file(filename)
    
    def get_metrics_summary(self) -> str:
        """Get metrics summary string."""
        return self.metrics.get_summary_string()
    
    def reset(self) -> None:
        """Reset the entire simulation."""
        self.clear_processes()
        self.scheduler = None
        self.last_result = None
        
        self.resource_manager.reset()
        self.rag.reset()
        self.deadlock_detector.reset()
        self.bankers.reset()
        
        self.sync_manager.reset()
        self.race_demo.reset()
        
        self.memory_manager.reset()
        for algo in self.replacement_algorithms.values():
            algo.reset()
        
        self.logger.clear()
        self.metrics.reset()
        
        self.current_time = 0
        self.is_running = False
        
        self._init_resolver()
