"""Simulation History Tracking for OS simulation."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any


@dataclass
class SimulationRun:
    """Data class to store each simulation run's data."""
    run_number: int
    algorithm: str
    timestamp: datetime
    processes: List[Any]  # List of Process objects
    gantt_data: List[Tuple[int, int, int]]  # (pid, start, end)
    metrics: Dict[str, Any]
    
    def get_process_names(self) -> List[str]:
        """Get list of process names in this run."""
        return [f"P{p.pid}" for p in self.processes]
    
    def get_formatted_timestamp(self) -> str:
        """Get formatted timestamp string."""
        return self.timestamp.strftime("%Y-%m-%d %H:%M")


class SimulationHistory:
    """Tracks all simulation runs."""
    
    def __init__(self):
        self._runs: List[SimulationRun] = []
        self._next_run_number: int = 1
    
    def add_run(self, algorithm: str, processes: List[Any],
                gantt_data: List[Tuple[int, int, int]], 
                metrics: Dict[str, Any]) -> SimulationRun:
        """Add a new simulation run to history.
        
        Args:
            algorithm: Name of the scheduling algorithm used
            processes: List of Process objects from the simulation
            gantt_data: Gantt chart data as list of (pid, start, end) tuples
            metrics: Dictionary containing simulation metrics
            
        Returns:
            The created SimulationRun object
        """
        # Create copies of processes to preserve state at this point
        run = SimulationRun(
            run_number=self._next_run_number,
            algorithm=algorithm,
            timestamp=datetime.now(),
            processes=processes.copy(),
            gantt_data=gantt_data.copy(),
            metrics=metrics.copy()
        )
        self._runs.append(run)
        self._next_run_number += 1
        return run
    
    def get_all_runs(self) -> List[SimulationRun]:
        """Get all simulation runs.
        
        Returns:
            List of all SimulationRun objects
        """
        return self._runs.copy()
    
    def get_run(self, run_number: int) -> Optional[SimulationRun]:
        """Get a specific simulation run by its number.
        
        Args:
            run_number: The run number to retrieve (1-indexed)
            
        Returns:
            The SimulationRun object if found, None otherwise
        """
        for run in self._runs:
            if run.run_number == run_number:
                return run
        return None
    
    def get_latest_run(self) -> Optional[SimulationRun]:
        """Get the most recent simulation run.
        
        Returns:
            The most recent SimulationRun or None if no runs exist
        """
        if self._runs:
            return self._runs[-1]
        return None
    
    def get_run_count(self) -> int:
        """Get the total number of simulation runs.
        
        Returns:
            Number of runs in history
        """
        return len(self._runs)
    
    def clear_history(self) -> None:
        """Clear all simulation history."""
        self._runs.clear()
        self._next_run_number = 1
    
    def has_runs(self) -> bool:
        """Check if there are any runs in history.
        
        Returns:
            True if there are runs, False otherwise
        """
        return len(self._runs) > 0
