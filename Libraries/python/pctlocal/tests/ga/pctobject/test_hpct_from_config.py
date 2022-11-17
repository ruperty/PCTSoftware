import uuid
from pct.nodes import PCTNode
from pct.errors import BaseErrorCollector
from pct.functions import Variable, FunctionFactory
from eepct.hpct import HPCTIndividual

namespace = uuid.uuid1()

test = 3

if test==1:
    cargs = { 'name': 'velocity', 'value': 0.2, 'links': {}}
    var = Variable(new_name=False, namespace=namespace, **cargs)
    print(var.get_config())

    fnname = 'Variable'
    func = FunctionFactory.createFunctionFromConfig(fnname, namespace, cargs)
    print(func.get_config())

    fndict = {'type': 'Proportional', 'name': 'proportional', 'value': 0, 'links': {}, 'gain': 10}
    fnname = fndict.pop('type')
    print(fndict)
    func1 = FunctionFactory.createFunctionFromConfig(fnname, namespace, fndict)
    print(func1.get_config())



if test==2:
    node = PCTNode(namespace=namespace)
    config_node = PCTNode.from_config({ 'name': 'mypctnode', 
        #'refcoll': {'0': {'type': 'Proportional', 'name': 'proportional', 'value': 0, 'links': {}, 'gain': 10}}, 
        'refcoll': {'0': {'type': 'Variable', 'name': 'proportional', 'value': 0, 'links': {}}}, 
        'percoll': {'0': {'type': 'Variable', 'name': 'velocity', 'value': 0.2, 'links': {}}}, 
        'comcoll': {'0': {'type': 'Subtract', 'name': 'subtract', 'value': 1, 'links': {0: 'constant', 1: 'velocity'}}}, 
        'outcoll': {'0': {'type': 'Proportional', 'name': 'proportional', 'value': 10, 'links': {0: 'subtract'}, 'gain': 10}}}, namespace=namespace)


if test==3:
    # config =  {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [0.03498833197860944, 0.20994561633454428, 0.012668159509212712, -0.2705237130920193, 0.047656152654718356], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.20994561633454428, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': 0.03498833197860944, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.2705237130920193, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 0.012668159509212712, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': -0.2705237130920193, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [0, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0.2705237130920193, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.05046166000036782, 'links': {0: 'CL0C0'}, 'gain': -0.1865332226280776}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -0.005282911840894066, 'links': {0: 'OL0C0'}, 'weights': [0.10469159835121472]}}}
    # config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [-0.04650788294424393, 0.018050934670020086, 3.9918996431478025e-05, -0.04900421103662206, -0.04646796394782306], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.018050934670020086, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': -0.04650788294424393, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.04900421103662206, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 3.9918996431478025e-05, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0.013672555272110396, 'links': {0: 'OL1C0'}, 'weights': [-0.31050335546384344]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': -0.07742124031441443, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0.09109379558652482, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.04912319635339796, 'links': {0: 'CL0C0'}, 'gain': -0.539259518577625}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': -0.014253281308875522, 'links': {0: 'OL1C0'}, 'weights': [0.32369162784103445]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': -0.030913357370170494, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0.016660076061294972, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': -0.005376804438986575, 'links': {0: 'CL0C1'}, 'gain': -0.32273588783175344}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': -0.030913357370170494, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0.030913357370170494, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0.02153677534213933, 'links': {0: 'CL1C0'}, 'gain': 0.6966818609912945}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -0.001229243017300775, 'links': {0: 'OL1C0', 1: 'OL0C1'}, 'weights': [0.11460735102238973, 0.6876790537549466]}}}
 
    config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [0.09167718645484463, 0.016581867845028825, 0.0005768263293848813, -0.016596000470601835, 0.09225401275224174], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.016581867845028825, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': 0.09167718645484463, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.016596000470601835, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 0.0005768263293848813, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0.0005626937038118712, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': -0.0005626937038118712, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.0005019000223479335, 'links': {0: 'CL0C0'}, 'gain': 0.8919595491257475}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 3.400675609195577e-05, 'links': {0: 'OL0C0'}, 'weights': [-0.06775603621786885]}}}
 
    ind, score = HPCTIndividual.run_from_config(config, render=True,  error_collector_type='InputsError', error_response_type='RootMeanSquareError', error_properties=None, error_limit=100, steps=500, verbose=False)

    # ind = HPCTIndividual.from_config(config)
    # env = ind.get_preprocessor()[0]
    # env.set_render(True)
    # error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'
    # error_collector = BaseErrorCollector.collector(error_response_type, error_collector_type, 100)
    # ind.draw(file='test_hpct_from_config_3.png', node_size=200, font_size=10, with_edge_labels=True)
    # ind.set_error_collector(error_collector)
    # ind.run(steps=500, verbose=False)
    # env.close()   
    # score=ind.get_error_collector().error()
    
    print("Best Score: %0.3f" % score)
    ind.summary()
    print(ind.get_parameters_list())



if test==4:
    dct = {
    "Animal": "Dog",
    "Fruit": "Pear",
    "Vegetable": "Cabbage",
    "Tree": "Maple",
    "Flower": "Daisy"
    }

    res = dict(reversed(list(dct.items())))
    print(res)

    dct = {v: k for k, v in dct.items()}
    print(dct)
    # dlist = dct.items()
    # print(dlist.reverse())

