

from pct.environments import WindTurbine

from pct.functions import Constant


steps=1

test = 1

if test ==1:
    # seed 3 circles anti-clockwise
    yaw = WindTurbine() 
    yaw.add_link(Constant(0))
    env_props={'series': 'steady'}
    yaw.set_properties(env_props)
    print(yaw.get_config())

    for i in range(100):
        yaw.run(steps=steps, verbose=True)
    yaw.close()

    # git test

