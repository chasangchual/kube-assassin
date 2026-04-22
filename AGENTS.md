# kube-assassin

## Toolchain

- **Package manager**: uv
- **Python**: 3.11+ (pinned in `.python-version`)
- Run: `uv run python app.py`
- Sync deps: `uv sync`
- Add deps: `uv add <package>`
- **Framework**: Textual (TUI)

## Project structure

```
app.py                  # App shell, keybindings, layout composition
theme.tcss              # Textual CSS (dark theme, cyan borders)
data/
  mock_resources.py     # Mock data generator (PodRow, ContextInfo)
widgets/
  metadata_panel.py    # Top-left key/value info block
  action_ribbon.py     # Keyboard shortcut strip
  resource_table.py    # Main DataTable (15 cols, color-coded statuses)
  filter_bar.py        # "/" filter input (docked overlay)
  modals.py            # HelpModal, DetailModal
```

## Architecture

Three-section vertical layout (k9s-style):
1. **Top** — horizontal header: metadata panel (left) + action ribbon (right)
2. **Middle** — bordered DataTable with 15 columns, fills remaining space
3. **Bottom** — one-line status bar (mode, namespace, pod count)

Key interactions:
- `q` quit · `/` filter · `?` help · `Enter` detail modal · `Esc` close overlays
- Arrow keys / PgUp/PgDn / Home/End navigate the table natively
- Filter input does live substring match on namespace/name/status

## Style conventions

- Dark background, cyan borders, yellow labels, magenta accents
- STATUS column: green=Running, cyan=Completed, yellow=Pending, red=CrashLoopBackOff
- Textual CSS in `theme.tcss` — no inline style hacks in Python