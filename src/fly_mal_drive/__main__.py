# Copyright (c) 2026 Martial Systems LLC
from pathlib import Path
import runpy


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    runpy.run_path(str(root / "scripts" / "extract_drive.py"), run_name="__main__")


if __name__ == "__main__":
    main()
