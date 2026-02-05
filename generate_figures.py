import matplotlib.pyplot as plt
import json
import numpy as np

def generate_figures():
    with open("results.json", "r") as f:
        data = json.load(f)

    boards = ["Simple", "Mid", "Hard"]
    board_keys = [
        "boards/sokoban_simple.txt",
        "boards/sokoban_mid.txt",
        "boards/sokoban_hard.txt",
    ]

    # 4 metrics → 2x2 grid
    metrics = ["nodes_expanded", "frontier", "time", "output length"]

    fig, axes = plt.subplots(2, 2, figsize=(15, 8))
    fig.suptitle(
        "A* vs Uniform Cost Search Performance Comparison",
        fontsize=16,
        fontweight="bold",
    )

    x = np.arange(len(boards))
    width = 0.35

    for idx, metric in enumerate(metrics):
        row, col = divmod(idx, 2)   # <-- KEY FIX
        ax = axes[row, col]

        astar_values = [data["A Star"][b][metric] for b in board_keys]
        ucs_values = [data["Uniform Cost Search"][b][metric] for b in board_keys]

        bars1 = ax.bar(
            x - width / 2, astar_values, width, label="A*", alpha=0.8
        )
        bars2 = ax.bar(
            x + width / 2, ucs_values, width, label="UCS", alpha=0.8
        )

        ax.set_xlabel("Board Difficulty", fontweight="bold")
        ax.set_ylabel(metric.replace("_", " ").title(), fontweight="bold")
        ax.set_title(metric.replace("_", " ").title())
        ax.set_xticks(x)
        ax.set_xticklabels(boards)
        ax.legend()
        ax.grid(axis="y", alpha=0.3, linestyle="--")

        # Log scale for everything (including output length)
        ax.set_yscale("log")

        # Value labels (output length shown on last subplot)
        for bars in (bars1, bars2):
            for bar in bars:
                h = bar.get_height()
                if metric == "time":
                    label = f"{h:.2f}s"
                else:
                    label = f"{int(h):,}"
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h,
                    label,
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

    plt.tight_layout()
    plt.savefig(
        "figures/performance_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )

    # -----------------------
    # HARD BOARD COMPARISON
    # -----------------------
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    metrics_display = ["Nodes Expanded", "Frontier Size", "Time (s)", "Output Length"]

    astar_hard = [
        data["A Star"]["boards/sokoban_hard.txt"]["nodes_expanded"],
        data["A Star"]["boards/sokoban_hard.txt"]["frontier"],
        data["A Star"]["boards/sokoban_hard.txt"]["time"],
        data["A Star"]["boards/sokoban_hard.txt"]["output length"],
    ]
    ucs_hard = [
        data["Uniform Cost Search"]["boards/sokoban_hard.txt"]["nodes_expanded"],
        data["Uniform Cost Search"]["boards/sokoban_hard.txt"]["frontier"],
        data["Uniform Cost Search"]["boards/sokoban_hard.txt"]["time"],
        data["Uniform Cost Search"]["boards/sokoban_hard.txt"]["output length"],
    ]

    x2 = np.arange(len(metrics_display))
    bars1 = ax2.bar(x2 - width / 2, astar_hard, width, label="A*", alpha=0.8)
    bars2 = ax2.bar(x2 + width / 2, ucs_hard, width, label="UCS", alpha=0.8)

    ax2.set_yscale("log")
    ax2.set_ylabel("Value", fontweight="bold")
    ax2.set_title(
        "Hard Board: A* vs UCS Performance (Including Output Length)",
        fontweight="bold",
    )
    ax2.set_xticks(x2)
    ax2.set_xticklabels(metrics_display)
    ax2.legend()
    ax2.grid(axis="y", alpha=0.3, linestyle="--")

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            label = f"{int(h):,}" if h >= 1 else f"{h:.2f}"
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                h,
                label,
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

    plt.tight_layout()
    plt.savefig(
        "figures/hard_board_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()


if __name__ == "__main__":
    generate_figures()
