import uuid
from pct.putils import loadjson
from eepct.hpct import HPCTIndividual
from eepct.hpct import HPCTArchitecture

from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTLEVEL

namespace = uuid.uuid1()

test = 1


if test==1:
    # config =  {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [0.03498833197860944, 0.20994561633454428, 0.012668159509212712, -0.2705237130920193, 0.047656152654718356], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.20994561633454428, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': 0.03498833197860944, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.2705237130920193, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 0.012668159509212712, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': -0.2705237130920193, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [0, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0.2705237130920193, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.05046166000036782, 'links': {0: 'CL0C0'}, 'gain': -0.1865332226280776}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -0.005282911840894066, 'links': {0: 'OL0C0'}, 'weights': [0.10469159835121472]}}}
    # config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [-0.04650788294424393, 0.018050934670020086, 3.9918996431478025e-05, -0.04900421103662206, -0.04646796394782306], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.018050934670020086, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': -0.04650788294424393, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.04900421103662206, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 3.9918996431478025e-05, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0.013672555272110396, 'links': {0: 'OL1C0'}, 'weights': [-0.31050335546384344]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': -0.07742124031441443, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0.09109379558652482, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.04912319635339796, 'links': {0: 'CL0C0'}, 'gain': -0.539259518577625}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': -0.014253281308875522, 'links': {0: 'OL1C0'}, 'weights': [0.32369162784103445]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': -0.030913357370170494, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0.016660076061294972, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': -0.005376804438986575, 'links': {0: 'CL0C1'}, 'gain': -0.32273588783175344}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': -0.030913357370170494, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0.030913357370170494, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0.02153677534213933, 'links': {0: 'CL1C0'}, 'gain': 0.6966818609912945}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -0.001229243017300775, 'links': {0: 'OL1C0', 1: 'OL0C1'}, 'weights': [0.11460735102238973, 0.6876790537549466]}}}
 
    #config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [0.09167718645484463, 0.016581867845028825, 0.0005768263293848813, -0.016596000470601835, 0.09225401275224174], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.016581867845028825, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': 0.09167718645484463, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.016596000470601835, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 0.0005768263293848813, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0.0005626937038118712, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': -0.0005626937038118712, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.0005019000223479335, 'links': {0: 'CL0C0'}, 'gain': 0.8919595491257475}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 3.400675609195577e-05, 'links': {0: 'OL0C0'}, 'weights': [-0.06775603621786885]}}}
 
    #config = loadjson("create_node_config.json")

    #ind = HPCTIndividual.from_config(config)

    print(HPCTFUNCTION.REFERENCE.name, HPCTFUNCTION.REFERENCE.value)
    print(HPCTARCH.LEVELS.name, HPCTARCH.LEVELS.value)
    
    arch = HPCTArchitecture()
    arch.configure()

    ind = HPCTIndividual(levels=3, cols=1, arch = arch)
    
    ind.get_node(2,0).get_function('output').set_name("OL2C0")
    ind.get_node(0,0).get_function('perception').set_name("PL0C0")
         
    #ind.summary()
    
    level=1
    column=1
    level_type=HPCTLEVEL.N
    levels_grid=ind.get_grid()
    node = ind.create_node(level, column, level_type, levels_grid)
    ind.add_node(node, level, column)

    print("---- node ----")
    node.summary()
    print("---- ind ----")
    ind.summary()
    


