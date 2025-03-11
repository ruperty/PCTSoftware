# in a loop create a new lunarlandercontinuous environment, reset it, and render it and then close it.
# record the image of the render for each loop iteration.
# after the loop, create a video from the recorded images.

import gym, copy
import warnings     
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

# create a loop to create a video of the lunarlander environment
# create a directory to store the images    
os.makedirs("images", exist_ok=True)
# create a new lunarlander environment
env = gym.make('LunarLanderContinuous-v2')
# create a figure
fig = plt.figure()
# create an empty list to store the images
frames = []
print()
print("Observation space:", env.observation_space)
# create a loop to render the environment and store the images
for i in range(20):
# reset the environment
    obs = env.reset(seed=i)
    print(f"Loop {i:02d}: obs = {[f'{x:+.3f}' for x in obs]}")
    # render the environment
    frames.append( env.render(mode='rgb_array'))
    # take a step in the environment
    # action = [0, 0]
    # obs, reward, done, info = env.step(action)
    # if done:
    #     break
# close the environment
env.close()

patch = plt.imshow(frames[0])
plt.axis('off')
def animate(i):
    patch.set_data(frames[i])
anim = animation.FuncAnimation(plt.gcf(), animate, \
                               frames=len(frames), interval=100)
anim.save('random_agent.gif', writer='imagemagick')# display the animation
plt.show()


