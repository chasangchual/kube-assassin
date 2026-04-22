from __future__ import annotations

from rich.text import Text
from textual.widgets import DataTable

from data.mock_resources import ALL_COLUMNS, PodRow

RIGHT_ALIGN_COLS = {
    "RESTARTS",
    "CPU",
    "%CPU/R",
    "%CPU/L",
    "MEM",
    "%MEM/R",
    "%MEM/L",
    "AGE",
}

_COL_INDEX = {col: i for i, col in enumerate(ALL_COLUMNS)}


def _status_style(status: str) -> str:
    if status == "Running":
        return "green"
    if status == "Completed":
        return "cyan"
    if status == "Pending":
        return "yellow"
    if status == "CrashLoopBackOff":
        return "bold red"
    return "white"


class ResourceTable(DataTable):
    DEFAULT_CSS = """
    ResourceTable {
        height: 1fr;
        width: 100%;
    }
    """

    def __init__(self) -> None:
        super().__init__(id="resource-table")

    def on_mount(self) -> None:
        self.cursor_type = "row"
        for col in ALL_COLUMNS:
            self.add_column(col, key=col)

    def load_rows(self, rows: list[PodRow]) -> None:
        self.clear(columns=False)
        for row in rows:
            cells = self._row_to_cells(row)
            self.add_row(*cells, key=f"{row.namespace}/{row.name}")

    def _row_to_cells(self, row: PodRow) -> tuple:
        return (
            row.namespace,
            row.name,
            Text(row.pf, style="cyan") if row.pf else "",
            row.ready,
            Text(row.status, style=_status_style(row.status)),
            str(row.restarts),
            row.cpu,
            row.cpu_pct_r,
            row.cpu_pct_l,
            row.mem,
            row.mem_pct_r,
            row.mem_pct_l,
            row.ip,
            row.node,
            row.age,
        )

    def filter_rows(self, rows: list[PodRow], query: str) -> list[PodRow]:
        if not query:
            return rows
        q = query.lower()
        return [
            r
            for r in rows
            if q in r.namespace.lower()
            or q in r.name.lower()
            or q in r.status.lower()
        ]