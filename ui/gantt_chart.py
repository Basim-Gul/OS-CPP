"""ASCII Gantt Chart generator for OS simulation."""

from typing import List, Tuple, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class GanttChart:
    """Generates ASCII Gantt charts for CPU scheduling visualization."""
    
    def __init__(self):
        self.console = Console()
        self.colors = [
            "red", "green", "blue", "yellow", "magenta", "cyan",
            "bright_red", "bright_green", "bright_blue", "bright_yellow"
        ]
    
    def generate_ascii(self, gantt_data: List[Tuple[int, int, int]], 
                       scale: int = 2) -> str:
        """Generate ASCII Gantt chart.
        
        Args:
            gantt_data: List of (pid, start_time, end_time)
            scale: Time units per character
            
        Returns:
            ASCII string representation
        """
        if not gantt_data:
            return "No scheduling data available."
        
        lines = []
        max_time = max(end for _, _, end in gantt_data)
        
        # Header
        lines.append("=" * 70)
        lines.append("                         GANTT CHART")
        lines.append("=" * 70)
        lines.append("")
        
        # Time axis header
        time_header = "Time: "
        for t in range(0, max_time + 1, scale * 5):
            time_header += f"{t:<10}"
        lines.append(time_header)
        lines.append("-" * 70)
        
        # Process bars
        pids = sorted(set(pid for pid, _, _ in gantt_data))
        
        for pid in pids:
            # Find all slots for this process
            slots = [(s, e) for p, s, e in gantt_data if p == pid]
            
            # Create bar
            bar = [" "] * ((max_time // scale) + 1)
            for start, end in slots:
                for t in range(start // scale, (end // scale)):
                    if t < len(bar):
                        bar[t] = "█"
            
            line = f"P{pid:2d}: |{''.join(bar)}|"
            lines.append(line)
        
        lines.append("-" * 70)
        
        # Timeline representation
        timeline = "     |"
        prev_end = 0
        for pid, start, end in gantt_data:
            if start > prev_end:
                # Idle time
                idle_width = (start - prev_end) // scale
                timeline += " " * idle_width
            
            width = max(1, (end - start) // scale)
            label = f"P{pid}"
            if width >= len(label):
                timeline += label.center(width)
            else:
                timeline += label[:width]
            prev_end = end
        
        timeline += "|"
        lines.append("     " + "-" * (len(timeline) - 5))
        lines.append(timeline)
        
        # Time markers
        markers = "     |"
        prev_end = 0
        for pid, start, end in gantt_data:
            if start > prev_end:
                idle_width = (start - prev_end) // scale
                markers += " " * idle_width
            
            width = max(1, (end - start) // scale)
            if width >= 2:
                markers += str(start).ljust(width)
            else:
                markers += str(start)[:width]
            prev_end = end
        markers += str(max_time)
        lines.append(markers)
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_rich(self, gantt_data: List[Tuple[int, int, int]]) -> None:
        """Generate and print Rich-formatted Gantt chart."""
        if not gantt_data:
            self.console.print("[yellow]No scheduling data available.[/yellow]")
            return
        
        max_time = max(end for _, _, end in gantt_data)
        
        # Create table
        table = Table(title="CPU Scheduling Gantt Chart", expand=True)
        table.add_column("Process", style="cyan", width=10)
        table.add_column("Execution Timeline", style="white")
        table.add_column("Total Time", style="green", width=12)
        
        # Get unique PIDs
        pids = sorted(set(pid for pid, _, _ in gantt_data))
        pid_colors = {pid: self.colors[i % len(self.colors)] for i, pid in enumerate(pids)}
        
        for pid in pids:
            slots = [(s, e) for p, s, e in gantt_data if p == pid]
            total_time = sum(e - s for s, e in slots)
            
            # Create visual bar
            bar = self._create_bar(slots, max_time, pid_colors[pid])
            
            table.add_row(
                f"P{pid}",
                bar,
                f"{total_time}ms"
            )
        
        self.console.print(table)
        
        # Time scale
        self._print_time_scale(max_time)
        
        # Detailed timeline
        self._print_detailed_timeline(gantt_data)
    
    def _create_bar(self, slots: List[Tuple[int, int]], max_time: int, 
                    color: str) -> Text:
        """Create a colored bar for a process."""
        bar_width = 50
        scale = max_time / bar_width if max_time > 0 else 1
        
        bar = Text()
        last_pos = 0
        
        for start, end in slots:
            start_pos = int(start / scale)
            end_pos = int(end / scale)
            
            # Idle gap
            if start_pos > last_pos:
                bar.append("─" * (start_pos - last_pos), style="dim")
            
            # Execution block
            block_width = max(1, end_pos - start_pos)
            bar.append("█" * block_width, style=color)
            last_pos = end_pos
        
        # Trailing space
        if last_pos < bar_width:
            bar.append("─" * (bar_width - last_pos), style="dim")
        
        return bar
    
    def _print_time_scale(self, max_time: int) -> None:
        """Print time scale."""
        bar_width = 50
        
        scale_line = "        "
        step = max(1, max_time // 10)
        
        for i in range(0, max_time + 1, step):
            pos = int(i / max_time * bar_width) if max_time > 0 else 0
            scale_line = scale_line[:8 + pos] + f"{i}" + scale_line[8 + pos + len(str(i)):]
        
        scale_line = scale_line[:8 + bar_width + 5]
        self.console.print(f"[dim]{scale_line}[/dim]")
        self.console.print(f"[dim]        Time (ms)[/dim]")
    
    def _print_detailed_timeline(self, gantt_data: List[Tuple[int, int, int]]) -> None:
        """Print detailed timeline."""
        self.console.print()
        self.console.print(Panel("Execution Sequence", style="bold cyan"))
        
        sequence = []
        for pid, start, end in gantt_data:
            sequence.append(f"[bold]P{pid}[/bold]({start}-{end})")
        
        self.console.print(" → ".join(sequence))
    
    def generate_summary_table(self, gantt_data: List[Tuple[int, int, int]],
                               processes: List = None) -> None:
        """Generate summary table with process metrics."""
        if not gantt_data:
            return
        
        table = Table(title="Process Execution Summary")
        
        table.add_column("PID", style="cyan")
        table.add_column("Start", style="green")
        table.add_column("End", style="red")
        table.add_column("Duration", style="yellow")
        table.add_column("Wait Time", style="magenta")
        table.add_column("Turnaround", style="blue")
        
        # Group by PID
        pid_data: Dict[int, List[Tuple[int, int]]] = {}
        for pid, start, end in gantt_data:
            if pid not in pid_data:
                pid_data[pid] = []
            pid_data[pid].append((start, end))
        
        for pid in sorted(pid_data.keys()):
            slots = pid_data[pid]
            first_start = min(s for s, _ in slots)
            last_end = max(e for _, e in slots)
            total_duration = sum(e - s for s, e in slots)
            
            # Calculate wait time (if process data available)
            wait_time = "-"
            turnaround = "-"
            if processes:
                for p in processes:
                    if p.pid == pid:
                        wait_time = str(p.waiting_time)
                        turnaround = str(p.turnaround_time)
                        break
            
            table.add_row(
                f"P{pid}",
                str(first_start),
                str(last_end),
                str(total_duration),
                wait_time,
                turnaround
            )
        
        self.console.print(table)
    
    def save_to_file(self, gantt_data: List[Tuple[int, int, int]], 
                     filename: str = "gantt_chart.txt") -> None:
        """Save Gantt chart to file."""
        ascii_chart = self.generate_ascii(gantt_data)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(ascii_chart)
