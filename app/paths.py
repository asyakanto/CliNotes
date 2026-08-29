from pathlib import Path

from app.constants import Constants as C


def data_dir() -> Path:
    return Path.home() / ".local" / "share" / C.DATA_DIR_NAME
