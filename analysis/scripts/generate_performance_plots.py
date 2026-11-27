#!/usr/bin/env python3
"""Reproducible Python/Matplotlib performance plots for the 4-bit RCA case study."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def paint_bars(ax, labels, values, colors, ylabel, fmt, ylim_max):
    x = np.arange(len(labels))
    ax.bar(x, values, width=0.62, color=colors, edgecolor="#1F1F1F", linewidth=0.8, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10, color="#1F1F1F")
    ax.set_ylabel(ylabel, fontsize=11, color="#1F1F1F")
    ax.set_ylim(0, ylim_max)
    ax.yaxis.grid(True, color="#404040", alpha=0.18, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#1F1F1F")
    ax.spines["bottom"].set_color("#1F1F1F")
    ax.tick_params(axis="both", direction="out", colors="#1F1F1F")

    offset = 0.025 * max(values)
    for idx, val in enumerate(values):
        ax.text(
            idx,
            val + offset,
            fmt.format(val),
            ha="center",
            va="bottom",
            fontsize=10,
            color="#1F1F1F",
        )


def main():
    repo_root = Path(__file__).resolve().parents[2]
    output_dir = repo_root / "assets" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)

    labels = ["Static CMOS", "C²MOS", "Domino Logic"]
    short_labels = ["Static", "C²MOS", "Domino"]
    delay_ps = np.array([251.81, 260.75, 222.35])
    power_uw = np.array([13.25, 29.49, 30.76])
    pdp_fj = (power_uw * delay_ps) / 1000.0

    expected_pdp = np.array([3.34, 7.69, 6.84])
    assert np.array_equal(np.round(pdp_fj, 2), expected_pdp), (
        f"Recalculated PDP {np.round(pdp_fj, 2)} does not match {expected_pdp}"
    )

    colors = ["#1F5785", "#D1661F", "#6B6B6B"]

    specs = [
        (
            "pdp_comparison",
            pdp_fj,
            "Power-Delay Product Comparison",
            "Lower PDP is better",
            "Power-Delay Product (fJ)",
            "{:.2f} fJ",
            8.8,
        ),
        (
            "delay_comparison",
            delay_ps,
            "Propagation Delay Comparison",
            "Domino is fastest in this dataset",
            "Propagation Delay (ps)",
            "{:.2f} ps",
            300.0,
        ),
        (
            "power_comparison",
            power_uw,
            "Average Power Comparison",
            "Static CMOS has the lowest reported average power",
            "Average Power (µW)",
            "{:.2f} µW",
            36.0,
        ),
    ]

    for stem, values, title, subtitle, ylabel, fmt, ylim_max in specs:
        fig, ax = plt.subplots(figsize=(7.4, 4.8), facecolor="white")
        paint_bars(ax, labels, values, colors, ylabel, fmt, ylim_max)
        ax.text(
            0.5, 1.075, title,
            transform=ax.transAxes, ha="center", va="bottom",
            fontsize=14, fontweight="bold", color="#191919",
        )
        ax.text(
            0.5, 1.015, subtitle,
            transform=ax.transAxes, ha="center", va="bottom",
            fontsize=10, color="#333333",
        )
        fig.tight_layout(rect=(0, 0, 1, 0.92))
        fig.savefig(output_dir / f"{stem}.png", dpi=300, facecolor="white")
        fig.savefig(output_dir / f"{stem}.pdf", facecolor="white")
        plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.4), facecolor="white")
    overview_specs = [
        (axes[0], pdp_fj, "PDP", "PDP (fJ)", "{:.2f}", 9.2),
        (axes[1], delay_ps, "Propagation Delay", "Delay (ps)", "{:.1f}", 300.0),
        (axes[2], power_uw, "Average Power", "Average Power (µW)", "{:.1f}", 35.0),
    ]
    for ax, values, panel_title, ylabel, fmt, ylim_max in overview_specs:
        paint_bars(ax, short_labels, values, colors, ylabel, fmt, ylim_max)
        ax.set_title(panel_title, fontsize=11, fontweight="bold", color="#191919")

    fig.suptitle(
        "Four-Bit RCA Performance Overview",
        fontsize=13,
        fontweight="bold",
        color="#191919",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(output_dir / "combined_performance.png", dpi=300, facecolor="white")
    fig.savefig(output_dir / "combined_performance.pdf", facecolor="white")
    plt.close(fig)

    print(
        f"Verified PDP (fJ): Static={pdp_fj[0]:.6f} ({pdp_fj[0]:.2f}), "
        f"C2MOS={pdp_fj[1]:.6f} ({pdp_fj[1]:.2f}), "
        f"Domino={pdp_fj[2]:.6f} ({pdp_fj[2]:.2f})"
    )
    print(f"Plots saved under: {output_dir}")


if __name__ == "__main__":
    main()
