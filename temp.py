from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual.containers import Horizontal
from core.CPU import *
from core.memory import *
from core.processes import *






class ProcEye(App):

    CSS = """
    #processes { width: 2fr; }
    #cpu { width: 1fr; }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self):
        yield Header()

        self.process_table = DataTable(id="processes")
        self.cpu_usage_table = DataTable(id="cpu")

        yield Horizontal(self.process_table, self.cpu_usage_table)
        yield Footer()

    def on_mount(self):
        self.process_table.add_columns("PID", "Process Name")
        self.cpu_usage_table.add_columns("CPU Core", "Usage %")

        self.process_table.cursor_type = "row"
        self.process_table.zebra_stripes = True

        self.set_interval(2, self.refresh_processes)
        self.set_interval(1, self.refresh_cpu)
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def refresh(self):
        self.process_table.clear()
        proc_data = running_processes()
        for pid, name in proc_data.items():
            self.process_table.add_row(str(pid), str(name))
        self.cpu_usage_table.clear()
        cpu_usages = get_cpu_usage_per_core()
        for cpu_id, usage in cpu_usages.items():
            self.cpu_usage_table.add_row(str(cpu_id), f"{usage:.2f}%")

if __name__ == "__main__":
    app = ProcEye()
    app.run()