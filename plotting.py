from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .config import SIZES_ORDER, CONDS_ORDER, LABEL_MAP, SIZE_LABELS

def plot_grouped_bars(summary: pd.DataFrame, y_label: str, title: str, save_path: Path | None = None) -> None:
    group_spacing = 0.4
    x = np.arange(len(SIZES_ORDER)) * group_spacing
    bar_w = 0.08
    sep = 0.08
    offsets = {"proximal": -sep, "cuff": 0.0, "distal": +sep}

    fig, ax = plt.subplots(figsize=(10, 5))

    for cond in CONDS_ORDER:
        sub = summary[summary["cond"] == cond].set_index("size").reindex(SIZES_ORDER)

        means = sub["mean"].to_numpy(dtype=float)
        sds = sub["standard_deviation"].to_numpy(dtype=float)
        sds = np.nan_to_num(sds, nan=0.0, posinf=0.0, neginf=0.0)

        ax.bar(
            x + offsets[cond],
            means,
            width=bar_w,
            label=LABEL_MAP[cond],
            yerr=sds,
            capsize=4,
        )

    ax.set_xticks(x)
    ax.set_xticklabels([SIZE_LABELS.get(s, s) for s in SIZES_ORDER])
    ax.set_xlabel("Electrode Size", fontsize=10, fontweight="bold")
    ax.set_ylabel(y_label, fontsize=10, fontweight="bold")
    ax.axhline(0, linewidth=1)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")

    y_top = np.nanmax((summary["mean"] + summary["standard_deviation"].fillna(0)).to_numpy(dtype=float))
    ax.set_ylim(0, y_top * 1.3 if np.isfinite(y_top) and y_top > 0 else 1)

    plt.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close(fig)
