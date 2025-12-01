"""Menu System for OS simulation console UI."""

from typing import Callable, Dict, List, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.text import Text


class MenuItem:
    """A single menu item."""
    
    def __init__(self, key: str, label: str, action: Callable = None,
                 description: str = ""):
        self.key = key
        self.label = label
        self.action = action
        self.description = description


class Menu:
    """A menu with multiple items."""
    
    def __init__(self, title: str, items: List[MenuItem] = None):
        self.title = title
        self.items = items or []
    
    def add_item(self, item: MenuItem) -> None:
        """Add an item to the menu."""
        self.items.append(item)
    
    def get_item(self, key: str) -> Optional[MenuItem]:
        """Get an item by key."""
        for item in self.items:
            if item.key == key:
                return item
        return None


class MenuSystem:
    """Manages menus and navigation."""
    
    def __init__(self):
        self.console = Console()
        self.menus: Dict[str, Menu] = {}
        self.current_menu: Optional[str] = None
        self.history: List[str] = []
        
        self._create_main_menu()
        self._create_submenus()
    
    def _create_main_menu(self) -> None:
        """Create the main menu."""
        main_menu = Menu("OS SIMULATION SYSTEM - v1.0")
        
        main_menu.add_item(MenuItem("1", "Create Process Manually"))
        main_menu.add_item(MenuItem("2", "Auto-Generate Processes"))
        main_menu.add_item(MenuItem("3", "Start Simulation"))
        main_menu.add_item(MenuItem("4", "View Gantt Chart"))
        main_menu.add_item(MenuItem("5", "View Detailed Logs"))
        main_menu.add_item(MenuItem("6", "Compare Scheduling Algorithms"))
        main_menu.add_item(MenuItem("7", "Demo Race Condition"))
        main_menu.add_item(MenuItem("8", "Export Reports"))
        main_menu.add_item(MenuItem("9", "Memory Management"))
        main_menu.add_item(MenuItem("10", "Resource Management"))
        main_menu.add_item(MenuItem("0", "Exit"))
        
        self.menus["main"] = main_menu
    
    def _create_submenus(self) -> None:
        """Create submenus."""
        # Scheduling submenu
        sched_menu = Menu("Scheduling Algorithms")
        sched_menu.add_item(MenuItem("1", "FCFS (First-Come-First-Serve)"))
        sched_menu.add_item(MenuItem("2", "SJF (Shortest Job First)"))
        sched_menu.add_item(MenuItem("3", "SRTF (Shortest Remaining Time First)"))
        sched_menu.add_item(MenuItem("4", "Round Robin"))
        sched_menu.add_item(MenuItem("5", "Priority (Non-Preemptive)"))
        sched_menu.add_item(MenuItem("6", "Priority (Preemptive with Aging)"))
        sched_menu.add_item(MenuItem("7", "MLFQ (Multi-Level Feedback Queue)"))
        sched_menu.add_item(MenuItem("8", "Adaptive Selection"))
        sched_menu.add_item(MenuItem("0", "Back"))
        self.menus["scheduling"] = sched_menu
        
        # Memory submenu
        mem_menu = Menu("Memory Management")
        mem_menu.add_item(MenuItem("1", "View Memory Status"))
        mem_menu.add_item(MenuItem("2", "Set Page Replacement Algorithm"))
        mem_menu.add_item(MenuItem("3", "Simulate Page Access"))
        mem_menu.add_item(MenuItem("4", "Compare Replacement Algorithms"))
        mem_menu.add_item(MenuItem("0", "Back"))
        self.menus["memory"] = mem_menu
        
        # Resource submenu
        res_menu = Menu("Resource Management")
        res_menu.add_item(MenuItem("1", "View Resources"))
        res_menu.add_item(MenuItem("2", "Request Resource"))
        res_menu.add_item(MenuItem("3", "Release Resource"))
        res_menu.add_item(MenuItem("4", "Check Deadlock"))
        res_menu.add_item(MenuItem("5", "View Resource Allocation Graph"))
        res_menu.add_item(MenuItem("6", "Run Banker's Algorithm"))
        res_menu.add_item(MenuItem("0", "Back"))
        self.menus["resources"] = res_menu
        
        # Export submenu
        export_menu = Menu("Export Reports")
        export_menu.add_item(MenuItem("1", "Export Activity Log"))
        export_menu.add_item(MenuItem("2", "Export Gantt Chart"))
        export_menu.add_item(MenuItem("3", "Export Metrics Summary"))
        export_menu.add_item(MenuItem("4", "Generate ANALYSIS_REPORT.md"))
        export_menu.add_item(MenuItem("0", "Back"))
        self.menus["export"] = export_menu
    
    def display_menu(self, menu_name: str = "main") -> None:
        """Display a menu."""
        menu = self.menus.get(menu_name)
        if not menu:
            self.console.print(f"[red]Menu '{menu_name}' not found[/red]")
            return
        
        self.current_menu = menu_name
        
        # Build menu box
        lines = []
        max_len = max(len(item.label) for item in menu.items) + 5
        
        for item in menu.items:
            lines.append(f" {item.key}. {item.label}")
        
        content = "\n".join(lines)
        
        panel = Panel(
            content,
            title=f"[bold cyan]{menu.title}[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print()
        self.console.print(panel)
    
    def get_choice(self, menu_name: str = None) -> str:
        """Get user's menu choice."""
        menu = self.menus.get(menu_name or self.current_menu)
        if not menu:
            return ""
        
        valid_keys = [item.key for item in menu.items]
        
        while True:
            choice = Prompt.ask("\n[bold green]Enter your choice[/bold green]")
            
            if choice in valid_keys:
                return choice
            
            self.console.print(f"[red]Invalid choice. Please enter one of: {', '.join(valid_keys)}[/red]")
    
    def navigate(self, menu_name: str) -> None:
        """Navigate to a menu."""
        if self.current_menu:
            self.history.append(self.current_menu)
        self.current_menu = menu_name
    
    def go_back(self) -> Optional[str]:
        """Go back to previous menu."""
        if self.history:
            self.current_menu = self.history.pop()
            return self.current_menu
        return None
    
    def prompt_int(self, prompt: str, default: int = None,
                   min_val: int = None, max_val: int = None) -> int:
        """Prompt for an integer."""
        while True:
            try:
                value = IntPrompt.ask(
                    f"[bold]{prompt}[/bold]",
                    default=default
                )
                
                if min_val is not None and value < min_val:
                    self.console.print(f"[red]Value must be at least {min_val}[/red]")
                    continue
                
                if max_val is not None and value > max_val:
                    self.console.print(f"[red]Value must be at most {max_val}[/red]")
                    continue
                
                return value
            except Exception:
                self.console.print("[red]Please enter a valid integer[/red]")
    
    def prompt_string(self, prompt: str, default: str = None) -> str:
        """Prompt for a string."""
        return Prompt.ask(f"[bold]{prompt}[/bold]", default=default)
    
    def prompt_confirm(self, prompt: str, default: bool = False) -> bool:
        """Prompt for confirmation."""
        return Confirm.ask(f"[bold]{prompt}[/bold]", default=default)
    
    def prompt_choice(self, prompt: str, choices: List[str]) -> str:
        """Prompt for a choice from a list."""
        self.console.print(f"\n[bold]{prompt}[/bold]")
        for i, choice in enumerate(choices, 1):
            self.console.print(f"  {i}. {choice}")
        
        while True:
            try:
                idx = IntPrompt.ask("Enter number")
                if 1 <= idx <= len(choices):
                    return choices[idx - 1]
                self.console.print(f"[red]Please enter 1-{len(choices)}[/red]")
            except Exception:
                self.console.print("[red]Please enter a valid number[/red]")
    
    def clear_screen(self) -> None:
        """Clear the console."""
        self.console.clear()
    
    def print_header(self, text: str) -> None:
        """Print a section header."""
        self.console.print()
        self.console.print(Panel(text, style="bold cyan"))
    
    def print_success(self, message: str) -> None:
        """Print a success message."""
        self.console.print(f"[bold green]✓ {message}[/bold green]")
    
    def print_error(self, message: str) -> None:
        """Print an error message."""
        self.console.print(f"[bold red]✗ {message}[/bold red]")
    
    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        self.console.print(f"[bold yellow]⚠ {message}[/bold yellow]")
    
    def print_info(self, message: str) -> None:
        """Print an info message."""
        self.console.print(f"[bold blue]ℹ {message}[/bold blue]")
    
    def wait_for_enter(self) -> None:
        """Wait for user to press Enter."""
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
