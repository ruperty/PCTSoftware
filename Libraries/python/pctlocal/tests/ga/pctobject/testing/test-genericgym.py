
import gym
import numpy as np

test = 0

# class to extract the information from a gym environment for the action_space
# create a method to extract the minimum and maximum values of the action space
# create a method to extract the number of actions possible
# create a method to extract the number of states possible
# create a method to take a set of values and map them to the action space

class GymMetaData:
    def __init__(self, env):
        self.env_name = env.spec.id
        self.action_space =  env.action_space
        self.observation_space = env.observation_space
        self.num_actions = self.get_num_actions()
        self.action_array = True
        if isinstance(self.action_space, gym.spaces.discrete.Discrete):
            self.action_array = False

    def get_env_inputs_names(self):
        ninputs = self.observation_space.shape[0]
        if self.env_name == 'CartPole-v1':
            env_inputs_names = ['ICP', 'ICV', 'IPA', 'IPV']
        else:
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

    def is_action_array(self):
        return self.action_array

    def get_action_limits(self):
        return self.action_space.low, self.action_space.high

    def get_action_space_bounds(self):
        # print(self.action_space)
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

    @classmethod
    def map_values_to_action_space(cls, action_space, values):
        if isinstance(action_space, gym.spaces.box.Box):
            vals = np.clip(values, action_space.low, action_space.high)
            return vals
        if isinstance(action_space, gym.spaces.discrete.Discrete):
            con = action_space.contains(values)
            if action_space.n == 2:
                return np.where(values > 0, 1, 0)
            elif action_space.n == 3:
                return np.where(values > 0, 1, np.where(values < 0, -1, 0))

if test == 0:
    # Example usage:

    # envs = [ 'CartPole-v1']
    envs = [ 'Acrobot-v1', 'CartPole-v1', 'MountainCarContinuous-v0', 'Pendulum-v1']
    for env_name in envs:
        env = gym.make(env_name) 
        env_info = GymMetaData(env)
        print('env_name', env_name)
        print("get_env_inputs_indexes", env_info.get_env_inputs_indexes())
        print("get_env_inputs_names", env_info.get_env_inputs_names())
        print("self.action_space", env_info.action_space)
        print("get_num_actions", env_info.get_num_actions())
        print("get_action_space_bounds", env_info.get_action_space_bounds())
        print("map_values_to_action_space", GymMetaData.map_values_to_action_space(env.action_space, 0.51))
        if env_info.is_action_array():
            print("map_values_to_action_space", GymMetaData.map_values_to_action_space(env.action_space, [-5.1, -.9,.9, 1.2]))

        
        print()


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

if test ==2:
    # import gymnasium as gym

    def get_input_names(env_name):
        # Create the environment
        env = gym.make(env_name)
        
        # Get the observation space
        obs_space = env.observation_space

        # Handle different types of observation spaces
        if isinstance(obs_space, gym.spaces.Dict):
            input_names = list(obs_space.spaces.keys())  # Extract dictionary keys as feature names
        elif isinstance(obs_space, gym.spaces.Box):
            input_names = [f"feature_{i}" for i in range(obs_space.shape[0])]  # Generate generic feature names
        else:
            input_names = ["observation"]  # Default case for Discrete and other spaces

        env.close()  # Close the environment to free resources
        return input_names

    # Example usage
    env_name = "CartPole-v1"  # Change this to your desired environment
    input_features = get_input_names(env_name)
    print(f"Input feature names for {env_name}: {input_features}")
