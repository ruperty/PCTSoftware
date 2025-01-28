

from pct.environments import Pendulum
from pct.environments import CartPoleV1, MountainCarContinuousV0


from pct.functions import Constant


steps=1

test = 1


if test ==1:
    import gym
    envs = [ 'CartPole-v1', 'MountainCarContinuous-v0', 'Pendulum-v1']
    for env_name in envs:
        env = gym.make(env_name) 
        env.reset()
        print(env_name)
        print("Observation space:", env.observation_space)
        print("Observation sample:", env.observation_space.sample())
        # as = env.action_space
        print("Action space:", env.action_space)
        # print("Action space:", as)
        action = env.action_space.sample()
        print("Action sample:", action)
        obs = env.step(action)
        print(obs)
        print()
        env.close()

