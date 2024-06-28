from pct.environments import ARC
from pct.functions import Constant

test = "mg+days"


if test == "mg+days":
    env = ARC()
    env.add_link(Constant(1))
    env.add_link(Constant(1))
    properties = {'dir': 'C:\\packages\\arc-prize-2024\\training', 'code':'1_007bbfb7.dat', 'fitness_type': 'dim_only'}
    env.set_properties(properties)
    env.set_render(True)
    env.reset()

    for i in range(6):
        state = env()
        env.summary()    
        print()
    print(env.get_config())
    print()
    print(env.output_string())    
    print()
    print(state)

    env.close()

