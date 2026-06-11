import os
from pathlib import Path


def sqlite_test_url(filename: str) -> str:
    original_path = Path(filename)
    db_name = f"{original_path.stem}_{os.getpid()}"
    return f"sqlite:///file:{db_name}?mode=memory&cache=shared&uri=true"
