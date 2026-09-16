#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Hop-1 from DA1 PNs and type-LH onto the mAL IDs that make -8810 GABA onto 88 pC1 coexpress.

Not hop-3. Not an Icarus battery.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data-raw"
OUT = ROOT / "data" / "templates"
LOGS = ROOT / "logs"

PARENT_GABA = 8810
PARENT_N_P1 = 88
PARENT_MAL_SHA = "e16856c"
PARENT_SENTENCE_SHA = "41437dc"
SIGN_SHA = "45aa064"

LOCK_SHA = {
    "annotations.feather": "2177e246113e4cfbf1e7772ec37c6da1955ff22e8063d0b1f833101f99a9a3b2",
    "neurotransmitters.feather": "95c9289220663abeb3409f3ad9e5a7f8a53f8093f5139d15502cd08da8879621",
    "edges.feather": "5c536423a62a688e59e7b441f9c04d6272c9a1f017e35814cf561f8c275d9e9e",
}

QUESTION = (
    "Does cVA (DA1 or LH intermediates) synapse onto the mAL IDs "
    "that make the -8810?"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hop_count(w: pd.DataFrame, nt_s: pd.Series, pre: set[int], post: set[int]) -> dict:
    h = w[w["body_pre"].isin(pre) & w["body_post"].isin(post)]
    if h.empty:
        return {
            "n_edges": 0,
            "weight": 0,
            "n_pre": 0,
            "n_post": 0,
            "nt": {},
            "post_ids": [],
            "pre_ids": [],
        }
    nt = h["body_pre"].map(nt_s)
    return {
        "n_edges": int(len(h)),
        "weight": int(h["weight"].sum()),
        "n_pre": int(h["body_pre"].nunique()),
        "n_post": int(h["body_post"].nunique()),
        "nt": {str(k): int(v) for k, v in h.groupby(nt)["weight"].sum().items()},
        "post_ids": sorted(int(x) for x in h["body_post"].unique()),
        "pre_ids": sorted(int(x) for x in h["body_pre"].unique()),
    }


def type_weights(w: pd.DataFrame, type_map: dict[int, str], pre: set[int], post: set[int], n: int = 12) -> list[dict]:
    h = w[w["body_pre"].isin(pre) & w["body_post"].isin(post)]
    if h.empty:
        return []
    s = h.copy()
    s["t"] = s["body_pre"].map(lambda b: type_map.get(int(b), ""))
    rows = []
    for t, wt in s.groupby("t")["weight"].sum().sort_values(ascending=False).head(n).items():
        rows.append({"type": str(t), "weight": int(wt)})
    return rows


def main() -> None:
    for name, expect in LOCK_SHA.items():
        got = sha256(RAW / name)
        if got != expect:
            raise SystemExit(f"{name} sha256 {got} != {expect}")

    ann = pd.read_feather(RAW / "annotations.feather")
    nt = pd.read_feather(RAW / "neurotransmitters.feather").rename(columns={"body": "bodyId"})
    w = pd.read_feather(RAW / "edges.feather")
    type_s = ann["type"].fillna("").astype(str)
    fru = ann["fruDsx"].fillna("").astype(str)
    body = ann["bodyId"].astype("int64")
    nt_s = nt.set_index("bodyId")["consensus_nt"]
    type_map = dict(zip(body.astype(int), type_s))

    p1 = set(body[type_s.str.startswith("pC1_") & fru.str.startswith("coexpress")].astype(int))
    mal = set(body[type_s.str.startswith("mAL")].astype(int))
    da1 = set(body[type_s.isin(["DA1_lPN", "DA1_vPN"])].astype(int))
    lh = set(body[type_s.str.startswith("LH")].astype(int))
    if len(p1) != PARENT_N_P1:
        raise SystemExit(f"P1_coexpress {len(p1)} != {PARENT_N_P1}")

    mal_p1 = w[w["body_pre"].isin(mal) & w["body_post"].isin(p1)].copy()
    mal_p1["nt"] = mal_p1["body_pre"].map(nt_s)
    gaba = mal_p1[mal_p1["nt"].eq("gaba")]
    gaba_sum = int(gaba["weight"].sum())
    if gaba_sum != PARENT_GABA:
        raise SystemExit(f"mAL GABA onto P1 {gaba_sum} != {PARENT_GABA}")
    gaba_by_mal = gaba.groupby(gaba["body_pre"].astype(int))["weight"].sum()
    mal_gaba_ids = set(int(x) for x in gaba_by_mal.index)
    if len(mal_gaba_ids) != 93:
        raise SystemExit(f"n_mal_gaba_pre {len(mal_gaba_ids)} != 93")

    da1_mal = hop_count(w, nt_s, da1, mal_gaba_ids)
    da1_hit = set(da1_mal["post_ids"])
    gaba_from_da1_hit = int(gaba_by_mal.reindex(list(da1_hit)).fillna(0).sum())
    da1_hit_types = [
        {
            "bodyId": bid,
            "type": type_map.get(bid, ""),
            "gaba_onto_p1": int(gaba_by_mal.get(bid, 0)),
        }
        for bid in da1_mal["post_ids"]
    ]

    lh_mal = hop_count(w, nt_s, lh, mal_gaba_ids)
    gaba_from_lh_hit = int(gaba_by_mal.reindex(lh_mal["post_ids"]).fillna(0).sum())

    da1_lh_all = hop_count(w, nt_s, da1, lh)
    lh_hitters = set(lh_mal["pre_ids"])
    da1_lh_hitters = hop_count(w, nt_s, da1, lh_hitters)
    da1_driven_lh = set(da1_lh_hitters["post_ids"])
    via = hop_count(w, nt_s, da1_driven_lh, mal_gaba_ids)
    gaba_via = int(gaba_by_mal.reindex(via["post_ids"]).fillna(0).sum())

    hop_written = "DA1_PN -> type-LH -> mAL_GABA_pre"
    present = bool(gaba_via > 0)
    fold_illegal = not present

    drive = {
        "dataset": "male-cns:v1.0",
        "weights": "significant-only",
        "kind": "hop1_da1_or_lh_onto_mal_gaba_ids",
        "question": QUESTION,
        "P1_definition": "type pC1_* and fruDsx coexpress_*",
        "mAL_definition": "type startswith mAL",
        "mAL_gaba": "pre consensus_nt gaba onto the 88",
        "LH_definition": "type startswith LH",
        "n_P1": len(p1),
        "n_mAL": len(mal),
        "n_DA1_PN": len(da1),
        "n_LH": len(lh),
        "n_LH_types": int(type_s[type_s.str.startswith("LH")].nunique()),
        "n_mal_gaba_pre": len(mal_gaba_ids),
        "mal_gaba_onto_p1": gaba_sum,
        "parent": {
            "repo": "fly_p1_mal",
            "numbers_sha": PARENT_MAL_SHA,
            "sentence_sha": PARENT_SENTENCE_SHA,
            "sign_sha": SIGN_SHA,
        },
        "hops": {
            "DA1_PN_to_mal_gaba_ids": {
                k: da1_mal[k] for k in ("n_edges", "weight", "n_pre", "n_post", "nt")
            },
            "LH_to_mal_gaba_ids": {
                k: lh_mal[k] for k in ("n_edges", "weight", "n_pre", "n_post", "nt")
            },
            "DA1_PN_to_LH": {
                k: da1_lh_all[k] for k in ("n_edges", "weight", "n_pre", "n_post", "nt")
            },
            "DA1_PN_to_LH_that_hit_mal_gaba": {
                k: da1_lh_hitters[k] for k in ("n_edges", "weight", "n_pre", "n_post", "nt")
            },
            "DA1_driven_LH_to_mal_gaba_ids": {
                k: via[k] for k in ("n_edges", "weight", "n_pre", "n_post", "nt")
            },
        },
        "da1_hop1_hit": {
            "cells": da1_hit_types,
            "gaba_onto_p1": gaba_from_da1_hit,
        },
        "lh_hop1_hit": {
            "n_mal_gaba_ids": lh_mal["n_post"],
            "gaba_onto_p1": gaba_from_lh_hit,
        },
        "da1_via_lh": {
            "n_lh_hitters": len(lh_hitters),
            "n_da1_driven_lh_hitters": len(da1_driven_lh),
            "n_mal_gaba_ids": via["n_post"],
            "gaba_onto_p1": gaba_via,
            "top_lh_types": type_weights(w, type_map, da1_driven_lh, mal_gaba_ids),
        },
        "hop": hop_written,
        "present_at_hop2": present,
        "fold_illegal": fold_illegal,
        "gaba_undriven_by_da1_lh": int(gaba_sum - gaba_via),
    }
    lock = {
        "schema": "fly_mal_drive.v1",
        "question": QUESTION,
        "honesty": (
            "Count only. DA1 PNs and type-LH hop-1 onto the 93 mAL GABA "
            "presynapses that make -8810 onto 88 pC1 coexpress. Not hop-3. "
            "Not an Icarus battery. Parent fly_p1_mal @e16856c holds those 8810."
        ),
        "n_P1": len(p1),
        "n_mal_gaba_pre": len(mal_gaba_ids),
        "mal_gaba_onto_p1": gaba_sum,
        "da1_hop1_weight": da1_mal["weight"],
        "da1_hop1_n_post": da1_mal["n_post"],
        "da1_hop1_gaba_onto_p1": gaba_from_da1_hit,
        "lh_hop1_weight": lh_mal["weight"],
        "lh_hop1_n_post": lh_mal["n_post"],
        "da1_driven_lh_n": len(da1_driven_lh),
        "da1_driven_lh_to_mal_weight": via["weight"],
        "da1_driven_lh_n_mal": via["n_post"],
        "da1_driven_lh_gaba_onto_p1": gaba_via,
        "hop": hop_written,
        "present_at_hop2": present,
        "fold_illegal": fold_illegal,
        "drive": drive,
        "parent_female_n": 139255,
        "parent_male_n": 166691,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    (OUT / "drive.json").write_text(json.dumps(drive, indent=2) + "\n", encoding="utf-8")
    (OUT / "provenance.lock.json").write_text(
        json.dumps(
            {
                "kind": "hop1_da1_or_lh_onto_mal_gaba_ids",
                "parent_male": {"map": "MaleCNS v1", "n": 166691, "citation": "Berg et al., Cell 2026"},
                "parent_tree": {
                    "repo": "fly_p1_mal",
                    "numbers_sha": PARENT_MAL_SHA,
                    "sentence_sha": PARENT_SENTENCE_SHA,
                },
                "sha256": LOCK_SHA,
                "extract": True,
                "note": "DA1 or type-LH hop-1 onto mAL GABA IDs that make -8810. Not hop-3.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (LOGS / "drive_s1.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(
        "da1_hop1", da1_mal["weight"], "gaba", gaba_from_da1_hit,
        "lh_hop1", lh_mal["weight"],
        "via_gaba", gaba_via, "hop", hop_written,
        "fold_illegal", fold_illegal,
    )


if __name__ == "__main__":
    main()
