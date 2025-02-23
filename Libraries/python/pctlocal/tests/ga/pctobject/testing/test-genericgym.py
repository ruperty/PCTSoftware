import gym, copy
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from pct.environments import GenericGym


from pct.functions import Constant


steps=1

test = 3

if test == 3:
    print()
    print("***")
    env = gym.make('LunarLanderContinuous-v2')
    # env.reset(seed=1, return_info=False)
    env.reset(seed=1)
    action = [0, 0]
    obs, reward, done, info = env.step(action)
    # print(obs)
    print([f'{i:4.5f}' for i in obs], f'{reward:4.8f}')
    action = [-0.073, 1.076 ]
    obs, reward, done, info = env.step(action)
    print([f'{i:4.5f}' for i in obs], f'{reward:4.8f}')
    # print(obs)
    env.close()

if test ==2:
    env = gym.make('LunarLanderContinuous-v2')
    print("action_space", env.action_space) 
    print("continuous", env.continuous)
    print(getattr(env, "__deepcopy__", None))
    env1 = copy.deepcopy(env)
    # env1.continuous = True
    print("action_space", env1.action_space) 
    print("continuous", env1.continuous)
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
