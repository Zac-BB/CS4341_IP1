import matplotlib.pyplot as plt
import json
import numpy as np

def generate_figures():
    data = []
    with open("results.json","r") as f:
        data = json.load(f)
    
    boards = ["Simple", "Mid", "Hard"]
    metrics = ["nodes_expanded", "frontier", "time"]
    board_keys = ["boards/sokoban_simple.txt", "boards/sokoban_mid.txt", "boards/sokoban_hard.txt"]

    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('A* vs Uniform Cost Search Performance Comparison', fontsize=16, fontweight='bold')

    
    x = np.arange(len(boards))
    width = 0.35

    
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        
        astar_values = [data["A Star"][board][metric] for board in board_keys]
        ucs_values = [data["Uniform Cost Search"][board][metric] for board in board_keys]
        
        bars1 = ax.bar(x - width/2, astar_values, width, label='A*', color='#2E86AB', alpha=0.8)
        bars2 = ax.bar(x + width/2, ucs_values, width, label='UCS', color='#A23B72', alpha=0.8)
        
        # Customize subplot
        ax.set_xlabel('Board Difficulty', fontweight='bold')
        ax.set_ylabel(metric.replace('_', ' ').title(), fontweight='bold')
        ax.set_title(metric.replace('_', ' ').title())
        ax.set_xticks(x)
        ax.set_xticklabels(boards)
        ax.legend()
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if metric == "time":
                    label = f'{height:.2f}s'
                else:
                    label = f'{int(height):,}'
                ax.text(bar.get_x() + bar.get_width()/2., height,
                    label, ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig('figures/performance_comparison.png', dpi=300, bbox_inches='tight')
    

    #
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    metrics_display = ['Nodes Expanded', 'Frontier Size', 'Time (s)']
    astar_hard = [
        data["A Star"]["boards/sokoban_hard.txt"]["nodes_expanded"],
        data["A Star"]["boards/sokoban_hard.txt"]["frontier"],
        data["A Star"]["boards/sokoban_hard.txt"]["time"]
    ]
    ucs_hard = [
        data["Uniform Cost Search"]["boards/sokoban_hard.txt"]["nodes_expanded"],
        data["Uniform Cost Search"]["boards/sokoban_hard.txt"]["frontier"],
        data["Uniform Cost Search"]["boards/sokoban_hard.txt"]["time"]
    ]

    x2 = np.arange(len(metrics_display))
    bars1 = ax2.bar(x2 - width/2, astar_hard, width, label='A*', color='#2E86AB', alpha=0.8)
    bars2 = ax2.bar(x2 + width/2, ucs_hard, width, label='UCS', color='#A23B72', alpha=0.8)

    ax2.set_ylabel('Value', fontweight='bold', fontsize=12)
    ax2.set_title('Hard Board: A* vs UCS - Dramatic Performance Difference', fontweight='bold', fontsize=14)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(metrics_display)
    ax2.legend(fontsize=12)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height >= 1000:
                label = f'{int(height):,}'
            else:
                label = f'{height:.2f}'
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('figures/hard_board_comparison.png', dpi=300, bbox_inches='tight')
    

    plt.show()




if __name__== "__main__":
    generate_figures()