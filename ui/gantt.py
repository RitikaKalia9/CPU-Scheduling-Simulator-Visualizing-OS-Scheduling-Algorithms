"""Matplotlib Gantt chart rendering."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import colormaps
import streamlit as st


COLORS = colormaps["tab20"]


def _color_map(pids):
    ids = sorted(set(p for p in pids if p != "IDLE"))
    mapping = {pid: COLORS(i % 20) for i, pid in enumerate(ids)}
    mapping["IDLE"] = (0.6, 0.6, 0.6, 1.0)
    return mapping


def draw(timeline, title: str, kind: str = "CPU"):
    """Draw a single timeline as a horizontal Gantt chart."""
    if not timeline:
        st.info(f"No {kind} activity.")
        return

    pids = [pid for pid, _, _ in timeline]
    cmap = _color_map(pids)

    fig, ax = plt.subplots(figsize=(11, 2.2))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    for pid, start, end in timeline:
        ax.broken_barh(
            [(start, end - start)],
            (0, 1),
            facecolors=cmap[pid],
            edgecolor="#0f172a",
            linewidth=1.6,
        )
        # Label inside bar
        if (end - start) > 0.4:
            ax.text(
                (start + end) / 2, 0.5, pid,
                ha="center", va="center",
                color="white", fontsize=9, fontweight="bold",
            )
        # Start time label
        ax.text(start, -0.15, str(start),
                ha="center", va="top", color="#94a3b8", fontsize=8)
    # End time
    ax.text(timeline[-1][2], -0.15, str(timeline[-1][2]),
            ha="center", va="top", color="#94a3b8", fontsize=8)

    ax.set_xlim(0, timeline[-1][2])
    ax.set_ylim(-0.5, 1.5)
    ax.set_yticks([])
    ax.set_xlabel("Time →", color="#cbd5e1")
    ax.set_title(title, color="#f1f5f9", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_color("#334155")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)