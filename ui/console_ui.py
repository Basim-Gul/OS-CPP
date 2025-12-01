"""Console UI for OS simulation using Rich library."""

from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

from models.process import Process, ProcessState
from engine.simulation_engine import SimulationEngine
from .gantt_chart import GanttChart
from .menu_system import MenuSystem


class ConsoleUI:
    """Rich console interface for OS simulation."""
    
    def __init__(self):
        self.console = Console()
        self.engine = SimulationEngine()
        self.menu = MenuSystem()
        self.gantt = GanttChart()
        self.running = True
    
    def run(self) -> None:
        """Run the console UI main loop."""
        self.display_welcome()
        
        while self.running:
            try:
                self.menu.display_menu("main")
                choice = self.menu.get_choice()
                self.handle_main_choice(choice)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted. Exiting...[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                self.menu.wait_for_enter()
        
        self.display_goodbye()
    
    def display_welcome(self) -> None:
        """Display welcome banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     ██████╗ ███████╗    ███████╗██╗███╗   ███╗                  ║
║    ██╔═══██╗██╔════╝    ██╔════╝██║████╗ ████║                  ║
║    ██║   ██║███████╗    ███████╗██║██╔████╔██║                  ║
║    ██║   ██║╚════██║    ╚════██║██║██║╚██╔╝██║                  ║
║    ╚██████╔╝███████║    ███████║██║██║ ╚═╝ ██║                  ║
║     ╚═════╝ ╚══════╝    ╚══════╝╚═╝╚═╝     ╚═╝                  ║
║                                                                  ║
║              OS SIMULATION SYSTEM v1.0                           ║
║         Pure Console Application for Ubuntu Terminal             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold cyan")
    
    def display_goodbye(self) -> None:
        """Display goodbye message."""
        self.console.print("\n[bold cyan]Thank you for using OS Simulation System![/bold cyan]")
        self.console.print("[dim]Goodbye![/dim]\n")
    
    def handle_main_choice(self, choice: str) -> None:
        """Handle main menu choice."""
        handlers = {
            "1": self.create_process_manual,
            "2": self.auto_generate_processes,
            "3": self.start_simulation,
            "4": self.view_gantt_chart,
            "5": self.view_logs,
            "6": self.compare_schedulers,
            "7": self.demo_race_condition,
            "8": self.export_menu,
            "9": self.memory_menu,
            "10": self.resource_menu,
            "0": self.exit_program
        }
        
        handler = handlers.get(choice)
        if handler:
            handler()
    
    # ==================== Process Management ====================
    
    def create_process_manual(self) -> None:
        """Create a process manually."""
        self.menu.print_header("Create Process Manually")
        
        name = self.menu.prompt_string("Process name", f"Process_{self.engine.next_pid}")
        burst = self.menu.prompt_int("Burst time (ms)", default=50, min_val=1)
        priority = self.menu.prompt_int("Priority (lower=higher)", default=5, min_val=0, max_val=10)
        arrival = self.menu.prompt_int("Arrival time (ms)", default=0, min_val=0)
        io_bound = self.menu.prompt_confirm("Is I/O bound?", default=False)
        pages = self.menu.prompt_int("Memory pages", default=5, min_val=1, max_val=20)
        
        process = self.engine.create_process(
            name=name,
            burst_time=burst,
            priority=priority,
            arrival_time=arrival,
            io_bound=io_bound,
            memory_pages=pages
        )
        
        self.menu.print_success(f"Created process P{process.pid}")
        self.display_process_table()
        self.menu.wait_for_enter()
    
    def auto_generate_processes(self) -> None:
        """Auto-generate processes."""
        self.menu.print_header("Auto-Generate Processes")
        
        count = self.menu.prompt_int("Number of processes", default=10, min_val=1, max_val=50)
        min_burst = self.menu.prompt_int("Minimum burst time (ms)", default=10, min_val=1)
        max_burst = self.menu.prompt_int("Maximum burst time (ms)", default=200, min_val=min_burst)
        io_ratio = self.menu.prompt_int("I/O bound percentage", default=30, min_val=0, max_val=100) / 100
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("Generating processes...", total=count)
            
            processes = self.engine.auto_generate_processes(
                count=count,
                burst_range=(min_burst, max_burst),
                io_ratio=io_ratio
            )
            
            for _ in range(count):
                progress.update(task, advance=1)
        
        self.menu.print_success(f"Generated {count} processes")
        self.display_process_table()
        self.menu.wait_for_enter()
    
    def display_process_table(self) -> None:
        """Display all processes in a table."""
        if not self.engine.processes:
            self.console.print("[yellow]No processes created yet.[/yellow]")
            return
        
        table = Table(title="Process List", box=box.ROUNDED)
        
        table.add_column("PID", style="cyan", justify="center")
        table.add_column("Name", style="white")
        table.add_column("State", justify="center")
        table.add_column("Burst (ms)", style="yellow", justify="right")
        table.add_column("Priority", style="magenta", justify="center")
        table.add_column("Arrival", style="green", justify="right")
        table.add_column("Type", justify="center")
        
        for p in self.engine.processes:
            state_color = p.get_state_color()
            state_emoji = p.get_state_emoji()
            proc_type = "I/O" if p.io_bound else "CPU"
            
            table.add_row(
                f"P{p.pid}",
                p.name,
                f"[{state_color}]{state_emoji} {p.state.value}[/{state_color}]",
                str(p.burst_time),
                str(p.priority),
                str(p.arrival_time),
                proc_type
            )
        
        self.console.print(table)
    
    # ==================== Simulation ====================
    
    def start_simulation(self) -> None:
        """Start the CPU scheduling simulation."""
        if not self.engine.processes:
            self.menu.print_error("No processes created. Create or generate processes first.")
            self.menu.wait_for_enter()
            return
        
        self.menu.print_header("Start Simulation")
        
        # Show scheduling menu
        self.menu.display_menu("scheduling")
        choice = self.menu.get_choice("scheduling")
        
        if choice == "0":
            return
        
        algorithm_map = {
            "1": "FCFS",
            "2": "SJF",
            "3": "SRTF",
            "4": "RR",
            "5": "Priority",
            "6": "PreemptivePriority",
            "7": "MLFQ",
            "8": None  # Adaptive
        }
        
        algorithm = algorithm_map.get(choice)
        quantum = 20
        
        if choice == "4":  # Round Robin
            quantum = self.menu.prompt_int("Time quantum (ms)", default=20, min_val=1)
        
        # Show adaptive recommendation if selected
        if algorithm is None:
            rec = self.engine.get_adaptive_recommendation()
            self.console.print(Panel(
                f"[bold green]Selected Algorithm: {rec['algorithm']}[/bold green]\n\n"
                f"{rec['justification']}",
                title="Adaptive Scheduler Recommendation",
                border_style="green"
            ))
            self.menu.wait_for_enter()
        
        # Run simulation with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Running simulation...", total=None)
            result = self.engine.run_scheduling(algorithm, quantum=quantum)
        
        self.menu.print_success(f"Simulation completed in {result.total_time}ms")
        
        # Show metrics
        self.display_metrics(result)
        self.menu.wait_for_enter()
    
    def display_metrics(self, result) -> None:
        """Display simulation metrics."""
        table = Table(title="Simulation Metrics", box=box.ROUNDED)
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")
        
        table.add_row("Algorithm", result.algorithm)
        table.add_row("Total Time", f"{result.total_time}ms")
        table.add_row("Context Switches", str(result.context_switches))
        table.add_row("Avg Waiting Time", f"{result.avg_waiting_time:.2f}ms")
        table.add_row("Avg Turnaround Time", f"{result.avg_turnaround_time:.2f}ms")
        table.add_row("Avg Response Time", f"{result.avg_response_time:.2f}ms")
        table.add_row("Avg Completion Time", f"{result.avg_completion_time:.2f}ms")
        table.add_row("CPU Utilization", f"{result.cpu_utilization:.2f}%")
        table.add_row("Throughput", f"{result.throughput:.2f} proc/sec")
        
        self.console.print(table)
        
        # Process details
        proc_table = Table(title="Process Details", box=box.ROUNDED)
        proc_table.add_column("PID", style="cyan")
        proc_table.add_column("Burst", justify="right")
        proc_table.add_column("Completion", style="blue", justify="right")
        proc_table.add_column("Waiting", style="yellow", justify="right")
        proc_table.add_column("Turnaround", style="green", justify="right")
        proc_table.add_column("Response", style="magenta", justify="right")
        
        for p in result.processes:
            proc_table.add_row(
                f"P{p.pid}",
                str(p.burst_time),
                str(p.completion_time),
                str(p.waiting_time),
                str(p.turnaround_time),
                str(p.response_time) if p.response_time >= 0 else "-"
            )
        
        self.console.print(proc_table)
    
    # ==================== Gantt Chart ====================
    
    def view_gantt_chart(self) -> None:
        """View the Gantt chart with sub-menu options."""
        # Check if any simulation data exists (either current or in history)
        has_current = bool(self.engine.get_gantt_chart())
        has_history = self.engine.history.has_runs()
        
        if not has_current and not has_history:
            self.menu.print_error("No simulation data. Run a simulation first.")
            self.menu.wait_for_enter()
            return
        
        while True:
            self.menu.display_menu("gantt")
            choice = self.menu.get_choice("gantt")
            
            if choice == "0":
                break
            elif choice == "1":
                self._view_current_simulation()
            elif choice == "2":
                self._view_all_history()
            elif choice == "3":
                self._view_specific_run()
            elif choice == "4":
                self._clear_history()
    
    def _view_current_simulation(self) -> None:
        """View Gantt chart for current simulation."""
        gantt_data = self.engine.get_gantt_chart()
        
        if not gantt_data:
            self.menu.print_error("No current simulation data. Run a simulation first.")
            self.menu.wait_for_enter()
            return
        
        self.menu.print_header("Current Simulation - Gantt Chart")
        
        # ASCII version
        ascii_chart = self.gantt.generate_ascii(gantt_data)
        self.console.print(ascii_chart)
        
        # Rich version
        self.gantt.generate_rich(gantt_data)
        self.gantt.generate_summary_table(gantt_data, self.engine.processes)
        
        self.menu.wait_for_enter()
    
    def _view_all_history(self) -> None:
        """View Gantt charts for all simulation runs."""
        if not self.engine.history.has_runs():
            self.menu.print_error("No simulation runs in history.")
            self.menu.wait_for_enter()
            return
        
        self.menu.print_header("All Simulation History")
        self.gantt.display_all_runs(self.engine.history)
        self.menu.wait_for_enter()
    
    def _view_specific_run(self) -> None:
        """View Gantt chart for a specific simulation run."""
        if not self.engine.history.has_runs():
            self.menu.print_error("No simulation runs in history.")
            self.menu.wait_for_enter()
            return
        
        # Show available runs
        self.gantt.list_runs(self.engine.history)
        
        run_count = self.engine.history.get_run_count()
        run_number = self.menu.prompt_int(
            "Enter run number to view", 
            default=run_count, 
            min_val=1, 
            max_val=run_count
        )
        
        self.menu.print_header(f"Simulation Run #{run_number}")
        self.gantt.display_single_run(self.engine.history, run_number)
        self.menu.wait_for_enter()
    
    def _clear_history(self) -> None:
        """Clear simulation history."""
        if not self.engine.history.has_runs():
            self.menu.print_warning("No history to clear.")
            self.menu.wait_for_enter()
            return
        
        if self.menu.prompt_confirm("Are you sure you want to clear all simulation history?"):
            self.engine.history.clear_history()
            self.menu.print_success("Simulation history cleared.")
        else:
            self.menu.print_info("History not cleared.")
        
        self.menu.wait_for_enter()
        
        self.menu.wait_for_enter()
    
    # ==================== Logs ====================
    
    def view_logs(self) -> None:
        """View activity logs."""
        events = self.engine.logger.get_events()
        
        if not events:
            self.menu.print_error("No logs available. Run a simulation first.")
            self.menu.wait_for_enter()
            return
        
        self.menu.print_header("Activity Logs")
        
        # Show last 20 events
        table = Table(title=f"Activity Log (Last 20 of {len(events)} events)", box=box.ROUNDED)
        table.add_column("Time (ms)", style="cyan", justify="right")
        table.add_column("Event", style="white")
        
        for event in events[-20:]:
            table.add_row(
                f"{event.timestamp:06d}",
                event.to_string()[12:]  # Remove timestamp prefix
            )
        
        self.console.print(table)
        
        # Summary
        summary = self.engine.logger.get_summary()
        self.console.print("\n[bold]Event Summary:[/bold]")
        for event_type, count in sorted(summary.items()):
            self.console.print(f"  {event_type}: {count}")
        
        self.menu.wait_for_enter()
    
    # ==================== Comparison ====================
    
    def compare_schedulers(self) -> None:
        """Compare all scheduling algorithms."""
        if not self.engine.processes:
            self.menu.print_error("No processes created. Create processes first.")
            self.menu.wait_for_enter()
            return
        
        self.menu.print_header("Scheduling Algorithm Comparison")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Comparing algorithms...", total=None)
            results = self.engine.compare_all_schedulers()
        
        table = Table(title="Algorithm Comparison", box=box.ROUNDED)
        
        table.add_column("Algorithm", style="cyan")
        table.add_column("Avg Wait", style="yellow", justify="right")
        table.add_column("Avg TAT", style="green", justify="right")
        table.add_column("Avg Response", style="magenta", justify="right")
        table.add_column("CPU Util", style="blue", justify="right")
        table.add_column("Ctx Switches", style="red", justify="right")
        
        best_wait = min(r['avg_waiting'] for r in results)
        
        for r in results:
            wait_style = "bold green" if r['avg_waiting'] == best_wait else ""
            
            table.add_row(
                r['algorithm'],
                f"[{wait_style}]{r['avg_waiting']:.2f}ms[/{wait_style}]" if wait_style else f"{r['avg_waiting']:.2f}ms",
                f"{r['avg_turnaround']:.2f}ms",
                f"{r['avg_response']:.2f}ms",
                f"{r['cpu_utilization']:.1f}%",
                str(r['context_switches'])
            )
        
        self.console.print(table)
        
        # Show recommendation
        rec = self.engine.get_adaptive_recommendation()
        self.console.print(Panel(
            f"[bold]Recommended: {rec['algorithm']}[/bold]\n"
            f"{rec['justification']}",
            title="Adaptive Recommendation",
            border_style="green"
        ))
        
        self.menu.wait_for_enter()
    
    # ==================== Race Condition Demo ====================
    
    def demo_race_condition(self) -> None:
        """Demonstrate race conditions."""
        self.menu.print_header("Race Condition Demonstration")
        
        threads = self.menu.prompt_int("Number of threads", default=5, min_val=2, max_val=20)
        increments = self.menu.prompt_int("Increments per thread", default=1000, min_val=100)
        
        self.console.print("\n[bold]Running race condition tests...[/bold]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Testing without mutex...", total=None)
            result = self.engine.run_race_condition_demo(threads, increments)
        
        # Display results
        without = result['without_mutex']
        with_mutex = result['with_mutex']
        
        # Without mutex
        self.console.print(Panel(
            f"Running {threads} threads, each incrementing shared counter {increments} times...\n"
            f"Expected: {without['expected']}\n"
            f"Actual: {without['actual']}\n\n"
            f"{without['message']}",
            title="[bold red]WITHOUT Mutex[/bold red]",
            border_style="red"
        ))
        
        # With mutex
        self.console.print(Panel(
            f"Running {threads} threads, each incrementing shared counter {increments} times...\n"
            f"Expected: {with_mutex['expected']}\n"
            f"Actual: {with_mutex['actual']}\n\n"
            f"{with_mutex['message']}",
            title="[bold green]WITH Mutex[/bold green]",
            border_style="green"
        ))
        
        self.menu.wait_for_enter()
    
    # ==================== Memory Menu ====================
    
    def memory_menu(self) -> None:
        """Memory management submenu."""
        while True:
            self.menu.display_menu("memory")
            choice = self.menu.get_choice("memory")
            
            if choice == "0":
                break
            elif choice == "1":
                self.view_memory_status()
            elif choice == "2":
                self.set_replacement_algorithm()
            elif choice == "3":
                self.simulate_page_access()
            elif choice == "4":
                self.compare_replacement_algorithms()
    
    def view_memory_status(self) -> None:
        """View memory status."""
        status = self.engine.get_memory_status()
        
        table = Table(title="Memory Status", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")
        
        table.add_row("Total Frames", str(status['total_frames']))
        table.add_row("Used Frames", str(status['used_frames']))
        table.add_row("Free Frames", str(status['free_frames']))
        table.add_row("Usage", f"{status['usage_percentage']:.1f}%")
        table.add_row("Page Faults", str(status['page_faults']))
        table.add_row("Fault Rate", f"{status['fault_rate']:.2f}%")
        
        self.console.print(table)
        self.menu.wait_for_enter()
    
    def set_replacement_algorithm(self) -> None:
        """Set page replacement algorithm."""
        algorithms = ['FIFO', 'LRU', 'Optimal', 'Clock']
        choice = self.menu.prompt_choice("Select algorithm", algorithms)
        self.engine.set_replacement_algorithm(choice)
        self.menu.print_success(f"Set replacement algorithm to {choice}")
        self.menu.wait_for_enter()
    
    def simulate_page_access(self) -> None:
        """Simulate page access."""
        if not self.engine.processes:
            self.menu.print_error("No processes. Create processes first.")
            self.menu.wait_for_enter()
            return
        
        pid = self.menu.prompt_int("Process ID", min_val=1)
        page = self.menu.prompt_int("Page ID", min_val=0)
        
        fault, frame = self.engine.access_memory(pid, page)
        
        if fault:
            self.menu.print_warning(f"Page fault! Loaded into frame {frame}")
        else:
            self.menu.print_success(f"Page hit! Found in frame {frame}")
        
        self.menu.wait_for_enter()
    
    def compare_replacement_algorithms(self) -> None:
        """Compare page replacement algorithms."""
        self.menu.print_header("Page Replacement Algorithm Comparison")
        
        # Generate random reference string
        import random
        ref_string = [(1, random.randint(0, 9)) for _ in range(20)]
        
        self.console.print(f"Reference string: {[f'P{p}-pg{pg}' for p, pg in ref_string]}")
        
        results = self.engine.compare_replacement_algorithms(ref_string, num_frames=5)
        
        table = Table(title="Algorithm Comparison (5 frames)", box=box.ROUNDED)
        table.add_column("Algorithm", style="cyan")
        table.add_column("Faults", style="red", justify="right")
        table.add_column("Hits", style="green", justify="right")
        table.add_column("Fault Rate", style="yellow", justify="right")
        
        for r in results:
            table.add_row(
                r['algorithm'],
                str(r['faults']),
                str(r['hits']),
                f"{r['fault_rate']:.1f}%"
            )
        
        self.console.print(table)
        self.menu.wait_for_enter()
    
    # ==================== Resource Menu ====================
    
    def resource_menu(self) -> None:
        """Resource management submenu."""
        while True:
            self.menu.display_menu("resources")
            choice = self.menu.get_choice("resources")
            
            if choice == "0":
                break
            elif choice == "1":
                self.view_resources()
            elif choice == "2":
                self.request_resource()
            elif choice == "3":
                self.release_resource()
            elif choice == "4":
                self.check_deadlock()
            elif choice == "5":
                self.view_rag()
            elif choice == "6":
                self.run_bankers()
    
    def view_resources(self) -> None:
        """View resource status."""
        status = self.engine.resource_manager.get_status()
        
        table = Table(title="System Resources", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Type", style="yellow")
        table.add_column("Available", style="green", justify="center")
        table.add_column("Total", style="blue", justify="center")
        table.add_column("Waiting", style="red", justify="center")
        
        for r in status['resources']:
            table.add_row(
                str(r['id']),
                r['name'],
                r['type'],
                str(r['available']),
                str(r['total']),
                str(len(r['waiting']))
            )
        
        self.console.print(table)
        self.menu.wait_for_enter()
    
    def request_resource(self) -> None:
        """Request a resource."""
        if not self.engine.processes:
            self.menu.print_error("No processes. Create processes first.")
            self.menu.wait_for_enter()
            return
        
        pid = self.menu.prompt_int("Process ID", min_val=1)
        rid = self.menu.prompt_int("Resource ID", min_val=1)
        
        success = self.engine.request_resource(pid, rid)
        
        if success:
            self.menu.print_success(f"Resource R{rid} allocated to P{pid}")
        else:
            self.menu.print_warning(f"P{pid} is waiting for R{rid}")
        
        self.menu.wait_for_enter()
    
    def release_resource(self) -> None:
        """Release a resource."""
        pid = self.menu.prompt_int("Process ID", min_val=1)
        rid = self.menu.prompt_int("Resource ID", min_val=1)
        
        released = self.engine.release_resource(pid, rid)
        
        if released > 0:
            self.menu.print_success(f"Released {released} instance(s) of R{rid} from P{pid}")
        else:
            self.menu.print_error("No resources to release")
        
        self.menu.wait_for_enter()
    
    def check_deadlock(self) -> None:
        """Check for deadlock."""
        result = self.engine.check_deadlock()
        
        if result['detected']:
            self.console.print(Panel(
                f"[bold red]⚠️ DEADLOCK DETECTED![/bold red]\n\n"
                f"Circular Wait Chain: {' → '.join(result['cycle'])}\n"
                f"Processes in Deadlock: {result['processes']}\n"
                f"Resources Involved: {result['resources']}",
                title="Deadlock Alert",
                border_style="red"
            ))
            
            if self.menu.prompt_confirm("Resolve deadlock?"):
                method = self.menu.prompt_choice(
                    "Resolution method",
                    ["termination", "preemption"]
                )
                resolve_result = self.engine.resolve_deadlock(method)
                if resolve_result and resolve_result['success']:
                    self.menu.print_success(resolve_result['message'])
        else:
            self.menu.print_success("No deadlock detected. System is in safe state.")
        
        self.menu.wait_for_enter()
    
    def view_rag(self) -> None:
        """View Resource Allocation Graph."""
        self.menu.print_header("Resource Allocation Graph")
        ascii_graph = self.engine.rag.to_ascii()
        self.console.print(ascii_graph)
        self.menu.wait_for_enter()
    
    def run_bankers(self) -> None:
        """Run Banker's Algorithm."""
        result = self.engine.bankers.is_safe()
        
        state_color = "green" if result.is_safe else "red"
        state_text = "SAFE" if result.is_safe else "UNSAFE"
        
        self.console.print(Panel(
            f"[bold {state_color}]System State: {state_text}[/bold {state_color}]\n\n"
            f"{result.message}",
            title="Banker's Algorithm",
            border_style=state_color
        ))
        
        self.menu.wait_for_enter()
    
    # ==================== Export Menu ====================
    
    def export_menu(self) -> None:
        """Export reports submenu."""
        while True:
            self.menu.display_menu("export")
            choice = self.menu.get_choice("export")
            
            if choice == "0":
                break
            elif choice == "1":
                self.export_logs()
            elif choice == "2":
                self.export_gantt()
            elif choice == "3":
                self.export_metrics()
            elif choice == "4":
                self.generate_analysis_report()
    
    def export_logs(self) -> None:
        """Export activity logs."""
        filename = self.menu.prompt_string("Filename", "simulation_log.txt")
        self.engine.export_logs(filename)
        self.menu.print_success(f"Logs exported to {filename}")
        self.menu.wait_for_enter()
    
    def export_gantt(self) -> None:
        """Export Gantt chart."""
        gantt_data = self.engine.get_gantt_chart()
        if not gantt_data:
            self.menu.print_error("No Gantt data. Run simulation first.")
            self.menu.wait_for_enter()
            return
        
        filename = self.menu.prompt_string("Filename", "gantt_chart.txt")
        self.gantt.save_to_file(gantt_data, filename)
        self.menu.print_success(f"Gantt chart exported to {filename}")
        self.menu.wait_for_enter()
    
    def export_metrics(self) -> None:
        """Export metrics summary."""
        summary = self.engine.get_metrics_summary()
        filename = self.menu.prompt_string("Filename", "metrics_summary.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        self.menu.print_success(f"Metrics exported to {filename}")
        self.menu.wait_for_enter()
    
    def generate_analysis_report(self) -> None:
        """Generate ANALYSIS_REPORT.md."""
        from docs.report_generator import generate_analysis_report
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task("Generating report...", total=None)
            generate_analysis_report(self.engine)
        
        self.menu.print_success("Generated docs/ANALYSIS_REPORT.md")
        self.menu.wait_for_enter()
    
    def exit_program(self) -> None:
        """Exit the program."""
        if self.menu.prompt_confirm("Are you sure you want to exit?"):
            self.running = False
