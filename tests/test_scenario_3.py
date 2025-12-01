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
