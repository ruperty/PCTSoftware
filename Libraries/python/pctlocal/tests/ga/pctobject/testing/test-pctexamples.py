
from pct.pctexamples import PCTExamples 

# Define the config file path
config_file = 'C:/Users/ryoung/Versioning/python/nbdev/pct/nbs/testfiles/MountainCar/MountainCar-cdf7cc1497ad143c0b04a3d9e72ab783.properties'


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
            'move': {'IV':[0, 0.6],'IP':[-0.6, 0.3],  'OL0C0sm':[-0.28, -0.2],'OL0C1sm':[0.28, -0.2], 'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]},
            'with_labels': True,
            'with_edge_labels': True,
            # 'funcdata': True,
            'font_size': 8,
            'node_size': 200
        }
    )

# with_labels=True, with_edge_labels=False,  font_size=12, font_weight='bold', font_color='black', 
            # color_mapping={'PL':'aqua','OL':'limegreen','CL':'goldenrod', 'RL':'red', 'I':'silver', 'A':'yellow'},
            # node_size=500, arrowsize=25, align='horizontal', file=None, figsize=(8,8), move={}, draw_fig=True,
            # node_color=None, layout={'r':2,'c':1,'p':2, 'o':0}, funcdata=False, interactive_mode=False, experiment=None):
    

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
