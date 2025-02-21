import gym, copy

from pct.environments import GenericGym


from pct.functions import Constant


steps=1

test = 2

if test ==2:
    env = gym.make('LunarLanderContinuous-v2')
    print(env.action_space) 
    print(env.continuous)
    env1 = copy.deepcopy(env)
    # env1.continuous = True
    print(env1.action_space)
    print(env1.continuous)
    env.close()
    env1.close()



if test ==1:

    mc = GenericGym(render=True, seed=93, gym_name='LunarLanderContinuous-v2') 
    mc.add_link(Constant(1))
    mc.add_link(Constant(2))
    print(mc.get_config())

    for i in range(100):
        mc.run(steps=steps, verbose=True)
    mc.close()
