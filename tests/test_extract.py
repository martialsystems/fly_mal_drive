# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LOCK = REPO / "logs" / "drive_s1.json"
DRIVE = REPO / "data" / "templates" / "drive.json"
QUESTION = (
    "Does cVA (DA1 or LH intermediates) synapse onto the mAL IDs "
    "that make the -8810?"
)


def test_drive_count_lock() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    assert data["question"] == QUESTION
    assert data["n_P1"] == 88
    assert data["n_mal_gaba_pre"] == 93
    assert data["mal_gaba_onto_p1"] == 8810
    assert data["da1_hop1_weight"] == 45
    assert data["da1_hop1_n_post"] == 1
    assert data["da1_hop1_gaba_onto_p1"] == 3
    assert data["lh_hop1_weight"] == 8148
    assert data["lh_hop1_n_post"] == 93
    assert data["da1_driven_lh_n"] == 161
    assert data["da1_driven_lh_to_mal_weight"] == 3301
    assert data["da1_driven_lh_n_mal"] == 90
    assert data["da1_driven_lh_gaba_onto_p1"] == 8773
    assert data["hop"] == "DA1_PN -> type-LH -> mAL_GABA_pre"
    assert data["present_at_hop2"] is True
    assert data["fold_illegal"] is False
    ext = json.loads(DRIVE.read_text(encoding="utf-8"))
    assert ext["kind"] == "hop1_da1_or_lh_onto_mal_gaba_ids"
    assert ext["da1_hop1_hit"]["cells"][0]["type"] == "mALB1"
    assert ext["da1_via_lh"]["top_lh_types"][0]["type"] == "LHAV4c2"
    assert ext["parent"]["numbers_sha"] == "e16856c"


def test_no_icarus_battery_in_lock() -> None:
    text = LOCK.read_text(encoding="utf-8")
    assert "hd_on_cva_off_ns" not in text
    assert "p1_mal_s1" not in text
