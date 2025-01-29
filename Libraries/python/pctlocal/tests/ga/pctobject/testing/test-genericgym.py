
import gym
import numpy as np

test = 0

# class to extract the information from a gym environment for the action_space
# create a method to extract the minimum and maximum values of the action space
# create a method to extract the number of actions possible
# create a method to extract the number of states possible
# create a method to take a set of values and map them to the action space

class GymEnvInfo:
    def __init__(self, env):
        self.action_space =  env.action_space
        self.observation_space = env.observation_space
        self.num_actions = self.get_num_actions()


    def get_action_space_bounds(self):
        print(self.action_space)
        if isinstance(self.action_space, gym.spaces.box.Box):
            return self.action_space.low, self.action_space.high
        elif isinstance(self.action_space, gym.spaces.discrete.Discrete):
            return self.action_space.n -1

    def get_num_actions(self):
        if isinstance(self.action_space, gym.spaces.discrete.Discrete):
            return self.action_space.n
        elif isinstance(self.action_space, gym.spaces.box.Box):
            return self.action_space.shape[0]
        else:
            return None

    def get_num_states(self):
        if hasattr(self.observation_space, 'shape'):
            return self.observation_space.shape[0]
        else:
            return None

    def map_values_to_action_space(self, values):
        if isinstance(self.action_space, gym.spaces.box.Box):
            vals = np.clip(values, self.action_space.low, self.action_space.high)
            return vals
        if isinstance(self.action_space, gym.spaces.discrete.Discrete):
            return values

if test == 0:
    # Example usage:
    # env_info = GymEnvInfo('CartPole-v1')
    env_name = 'MountainCarContinuous-v0'
    env = gym.make(env_name) 
    env_info = GymEnvInfo(env)
    print("Action space bounds:", env_info.get_action_space_bounds())
    print("Number of actions:", env_info.get_num_actions())
    print("Number of input states:", env_info.get_num_states())
    # print("Mapped values to action space:", env_info.map_values_to_action_space([0.5]))
    print("Mapped values to action space:", env_info.map_values_to_action_space([3]))



if test ==1:
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

