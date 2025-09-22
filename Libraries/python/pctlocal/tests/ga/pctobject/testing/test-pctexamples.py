
from pct.pctexamples import PCTExamples  # type: ignore
import getpass
import os
import pathlib

# Get the home directory (works across platforms)
home_dir = str(pathlib.Path.home())
print(f"Home directory: {home_dir}")

# We don't need the username anymore since we're using the home directory
# user = os.environ.get('USERNAME') or os.environ.get('USER') or getpass.getuser()
# print(f"Detected username: {user}")


env = "LunarLander"
# env = "MountainCar"

test = "draw"
# test = "run"
test = "video"
suffixes = True

if env == "LunarLander":
    config_file = os.path.join(home_dir, 'Versioning/python/nbdev/pct/nbs/testfiles/LunarLander/LunarLander-4905d2.properties')
    # Use normalized path with OS-specific separators
    config_file = os.path.normpath(config_file)
    if not os.path.exists(config_file):
        print(f"WARNING: Config file not found: {config_file}")
        print("Please update the path to point to the correct location.")
    suffixes = False
    # Configure positions for the LunarLander control unit elements, arranging them from left to right
    # The format is 'element_name': [x_position, y_position]
    move = {
        # Input nodes (sensor variables)
        'IX': [-0.5, 0],          # X position
        'IY': [-0.5, 0],       # Y position
        'IVX': [-0.5, 0],      # X velocity
        'IVY': [-0.5, 0],      # Y velocity
        'IA': [-0.5, 0],       # Angle
        'IVA': [-0.5, 0],      # Angular velocity
        'ILC': [-0.5, 0],      # Left contact
        'IRC': [-0.5, 0],      # Right contact

        # References
        'RL0C0c': [-0.6, 0], # X position reference
        'RL0C1c': [-0.15, 0], # Y position reference
        'RL0C2c': [0.3, 0], # X velocity reference
        'RL0C3c': [0.65, 0], # Y velocity reference
        'RL0C4c': [0.9, 0], # Angle reference
        'RL0C5c': [1.4, 0], # Angular velocity reference
        
        # # # Perceptual functions
        'PL0C0ws': [-0.8, 0], # X position perception
        'PL0C1ws': [-0.35, 0], # Y position perception
        'PL0C2ws': [0.1, 0], # X velocity perception
        'PL0C3ws': [0.45, 0], # Y velocity perception
        'PL0C4ws': [0.75, 0], # Angle perception
        'PL0C5ws': [1.1, 0], # Angular velocity perception

        # # # Comparator functions
        'CL0C0': [-0.95, 0],     # X position comparator
        'CL0C1': [-0.35, 0],  # Y position comparator
        'CL0C2': [0.25, 0],  # X velocity comparator
        'CL0C3': [0.75, 0],  # Y velocity comparator
        'CL0C4': [1.25, 0],  # Angle comparator
        'CL0C5': [1.85, 0],  # Angular velocity comparator

        # # # Output functions
        # 'OL0C0p': [-0.5, 0],    # X position output
        # 'OL0C1p': [0, 0], # Y position output
        # 'OL0C2p': [0.65, 0], # X velocity output
        # 'OL0C3p': [0.85, 0], # Y velocity output
        # 'OL0C4p': [1.5, 0], # Angle output
        # 'OL0C5p': [2, 0], # Angular velocity output

        'OL0C0p': [-1.85, 0],    # X position output
        'OL0C1p': [-0.9, 0], # Y position output
        'OL0C2p': [0.2, 0], # X velocity output
        'OL0C3p': [0.75, 0], # Y velocity output
        'OL0C4p': [1.8, 0], # Angle output
        'OL0C5p': [2.75, 0], # Angular velocity output

        # Action output nodes
        'Action1sg': [0.5, 0], # Main engine
        'Action2sg': [1.5, 0], # Left-right engine
        
        # Environment
        'GenericGym': [0, -0.1] # The environment node
    }

if env == "MountainCar":
    config_file = os.path.join(home_dir, 'Versioning/python/nbdev/pct/nbs/testfiles/MountainCar/MountainCar-cdf7cc.properties')
    # Use normalized path with OS-specific separators
    config_file = os.path.normpath(config_file)
    if not os.path.exists(config_file):
        print(f"WARNING: Config file not found: {config_file}")
        print("Please update the path to point to the correct location.")
    move = {'IV':[0, 0.05],'IP':[-0.6, 0.3],  'OL0C0sm':[-0.28, -0.2],'OL0C1sm':[0.28, -0.2], 'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}
    # suffixes = False


if test == "draw":
    result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=False,
        run_hierarchy=False,
        image_params={
            'file': f'/tmp/{env}_image.png',
            'move': move,
            'with_labels': True,
            'with_edge_labels': True,
            'funcdata': False,
            'font_size': 6,
            'node_size': 200,
            'layout_seed': 42
        },
        get_model_details=True
        # ,
        # suffixes=suffixes
    )


if test == "run":
    result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=False,
        run_hierarchy=True,
        steps=500,
        verbose=False,
        render=True,
        early_termination=True
    )

if test == "video":
    # Check if config file exists before attempting to run
    if not os.path.exists(config_file):
        print(f"ERROR: Cannot run example because config file does not exist: {config_file}")
        print("Please update the path to point to the correct location.")
    else:
        # Create video and plots
        result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=False,
        run_hierarchy=True,
        steps=500,
        render=True,
        # verbose=True,
        early_termination=True,
        video_params={
            'fps': 30,
            'filename': f'/tmp/{env}_simulation_video.mp4'
        }
    )

# Print the result if it exists
if 'result' in locals():
    print("Result:", result)
else:
    print("No result was produced. Check the errors above.")
