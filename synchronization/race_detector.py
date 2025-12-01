"""Race Condition Demonstration for OS simulation."""

from typing import List, Tuple
from dataclasses import dataclass
import threading
import time


@dataclass
class RaceConditionResult:
    """Result of a race condition test."""
    test_type: str  # 'without_mutex' or 'with_mutex'
    num_threads: int
    increments_per_thread: int
    expected_value: int
    actual_value: int
    race_detected: bool
    lost_updates: int
    message: str
    execution_time: float


class SharedCounter:
    """A shared counter for demonstrating race conditions."""
    
    def __init__(self):
        self.value = 0
        self.mutex = threading.Lock()
        self.operations = 0
    
    def increment_unsafe(self) -> None:
        """Increment without synchronization (race condition)."""
        # Simulating read-modify-write with explicit steps
        current = self.value
        # Small delay to increase chance of race condition
        time.sleep(0.0001)
        self.value = current + 1
        self.operations += 1
    
    def increment_safe(self) -> None:
        """Increment with mutex protection (thread-safe)."""
        with self.mutex:
            current = self.value
            time.sleep(0.0001)
            self.value = current + 1
            self.operations += 1
    
    def reset(self) -> None:
        """Reset the counter."""
        self.value = 0
        self.operations = 0


class RaceConditionDemo:
    """Demonstrates race conditions with and without synchronization."""
    
    def __init__(self):
        self.results: List[RaceConditionResult] = []
    
    def run_without_mutex(self, num_threads: int = 5, 
                          increments: int = 1000) -> RaceConditionResult:
        """Run race condition demo WITHOUT mutex protection.
        
        This should demonstrate lost updates due to race conditions.
        """
        counter = SharedCounter()
        threads: List[threading.Thread] = []
        
        expected = num_threads * increments
        start_time = time.time()
        
        # Create worker threads
        def worker():
            for _ in range(increments):
                counter.increment_unsafe()
        
        # Start threads
        for i in range(num_threads):
            t = threading.Thread(target=worker, name=f"Thread-{i+1}")
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        execution_time = time.time() - start_time
        actual = counter.value
        race_detected = actual != expected
        lost = expected - actual
        
        if race_detected:
            message = f"❌ Race condition occurred! Lost {lost} increments"
        else:
            message = "✅ No race condition (unlikely with proper test)"
        
        result = RaceConditionResult(
            test_type='without_mutex',
            num_threads=num_threads,
            increments_per_thread=increments,
            expected_value=expected,
            actual_value=actual,
            race_detected=race_detected,
            lost_updates=lost,
            message=message,
            execution_time=execution_time
        )
        
        self.results.append(result)
        return result
    
    def run_with_mutex(self, num_threads: int = 5, 
                       increments: int = 1000) -> RaceConditionResult:
        """Run race condition demo WITH mutex protection.
        
        This should demonstrate how mutex prevents race conditions.
        """
        counter = SharedCounter()
        threads: List[threading.Thread] = []
        
        expected = num_threads * increments
        start_time = time.time()
        
        # Create worker threads
        def worker():
            for _ in range(increments):
                counter.increment_safe()
        
        # Start threads
        for i in range(num_threads):
            t = threading.Thread(target=worker, name=f"Thread-{i+1}")
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        execution_time = time.time() - start_time
        actual = counter.value
        race_detected = actual != expected
        lost = expected - actual
        
        if race_detected:
            message = f"❌ Unexpected race condition! Lost {lost} increments"
        else:
            message = "✅ Mutex prevented race condition! Data integrity maintained."
        
        result = RaceConditionResult(
            test_type='with_mutex',
            num_threads=num_threads,
            increments_per_thread=increments,
            expected_value=expected,
            actual_value=actual,
            race_detected=race_detected,
            lost_updates=lost,
            message=message,
            execution_time=execution_time
        )
        
        self.results.append(result)
        return result
    
    def run_full_demo(self, num_threads: int = 5,
                      increments: int = 1000) -> Tuple[RaceConditionResult, RaceConditionResult]:
        """Run both demos and return results."""
        without_result = self.run_without_mutex(num_threads, increments)
        with_result = self.run_with_mutex(num_threads, increments)
        return without_result, with_result
    
    def format_result(self, result: RaceConditionResult) -> str:
        """Format a result for display."""
        lines = [
            f"{'='*60}",
            f"Race Condition Test: {'WITHOUT' if result.test_type == 'without_mutex' else 'WITH'} Mutex",
            f"{'='*60}",
            f"Running {result.num_threads} threads, each incrementing shared counter {result.increments_per_thread} times...",
            f"Expected: {result.expected_value}",
            f"Actual:   {result.actual_value}",
            f"",
            result.message,
            f"",
            f"Execution time: {result.execution_time:.4f}s"
        ]
        return "\n".join(lines)
    
    def format_comparison(self, without: RaceConditionResult, 
                          with_mutex: RaceConditionResult) -> str:
        """Format comparison of both results."""
        lines = [
            "",
            "╔════════════════════════════════════════════════════════════╗",
            "║              RACE CONDITION DEMONSTRATION                   ║",
            "╠════════════════════════════════════════════════════════════╣",
            "",
            f"Configuration: {without.num_threads} threads × {without.increments_per_thread} increments",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "WITHOUT Mutex:",
            f"  Expected: {without.expected_value}",
            f"  Actual:   {without.actual_value}",
            f"  {without.message}",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "WITH Mutex:",
            f"  Expected: {with_mutex.expected_value}",
            f"  Actual:   {with_mutex.actual_value}",
            f"  {with_mutex.message}",
            "",
            "╚════════════════════════════════════════════════════════════╝"
        ]
        return "\n".join(lines)
    
    def get_results(self) -> List[RaceConditionResult]:
        """Get all test results."""
        return self.results
    
    def reset(self) -> None:
        """Reset results."""
        self.results.clear()
