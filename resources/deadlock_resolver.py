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
