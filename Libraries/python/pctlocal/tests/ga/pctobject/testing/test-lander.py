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
    
    # Save frames as a video/gif using Pillow instead of matplotlib
    from PIL import Image
    
    # Convert frames to PIL Images
    pil_frames = [Image.fromarray(frame) for frame in frames]
    
    # Save as GIF
    if filename.endswith('.gif'):
        print(f"Saving animation as GIF: {filename}")
        pil_frames[0].save(
            filename,
            save_all=True,
            append_images=pil_frames[1:],
            optimize=False,
            duration=100,  # Duration between frames in milliseconds
            loop=0  # 0 means loop forever
        )
    # Save as MP4 using Pillow and imageio
    elif filename.endswith('.mp4'):
        try:
            import imageio
            print(f"Saving animation as MP4: {filename}")
            imageio.mimsave(filename, frames, fps=10)
        except ImportError:
            # Fall back to GIF if imageio is not available
            new_filename = filename.replace('.mp4', '.gif')
            print(f"imageio not available, saving as GIF instead: {new_filename}")
            pil_frames[0].save(
                new_filename,
                save_all=True,
                append_images=pil_frames[1:],
                optimize=False,
                duration=100,
                loop=0
            )
            filename = new_filename
    
    print(f"Animation saved as {filename}")
    
    # Display the animation (still using matplotlib for display only)
    patch = plt.imshow(frames[0])
    plt.axis('off')
    plt.show()
    
    return frames

def run_lunar_lander_with_random_actions(max_steps=200, seed=42, filename='random_actions.mp4'):
    """
    Runs the LunarLanderContinuous-v2 environment with random actions and records a video.
    
    This function creates a single run of the environment, taking random actions at each step,
    and records the entire episode as a video file.
    
    Parameters:
    -----------
    max_steps : int
        Maximum number of steps to run the environment (default: 200)
    seed : int
        Seed value for environment initialization and random actions (default: 42)
    filename : str
        Name of the output video file (default: 'random_actions.mp4')
        
    Returns:
    --------
    tuple
        (frames, total_reward) - List of frames captured and the total reward obtained
    """
    # Set random seed for reproducibility
    np.random.seed(seed)
    
    # Create a new LunarLander environment
    env = gym.make('LunarLanderContinuous-v2')
    
    # Reset the environment with the specified seed
    observation = env.reset(seed=seed)
    
    # Create an empty list to store the frames
    frames = []
    
    # Track total reward
    total_reward = 0
    
    print(f"\nStarting LunarLander random action run (seed: {seed})")
    print(f"Action space: {env.action_space}")
    
    # Run the environment for max_steps or until done
    for step in range(max_steps):
        # Generate a random action
        # For LunarLanderContinuous-v2, action is [main_engine, left_right_engine]
        # Each value is in range [-1, 1]
        action = env.action_space.sample()
        
        # Take a step in the environment
        observation, reward, done, info = env.step(action)
        
        # Update total reward
        total_reward += reward
        
        # Render and capture the frame
        frames.append(env.render(mode='rgb_array'))
        
        # Print progress every 20 steps
        if step % 20 == 0:
            print(f"Step {step}: Action {[f'{a:.2f}' for a in action]}, Reward {reward:.2f}, Total {total_reward:.2f}")
        
        # Stop if the episode is done
        if done:
            print(f"Episode finished after {step+1} steps with total reward {total_reward:.2f}")
            break
    
    # Close the environment
    env.close()
    
    # Create animation and save as video
    print(f"Creating video with {len(frames)} frames...")
    
    # Save frames as a video/gif using Pillow instead of matplotlib
    from PIL import Image
    
    # Convert frames to PIL Images
    pil_frames = [Image.fromarray(frame) for frame in frames]
    
    # Save as GIF
    if filename.endswith('.gif'):
        print(f"Saving animation as GIF: {filename}")
        pil_frames[0].save(
            filename,
            save_all=True,
            append_images=pil_frames[1:],
            optimize=False,
            duration=50,  # Duration between frames in milliseconds
            loop=0  # 0 means loop forever
        )
    # Save as MP4 using Pillow and imageio
    elif filename.endswith('.mp4'):
        try:
            import imageio
            print(f"Saving animation as MP4: {filename}")
            imageio.mimsave(filename, frames, fps=30)
        except ImportError:
            # Fall back to GIF if imageio is not available
            new_filename = filename.replace('.mp4', '.gif')
            print(f"imageio not available, saving as GIF instead: {new_filename}")
            pil_frames[0].save(
                new_filename,
                save_all=True,
                append_images=pil_frames[1:],
                optimize=False,
                duration=50,
                loop=0
            )
            filename = new_filename
    
    print(f"Animation saved as {filename}")
    
    # Display the animation (still using matplotlib for display only)
    # fig, ax = plt.subplots(figsize=(8, 6))
    # patch = plt.imshow(frames[0])
    # plt.axis('off')
    # plt.tight_layout()
    # plt.show()
    
    return frames, total_reward

# Execute the functions to create animations
if __name__ == "__main__":
    # Uncomment the function you want to run
    # capture_lunar_lander_initializations()
    run_lunar_lander_with_random_actions(seed=4)


