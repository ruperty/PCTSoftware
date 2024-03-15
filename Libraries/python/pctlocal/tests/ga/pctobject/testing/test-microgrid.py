import numpy as np
from drl_microgrid_ems.tcl_env_dqn import MicroGridEnv, ACTIONS

# from tcl_env_dqn import MicroGridEnv

from matplotlib import pyplot
from tqdm import tqdm
from pct.environments import MicroGrid
from pct.putils import Timer

steps=1

test = 2

if test == 3:
    env = MicroGridEnv()
    env.seed(1)
    state = env.reset(day=1)
    action = [3,3,1,1]
    state, reward, terminal, _ = env.step(action)
    print(state, reward)

if test == 1:
    env = MicroGrid(seed=1)
    env(True)
    env.summary()


if test == 2:

    timer = Timer()
    # Initialize the environment
    env = MicroGridEnv()
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
    # print(ACTIONS)

    # Plot the TCL SoCs 
    # states = np.array(rewards)
    # pyplot.plot(rewards)
    # pyplot.title("rewards")
    # pyplot.xlabel("Time")
    # pyplot.ylabel("rewards")
    # pyplot.show()

    # con = Constant(1, namespace=yaw.namespace)
    # yaw.add_link(con)
    # env_props={'series': 'steady'}
    # yaw.set_properties(env_props)
    # print(yaw.get_config())
    # actions = [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,1,1,1,1,1,1,1, 1, 1]
    # for i in range(len(actions)):
    #     con.set_value(actions[i])
    #     print(i, end=" ")
    #     yaw.run(steps=steps, verbose=True)
    #     print()
    # yaw.close()

    # git test

