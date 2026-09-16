# Agent notes: fly_mal_drive

MIT for original code. FlyWire and MaleCNS remain under their published licenses (typically CC BY 4.0).

Question: Does cVA (DA1 or LH intermediates) synapse onto the mAL IDs that make the -8810?

Count only. Parent `fly_p1_mal` `@e16856c` holds the -8810. `@41437dc` holds that sentence. Do not restamp those logs. Do not run Icarus rows. Do not hop-3.

If drive is missing: fold illegal, `fly_p1_sign` `@45aa064` stands. If present: write the hop and stop.

Verify-before-done is the finish gate. No GraphForge pin on this count tree unless the operator asks.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

Do not use stock `/usr/bin/python3 -m pytest`.
