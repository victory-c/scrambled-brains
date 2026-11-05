#!/usr/bin/env python3
"""Build site/data.json from the fly-brain results folder (the simulator repo keeps the raw runs).

    python3 tools/export_data.py [~/flybrain/fly_brain/results]

gate     results/gate/v<V0>_s<SEED>/cem.json             the balance gate on the real wiring (R0)
rides    results/rungs/<TAG>/[<READOUT>/]v<V0>_s<SEED>/cem.json   the same search on a rewired brain or another readout
pretest  results/rungs/pretest_<RUNG>[_b<BRAINS>]_w<SCALE>.json    transmission pre-test; 8 brains unless _b<N>
Riding time is `upright_mean` (mean seconds upright over the riders of a generation).
"""
import datetime
import json
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "~/flybrain/fly_brain/results").expanduser()
OUT = Path(__file__).resolve().parents[1] / "site" / "data.json"
PT_KEYS = ["network_spikes_per_s", "network_active", "outputs_z3", "max_abs_z", "null_outputs_z3_mean",
           "null_outputs_z3_max", "null_max_abs_z"]


def run(path):
    d = json.loads(path.read_text())
    c, h = d["config"], d["history"]
    return {"v0": c["v0"], "seed": c["seed"], "gens": len(h), "riders": c["riders"], "seconds": c["seconds"],
            "gust": c["gust"], "wall_h": round(d["wall_seconds"] / 3600, 2), "device": d.get("device", "cuda"),
            "readout": c.get("readout", "lane"), "w_syn_scale": c.get("w_syn_scale"),
            "history": [[r["gen"], round(r["upright_mean"], 2), round(r["upright_best_rider"], 2),
                         round(r["finish_frac"], 3)] for r in h]}


def r2(v):
    return round(v, 2) if isinstance(v, float) else v


data = {"generated": datetime.date.today().isoformat(), "gate": {}, "rides": {}, "pretest": {}}
for p in sorted((SRC / "gate").glob("v*_s*/cem.json")):
    g = run(p)
    for k in ("device", "readout", "w_syn_scale"):
        g.pop(k)
    data["gate"][p.parent.name] = g
for p in sorted((SRC / "rungs").glob("**/v*_s*/cem.json")):
    rel = p.parent.relative_to(SRC / "rungs").parts  # (tag, [readout], v_s)
    data["rides"]["/".join(rel)] = {"tag": rel[0], "variant": rel[1] if len(rel) == 3 else "lane", **run(p)}
for p in sorted((SRC / "rungs").glob("pretest_*.json")):
    m = re.fullmatch(r"pretest_(.+?)(_b(\d+))?_w([\d.]+)\.json", p.name)
    if not m:
        continue
    d = json.loads(p.read_text())
    key = m.group(1) + (m.group(2) or "")
    cell = {}
    for pop, row in d["pops"].items():
        cell[pop] = {k: r2(row[k]) for k in PT_KEYS}
        if m.group(3):
            cell[pop].update(brains=d["brains"], null_splits=row.get("null_splits"),
                             null_outputs_z3_p95=row.get("null_outputs_z3_p95"))
    data["pretest"].setdefault(key, {})[f"{float(m.group(4)):g}"] = cell  # 1.0 and 1 are the same column
OUT.write_text(json.dumps(data, separators=(",", ":")))
print(f"{OUT}: {len(data['gate'])} gate runs, {len(data['rides'])} rung rides, "
      f"{sum(len(v) for v in data['pretest'].values())} pre-test cells in {len(data['pretest'])} rows")
