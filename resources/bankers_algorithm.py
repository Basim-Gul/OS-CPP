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
