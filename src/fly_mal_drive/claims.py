# Copyright (c) 2026 Martial Systems LLC
"""Fail closed on banned claim tokens."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

BANNED: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("unique_brains", re.compile(r"unique reconstructed|1,?000 unique", re.I)),
    (
        "population_spike",
        re.compile(
            r"(default|population).{0,40}(full[- ]cns|139k|167k|166k).{0,20}spike|"
            r"live (whole-cns|139k|167k|166k) LIF",
            re.I,
        ),
    ),
    ("grown_connectome", re.compile(r"grew a (new )?connectome|grown connectome", re.I)),
    ("parent_f_restamp", re.compile(r"F = 0\.524|IBD F = 0\.524", re.I)),
    ("unfreeze_licensed", re.compile(r"unfreeze is licensed", re.I)),
    ("icarus_rows", re.compile(r"hd_on_cva_off_ns", re.I)),
    ("hop3_finding", re.compile(r"\bhop-3\b.{0,40}\b(finding|result|drive)\b", re.I)),
)


class ClaimBanError(RuntimeError):
    pass


def scan_text(text: str) -> list[str]:
    return [name for name, pat in BANNED if pat.search(text or "")]


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")
    if "—" in (text or ""):
        raise ClaimBanError(f"{source}: em dash")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))
