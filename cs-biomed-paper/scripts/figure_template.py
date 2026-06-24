#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Submission-grade figure templates (matplotlib) → vector .pdf / .svg.

The "output first" tool for stage 05. Produces journal-ready figures with the defaults from
references/figure-standards.md baked in: vector output, embedded fonts, colourblind-safe palette
(Okabe-Ito), perceptually-uniform colormap (viridis), minimum font sizes, uncertainty shown, honest
axes, and a self-contained caption stub printed to stdout.

It runs out-of-the-box on built-in demo data so you can see the template, then swap in your own data
via --csv (or by editing the load_* functions). It NEVER invents your results — demo mode is clearly
labelled "DEMO DATA" on the figure so a placeholder can't be mistaken for real output.

Figure kinds:
    roc          ROC curve(s) with AUC (single or multiple models)
    calibration  calibration / reliability plot for a risk model
    forest       forest plot of effect sizes with 95% CIs
    box          box + jittered points (small-n distributions)
    bars         grouped bar chart with error bars (e.g. ablations)
    heatmap      clustered-style heatmap (e.g. omics / confusion)

Usage:
    python figure_template.py --kind roc        --out fig_roc.pdf
    python figure_template.py --kind forest     --out fig_forest.svg --title "Subgroup AUC"
    python figure_template.py --kind bars --csv ablation.csv --out fig_ablation.pdf
    # --csv is optional; without it you get a clearly-labelled DEMO figure.

CSV column layouts (one header row; UTF-8; see each load_* for details):
    roc          model,fpr,tpr                 (one row per ROC point; AUC computed per model)
    calibration  mean_pred,frac_pos,ci_low,ci_high   (one row per probability bin)
    forest       label,estimate,ci_low,ci_high (one row per subgroup/effect)
    box          group,value                   (long format; one row per observation)
    bars         group,series,mean,err         (long format; pivoted to grouped bars)
    heatmap      matrix: header ['',col1,...]; each row [rowlabel,v,...]

Output: writes the figure to --out (.pdf or .svg recommended) and prints a caption stub + the column
size used. Requires matplotlib + numpy (see requirements.txt).
"""

import argparse
import csv
import sys

# Caption stubs carry Chinese [待补充] placeholders; force UTF-8 so Windows consoles
# (cp936/cp1252) don't mojibake or raise UnicodeEncodeError.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

try:
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError as e:  # pragma: no cover
    sys.exit(f"[error] needs matplotlib + numpy: pip install matplotlib numpy ({e})")

# Okabe-Ito colourblind-safe qualitative palette.
OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442", "#000000"]
# Common single-column ~89 mm and double-column ~183 mm, in inches.
COL_WIDTH = {"single": 3.5, "double": 7.2}


def apply_style(min_font=7):
    """Production defaults: embedded TrueType fonts, sans-serif, min font sizes, tight layout."""
    plt.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",  # editable embedded text
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": min_font, "axes.labelsize": min_font + 1, "axes.titlesize": min_font + 1,
        "xtick.labelsize": min_font, "ytick.labelsize": min_font, "legend.fontsize": min_font,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.8, "lines.linewidth": 1.5, "figure.dpi": 300,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    })


def _demo_note(ax):
    ax.text(0.99, 0.01, "DEMO DATA — replace with your results", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=6, color="0.5", style="italic")


# ---------------------------------------------------------------- ROC
def fig_roc(ax, data):
    """data: list of (label, fpr_array, tpr_array, auc). Demo: two synthetic models."""
    for i, (label, fpr, tpr, auc) in enumerate(data):
        ax.plot(fpr, tpr, color=OKABE_ITO[i % len(OKABE_ITO)], label=f"{label} (AUC={auc:.2f})")
    ax.plot([0, 1], [0, 1], "--", color="0.6", linewidth=0.8)
    ax.set_xlabel("1 − Specificity"); ax.set_ylabel("Sensitivity")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.02); ax.set_aspect("equal")
    ax.legend(loc="lower right", frameon=False)


def demo_roc():
    rng = np.random.default_rng(0)
    out = []
    for name, strength in [("Proposed", 2.2), ("Baseline", 1.2)]:
        x = np.linspace(0, 1, 200)
        tpr = x ** (1.0 / strength)            # concave synthetic ROC
        _trap = getattr(np, "trapezoid", getattr(np, "trapz", None))  # numpy 2.x renamed trapz
        auc = float(_trap(tpr, x))
        out.append((name, x, tpr, auc))
    return out, True


# ---------------------------------------------------------------- calibration
def fig_calibration(ax, data):
    """data: (mean_pred, frac_pos, ci_low, ci_high). Demo: slightly over-confident model."""
    mp, fp, lo, hi = data
    ax.plot([0, 1], [0, 1], "--", color="0.6", linewidth=0.8, label="Ideal")
    ax.errorbar(mp, fp, yerr=[fp - lo, hi - fp], fmt="o-", color=OKABE_ITO[0],
                capsize=2, markersize=3, label="Model")
    ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.legend(loc="upper left", frameon=False)


def demo_calibration():
    mp = np.linspace(0.05, 0.95, 10)
    fp = np.clip(mp ** 1.25, 0, 1)
    se = 0.04
    return (mp, fp, np.clip(fp - se, 0, 1), np.clip(fp + se, 0, 1)), True


# ---------------------------------------------------------------- forest
def fig_forest(ax, data):
    """data: list of (label, estimate, ci_low, ci_high). Demo: subgroup AUCs."""
    labels = [d[0] for d in data]
    est = np.array([d[1] for d in data]); lo = np.array([d[2] for d in data])
    hi = np.array([d[3] for d in data]); y = np.arange(len(data))[::-1]
    ax.errorbar(est, y, xerr=[est - lo, hi - est], fmt="s", color=OKABE_ITO[0],
                capsize=2, markersize=4)
    ax.axvline(est.mean(), linestyle="--", color="0.6", linewidth=0.8)
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel("Effect size (95% CI)")
    ax.set_ylim(-0.6, len(data) - 0.4)


def demo_forest():
    rows = [("Overall", 0.88, 0.85, 0.91), ("Site A", 0.90, 0.86, 0.94),
            ("Site B", 0.84, 0.79, 0.89), ("Age <60", 0.89, 0.85, 0.93),
            ("Age >=60", 0.86, 0.81, 0.90)]
    return rows, True


# ---------------------------------------------------------------- box
def fig_box(ax, data):
    """data: dict group -> 1D array. Demo: two groups."""
    groups = list(data); vals = [np.asarray(data[g]) for g in groups]
    bp = ax.boxplot(vals, showfliers=False, widths=0.5, patch_artist=True)
    for patch in bp["boxes"]:
        patch.set(facecolor="#E8E8E8", edgecolor="black", linewidth=0.8)
    rng = np.random.default_rng(1)
    for i, v in enumerate(vals, 1):
        ax.scatter(rng.normal(i, 0.05, len(v)), v, s=8,
                   color=OKABE_ITO[(i - 1) % len(OKABE_ITO)], alpha=0.7, zorder=3)
    ax.set_xticks(range(1, len(groups) + 1)); ax.set_xticklabels(groups)
    ax.set_ylabel("Metric")


def demo_box():
    rng = np.random.default_rng(2)
    return {"Proposed": rng.normal(0.88, 0.03, 20), "Baseline": rng.normal(0.81, 0.05, 20)}, True


# ---------------------------------------------------------------- bars
def fig_bars(ax, data):
    """data: (groups, series_dict{name: (means, errs)}). Demo: ablation."""
    groups, series = data
    x = np.arange(len(groups)); n = len(series); w = 0.8 / max(n, 1)
    for i, (name, (means, errs)) in enumerate(series.items()):
        ax.bar(x + i * w - 0.4 + w / 2, means, w, yerr=errs, capsize=2,
               color=OKABE_ITO[i % len(OKABE_ITO)], label=name, edgecolor="black", linewidth=0.5)
    ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylabel("Score")
    ax.legend(frameon=False)


def demo_bars():
    groups = ["Dice", "Sensitivity", "Specificity"]
    series = {"Full model": ([0.86, 0.88, 0.91], [0.02, 0.02, 0.01]),
              "w/o module A": ([0.81, 0.83, 0.90], [0.03, 0.03, 0.02])}
    return (groups, series), True


# ---------------------------------------------------------------- heatmap
def fig_heatmap(ax, data):
    """data: (matrix, row_labels, col_labels). Demo: random correlation-like matrix."""
    mat, rows, cols = data
    im = ax.imshow(mat, cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=45, ha="right")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows)
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=6)


def demo_heatmap():
    rng = np.random.default_rng(3)
    mat = rng.random((6, 8))
    return (mat, [f"feat{i}" for i in range(6)], [f"s{j}" for j in range(8)]), True


# ---------------------------------------------------------------- CSV loaders
# Each loader returns data in the SAME shape the matching demo_* returns, so a real CSV drops straight
# into the builder. Column layouts are documented in the module docstring. Loaders never invent values:
# a malformed/missing column is a hard error, not a silent default.
def _rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"[error] {path}: no data rows")
    return rows


def _need(rows, cols, kind):
    missing = [c for c in cols if c not in rows[0]]
    if missing:
        sys.exit(f"[error] {kind}: CSV is missing column(s) {missing}; expected columns {cols}")


def _floats(rows, col, kind):
    try:
        return np.array([float(r[col]) for r in rows])
    except ValueError as e:
        sys.exit(f"[error] {kind}: non-numeric value in column '{col}' ({e})")


def load_roc(path):
    """columns: model, fpr, tpr  (one row per ROC point; AUC computed by trapezoid per model)."""
    rows = _rows(path); _need(rows, ["model", "fpr", "tpr"], "roc")
    _trap = getattr(np, "trapezoid", getattr(np, "trapz"))
    groups = {}
    for r in rows:
        groups.setdefault(r["model"], []).append((float(r["fpr"]), float(r["tpr"])))
    out = []
    for name, pts in groups.items():
        pts.sort()
        fpr = np.array([p[0] for p in pts]); tpr = np.array([p[1] for p in pts])
        out.append((name, fpr, tpr, float(_trap(tpr, fpr))))
    return out


def load_calibration(path):
    """columns: mean_pred, frac_pos, ci_low, ci_high  (one row per probability bin)."""
    rows = _rows(path); _need(rows, ["mean_pred", "frac_pos", "ci_low", "ci_high"], "calibration")
    return (_floats(rows, "mean_pred", "calibration"), _floats(rows, "frac_pos", "calibration"),
            _floats(rows, "ci_low", "calibration"), _floats(rows, "ci_high", "calibration"))


def load_forest(path):
    """columns: label, estimate, ci_low, ci_high  (one row per subgroup/effect)."""
    rows = _rows(path); _need(rows, ["label", "estimate", "ci_low", "ci_high"], "forest")
    return [(r["label"], float(r["estimate"]), float(r["ci_low"]), float(r["ci_high"])) for r in rows]


def load_box(path):
    """columns: group, value  (long format; one row per observation)."""
    rows = _rows(path); _need(rows, ["group", "value"], "box")
    d = {}
    for r in rows:
        d.setdefault(r["group"], []).append(float(r["value"]))
    return {g: np.asarray(v) for g, v in d.items()}


def load_bars(path):
    """columns: group, series, mean, err  (long format; pivoted to grouped bars)."""
    rows = _rows(path); _need(rows, ["group", "series", "mean", "err"], "bars")
    groups = list(dict.fromkeys(r["group"] for r in rows))
    names = list(dict.fromkeys(r["series"] for r in rows))
    table = {(r["group"], r["series"]): (float(r["mean"]), float(r["err"])) for r in rows}
    series = {}
    for s in names:
        series[s] = ([table.get((g, s), (0.0, 0.0))[0] for g in groups],
                     [table.get((g, s), (0.0, 0.0))[1] for g in groups])
    return (groups, series)


def load_heatmap(path):
    """matrix format: header row = ['', col1, col2, ...]; each data row = [rowlabel, v, v, ...]."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = [r for r in csv.reader(f) if r]
    if len(reader) < 2:
        sys.exit("[error] heatmap: need a header row + at least one data row")
    cols = reader[0][1:]
    labels, mat = [], []
    for r in reader[1:]:
        labels.append(r[0])
        try:
            mat.append([float(x) for x in r[1:]])
        except ValueError as e:
            sys.exit(f"[error] heatmap: non-numeric cell ({e})")
    return (np.array(mat), labels, cols)


LOADERS = {"roc": load_roc, "calibration": load_calibration, "forest": load_forest,
           "box": load_box, "bars": load_bars, "heatmap": load_heatmap}


KINDS = {
    "roc": (fig_roc, demo_roc, "ROC curves with AUC and 95% CI; n=[待补充] test patients."),
    "calibration": (fig_calibration, demo_calibration,
                    "Calibration plot; predicted vs observed risk with 95% CI; n=[待补充]."),
    "forest": (fig_forest, demo_forest, "Forest plot of [metric] by subgroup with 95% CI."),
    "box": (fig_box, demo_box, "Distribution of [metric] per group; box = IQR, points = folds/seeds."),
    "bars": (fig_bars, demo_bars, "Ablation: [metric] per configuration; error bars = SD over [N] seeds."),
    "heatmap": (fig_heatmap, demo_heatmap, "[Feature x sample] matrix (viridis); values = [待补充]."),
}


def main():
    ap = argparse.ArgumentParser(description="Generate a submission-grade figure template.")
    ap.add_argument("--kind", choices=list(KINDS), required=True)
    ap.add_argument("--out", required=True, help="output path (.pdf or .svg recommended)")
    ap.add_argument("--csv", help="optional CSV with your data (see each kind's docstring)")
    ap.add_argument("--width", choices=["single", "double"], default="single")
    ap.add_argument("--title", default="")
    ap.add_argument("--min-font", type=int, default=7, help="minimum font size at final print size")
    args = ap.parse_args()

    apply_style(args.min_font)
    builder, demo, caption = KINDS[args.kind]

    if args.csv:
        data = LOADERS[args.kind](args.csv)
        is_demo = False
    else:
        data, is_demo = demo()

    w = COL_WIDTH[args.width]
    fig, ax = plt.subplots(figsize=(w, w * 0.8))
    builder(ax, data)
    if args.title:
        ax.set_title(args.title)
    if is_demo:
        _demo_note(ax)
    fig.savefig(args.out)
    plt.close(fig)

    print(f"[ok] wrote {args.out}  ({args.width}-column, {w}in wide, vector if .pdf/.svg)")
    print(f"[caption stub] Figure X. {caption} "
          "Define error bars, test, and n; ensure de-identification for image panels.")
    if is_demo:
        print("[reminder] DEMO DATA used — replace with your real results before submission.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
