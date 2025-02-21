

from pct.environments import GenericGym


from pct.functions import Constant


steps=1

test = 1

if test ==1:
    # seed 3 circles anti-clockwise
    mc = GenericGym(render=True, seed=93, gym_name='LunarLanderContinuous-v2') 
    mc.add_link(Constant(1))
    mc.add_link(Constant(2))
    print(mc.get_config())

    for i in range(100):
        mc.run(steps=steps, verbose=True)
    mc.close()
