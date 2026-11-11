#!/usr/bin/env python3
"""Interim three-row figure (milestone of 13 November 2026): riding, decoder-free predictions and decodability on the
wiring ladder R0 to R5, one row each, on a shared axis. Every number is read from fly-brain's result files; nothing is
typed in by hand except the hands-off floor (fly-brain docs/CURRENT_NUMBERS.md, 16 riders, 2026-10-29, which the docs quote
as the hands-off level).

    python3 tools/interim_figure.py [--fly ~/flybrain/fly_brain/results]

Writes site/figures/interim.svg, interim.png and interim.json (every plotted value with its source file).

Row A, riding: last-generation mean riding time (48 riders x 15 s) of each finished search with the hand-picked readout at
4.5 m/s. Confirmatory rides (preregistration prereg-v1: R0 and draws 3-5 of R1-R3, CEM seeds 211-215, GPU; R3.5, R4 and
R5 draw 1, seed 211, at their closed-loop synaptic scale, CPU) are filled; pilot rides (draws 1-2, seeds 201-203, before
the tag) are open. Searches of 60 generations only, except R0's three gate pilots, which stopped at 57, 58 and 60.
Row B, decoder-free: Track B confirmatory score (fraction of the six scored predictions a brain passes), each draw a dot,
the line is the mean over draws (R1 and R2 100 draws, R3-R5 3 draws), at scale 0.47 and, for R4 and R5, at their
closed-loop scale.
Row C, decodability: Track C pilot, descending-neuron site, number of neurons needed for 90% of the site's R^2 in screen
order and in random order (median, 25-75% over 20 orders, all 1,314 descending neurons), one replay per brain (draw 1).
Not measured past R3.
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
RUNGS = ["R0", "R1", "R2", "R3", "R3.5", "R4", "R5"]
KEEPS = ["real wiring", "transmitter\nerrors", "synapse-count\njitter", "cell types\nkept", "input strength\nkept",
         "degrees\nkept", "random"]
X = {r: i for i, r in enumerate(RUNGS)}
HANDS_OFF = 5.7  # s, 4.5 m/s, docs/CURRENT_NUMBERS.md "Hands-off floor"
BLUE, ORANGE = "#2a78d6", "#eb6834"  # dataviz reference palette, slots 1 and 2
INK, INK2, MUTE, GRID = "#1c1b18", "#5f5b53", "#8b867c", "#e6e2d9"  # the site's light tokens


def last_gen(path):
    d = json.loads(path.read_text())
    h = d["history"]
    assert d["config"]["v0"] == 4.5 and d["config"]["readout"] == "lane", path
    return len(h), h[-1]["upright_mean"]


def riding(res):
    """(rung, kind, label, value, generations, source) for every ride of row A."""
    out = []

    def add(rung, kind, label, path, need60=True):
        if not path.exists():
            return
        n, v = last_gen(path)
        if need60 and n < 60:
            return
        out.append({"rung": rung, "kind": kind, "label": label, "riding_s": round(v, 3), "generations": n, "source": str(path.relative_to(res))})

    for p in sorted(res.glob("gate/v4.5_s20*/cem.json")):
        add("R0", "pilot", f"gate seed {p.parent.name[-3:]}", p, need60=False)
    for p in sorted(res.glob("rungs/r[123]_s[12]_cpu/v4.5_s*/cem.json")):
        m = re.match(r"r(\d)_s(\d)_cpu", p.parent.parent.name)
        add(f"R{m[1]}", "pilot", f"draw {m[2]}, seed {p.parent.name[-3:]}", p)
    for p in sorted(res.glob("rungs/conf_r0/v4.5_s*/cem.json")):
        add("R0", "confirmatory", f"seed {p.parent.name[-3:]}", p)
    for p in sorted(res.glob("rungs/conf_r[123]_s[345]/v4.5_s*/cem.json")):
        m = re.match(r"conf_r(\d)_s(\d)", p.parent.parent.name)
        add(f"R{m[1]}", "confirmatory", f"draw {m[2]}, seed {p.parent.name[-3:]}", p)
    for rung, tag, scale in (("R3.5", "conf_r35_s1_w0.47_cpu", "0.47"), ("R4", "conf_r4_s1_w1.2_cpu", "1.2"), ("R5", "conf_r5_s1_w2_cpu", "2.0")):
        add(rung, "confirmatory", f"draw 1, seed 211, scale {scale}, CPU", res / "rungs" / tag / "v4.5_s211" / "cem.json")
    return out


def decoder_free(res):
    src = res / "track_b" / "confirmatory" / "scores.json"
    scores = json.loads(src.read_text())
    out = []
    for stem, s in sorted(scores.items()):
        m = re.fullmatch(r"r(\d+)(?:_s(\d+))?(?:_w([\d.]+))?", stem)
        rung = {"0": "R0", "1": "R1", "2": "R2", "3": "R3", "35": "R3.5", "4": "R4", "5": "R5"}[m[1]]
        out.append({"rung": rung, "draw": int(m[2]) if m[2] else None, "scale": m[3] or "0.47", "score": round(s["score"], 4), "source": f"track_b/confirmatory/{stem}.json"})
    return out


def decodability(res):
    out = []
    for i, rung in enumerate(RUNGS[:4]):
        src = res / "track_c" / f"r{i}.json"
        ref = json.loads(src.read_text())["sites"]["descending"]["references"]["site"]
        rnd = ref["n90_random_all_site_neurons"]
        out.append({"rung": rung, "n90_screen": ref["n90_screen"], "n90_random_median": rnd["median"], "n90_random_q25_q75": rnd["q25_q75"],
                    "random_orders_reached": rnd["reached"], "target_r2": ref["target_r2"], "source": f"track_c/r{i}.json"})
    return out


def jitter(i, n, width):
    return 0.0 if n == 1 else -width / 2 + width * i / (n - 1)


def draw(data, out_svg, out_png):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": MUTE, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "text.color": INK, "svg.fonttype": "none"})
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 8.4), sharex=True, gridspec_kw={"hspace": 0.32})
    for ax in axes:
        ax.set_facecolor("white")
        ax.grid(axis="y", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.axvspan(3.5, 6.5, color="#f4f2ed", zorder=0)
    fig.patch.set_facecolor("white")

    # A: riding
    ax = axes[0]
    for kind, face, edge, z in (("pilot", "white", MUTE, 3), ("confirmatory", INK, "white", 4)):
        for rung in RUNGS:
            pts = [r for r in data["riding"] if r["rung"] == rung and r["kind"] == kind]
            off = -0.17 if kind == "pilot" else 0.17
            for i, r in enumerate(pts):
                ax.scatter(X[rung] + off + jitter(i, len(pts), 0.22), r["riding_s"], s=46 if kind == "confirmatory" else 34, facecolor=face,
                           edgecolor=edge, linewidth=1.0 if kind == "confirmatory" else 1.6, zorder=z)
                if rung in ("R3.5", "R4", "R5"):
                    ax.text(X[rung] + off + 0.14, r["riding_s"], "scale " + r["label"].split("scale ")[1].split(",")[0], va="center", fontsize=7.5, color=INK2)
    ax.axhline(HANDS_OFF, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=2)
    ax.text(6.45, HANDS_OFF + 0.35, "no steering (hands-off) 5.7 s", ha="right", va="bottom", fontsize=8, color=INK2)
    ax.set_ylim(0, 15.5)
    ax.set_yticks([0, 5, 10, 15])
    ax.set_ylabel("Riding time (s)\nof 15 s, at 4.5 m/s")
    ax.scatter([], [], s=46, facecolor=INK, edgecolor="white", linewidth=1.0, label="confirmatory ride")
    ax.scatter([], [], s=34, facecolor="white", edgecolor=MUTE, linewidth=1.6, label="pilot ride")
    ax.legend(loc="lower left", frameon=False, fontsize=8, handletextpad=0.3, borderaxespad=0.2)
    ax.set_title("A   Learning to ride: a decoder trained on each brain", loc="left", fontsize=10, fontweight="bold")

    # B: decoder-free
    ax = axes[1]
    for scale, color, off in (("0.47", BLUE, -0.15), ("closed", ORANGE, 0.15)):
        for rung in RUNGS:
            pts = [r for r in data["decoder_free"] if r["rung"] == rung and (r["scale"] == "0.47") == (scale == "0.47")]
            if not pts:
                continue
            if rung in ("R0", "R3", "R3.5"):
                off_r = 0.0
            else:
                off_r = off
            vals = sorted(p["score"] for p in pts)
            n = len(vals)
            for i, v in enumerate(vals):
                ax.scatter(X[rung] + off_r + jitter(i, n, 0.26 if n > 3 else 0.14), v, s=10 if n > 3 else 22, color=color, alpha=0.35 if n > 3 else 0.9,
                           linewidth=0, zorder=3)
            mean = sum(vals) / n
            ax.plot([X[rung] + off_r - 0.16, X[rung] + off_r + 0.16], [mean, mean], color=INK, lw=2, solid_capstyle="round", zorder=4)
            if n > 3:
                for level in sorted(set(vals)):
                    ax.text(X[rung] + off_r + 0.22, level, f"{vals.count(level)}", va="center", fontsize=7.5, color=INK2)
    ax.set_ylim(-0.08, 1.1)
    ax.set_yticks([0, 0.5, 1])
    ax.set_ylabel("Predictions passed\n(fraction of 6)")
    ax.scatter([], [], s=22, color=BLUE, label="synaptic scale 0.47")
    ax.scatter([], [], s=22, color=ORANGE, label="the rung's closed-loop scale")
    ax.plot([], [], color=INK, lw=2, label="mean over draws")
    ax.plot([], [], ls="none", label="small numbers: draws at that score")
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.55), frameon=False, fontsize=8, handletextpad=0.3)
    ax.set_title("B   Decoder-free: six feeding and escape predictions from the literature", loc="left", fontsize=10, fontweight="bold")

    # C: decodability
    ax = axes[2]
    ax.set_yscale("log")
    for r in data["decodability"]:
        x = X[r["rung"]]
        lo, hi = r["n90_random_q25_q75"]
        ax.plot([x + 0.12, x + 0.12], [lo, hi], color=MUTE, lw=2, zorder=3, solid_capstyle="round")
        ax.scatter(x + 0.12, r["n90_random_median"], s=34, color=MUTE, edgecolor="white", linewidth=1.2, zorder=4)
        ax.scatter(x - 0.12, r["n90_screen"], s=40, color=INK, edgecolor="white", linewidth=1.2, zorder=4)
    for rung in RUNGS[4:]:
        ax.text(X[rung], 4, "not yet\nmeasured", ha="center", va="center", fontsize=8, color=MUTE)
    ax.axhline(1314, color=MUTE, lw=0.8, ls=":")
    ax.text(-0.4, 1314 * 1.12, "all 1,314 descending neurons", fontsize=7.5, color=MUTE, va="bottom")
    ax.set_ylim(1, 3000)
    ax.set_yticks([1, 10, 100, 1000])
    ax.set_yticklabels(["1", "10", "100", "1,000"])
    ax.set_ylabel("Neurons for 90% of\nthe roll-rate R²")
    ax.scatter([], [], s=40, color=INK, label="best neurons first (screen order)")
    ax.plot([], [], color=MUTE, lw=2, marker="o", markersize=5, label="random neurons (median, 25–75%)")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.86), frameon=False, fontsize=8, handletextpad=0.3)
    ax.set_title("C   Decodability: recording descending neurons (pilot)", loc="left", fontsize=10, fontweight="bold")

    ax.set_xlim(-0.5, 6.5)
    ax.set_xticks(range(len(RUNGS)))
    ax.set_xticklabels([f"{r}\n{k}" for r, k in zip(RUNGS, KEEPS)], fontsize=8)
    ax.tick_params(axis="x", length=0)
    fig.text(0.99, 0.005, f"Scrambled Brains, interim figure; data of {data['data_date']}", ha="right", fontsize=7, color=MUTE)
    fig.savefig(out_svg, bbox_inches="tight")
    fig.savefig(out_png, dpi=200, bbox_inches="tight")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fly", default=str(Path.home() / "flybrain" / "fly_brain" / "results"))
    a = ap.parse_args()
    res = Path(a.fly)
    data = {"hands_off_s": HANDS_OFF, "riding": riding(res), "decoder_free": decoder_free(res), "decodability": decodability(res)}
    newest = max((res / x["source"]).stat().st_mtime for x in data["riding"] + data["decodability"])
    newest = max(newest, (res / "track_b" / "confirmatory" / "scores.json").stat().st_mtime)
    data["data_date"] = datetime.fromtimestamp(newest).strftime("%Y-%m-%d")  # the newest result file read
    out = HERE / "site" / "figures"
    out.mkdir(exist_ok=True)
    (out / "interim.json").write_text(json.dumps(data, indent=1))
    draw(data, out / "interim.svg", out / "interim.png")
    for rung in RUNGS:
        rides = [r["riding_s"] for r in data["riding"] if r["rung"] == rung]
        print(rung, f"{len(rides)} rides", [round(v, 2) for v in rides])


if __name__ == "__main__":
    main()
