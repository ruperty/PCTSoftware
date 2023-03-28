

from pct.environments import Pendulum_1
from pct.environments import Pendulum
from pct.environments import CartPoleV1, MountainCarContinuousV0


from pct.functions import Constant


steps=1

test = 5

if test ==1:
    # seed 3 circles anti-clockwise
    mc = Pendulum(render=True, seed=4) 
    mc.add_link(Constant([1]))
    print(mc.get_config())

    for i in range(100):
        mc.run(steps=steps, verbose=True)
    mc.close()

if test ==2:
    # seed 3 circles anti-clockwise
    cp = CartPoleV1(render=True, seed=1) 
    cp.add_link(Constant(0))
    print(cp.get_config())

    for ctr in range(10):
        for i in range(1):
            cp.run(steps=steps, verbose=True)
        print()
        cp.reset(full=False, seed=1)
    
    cp.close()

if test ==3:
    mc = Pendulum_1(render=True, seed=1)
    namespace=mc.namespace
    mc.add_link(Constant([1], namespace=namespace))
    print(mc.get_config())
    mc.run(steps=20, verbose=True)


if test ==4:
    import gym
    env = gym.make('Pendulum-v1') 
    env.reset(seed=1)
    obs = env.step([[1]])
    print(obs)
    
    #self.env.seed(seed)
  
  
if test ==5:
 
    mc = MountainCarContinuousV0(render=True, seed=4) 
    mc.add_link(Constant([1]))
    print(mc.get_config())

    for i in range(100):
        mc.run(steps=steps, verbose=True)
    mc.close()