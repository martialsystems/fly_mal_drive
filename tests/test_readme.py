# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

from fly_mal_drive.claims import scan_text

REPO = Path(__file__).resolve().parents[1]
LOCK = REPO / "logs" / "drive_s1.json"
QUESTION = (
    "Does cVA (DA1 or LH intermediates) synapse onto the mAL IDs "
    "that make the -8810?"
)


def test_readme_question_first() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert text.startswith("# fly_mal_drive\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith(QUESTION)
    assert "Yes at hop-2" in text
    assert "DA1_PN -> type-LH -> mAL_GABA_pre" in text
    assert "8773" in text
    assert "What it is not" not in text
    assert "—" not in text
    assert scan_text(text) == []
    assert "139,255" in text
    assert "166,691" in text
    assert ".venv/bin/python -m pytest" in text
    assert "https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178" in text
    assert "@e16856c" in text
    desc = (REPO / "description.txt").read_text(encoding="utf-8")
    assert QUESTION in desc
    assert "8773" in desc
    assert "—" not in desc
    assert scan_text(desc) == []


def test_lock_numbers_in_readme() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert data["question"] == QUESTION
    assert str(data["da1_hop1_gaba_onto_p1"]) in text
    assert str(data["da1_driven_lh_gaba_onto_p1"]) in text
    assert str(data["mal_gaba_onto_p1"]) in text
    assert data["hop"] in text
    footer = "[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)"
    assert footer in text
    assert "hd_on_cva_off_ns" not in text
    next_text = (REPO / "NEXT.md").read_text(encoding="utf-8")
    assert next_text.startswith("# Next question\n")
    assert "This tree is closed" in next_text
    assert "No Icarus rows" in next_text
    assert scan_text(next_text) == []


def test_methods_card_and_citation() -> None:
    methods = (REPO / "METHODS.yaml").read_text(encoding="utf-8")
    assert "science_lock:" in methods
    assert "pre_specified: false" in methods
    assert "—" not in methods
    assert "What it is not" not in methods
    cite = (REPO / "CITATION.cff").read_text(encoding="utf-8")
    assert "cff-version: 1.2.0" in cite
    assert "Martial Systems LLC" in cite
