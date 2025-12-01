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
        estimates['RR'] = PerformanceEstimate(f'RR (q={quantum})', rr_wait, 
                                               lambda: RoundRobinScheduler(quantum))
        
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
        
        # Create scheduler instance
        if callable(selected.scheduler_class):
            try:
                scheduler = selected.scheduler_class()
            except TypeError:
                # It's a lambda returning the scheduler
                scheduler = selected.scheduler_class()
        else:
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
