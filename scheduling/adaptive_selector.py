"""Adaptive Scheduler Selector for OS simulation."""

from typing import List, Tuple, Optional, Type
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


class AdaptiveSelector:
    """Intelligent scheduler selector based on workload analysis."""
    
    # Constants for Round Robin quantum calculation
    MIN_TIME_QUANTUM = 10
    MAX_TIME_QUANTUM = 50
    QUANTUM_DIVISOR = 5
    
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
    
    def select_scheduler(self, processes: List[Process]) -> SchedulerRecommendation:
        """Select the best scheduling algorithm based on workload analysis."""
        analysis = self.analyze_workload(processes)
        
        # Decision tree for scheduler selection
        if analysis.process_count == 0:
            return SchedulerRecommendation(
                scheduler=FCFSScheduler(),
                algorithm_name="FCFS",
                justification="No processes to schedule. FCFS selected as default.",
                expected_avg_wait=0,
                confidence=1.0
            )
        
        # 1. Check for batch workload first (high burst, low I/O)
        if analysis.is_batch:
            if analysis.coefficient_of_variation < 0.3:
                return self._recommend_fcfs(analysis)
            else:
                return self._recommend_sjf(analysis)
        
        # 2. Check for interactive workload (low burst, high I/O)
        if analysis.is_interactive:
            if analysis.process_count > 15:
                return self._recommend_mlfq(analysis)
            else:
                return self._recommend_round_robin(analysis)
        
        # 3. ONLY use priority if variance is VERY high (>6) AND range is wide (>7)
        if analysis.priority_variance > 6 and analysis.priority_range > 7:
            if analysis.is_interactive or analysis.io_bound_ratio > 0.3:
                return self._recommend_preemptive_priority(analysis)
            else:
                return self._recommend_priority(analysis)
        
        # Mixed workload - use CV to decide
        if analysis.coefficient_of_variation > 0.5:
            # High variance in burst times -> SRTF is optimal
            return self._recommend_srtf(analysis)
        elif analysis.coefficient_of_variation > 0.3:
            # Moderate variance -> SJF works well
            return self._recommend_sjf(analysis)
        elif analysis.process_count > 10:
            # Many processes with similar burst times -> Round Robin
            return self._recommend_round_robin(analysis)
        else:
            # Simple workload -> FCFS is sufficient
            return self._recommend_fcfs(analysis)
    
    def _recommend_fcfs(self, analysis: WorkloadAnalysis) -> SchedulerRecommendation:
        expected_wait = analysis.avg_burst_time * (analysis.process_count - 1) / 2
        return SchedulerRecommendation(
            scheduler=FCFSScheduler(),
            algorithm_name="FCFS",
            justification=(
                f"Low burst time variance (CV={analysis.coefficient_of_variation:.2f}) with "
                f"{analysis.process_count} processes. FCFS provides simplicity and fairness "
                f"with minimal overhead. Expected avg wait time: {expected_wait:.0f}ms"
            ),
            expected_avg_wait=expected_wait,
            confidence=0.75
        )
    
    def _recommend_sjf(self, analysis: WorkloadAnalysis) -> SchedulerRecommendation:
        # Approximate expected wait (SJF is optimal for non-preemptive)
        expected_wait = analysis.avg_burst_time * (analysis.process_count - 1) / 3
        return SchedulerRecommendation(
            scheduler=SJFScheduler(),
            algorithm_name="SJF",
            justification=(
                f"Moderate burst variance (CV={analysis.coefficient_of_variation:.2f}) with "
                f"{analysis.process_count} processes. SJF minimizes average waiting time "
                f"for non-preemptive scheduling. Expected avg wait time: {expected_wait:.0f}ms"
            ),
            expected_avg_wait=expected_wait,
            confidence=0.85
        )
    
    def _recommend_srtf(self, analysis: WorkloadAnalysis) -> SchedulerRecommendation:
        expected_wait = analysis.avg_burst_time * (analysis.process_count - 1) / 4
        return SchedulerRecommendation(
            scheduler=SRTFScheduler(),
            algorithm_name="SRTF",
            justification=(
                f"Moderate burst variance (CV={analysis.coefficient_of_variation:.2f}) with "
                f"{analysis.process_count} processes. SRTF provides optimal response time "
                f"for interactive workloads while maintaining efficiency. "
                f"Expected avg wait time: {expected_wait:.0f}ms"
            ),
            expected_avg_wait=expected_wait,
            confidence=0.90
        )
    
    def _recommend_round_robin(self, analysis: WorkloadAnalysis) -> SchedulerRecommendation:
        # Choose time quantum based on average burst time
        quantum = max(self.MIN_TIME_QUANTUM, int(analysis.avg_burst_time / self.QUANTUM_DIVISOR))
        quantum = min(quantum, self.MAX_TIME_QUANTUM)
        
        expected_wait = analysis.avg_burst_time * analysis.process_count / 2
        return SchedulerRecommendation(
            scheduler=RoundRobinScheduler(time_quantum=quantum),
            algorithm_name=f"Round Robin (q={quantum})",
            justification=(
                f"Interactive workload detected with {analysis.process_count} processes "
                f"and {analysis.io_bound_ratio*100:.0f}% I/O-bound processes. "
                f"Round Robin ensures fair CPU time distribution and good response time. "
                f"Time quantum set to {quantum}ms. Expected avg wait time: {expected_wait:.0f}ms"
            ),
            expected_avg_wait=expected_wait,
            confidence=0.80
        )
    
    def _recommend_priority(self, analysis: WorkloadAnalysis) -> SchedulerRecommendation:
        expected_wait = analysis.avg_burst_time * (analysis.process_count - 1) / 3
        return SchedulerRecommendation(
            scheduler=PriorityScheduler(),
            algorithm_name="Priority",
            justification=(
                f"High priority variance (range={analysis.priority_range}) detected with "
                f"{analysis.process_count} processes. Priority scheduling ensures "
                f"critical processes are handled first. Expected avg wait time: {expected_wait:.0f}ms"
            ),
            expected_avg_wait=expected_wait,
            confidence=0.75
        )
    
    def _recommend_preemptive_priority(self, analysis: WorkloadAnalysis) -> SchedulerRecommendation:
        expected_wait = analysis.avg_burst_time * (analysis.process_count - 1) / 4
        return SchedulerRecommendation(
            scheduler=PreemptivePriorityScheduler(),
            algorithm_name="Preemptive Priority with Aging",
            justification=(
                f"High priority variance (range={analysis.priority_range}) with interactive "
                f"workload ({analysis.io_bound_ratio*100:.0f}% I/O-bound). Preemptive priority "
                f"with aging prevents starvation while ensuring critical processes run first. "
                f"Expected avg wait time: {expected_wait:.0f}ms"
            ),
            expected_avg_wait=expected_wait,
            confidence=0.85
        )
    
    def _recommend_mlfq(self, analysis: WorkloadAnalysis) -> SchedulerRecommendation:
        expected_wait = analysis.avg_burst_time * analysis.process_count / 3
        return SchedulerRecommendation(
            scheduler=MLFQScheduler(),
            algorithm_name="MLFQ",
            justification=(
                f"Mixed interactive workload with {analysis.process_count} processes. "
                f"MLFQ automatically adapts to process behavior, favoring short/interactive "
                f"processes while preventing starvation of longer ones. "
                f"Expected avg wait time: {expected_wait:.0f}ms"
            ),
            expected_avg_wait=expected_wait,
            confidence=0.85
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
