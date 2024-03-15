
import random
from pct.putils import Timer
from pct.microgrid import MicroGridEnvPlus

env = MicroGridEnvPlus()
env.seed(1)
env.initialise(properties={'day_mode': 'ordered', 'initial_seed': 1})
timer = Timer()
state = env.reset(day=1)

print(env.tcls_parameters[0][0])
print(env.loads_parameters[0][0])

timer.start()
while True:
    # action = env.action_space.sample()
    action = random.randint(1,80)
    state, reward, terminal, _ = env.step(action)
    if terminal:
        break
print('reward=',reward)
timer.stop()

print(f'Mean time: {timer.mean()}')


# b4 changing _build_state
# 0.004480324498017617
# 0.6354007133590609
# reward= -0.08456485909879799
# Mean time: 0.1164777000000008

# after
# 0.004480324498017617
# 0.6354007133590609
# reward= -0.08456485909879799
# Mean time: 0.04430849999999964


