
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 

def extract_binary_crossword_grid(filename: str, grid_size: int = 23, threshold: int = 128):
    """
    Load a grayscale crossword image and return a binary 2D grid representing black/white squares.

    Parameters:
    - filename: str, path to the image file
    - grid_size: int, number of squares per row/column
    - threshold: int, grayscale threshold to determine black (1) vs white (0)

    Returns:
    - binary_grid: np.ndarray of shape (grid_size, grid_size), dtype=int
    """
    img = Image.open(filename).convert("L")
    width, height = img.size

    dx = width / grid_size
    dy = height / grid_size

    binary_grid = np.zeros((grid_size, grid_size), dtype=int)

    for row in range(grid_size):
        for col in range(grid_size):
            x = int((col + 0.5) * dx)
            y = int((row + 0.5) * dy)
            pixel_value = img.getpixel((x, y))
            binary_grid[row, col] = 1 if pixel_value < threshold else 0

    return binary_grid


def render_crossword_image(binary_grid: np.ndarray, square_size: int = 32) -> Image.Image:
    """
    Render a crossword-style image from a binary grid.

    Parameters:
    - binary_grid: 2D numpy array (1=black, 0=white)
    - square_size: size of each square in pixels

    Returns:
    - PIL.Image.Image: rendered crossword image
    """
    grid_size = binary_grid.shape[0]
    img_size = grid_size * square_size

    # Create a blank (white) image
    img = Image.new("L", (img_size, img_size), color=255)

    # Draw each square
    for row in range(grid_size):
        for col in range(grid_size):
            color = 0 if binary_grid[row, col] == 1 else 255
            for y in range(row * square_size, (row + 1) * square_size):
                for x in range(col * square_size, (col + 1) * square_size):
                    img.putpixel((x, y), color)

    return img


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


grid = extract_binary_crossword_grid("/tmp/cw.png", grid_size=15)
print(grid)

# Assume 'grid' is a 23x23 array of 0s and 1s
# image = render_crossword_image(grid, square_size=32)
# image.save("rendered_crossword.png")
# image.show()


plot_crossword_grid(grid, filename='crossword_grid.png', black_prob=None)
