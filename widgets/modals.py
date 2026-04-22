from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

from data.mock_resources import PodRow


class HelpModal(ModalScreen[None]):
    DEFAULT_CSS = """
    HelpModal {
        align: center middle;
    }
    HelpModal > Vertical {
        width: 64;
        height: auto;
        max-height: 80%;
        border: round cyan;
        padding: 1 2;
        background: $surface;
    }
    HelpModal .title {
        text-align: center;
        margin-bottom: 1;
    }
    HelpModal .shortcut {
        margin-bottom: 0;
    }
    """

    BINDINGS = [
        ("escape", "close", "Close"),
        ("question_mark", "close", "Close"),
    ]

    SHORTCUTS = [
        ("↑ / ↓", "Move selection"),
        ("PgUp / PgDn", "Scroll page"),
        ("Home / End", "Jump to start/end"),
        ("/", "Filter rows"),
        ("Esc", "Exit filter / close modal"),
        ("?", "This help"),
        ("Enter", "View pod details"),
        ("a", "Show all namespaces"),
        ("d", "Describe selected"),
        ("e", "Edit selected"),
        ("l", "View logs"),
        ("s", "Open shell"),
        ("y", "View YAML"),
        ("q", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("[bold cyan]Keyboard Shortcuts[/]", classes="title")
            lines: list[str] = []
            for key, desc in self.SHORTCUTS:
                lines.append(f"  [bold cyan]{key:<18}[/] [dim]{desc}[/]")
            yield Static("\n".join(lines), classes="shortcut")
            yield Static("\n[dim]Press Esc or ? to close[/]", classes="title")

    def action_close(self) -> None:
        self.dismiss(None)


class DetailModal(ModalScreen[None]):
    DEFAULT_CSS = """
    DetailModal {
        align: center middle;
    }
    DetailModal > Vertical {
        width: 72;
        height: auto;
        max-height: 80%;
        border: round cyan;
        padding: 1 2;
        background: $surface;
    }
    DetailModal .title {
        text-align: center;
        margin-bottom: 1;
    }
    DetailModal .detail-line {
        margin-bottom: 0;
    }
    """

    BINDINGS = [
        ("escape", "close", "Close"),
        ("enter", "close", "Close"),
    ]

    def __init__(self, pod: PodRow) -> None:
        self._pod = pod
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical():
            p = self._pod
            yield Static(f"[bold cyan]Pod Detail[/]", classes="title")
            lines = [
                f"  [bold yellow]Namespace[/]    [white]{p.namespace}[/]",
                f"  [bold yellow]Name[/]        [white]{p.name}[/]",
                f"  [bold yellow]Ready[/]        [white]{p.ready}[/]",
                f"  [bold yellow]Status[/]       [white]{p.status}[/]",
                f"  [bold yellow]Restarts[/]     [white]{p.restarts}[/]",
                f"  [bold yellow]CPU[/]           [white]{p.cpu}[/]",
                f"  [bold yellow]%CPU/R[/]       [white]{p.cpu_pct_r}[/]",
                f"  [bold yellow]%CPU/L[/]       [white]{p.cpu_pct_l}[/]",
                f"  [bold yellow]MEM[/]           [white]{p.mem}[/]",
                f"  [bold yellow]%MEM/R[/]       [white]{p.mem_pct_r}[/]",
                f"  [bold yellow]%MEM/L[/]       [white]{p.mem_pct_l}[/]",
                f"  [bold yellow]IP[/]            [white]{p.ip}[/]",
                f"  [bold yellow]Node[/]          [white]{p.node}[/]",
                f"  [bold yellow]Age[/]           [white]{p.age}[/]",
            ]
            yield Static("\n".join(lines), classes="detail-line")
            yield Static("\n[dim]Press Esc or Enter to close[/]", classes="title")

    def action_close(self) -> None:
        self.dismiss(None)