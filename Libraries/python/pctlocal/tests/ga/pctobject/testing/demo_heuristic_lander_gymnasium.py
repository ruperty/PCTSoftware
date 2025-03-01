
import gymnasium as gym
from gymnasium.utils.step_api_compatibility import step_api_compatibility
from gymnasium.envs.box2d.lunar_lander import heuristic

def demo_heuristic_lander(env, seed=None, render=False):
    total_reward = 0
    steps = 0
    s, info = env.reset(seed=seed)
    while True:
        a = heuristic(env, s)
        s, r, terminated, truncated, info = step_api_compatibility(env.step(a), True)
        total_reward += r

        if render:
            still_open = env.render()
            if still_open is False:
                break

        if steps % 20 == 0 or terminated or truncated:
            print("observations:", " ".join([f"{x:+0.2f}" for x in s]), f' {r:+0.2f}')
            print(f"step {steps} total_reward {total_reward:+0.2f}")
        if r > 9:
            print(f'>>> step {steps}', " ".join([f"{x:+0.2f}" for x in s]) ,f'reward {r:+0.2f}')
        steps += 1
        if terminated or truncated:
            break
    if render:
        env.close()
    return total_reward




if __name__ == "__main__":
    env = gym.make("LunarLander-v3", render_mode="human")
    demo_heuristic_lander(env, render=True)
