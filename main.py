#!/usr/bin/env python3
"""
OS Simulation System - Main Entry Point

A comprehensive Python-based OS simulation for Ubuntu terminal.
Pure console application with beautiful text-based UI using Rich library.

Usage:
    python3 main.py          - Start the interactive simulation
    python3 main.py --test   - Run all test scenarios
    python3 main.py --help   - Show help message

Author: OS Simulation Team
Version: 1.0
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def show_help():
    """Display help message."""
    help_text = """
╔══════════════════════════════════════════════════════════════════╗
║                    OS SIMULATION SYSTEM                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Usage:                                                          ║
║    python3 main.py              Start interactive simulation     ║
║    python3 main.py --test       Run all test scenarios           ║
║    python3 main.py --test N     Run specific test (1-5)          ║
║    python3 main.py --help       Show this help message           ║
║                                                                  ║
║  Test Scenarios:                                                 ║
║    1. CPU-Bound Batch Processing                                 ║
║    2. Interactive Mixed Workload                                 ║
║    3. Deadlock Detection and Resolution                          ║
║    4. Race Condition Demonstration                               ║
║    5. Memory Thrashing                                           ║
║                                                                  ║
║  Features:                                                       ║
║    • 7 CPU Scheduling Algorithms                                 ║
║    • Adaptive Scheduler Selection                                ║
║    • Deadlock Detection (DFS Cycle Detection)                    ║
║    • Banker's Algorithm for Deadlock Prevention                  ║
║    • Mutex and Semaphore Synchronization                         ║
║    • Race Condition Demonstration                                ║
║    • 4 Page Replacement Algorithms                               ║
║    • Complete Activity Logging                                   ║
║    • Gantt Chart Visualization                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def run_tests(test_num=None):
    """Run test scenarios."""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    tests = [
        ("CPU-Bound Batch", "tests.test_scenario_1", "test_cpu_bound_batch"),
        ("Interactive Mixed", "tests.test_scenario_2", "test_interactive_mixed"),
        ("Deadlock Demo", "tests.test_scenario_3", "test_deadlock_demo"),
        ("Race Condition", "tests.test_scenario_4", "test_race_condition"),
        ("Memory Thrashing", "tests.test_scenario_5", "test_memory_thrashing"),
    ]
    
    if test_num is not None:
        if 1 <= test_num <= 5:
            tests = [tests[test_num - 1]]
        else:
            console.print(f"[red]Invalid test number: {test_num}. Must be 1-5.[/red]")
            return False
    
    console.print(Panel(
        "[bold cyan]OS Simulation Test Suite[/bold cyan]",
        border_style="cyan"
    ))
    
    results = []
    
    for name, module_name, func_name in tests:
        console.print(f"\n[bold]Running: {name}[/bold]")
        console.print("=" * 60)
        
        try:
            import importlib
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            success = func()
            results.append((name, success))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            results.append((name, False))
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold]Test Summary[/bold]")
    console.print("=" * 60)
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    for name, success in results:
        status = "[green]✓ PASS[/green]" if success else "[red]✗ FAIL[/red]"
        console.print(f"  {name}: {status}")
    
    console.print(f"\n[bold]Results: {passed}/{total} tests passed[/bold]")
    
    return passed == total


def main():
    """Main entry point."""
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        show_help()
        return 0
    
    if "--test" in args:
        # Find test number if specified
        test_num = None
        test_idx = args.index("--test")
        if test_idx + 1 < len(args):
            try:
                test_num = int(args[test_idx + 1])
            except ValueError:
                pass
        
        success = run_tests(test_num)
        return 0 if success else 1
    
    # Run interactive UI
    try:
        from ui.console_ui import ConsoleUI
        
        ui = ConsoleUI()
        ui.run()
        return 0
    
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return 1
    except KeyboardInterrupt:
        print("\nExiting...")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
