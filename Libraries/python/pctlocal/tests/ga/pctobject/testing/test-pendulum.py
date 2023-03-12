

from pct.environments import Pendulum_1
from pct.environments import Pendulum
from pct.environments import CartPoleV1


from pct.functions import Constant


steps=1

test = 2

if test ==1:
    # seed 3 circles anti-clockwise
    pen = Pendulum(render=True, seed=4) 
    pen.add_link(Constant([1]))
    print(pen.get_config())

    for i in range(100):
        pen.run(steps=steps, verbose=True)
    pen.close()

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
    pen = Pendulum_1(render=True)
    namespace=pen.namespace
    pen.add_link(Constant([1], namespace=namespace))
    print(pen.get_config())
    pen.run(steps=20, verbose=True)


