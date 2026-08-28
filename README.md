# CliNotes

A lightweight, keyboard-driven CLI app for managing notes with **tags**, **archiving**, and **search**. Built with Python and prompt-toolkit.

## Features

- **Create, view, edit, archive & delete** notes
- **Tagging** — auto-extract and manage tags
- **Search** — filter notes with plain queries (press `%h` in search for help)
- **Archiving** — move notes to archive, auto-delete on expiration
- **Settings** — colors, hints, auto-save, notes path, log level and more
- **Easter eggs** just for fun

## Requirements

- **Python** 3.14+
- **uv** (package manager)

## Installation

```sh
git clone https://github.com/asyakanto/CliNotes.git
cd CliNotes
uv tool install .
uv tool update-shell
```

> `uv tool update-shell` adds uv's bin directory (e.g. `~/.local/bin`) to your `PATH` so the `clinotes` command is found. Run it once if prompted.

## Usage

```sh
clinotes
```

Notes and settings are stored as JSON files next to the package (see `storage.py`). The app autosaves on quit.

## Uninstall

```sh
uv tool uninstall clinotes
```

## Development

```sh
uv sync                 # install dev dependencies (mypy, ruff)
uv run ruff check .     # lint
uv run ruff format .    # format
uv run mypy . --strict  # type check
```

## Project structure

```text
app/
  app.py          # NotesApp — business logic
  storage.py      # JSON read/write (atomic saves)
  models.py       # Note dataclass + NoteDict schema
  settings.py     # typed settings
  ui_*.py         # input / display / menus
  cli.py          # entry point
  constants.py    # all magic strings
```

---

CliNotes —  AsyaKanto<3