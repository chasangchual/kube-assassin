from __future__ import annotations

from textual.widgets import Static

from data.mock_resources import ContextInfo


class MetadataPanel(Static):
    DEFAULT_CSS = """
    MetadataPanel {
        height: auto;
        width: auto;
        padding: 0 1;
    }
    """

    def __init__(self, ctx: ContextInfo) -> None:
        self._ctx = ctx
        super().__init__(id="metadata-panel")

    def render(self) -> str:
        c = self._ctx
        lines = [
            f"[bold yellow]Context[/]    [white]{c.context}[/]",
            f"[bold yellow]Cluster[/]    [white]{c.cluster}[/]",
            f"[bold yellow]User[/]        [white]{c.user}[/]",
            f"[bold yellow]Namespace[/]  [magenta]{c.namespace}[/]",
            f"[bold yellow]Version[/]     [white]{c.k8s_version}[/]",
            f"[bold yellow]CPU[/]          [green]{c.cpu_usage}[/]  [bold yellow]MEM[/]  [green]{c.mem_usage}[/]",
        ]
        return "\n".join(lines)