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
def plot_crossword_grid(grid, filename='crossword_grid.png', black_prob=None, check_validity=True):
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
    
    # Check validity if requested
    validity_str = ""
    if check_validity:
        is_valid = is_valid_crossword_grid(grid_array)
        validity_str = " (VALID)" if is_valid else " (INVALID - has words < 3 letters)"
    
    # Set the title, including grid size, validity, and black_prob if provided
    grid_size_str = f'{nrows}x{ncols}'
    if black_prob is not None:
        ax.set_title(f'Crossword Puzzle Grid {grid_size_str}{validity_str} (black_prob={black_prob:.2f})', fontsize=14)
    else:
        ax.set_title(f'Crossword Puzzle Grid {grid_size_str}{validity_str}', fontsize=14)
    # Show the grid
    # plt.show()
    # Save the grid as an image
    fig.savefig(filename, bbox_inches='tight', dpi=300)


def extract_center_subgrid(grid: np.ndarray, subgrid_size: int) -> np.ndarray:
    """
    Extract a subgrid from the center of the main grid.
    
    Parameters:
    - grid: np.ndarray, the main grid (2D array)
    - subgrid_size: int, the size of the square subgrid to extract
    
    Returns:
    - subgrid: np.ndarray of shape (subgrid_size, subgrid_size)
    
    Raises:
    - ValueError: if subgrid_size is larger than the main grid or if subgrid_size is even
    """
    if len(grid.shape) != 2 or grid.shape[0] != grid.shape[1]:
        raise ValueError("Grid must be a square 2D array")
    
    main_size = grid.shape[0]
    
    if subgrid_size > main_size:
        raise ValueError(f"Subgrid size ({subgrid_size}) cannot be larger than main grid size ({main_size})")
    
    if subgrid_size % 2 == 0:
        raise ValueError("Subgrid size must be odd to have a clear center")
    
    # Calculate the starting position for the center extraction
    start_pos = (main_size - subgrid_size) // 2
    end_pos = start_pos + subgrid_size
    
    # Extract the subgrid
    subgrid = grid[start_pos:end_pos, start_pos:end_pos]
    
    return subgrid


def is_valid_crossword_grid(grid: np.ndarray, min_word_length: int = 3) -> bool:
    """
    Check if a crossword grid is valid by ensuring all white cells are part of words
    that are at least min_word_length long in both horizontal and vertical directions.
    
    Parameters:
    - grid: np.ndarray, binary grid where 1=black, 0=white
    - min_word_length: int, minimum required word length (default 3)
    
    Returns:
    - bool: True if all white cells are part of valid words, False otherwise
    """
    rows, cols = grid.shape
    
    # For each white cell, check if it's part of valid words in both directions
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 0:  # White square
                # Check horizontal word length containing this cell
                h_start = col
                h_end = col
                
                # Find start of horizontal word
                while h_start > 0 and grid[row, h_start - 1] == 0:
                    h_start -= 1
                
                # Find end of horizontal word
                while h_end < cols - 1 and grid[row, h_end + 1] == 0:
                    h_end += 1
                
                h_word_length = h_end - h_start + 1
                
                # Check vertical word length containing this cell
                v_start = row
                v_end = row
                
                # Find start of vertical word
                while v_start > 0 and grid[v_start - 1, col] == 0:
                    v_start -= 1
                
                # Find end of vertical word
                while v_end < rows - 1 and grid[v_end + 1, col] == 0:
                    v_end += 1
                
                v_word_length = v_end - v_start + 1
                
                # Both horizontal and vertical words must meet minimum length
                # (unless one direction has only 1 cell, which means it's not really a word)
                if h_word_length > 1 and h_word_length < min_word_length:
                    return False
                if v_word_length > 1 and v_word_length < min_word_length:
                    return False
    
    return True

num=2
grid = extract_binary_crossword_grid(f"/tmp/cw{num}.png", grid_size=15)
print("Full grid:")
print(grid.tolist())
print(f"Grid size: {grid.shape[0]}x{grid.shape[1]}")

# Extract subgrids for all odd numbers from 5 upwards
main_size = grid.shape[0]
subgrids = {}

print(f"\nExtracting center subgrids for all odd sizes from 5 to {main_size}:")
for size in range(5, main_size + 1, 2):  # Start at 5, go up by 2 (odd numbers only)
    try:
        subgrid = extract_center_subgrid(grid, size)
        subgrids[size] = subgrid
        is_valid = is_valid_crossword_grid(subgrid)
        validity_status = "VALID" if is_valid else "INVALID (has words < 3 letters)"
        print(f"\nCenter {size}x{size} subgrid [{validity_status}]:")
        print(subgrid.tolist())
    except ValueError as e:
        print(f"Error extracting {size}x{size} subgrid: {e}")

# Plot the full grid
plot_crossword_grid(grid, filename=f'/tmp/crossword_grid{num}.png', black_prob=None)

# Plot all the center subgrids
print(f"\nGenerating visualization files for all subgrids...")
for size, subgrid in subgrids.items():
    filename = f'/tmp/center_subgrid_{size}x{size}.png'
    plot_crossword_grid(subgrid, filename=filename, black_prob=None)
    print(f"Saved: {filename}")

print(f"\nGenerated {len(subgrids)} subgrid visualizations.")
