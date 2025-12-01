#!/usr/bin/env python3
"""Test Scenario 4: Race Condition Demonstration

Demonstrates race conditions with and without mutex protection.
Shows 5 threads each incrementing a shared counter 1000 times.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from synchronization.race_detector import RaceConditionDemo


def test_race_condition():
    """Run race condition demonstration test."""
    console = Console()
    
    console.print(Panel(
        "[bold]Test Scenario 4: Race Condition Demonstration[/bold]\n\n"
        "• 5 threads\n"
        "• Each thread increments a shared counter 1000 times\n"
        "• Expected: 5000 increments total\n\n"
        "Testing both WITH and WITHOUT mutex protection",
        title="Test Configuration",
        border_style="cyan"
    ))
    
    demo = RaceConditionDemo()
    num_threads = 5
    increments = 1000
    
    # Test WITHOUT mutex
    console.print("\n" + "="*60)
    console.print("[bold red]Test 1: WITHOUT Mutex Protection[/bold red]")
    console.print("="*60 + "\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Running threads without mutex...", total=None)
        without_result = demo.run_without_mutex(num_threads, increments)
    
    console.print(Panel(
        f"Running {num_threads} threads, each incrementing shared counter {increments} times...\n\n"
        f"Expected: [bold]{without_result.expected_value}[/bold]\n"
        f"Actual:   [bold]{without_result.actual_value}[/bold]\n\n"
        f"{without_result.message}\n\n"
        f"[dim]Execution time: {without_result.execution_time:.4f}s[/dim]",
        title="WITHOUT Mutex Results",
        border_style="red" if without_result.race_detected else "green"
    ))
    
    # Test WITH mutex
    console.print("\n" + "="*60)
    console.print("[bold green]Test 2: WITH Mutex Protection[/bold green]")
    console.print("="*60 + "\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Running threads with mutex...", total=None)
        with_result = demo.run_with_mutex(num_threads, increments)
    
    console.print(Panel(
        f"Running {num_threads} threads, each incrementing shared counter {increments} times...\n\n"
        f"Expected: [bold]{with_result.expected_value}[/bold]\n"
        f"Actual:   [bold]{with_result.actual_value}[/bold]\n\n"
        f"{with_result.message}\n\n"
        f"[dim]Execution time: {with_result.execution_time:.4f}s[/dim]",
        title="WITH Mutex Results",
        border_style="green" if not with_result.race_detected else "red"
    ))
    
    # Comparison Summary
    console.print("\n" + "="*60)
    console.print("[bold cyan]Summary Comparison[/bold cyan]")
    console.print("="*60 + "\n")
    
    table = Table(box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Without Mutex", style="red")
    table.add_column("With Mutex", style="green")
    
    table.add_row(
        "Expected Value",
        str(without_result.expected_value),
        str(with_result.expected_value)
    )
    table.add_row(
        "Actual Value",
        str(without_result.actual_value),
        str(with_result.actual_value)
    )
    table.add_row(
        "Lost Updates",
        str(without_result.lost_updates),
        str(with_result.lost_updates)
    )
    table.add_row(
        "Race Detected",
        "Yes ❌" if without_result.race_detected else "No ✓",
        "Yes ❌" if with_result.race_detected else "No ✓"
    )
    table.add_row(
        "Data Integrity",
        "Compromised ❌" if without_result.race_detected else "Maintained ✓",
        "Compromised ❌" if with_result.race_detected else "Maintained ✓"
    )
    table.add_row(
        "Execution Time",
        f"{without_result.execution_time:.4f}s",
        f"{with_result.execution_time:.4f}s"
    )
    
    console.print(table)
    
    # Verification
    console.print("\n[bold]Test Verification:[/bold]")
    
    # Without mutex should show race condition (usually)
    if without_result.race_detected:
        console.print("[green]✓ Race condition demonstrated without mutex[/green]")
    else:
        console.print("[yellow]⚠ No race condition in this run (can happen occasionally)[/yellow]")
    
    # With mutex should NEVER show race condition
    if not with_result.race_detected:
        console.print("[green]✓ Mutex successfully prevented race condition[/green]")
        console.print("[bold green]✓ PASS: Test scenario completed successfully[/bold green]")
        return True
    else:
        console.print("[red]✗ FAIL: Race condition occurred even with mutex[/red]")
        return False


def demonstrate_producer_consumer():
    """Demonstrate producer-consumer problem with semaphores."""
    console = Console()
    
    console.print("\n" + "="*60)
    console.print("[bold cyan]Producer-Consumer Problem Demonstration[/bold cyan]")
    console.print("="*60 + "\n")
    
    from synchronization.critical_section import ProducerConsumerProblem
    import threading
    import time
    
    pc = ProducerConsumerProblem(buffer_size=5)
    
    console.print(Panel(
        "• Buffer size: 5\n"
        "• 3 producers, each producing 5 items\n"
        "• 2 consumers, each consuming 7-8 items",
        title="Configuration",
        border_style="cyan"
    ))
    
    # Producer function
    def producer(producer_id, count):
        for i in range(count):
            item = f"Item_{producer_id}_{i}"
            pc.produce(producer_id, item)
            time.sleep(0.1)
    
    # Consumer function
    def consumer(consumer_id, count):
        for i in range(count):
            item = pc.consume(consumer_id)
            time.sleep(0.15)
    
    # Create threads
    threads = []
    
    # 3 producers, each producing 5 items
    for i in range(3):
        t = threading.Thread(target=producer, args=(i+1, 5))
        threads.append(t)
    
    # 2 consumers, each consuming 7-8 items
    for i in range(2):
        t = threading.Thread(target=consumer, args=(i+1, 7 if i == 0 else 8))
        threads.append(t)
    
    console.print("[bold]Running producer-consumer simulation...[/bold]\n")
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Wait for completion
    for t in threads:
        t.join()
    
    # Show results
    status = pc.get_buffer_status()
    
    table = Table(title="Producer-Consumer Results", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")
    
    table.add_row("Buffer Size", str(status['buffer_size']))
    table.add_row("Items in Buffer", str(status['items_in_buffer']))
    table.add_row("Total Produced", str(status['total_produced']))
    table.add_row("Total Consumed", str(status['total_consumed']))
    
    console.print(table)
    
    # Show last 5 events
    console.print("\n[bold]Last 5 Events:[/bold]")
    for event in pc.get_events()[-5:]:
        console.print(f"  {event}")
    
    if status['total_produced'] == 15 and status['total_consumed'] == 15:
        console.print("\n[bold green]✓ Producer-Consumer synchronized correctly![/bold green]")


if __name__ == "__main__":
    success = test_race_condition()
    print()
    demonstrate_producer_consumer()
    sys.exit(0 if success else 1)
