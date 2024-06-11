import numpy as np
import drl_microgrid_ems.tcl_env_dqn as drlmg0

from matplotlib import pyplot
from tqdm import tqdm
from pct.environments import MicroGrid
from pct.putils import Timer
from pct.microgrid import MicroGridEnv0Plus, MicroGridEnvPlus

steps=1

# test = "mg+reset"
test = "mg+days"


if test == "mg+days":
    its=48
    env = MicroGridEnvPlus()
    properties = {'day_mode' : 'ordered', 'initial_day' :1 }
    env.seed(1)
    env.initialise(properties)
    state = env.reset()
    action = [2,2,1,1]
    for it in range(its): 
        state, reward, done, _ = env.step(action)
        print(it, env.day, [eval(f'{i:4.3f}') for i in state[:3]], f'{reward:4.3f}', state[102]*(its-1))
        if (it + 1) % 24 == 0:
            env.reset()



if test == "mg0+days":
    its=264
    env = MicroGridEnv0Plus()
    properties = {'iterations' : its, 'day_mode' : 'ordered', 'initial_day' :1 }
    env.seed(1)
    env.initialise(properties)
    state = env.reset()
    action = [2,2,1,1]
    for it in range(its): 
        state, reward, terminal, _ = env.step(action)
        print(it, env.day, [eval(f'{i:4.3f}') for i in state], f'{reward:4.3f}', state[7]*24)
        if (it + 1) % 24 == 0:
            env.reset()


if test == "mg0+reset":
    env = MicroGridEnv0Plus()
    properties = {'iterations' : 24, 'day_mode' : 'ordered', 'initial_day' :1 }
    env.seed(1)
    env.initialise(properties)
    action = [2,2,1,1]
    for i in range(2): 
        for day in range(1,11,1): 
            state = env.reset(day=day)
            state, reward, terminal, _ = env.step(action)
            print([eval(f'{i:4.3f}') for i in state], reward, state[7]*24)





if test == 3:
    env = drlmg0.MicroGridEnv0()
    env.seed(1)
    state = env.reset(day=1)
    action = [2,2,1,1]
    state, reward, terminal, _ = env.step(action)
    print([eval(f'{i:4.3f}') for i in state], reward)
    # env = MicroGridEnv()
    # env.seed(1)
    state = env.reset(day=1)
    state, reward, terminal, _ = env.step(action)
    print([eval(f'{i:4.3f}') for i in state], reward)

if test == 1:
    env = MicroGrid(seed=1)
    env(True)
    env.summary()


if test == 2:

    timer = Timer()
    # Initialize the environment
    env = drlmg0.MicroGridEnv0()
    env.seed(1)
    # Save the rewards in a list
    rewards = []
    # reset the environment to the initial state
    state = env.reset()
    # Call render to prepare the visualization
    env.render()
    ctr = 1
    # Interact with the environment (here we choose random actions) until the terminal state is reached
    timer.start()
    while True:
        # Pick an action from the action space (here we pick an index between 0 and 80)
        action = env.action_space.sample()
        # Using the index we get the actual action that we will send to the environment
        # print(ACTIONS[action])
        # Perform a step in the environment given the chosen action
        state, reward, terminal, _ = env.step(action)
        env.render()
        # print(ctr, state, reward, terminal)
        rewards.append(reward)
        ctr += 1
        if terminal:
            break

    print(ctr)
    timer.stop()
    print("Total Reward:",sum(rewards))
    print(f'Mean time: {timer.mean()}')
    
    
