from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual.containers import Horizontal, Vertical
from core.CPU import *
from core.memory import *
from core.processes import *


class ProcEye(App):
    """System Monitor."""

    CSS = """

    #cpu_table {
        height: 50%;
        border: solid green;
    }
    
    #proc_table {
        width: 1fr;
        height: 100%;
        border: solid blue;
    }

    #mem_table {
        height: 50%;
        border: solid red;
    }

    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        self.process_table = DataTable(id="proc_table")
        self.cpu_usage_table = DataTable(id="cpu_table")
        self.memory_table = DataTable(id="mem_table")

        yield Horizontal(
            self.process_table,
            
            Vertical(
                self.memory_table,
                self.cpu_usage_table
            )
            
        )
        

    def on_mount(self):
        """Called when the app is mounted."""
        self.process_table.add_columns("process ID", "process Name")
        self.cpu_usage_table.add_columns("CPU Core", "Usage %")
        self.memory_table.add_columns("Metric", "Value")
        self.last_cpu_stats = read_all_cpu_stats()
        self.set_interval(1, self.update_fast_stats)
        self.set_interval(5, self.update_slow_stats)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def update_fast_stats(self):

        """Update CPU usage stats."""
        self.cpu_usage_table.clear()
        current_stats = read_all_cpu_stats()
        for cpu_id in current_stats.keys():
            usage = cpu_usage(cpu_id, self.last_cpu_stats, current_stats)
            self.cpu_usage_table.add_row(cpu_id, f"{usage:.2f}%")
        self.last_cpu_stats = current_stats

        """Update Memory stats."""
        self.memory_table.clear()
        mem_stats = calculate_memory_usage()
        if mem_stats:
            self.memory_table.add_row("Total Memory", f"{mem_stats['MemTotal']:.2f} GB")
            self.memory_table.add_row("Available Memory", f"{mem_stats['MemAvailable']:.2f} GB")
            self.memory_table.add_row("Used Memory", f"{mem_stats['MemUsed']:.2f} GB")
            self.memory_table.add_row("Memory Usage Percentage", f"{mem_stats['MemUsagePercentage']:.2f}%")
        
    def update_slow_stats(self):

        """Update process list."""
        self.process_table.clear()
        proc_data = running_processes()
        for pid, name in proc_data.items():
            self.process_table.add_row(str(pid), str(name))

if __name__ == "__main__":
    app = ProcEye()
    app.run()


