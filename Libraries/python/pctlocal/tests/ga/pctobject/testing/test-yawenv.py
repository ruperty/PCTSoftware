

from pct.environments import WindTurbine

from pct.functions import Constant


steps=1

test = 1

if test ==1:
    # seed 3 circles anti-clockwise
    yaw = WindTurbine() 
    con = Constant(1, namespace=yaw.namespace)
    yaw.add_link(con)
    env_props={'series': 'steady'}
    yaw.set_properties(env_props)
    print(yaw.get_config())
    actions = [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,1,1,1,1,1,1,1, 1, 1]
    for i in range(len(actions)):
        con.set_value(actions[i])
        print(i, end=" ")
        yaw.run(steps=steps, verbose=True)
        print()
    yaw.close()

    # git test

