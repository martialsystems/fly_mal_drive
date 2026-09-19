# fly_mal_drive

Does cVA (DA1 or LH intermediates) synapse onto the mAL IDs that make the -8810?

Yes at hop-2. DA1 hop-1 onto the 93 mAL GABA IDs is 45 ACh onto one mALB1 cell, which accounts for 3 of 8810. DA1-driven type-LH synapses onto 90 of those IDs, which account for 8773 of 8810. Hop: `DA1_PN -> type-LH -> mAL_GABA_pre`. `logs/drive_s1.json`.

Parent [fly_p1_mal](https://github.com/martialsystems/fly_p1_mal) `@e16856c` holds the -8810. `@41437dc` holds the sentence that mAL GABA is large enough to pass W_crit if assigned to cVA. This tree is the drive count only.

| hop | weight | onto mAL GABA IDs | GABA those IDs send to the 88 |
|-----|-------:|------------------:|------------------------------:|
| DA1_PN → those IDs | 45 ACh | 1 of 93 | 3 of 8810 |
| type-LH → those IDs | 8148 | 93 of 93 | 8810 of 8810 |
| DA1_PN → type-LH that hit those IDs | 8425 | 161 LH cells | |
| those DA1-driven LH → those IDs | 3301 | 90 of 93 | 8773 of 8810 |

37 of 8810 sit on 3 mAL GABA IDs with no DA1-driven LH hop-1. fold_illegal is false.

DA1-driven LH types onto those IDs, top weights: LHAV4c2 1012, LH007m 814, LH008m 360, LHAV4c1 231. LH definition: type startswith LH (2,028 cells, 422 types). n_P1 = 88. n_mAL = 159.

Female template count: FlyWire 139,255. Male template count: MaleCNS 166,691.

## Methods card

Copied from `METHODS.yaml`.

| Field | Value |
|-------|-------|
| Object | connectome measurement |
| Status | Closed |
| Falsifier | DA1 does not reach those mAL IDs at hop-1 or hop-2 |
| n / seeds | 1 extract |
| Science lock | `de95257` |
| Pre-specified | false |


## How to run

```
.venv/bin/python -m pytest
.venv/bin/python scripts/extract_drive.py
```

Do not overwrite `logs/drive_s1.json` once locked. Do not run Icarus rows in this tree.

## Files

| Path | Role |
|------|------|
| `scripts/extract_drive.py` | The count |
| `data/templates/drive.json` | Raw hop tables |
| `logs/drive_s1.json` | Locked count |
| `METHODS.yaml` | Methods card |
| `CITATION.cff` | Citation file; DOI empty until a deposit exists |
| `AGENTS.md` | Project rules and VBD |
| `NEXT.md` | Closed. Hop written. |
| `THIRD_PARTY.md` | Connectome attribution |

[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)
