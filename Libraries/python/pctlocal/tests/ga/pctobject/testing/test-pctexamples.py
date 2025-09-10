
from pct.pctexamples import PCTExamples 
import getpass

# Define the config file path
user = getpass.getuser()
config_file = f'C:/Users/{user}/Versioning/python/nbdev/pct/nbs/testfiles/MountainCar/MountainCar-cdf7cc.properties'


# Create only video (no plots)

test = "draw"
# test = "run"
# test = "video"


if test == "draw":
    result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=False,
        run_hierarchy=False,
        image_params={
            'file': '/tmp/mountaincar_image.png',
            # 'move': {'IV':[0, 0.6],'IP':[-0.6, 0.3],  'OL0C0sm':[-0.28, -0.2],'OL0C1sm':[0.28, -0.2], 'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]},
            'move': {'IV':[0, 0.05],'IP':[-0.6, 0.3],  'OL0C0sm':[-0.28, -0.2],'OL0C1sm':[0.28, -0.2], 'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]},
            'with_labels': True,
            'with_edge_labels': True,
            # 'funcdata': True,
            'font_size': 6,
            'node_size': 200
        },
        get_model_details=True
    )

#  


    

if test == "run":
    result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=False,
        run_hierarchy=True,
        steps=200,
        verbose=True,
        render=True,
        early_termination=True
    )

if test == "video":
    # Create video and plots
    result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=False,
        run_hierarchy=True,
        steps=200,
        render=True,
        # verbose=True,
        early_termination=True,
        video_params={
            'fps': 30,
            'filename': '/tmp/mountaincar_simulation_video.mp4'
        }
    )

print("Result:", result)
