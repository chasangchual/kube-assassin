from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static

from data.mock_resources import generate_context, generate_pods
from widgets.action_ribbon import ActionRibbon
from widgets.filter_bar import FilterBar
from widgets.metadata_panel import MetadataPanel
from widgets.modals import DetailModal, HelpModal
from widgets.resource_table import ResourceTable

CSS_PATH = str(Path(__file__).parent / "theme.tcss")


class KubeAssassinApp(App[None]):
    CSS_PATH = CSS_PATH

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("question_mark", "help_screen", "Help", show=False),
        Binding("slash", "start_filter", "Filter", show=False),
        Binding("escape", "close_overlay", "Close", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._ctx = generate_context()
        self._all_pods = generate_pods(60)
        self._filter_active = False

    def compose(self) -> ComposeResult:
        with Horizontal(id="header-zone"):
            yield MetadataPanel(self._ctx)
            yield ActionRibbon()

        with Vertical(id="main-zone"):
            yield ResourceTable()

        yield Static("", id="footer-bar")

    def on_mount(self) -> None:
        table = self.query_one("#resource-table", ResourceTable)
        table.load_rows(self._all_pods)
        table.border_title = f"pods(all)[{len(self._all_pods)}]"
        table.focus()
        self._update_footer()

    def _update_footer(self) -> None:
        footer = self.query_one("#footer-bar", Static)
        mode = "filter" if self._filter_active else "normal"
        footer.update(
            f"  kube-assassin  \u2502  mode:[magenta]{mode}[/]  \u2502  "
            f"ns:[cyan]{self._ctx.namespace}[/]  \u2502  "
            f"pods:[white]{len(self._all_pods)}[/]  \u2502  "
            f"[dim]?=help  q=quit  /=filter[/]"
        )

    # ── actions ──────────────────────────────────────────────────

    def action_help_screen(self) -> None:
        self.push_screen(HelpModal())

    def action_start_filter(self) -> None:
        if self._filter_active:
            return
        self._filter_active = True
        main_zone = self.query_one("#main-zone", Vertical)
        main_zone.mount(FilterBar())
        filter_input = self.query_one("#filter-bar", FilterBar)
        filter_input.focus()
        self._update_footer()

    def action_close_overlay(self) -> None:
        if self._filter_active:
            self._close_filter()
        elif isinstance(self.screen, (HelpModal, DetailModal)):
            self.screen.dismiss(None)

    # ── DataTable row selection (Enter key) ──────────────────────

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if self._filter_active:
            return
        row_key = event.row_key
        key_str = str(row_key.value) if hasattr(row_key, "value") else str(row_key)
        ns = key_str.split("/")[0] if "/" in key_str else ""
        name = key_str.split("/")[1] if "/" in key_str else key_str
        pod = next(
            (p for p in self._all_pods if p.namespace == ns and p.name == name),
            None,
        )
        if pod:
            self.push_screen(DetailModal(pod))

    # ── filter handling ───────────────────────────────────────────

    def on_input_changed(self, event: FilterBar.Changed) -> None:
        if event.input.id != "filter-bar":
            return
        query = event.value.strip()
        table = self.query_one("#resource-table", ResourceTable)
        filtered = table.filter_rows(self._all_pods, query)
        table.load_rows(filtered)
        count = len(filtered) if query else len(self._all_pods)
        table.border_title = f"pods(all)[{count}]"

    def _close_filter(self) -> None:
        self._filter_active = False
        try:
            filter_bar = self.query_one("#filter-bar", FilterBar)
            filter_bar.remove()
        except Exception:
            pass
        table = self.query_one("#resource-table", ResourceTable)
        table.load_rows(self._all_pods)
        table.border_title = f"pods(all)[{len(self._all_pods)}]"
        table.focus()
        self._update_footer()


if __name__ == "__main__":
    app = KubeAssassinApp()
    app.run()