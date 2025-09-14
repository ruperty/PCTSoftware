
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
# test = "video"
suffixes = True

if env == "LunarLander":
    config_file = os.path.join(home_dir, 'Versioning/python/nbdev/pct/nbs/testfiles/LunarLander/LunarLander-4905d2.properties')
    # Use normalized path with OS-specific separators
    config_file = os.path.normpath(config_file)
    if not os.path.exists(config_file):
        print(f"WARNING: Config file not found: {config_file}")
        print("Please update the path to point to the correct location.")
    suffixes = False
    move = {}
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
        print_summary=True,
        run_hierarchy=False,
        image_params={
            'file': f'/tmp/{env}_image.png',
            'move': move,
            'with_labels': True,
            'with_edge_labels': True,
            'funcdata': False,
            'font_size': 6,
            'node_size': 200
        },
        suffixes=suffixes,
        get_model_details=True
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
