"""Path helpers: resolve the application data directory."""

from pathlib import Path

from app.constants import Constants


def data_dir() -> Path:
    """Return the directory where application data is stored."""
    return Path.home() / ".local" / "share" / Constants.DATA_DIR_NAME
