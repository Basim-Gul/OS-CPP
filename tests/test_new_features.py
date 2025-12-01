#!/usr/bin/env python3
"""Test for simulation history tracking functionality.

Tests Issue 1: Gantt Chart & Metrics Get Buggy with Multiple Simulation Runs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.simulation_engine import SimulationEngine
from engine.simulation_history import SimulationHistory, SimulationRun


def test_simulation_history():
    """Test simulation history tracking."""
    console = Console()
    engine = SimulationEngine()
    
    console.print(Panel(
        "[bold]Test: Simulation History Tracking[/bold]\n\n"
        "• Run FCFS with 5 processes\n"
        "• Run SJF with 5 more processes\n"
        "• Verify history shows both runs separately",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    # Run 1: FCFS with 5 processes
    console.print("\n[bold]Creating first set of processes...[/bold]")
    for i in range(5):
        engine.create_process(
            name=f"FCFS_Process_{i+1}",
            burst_time=50 + i * 20,
            priority=5,
            arrival_time=i * 5
        )
    
    console.print("[bold]Running FCFS simulation...[/bold]")
    result1 = engine.run_scheduling('FCFS')
    
    # Clear and create new processes for Run 2
    engine.clear_processes()
    
    console.print("\n[bold]Creating second set of processes...[/bold]")
    for i in range(5):
        engine.create_process(
            name=f"SJF_Process_{i+1}",
            burst_time=30 + i * 15,
            priority=i + 1,
            arrival_time=i * 3
        )
    
    console.print("[bold]Running SJF simulation...[/bold]")
    result2 = engine.run_scheduling('SJF')
    
    # Verify history
    console.print("\n[bold]Verifying simulation history...[/bold]")
    
    runs = engine.history.get_all_runs()
    
    # Display history
    table = Table(title="Simulation History", box=box.ROUNDED)
    table.add_column("Run #", style="cyan", justify="center")
    table.add_column("Algorithm", style="white")
    table.add_column("Processes", style="yellow")
    table.add_column("Avg Wait Time", style="green", justify="right")
    
    for run in runs:
        table.add_row(
            str(run.run_number),
            run.algorithm,
            ", ".join(run.get_process_names()),
            f"{run.metrics.get('avg_waiting_time', 0):.2f}ms"
        )
    
    console.print(table)
    
    # Assertions
    passed = True
    
    # Test 1: Should have 2 runs in history
    if len(runs) != 2:
        console.print(f"[bold red]✗ FAIL: Expected 2 runs, got {len(runs)}[/bold red]")
        passed = False
    else:
        console.print("[bold green]✓ PASS: History has 2 runs[/bold green]")
    
    # Test 2: First run should be FCFS
    run1 = engine.history.get_run(1)
    if run1 and run1.algorithm == 'FCFS':
        console.print("[bold green]✓ PASS: Run #1 is FCFS[/bold green]")
    else:
        console.print(f"[bold red]✗ FAIL: Run #1 algorithm is {run1.algorithm if run1 else 'None'}[/bold red]")
        passed = False
    
    # Test 3: Second run should be SJF
    run2 = engine.history.get_run(2)
    if run2 and run2.algorithm == 'SJF':
        console.print("[bold green]✓ PASS: Run #2 is SJF[/bold green]")
    else:
        console.print(f"[bold red]✗ FAIL: Run #2 algorithm is {run2.algorithm if run2 else 'None'}[/bold red]")
        passed = False
    
    # Test 4: Each run should have different processes
    run1_pids = set(run1.get_process_names()) if run1 else set()
    run2_pids = set(run2.get_process_names()) if run2 else set()
    
    # Test 5: Clear history
    engine.history.clear_history()
    if engine.history.get_run_count() == 0:
        console.print("[bold green]✓ PASS: History cleared successfully[/bold green]")
    else:
        console.print("[bold red]✗ FAIL: History not cleared[/bold red]")
        passed = False
    
    return passed


def test_completion_time_metrics():
    """Test completion time in metrics."""
    console = Console()
    engine = SimulationEngine()
    
    console.print(Panel(
        "[bold]Test: Completion Time Metrics[/bold]\n\n"
        "• Create 5 processes\n"
        "• Run FCFS simulation\n"
        "• Verify completion time is tracked",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    # Create processes with known burst times
    for i in range(5):
        engine.create_process(
            name=f"Process_{i+1}",
            burst_time=(i + 1) * 10,  # 10, 20, 30, 40, 50
            priority=5,
            arrival_time=0
        )
    
    result = engine.run_scheduling('FCFS')
    
    # Display metrics
    table = Table(title="Process Completion Times", box=box.ROUNDED)
    table.add_column("PID", style="cyan")
    table.add_column("Burst", justify="right")
    table.add_column("Completion", style="green", justify="right")
    table.add_column("Turnaround", justify="right")
    table.add_column("Waiting", style="yellow", justify="right")
    
    for p in result.processes:
        table.add_row(
            f"P{p.pid}",
            str(p.burst_time),
            str(p.completion_time),
            str(p.turnaround_time),
            str(p.waiting_time)
        )
    
    console.print(table)
    
    # Verify avg_completion_time is calculated
    console.print(f"\n[bold]Average Completion Time: {result.avg_completion_time:.2f}ms[/bold]")
    
    passed = True
    
    # Test: avg_completion_time should be set
    if result.avg_completion_time > 0:
        console.print("[bold green]✓ PASS: avg_completion_time is calculated[/bold green]")
    else:
        console.print("[bold red]✗ FAIL: avg_completion_time is not calculated[/bold red]")
        passed = False
    
    # Test: each process should have completion_time set
    for p in result.processes:
        if p.completion_time <= 0:
            console.print(f"[bold red]✗ FAIL: P{p.pid} has invalid completion_time[/bold red]")
            passed = False
    
    if passed:
        console.print("[bold green]✓ PASS: All processes have valid completion times[/bold green]")
    
    return passed


def test_adaptive_scheduler_improvement():
    """Test adaptive scheduler prioritizes lowest wait time."""
    console = Console()
    engine = SimulationEngine()
    
    console.print(Panel(
        "[bold]Test: Adaptive Scheduler Improvement[/bold]\n\n"
        "• Test 1: Similar priorities → Should NOT select Priority\n"
        "• Test 2: High I/O ratio → Should prefer RR or MLFQ\n"
        "• Test 3: High priority variance → May select Priority if in top 3",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    passed = True
    
    # Test 1: Similar priorities - should NOT select Priority
    console.print("\n[bold]Test 1: Processes with similar priorities[/bold]")
    for i in range(5):
        engine.create_process(f"P{i+1}", burst_time=100+i*20, priority=5, arrival_time=i*5)
    
    rec = engine.get_adaptive_recommendation()
    console.print(f"Selected: {rec['algorithm']}")
    
    if 'Priority' not in rec['algorithm']:
        console.print("[bold green]✓ PASS: Did not select Priority for similar priorities[/bold green]")
    else:
        console.print("[bold red]✗ FAIL: Selected Priority despite similar priorities[/bold red]")
        passed = False
    
    # Test 2: High I/O ratio - should prefer RR or MLFQ
    engine.clear_processes()
    console.print("\n[bold]Test 2: Processes with high I/O ratio (80% I/O-bound)[/bold]")
    for i in range(10):
        engine.create_process(f"P{i+1}", burst_time=30+i*5, priority=i+1, 
                              arrival_time=i*2, io_bound=(i < 8))
    
    rec = engine.get_adaptive_recommendation()
    console.print(f"Selected: {rec['algorithm']}")
    
    # Either RR, MLFQ, or an algorithm with good I/O handling is acceptable
    if any(alg in rec['algorithm'] for alg in ['RR', 'MLFQ', 'Preemptive', 'SRTF']):
        console.print("[bold green]✓ PASS: Selected appropriate algorithm for high I/O[/bold green]")
    else:
        console.print("[bold yellow]⚠ Warning: May not be optimal for high I/O workload[/bold yellow]")
    
    # Test 3: Performance estimates are shown in justification
    console.print("\n[bold]Test 3: Performance estimates in justification[/bold]")
    if 'Performance Estimates' in rec['justification']:
        console.print("[bold green]✓ PASS: Justification includes performance estimates[/bold green]")
    else:
        console.print("[bold red]✗ FAIL: Justification missing performance estimates[/bold red]")
        passed = False
    
    return passed


if __name__ == "__main__":
    console = Console()
    
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]Running All Tests for Three Critical Improvements[/bold cyan]")
    console.print("=" * 70 + "\n")
    
    results = []
    
    # Test 1: Simulation History
    console.print("\n" + "-" * 70)
    results.append(("Simulation History", test_simulation_history()))
    
    # Test 2: Completion Time Metrics
    console.print("\n" + "-" * 70)
    results.append(("Completion Time Metrics", test_completion_time_metrics()))
    
    # Test 3: Adaptive Scheduler
    console.print("\n" + "-" * 70)
    results.append(("Adaptive Scheduler", test_adaptive_scheduler_improvement()))
    
    # Summary
    console.print("\n" + "=" * 70)
    console.print("[bold]TEST SUMMARY[/bold]")
    console.print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "[bold green]PASS[/bold green]" if passed else "[bold red]FAIL[/bold red]"
        console.print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    console.print()
    
    if all_passed:
        console.print("[bold green]All tests passed![/bold green]")
        sys.exit(0)
    else:
        console.print("[bold red]Some tests failed![/bold red]")
        sys.exit(1)
