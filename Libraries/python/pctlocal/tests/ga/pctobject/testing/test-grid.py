import matplotlib.pyplot as plt 
import numpy as np
import random
from itertools import groupby
import os

def generate_symmetric_crossword_grid(size=13, min_run=3, black_prob=0.2):
    """
    Generate a 180-degree rotationally symmetric crossword grid.
    - size: grid size (size x size)
    - min_run: min length of contiguous white squares (across and down)
    - black_prob: probability to start a black square (for more randomness)
    """
    max_run = size  # Set maximum white run to grid size
    grid = np.zeros((size, size), dtype=int)
    half = (size * size + 1) // 2  # Only fill half, then mirror

    def would_create_short_white_run(g, i, j):
        # Check row
        row = g[i, :]
        row[j] = 1  # Temporarily set black
        white_runs = [len(list(group)) for val, group in groupby(row) if val == 0]
        row[j] = 0  # Restore
        if white_runs and min(white_runs) < min_run:
            return True
        # Check column
        col = g[:, j]
        col[i] = 1
        white_runs = [len(list(group)) for val, group in groupby(col) if val == 0]
        col[i] = 0
        if white_runs and min(white_runs) < min_run:
            return True
        return False


    for idx in range(half):
        i, j = divmod(idx, size)

        # --- ENFORCE LOCAL WHITE BLOCK CONSTRAINT FIRST ---
        if i > 0 and j > 0 and (
            grid[i, j-1] == 0 and
            grid[i-1, j] == 0 and
            grid[i-1, j-1] == 0
        ):
            grid[i, j] = 1
            grid[size-1-i, size-1-j] = 1
            continue  # skip to next cell

        if random.random() < black_prob:
            # Only place black if it doesn't create a too-short white run
            if not would_create_short_white_run(grid, i, j):
                grid[i, j] = 1
                grid[size-1-i, size-1-j] = 1
            else:
                grid[i, j] = 0
                grid[size-1-i, size-1-j] = 0
        else:
            # Optionally, enforce run length constraints
            row_run = 1
            col_run = 1
            # Check previous cells in row
            for k in range(1, max_run+1):
                if j-k >= 0 and grid[i, j-k] == 0:
                    row_run += 1
                else:
                    break
            # Check previous cells in column
            for k in range(1, max_run+1):
                if i-k >= 0 and grid[i-k, j] == 0:
                    col_run += 1
                else:
                    break
            # If run too long, force black
            if row_run > max_run or col_run > max_run:
                if not would_create_short_white_run(grid, i, j):
                    grid[i, j] = 1
                    grid[size-1-i, size-1-j] = 1
                else:
                    grid[i, j] = 0
                    grid[size-1-i, size-1-j] = 0
            else:
                grid[i, j] = 0
                grid[size-1-i, size-1-j] = 0
    return grid.tolist()

# grid represents crossword puzzle grid of black and white squares where 1 is black and 0 is white.
# create an image of the grid using matplotlib
def plot_crossword_grid(grid, filename='crossword_grid.png', black_prob=None):
    # Convert the grid to a numpy array
    grid_array = np.array(grid)
    nrows, ncols = grid_array.shape
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    # Display the grid as an image with 1 as black and 0 as white
    ax.imshow(grid_array, cmap='binary', interpolation='nearest')
    # Draw black borders around each square
    for i in range(nrows):
        for j in range(ncols):
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, linewidth=1, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
    # Set the ticks to be empty
    ax.set_xticks([])
    ax.set_yticks([])
    # Set the aspect ratio to be equal
    ax.set_aspect('equal')
    # Set the title, including black_prob if provided
    if black_prob is not None:
        ax.set_title(f'Crossword Puzzle Grid (black_prob={black_prob:.2f})', fontsize=16)
    else:
        ax.set_title('Crossword Puzzle Grid', fontsize=16)
    # Show the grid
    plt.show()
    # Save the grid as an image
    fig.savefig(filename, bbox_inches='tight', dpi=300)

# Example usage:
grid = [
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1], 
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0]
]

print(grid)

# Example usage:
# plot_crossword_grid(grid)

tmp_folder = "/tmp"
os.makedirs(tmp_folder, exist_ok=True)

for i in range(5):
    black_prob = random.uniform(0.15, 0.5)
    new_grid = generate_symmetric_crossword_grid(size=8, min_run=3, black_prob=black_prob)
    filename = os.path.join(
        tmp_folder,
        f'symmetric_crossword_grid_{i:02d}_bp_{black_prob:.2f}.png'
    )
    plot_crossword_grid(new_grid, filename=filename, black_prob=black_prob)
