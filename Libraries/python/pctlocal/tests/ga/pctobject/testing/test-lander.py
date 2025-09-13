import gym, copy
import warnings     
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

def capture_lunar_lander_initializations(num_frames=20, seed_start=0, filename='random_agent.gif'):
    """
    Creates a GIF animation showing different initializations of the LunarLanderContinuous-v2 environment.
    
    This function initializes the environment multiple times with different seeds,
    captures the initial state of each initialization as a frame, and combines
    these frames into a GIF animation. This demonstrates the variety of starting
    conditions in the lunar lander environment without taking any actions.
    
    Parameters:
    -----------
    num_frames : int
        Number of environment initializations to capture (default: 20)
    seed_start : int
        Starting seed value for environment resets (default: 0)
    filename : str
        Name of the output GIF file (default: 'random_agent.gif')
        
    Returns:
    --------
    frames : list
        List of frames (numpy arrays) captured from the environment
    """
    # Create a directory to store images if needed
    os.makedirs("images", exist_ok=True)
    
    # Create a new LunarLander environment
    env = gym.make('LunarLanderContinuous-v2')
    
    # Create a figure for the animation
    fig = plt.figure()
    
    # Create an empty list to store the frames
    frames = []
    
    print()
    print("Observation space:", env.observation_space)
    
    # Loop to capture frames from different environment initializations
    for i in range(num_frames):
        # Reset the environment with a different seed each time
        obs = env.reset(seed=i+seed_start)
        print(f"Loop {i:02d}: obs = {[f'{x:+.3f}' for x in obs]}")
        
        # Render the environment and store the frame
        frames.append(env.render(mode='rgb_array'))
    
    # Close the environment
    env.close()
    
    # Create the animation
    patch = plt.imshow(frames[0])
    plt.axis('off')
    
    def animate(i):
        patch.set_data(frames[i])
    
    # Generate the animation and save it
    anim = animation.FuncAnimation(plt.gcf(), animate, 
                                  frames=len(frames), interval=100)
    anim.save(filename, writer='imagemagick')
    
    # Display the animation
    plt.show()
    
    return frames

# Execute the function to create the animation
if __name__ == "__main__":
    capture_lunar_lander_initializations()


