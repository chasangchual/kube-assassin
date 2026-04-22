from __future__ import annotations

from textual.widgets import Static

SHORTCUTS = [
    ("a", "All"),
    ("ctrl-d", "Delete"),
    ("d", "Describe"),
    ("e", "Edit"),
    ("l", "Logs"),
    ("shift-f", "Port-Forward"),
    ("s", "Shell"),
    ("y", "YAML"),
    ("/", "Filter"),
    ("?", "Help"),
    ("q", "Quit"),
]


class ActionRibbon(Static):
    DEFAULT_CSS = """
    ActionRibbon {
        height: auto;
        width: 100%;
        padding: 0 1;
        color: $text;
    }
    """

    def render(self) -> str:
        parts: list[str] = []
        for key, label in SHORTCUTS:
            display_key = key.replace("ctrl-", "^").replace("shift-", "⇧")
            parts.append(f"[bold cyan]<{display_key}>[/] [dim]{label}[/]")
        return "  ".join(parts)