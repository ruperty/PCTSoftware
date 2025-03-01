
import gym
from gym.envs.box2d.lunar_lander import heuristic
from gym.envs.box2d.lunar_lander import LunarLander

def demo_heuristic_lander(env, seed=None, render=False):
    total_reward = 0
    steps = 0
    s = env.reset(seed=seed)
    while True:
        a = heuristic(env, s)
        s, r, done, info = env.step(a)
        total_reward += r

        if render:
            still_open = env.render()
            if still_open is False:
                break

        if steps % 20 == 0 or done:
            print("observations:", " ".join([f"{x:+0.2f}" for x in s]), f' {r:+0.2f}')
            print(f"step {steps} total_reward {total_reward:+0.2f}")
        if r > 9 or r < -9:
            print(f'>>> step {steps}', " ".join([f"{x:+0.2f}" for x in s]) ,f'reward {r:+0.2f}')
        steps += 1
        if done:
            break
    if render:
        env.close()
    return total_reward




if __name__ == "__main__":
    demo_heuristic_lander(LunarLander(), render=True)
