from __future__ import annotations

from textual.widgets import Input


class FilterBar(Input):
    DEFAULT_CSS = """
    FilterBar {
        dock: top;
        width: 100%;
        height: 3;
        padding: 0 1;
        border: round cyan;
        background: $surface;
    }
    """

    def __init__(self) -> None:
        super().__init__(
            placeholder="Filter by namespace / name / status... (Esc to close)",
            id="filter-bar",
        )