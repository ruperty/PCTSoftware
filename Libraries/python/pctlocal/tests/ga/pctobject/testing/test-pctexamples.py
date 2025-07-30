
from pct.pctexamples import PCTExamples 

# Define the config file path
config_file = 'C:/Users/ryoung/Versioning/python/nbdev/pct/nbs/testfiles/MountainCar/MountainCar-cdf7cc1497ad143c0b04a3d9e72ab783.properties'


# Create only video (no plots)

test = 1

if test == 1:
    video_result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=True,
        run_hierarchy=True,
        steps=200,
        verbose=True,
        render=True,
        early_termination=True
    )

if test == 2:
    # Create video and plots
    video_result = PCTExamples.run_example(
        config_file=config_file,
        print_summary=True,
        run_hierarchy=True,
        steps=1000,
        verbose=True,
        video_params={
            'fps': 30,
            'filename': '/tmp/mountaincar_simulation_video.mp4'
        }
    )

