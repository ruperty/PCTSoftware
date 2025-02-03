
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

    def get_env_inputs_names(self):
        ninputs = self.observation_space.shape[0]

        env_inputs_names = [f"I{i}" for i in range(ninputs)]

        return env_inputs_names

    def get_env_inputs_indexes(self):
        ninputs = self.observation_space.shape[0]

        env_inputs_indexes = [i for i in range(ninputs)]

        return env_inputs_indexes

    def get_num_actions(self):
        if isinstance(self.action_space, gym.spaces.discrete.Discrete):
            return 1
        elif isinstance(self.action_space, gym.spaces.box.Box):
            return self.action_space.shape[0]
        else:
            return None

    def get_action_limits(self):
        return self.action_space.low, self.action_space.high

    def get_action_space_bounds(self):
        print(self.action_space)
        if isinstance(self.action_space, gym.spaces.box.Box):
            return self.action_space.low, self.action_space.high
        elif isinstance(self.action_space, gym.spaces.discrete.Discrete):
            if self.action_space.n == 2:
                return np.array([0], dtype=self.action_space.dtype), np.array([1], dtype=self.action_space.dtype)
            elif self.action_space.n == 3:
                return np.array([-1], dtype=self.action_space.dtype), np.array([0], dtype=self.action_space.dtype), np.array([1], dtype=self.action_space.dtype)
        
    

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

    envs = [ 'CartPole-v1', 'MountainCarContinuous-v0', 'Pendulum-v1']
    for env_name in envs:
        env = gym.make(env_name) 
        env_info = GymEnvInfo(env)
        print("get_env_inputs_indexes", env_info.get_env_inputs_indexes())
        print("get_env_inputs_names", env_info.get_env_inputs_names())
        print("self.action_space", env_info.action_space)
        print("get_num_actions", env_info.get_num_actions())
        print("get_action_space_bounds", env_info.get_action_space_bounds())
        print()

        # print("Action space bounds:", env_info.get_action_space_bounds())
        # print("Number of actions:", env_info.get_num_actions())
        # print("Number of input states:", env_info.get_num_states())
        # # print("Mapped values to action space:", env_info.map_values_to_action_space([0.5]))
        # print("Mapped values to action space:", env_info.map_values_to_action_space([3]))



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

