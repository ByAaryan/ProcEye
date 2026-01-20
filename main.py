from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual.containers import Horizontal, Vertical
from core.CPU import *
from core.memory import *
from core.processes import *
from core.network import *


class ProcEye(App):
    """System Monitor."""

    CSS = """


    #network_table {
        height: 30%;
        border: solid orange;
    }

    #cpu_table {
        height: 50%;
        border: solid green;
    }

    #proc_table {
        width: 1fr;
        height: 70%;
        border: solid blue;
    }

    #mem_table {
        height: 50%;
        border: solid red;
    }

    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("m", "sort_by_memory", "Sort Processes by Memory")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        self.process_table = DataTable(id="proc_table")
        self.cpu_usage_table = DataTable(id="cpu_table")
        self.memory_table = DataTable(id="mem_table")
        self.network_table = DataTable(id="network_table")

        yield Horizontal(

            Vertical(
                self.memory_table,
                self.cpu_usage_table,
            ),

            Vertical(
                self.process_table,
                self.network_table,
            ),
        )


    def on_mount(self):
        """Called when the app is mounted."""
        self.process_table.add_columns("process ID", "process Name", "Memory Usage")
        self.cpu_usage_table.add_columns("CPU Core", "Usage %")
        self.memory_table.add_columns("Metric", "Value")
        self.network_table.add_columns("Interface", "RX Speed", "TX Speed")

        self.last_cpu_stats = read_all_cpu_stats()

        self.old_network_stat = network_stat()
        self.sort_by_memory = False
        self.proc_data = {}

        """Initial update of stats."""
        self.update_fast_stats()
        self.update_slow_stats()
        """Schedule periodic updates."""
        self.set_interval(1, self.update_fast_stats)
        self.set_interval(5, self.update_slow_stats)

    def action_sort_by_memory(self) -> None:
        """An action to sort processes by memory usage."""
        if not self.sort_by_memory:
            self.sort_by_memory = True
        else:
            self.sort_by_memory = False
        self.render_process_data()

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
            self.cpu_usage_table.add_row(cpu_id, f"{self.bar(usage)} {usage:.2f}%")
        self.last_cpu_stats = current_stats

        """Update Memory stats."""
        self.memory_table.clear()
        mem_stats = calculate_memory_usage()
        if mem_stats:
            self.memory_table.add_row("Total Memory", f"{mem_stats['MemTotal']:.2f} GB")
            self.memory_table.add_row("Available Memory", f"{mem_stats['MemAvailable']:.2f} GB")
            self.memory_table.add_row("Used Memory", f"{mem_stats['MemUsed']:.2f} GB")
            mem_bar = self.bar(mem_stats['MemUsagePercentage'])
            self.memory_table.add_row("Memory Usage:", f"{mem_bar} {mem_stats['MemUsagePercentage']:.2f}%")

        """Update Network stats."""
        self.network_table.clear()
        new_network_stat = network_stat()
        interval = 1  # seconds
        speeds, total_rx, total_tx = compute_speed(self.old_network_stat, new_network_stat, interval)
        self.network_table.add_row("Total", format_speed(total_rx), format_speed(total_tx))
        for iface, (rx_speed, tx_speed) in speeds.items():
            self.network_table.add_row(iface, format_speed(rx_speed), format_speed(tx_speed))
        self.old_network_stat = new_network_stat

    def bar(self, percent, width=20):
        filled = int((percent / 100) * width)
        empty = width - filled
        return "(" + "#" * filled + "-" * empty + ")"


    def render_process_data(self):
        """Render process data in the table."""
        self.process_table.clear()
        proc_data = self.proc_data
        if self.sort_by_memory:
            proc_data = dict(sorted(proc_data.items(), key=lambda item: item[1][1], reverse=True))
        for pid, (name, memory) in proc_data.items():
            self.process_table.add_row(str(pid), str(name), f"{memory:.2f} MB")



    def update_slow_stats(self):

        """Update process list."""
        self.proc_data = running_processes()
        self.render_process_data()

if __name__ == "__main__":
    app = ProcEye()
    app.run()


