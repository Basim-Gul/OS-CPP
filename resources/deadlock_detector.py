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
