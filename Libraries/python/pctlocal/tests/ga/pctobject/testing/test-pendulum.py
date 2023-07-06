

from pct.environments import Pendulum
from pct.environments import CartPoleV1, MountainCarContinuousV0


from pct.functions import Constant


steps=1

test = 1

if test ==1:
    # seed 3 circles anti-clockwise
    mc = Pendulum(render=True, seed=93) 
    mc.add_link(Constant(0))
    print(mc.get_config())

    for i in range(100):
        mc.run(steps=steps, verbose=True)
    mc.close()

if test ==2:
    # seed 3 circles anti-clockwise
    cp = CartPoleV1(render=True, seed=1) 
    cp.add_link(Constant(0))
    print(cp.get_config())

    for ctr in range(2):
        for i in range(100):
            cp.run(steps=steps, verbose=True)
        print()
        cp.reset(full=False, seed=1)
    
    cp.close()

# if test ==3:
#     mc = Pendulum_1(render=True, seed=1)
#     namespace=mc.namespace
#     mc.add_link(Constant([1], namespace=namespace))
#     print(mc.get_config())
#     mc.run(steps=20, verbose=True)

#     mc.close()



if test ==3:
    import gym
    for i in range(10):
        env = gym.make('Pendulum-v1') 
        env.reset(seed=93)
        # for i in range(1, 100, 1):
        obs = env.step([0])

        # env.render()
        print(obs[0], obs[1])
        
        #self.env.seed(seed)
        env.close()


if test ==4:
    import gym
    env = gym.make('Pendulum-v1') 
    env.reset(seed=93)
    for i in range(1, 100, 1):
        obs = env.step([0])

        env.render()
        print(obs[0], obs[1])
    
    #self.env.seed(seed)
    env.close()
  
if test ==5:
 
    mc = MountainCarContinuousV0(render=True, seed=4) 
    mc.add_link(Constant([1]))
    print(mc.get_config())

    for i in range(100):
        mc.run(steps=steps, verbose=True)
    mc.close()




if test ==6:
     
    import gym
    # down [4, 10, 29, 34, 41, 51, 53, 64, 65, 66, 82, 85, 93, 98]
    down=[]
    for seed in range(1,101, 1):

        env = gym.make('Pendulum-v1') 
        env.reset(seed=seed)
        #env.render()
        obs = env.step([[1]])
        dir = obs[0][0]
        if dir > -1 and dir < -0.9: 
            print(seed, dir, obs[0][1], obs[0][2])        
            down.append(seed)
        env.close()

    print(down)

# windows
#  4 [-0.94407326] [0.32973573] [0.43530822]
# 10 [-0.9588292] [0.28398332] [-0.22993018]
# 29 [-0.95203173] [-0.30599934] [-0.06932865]
# 34 [-0.997615] [-0.06902394] [0.8753732]
# 41 [-0.9705893] [0.24074157] [0.898946]
# 51 [-0.93583673] [0.35243383] [0.02964205]
# 53 [-0.9953297] [-0.09653387] [0.5354293]
# 64 [-0.9453366] [0.32609618] [0.45740095]
# 65 [-0.9564848] [-0.29178223] [-0.03359708]
# 66 [-0.90681845] [0.42152146] [0.88143444]
# 82 [-0.9995882] [-0.02869503] [0.8707026]
# 85 [-0.96300477] [-0.2694844] [-0.1126398]
# 93 [-0.99711835] [0.07586187] [0.3046366] ***
# 98 [-0.95581126] [0.29398108] [1.1126672]