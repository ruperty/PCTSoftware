from pct.environments import ARC
from pct.functions import Constant

test = "mg+days"


if test == "mg+days":
    env = ARC()
    
    env.add_link(Constant(1))
    env.add_link(Constant(2))
    properties = {'dir': 'C:\\packages\\arc-prize-2024\\training', 'code':'1_007bbfb7.dat'}
    env.set_properties(properties)
    env.reset()
    state = env()
    env.summary()
    print(env.get_config())
    print(env.output_string())    
    print(state)


