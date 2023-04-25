import uuid
from pct.nodes import PCTNode
from pct.hierarchy import PCTHierarchy
from pct.errors import BaseErrorCollector
from pct.functions import Variable, FunctionFactory
from eepct.hpct import HPCTIndividual
from pct.network import ConnectionManager

namespace = uuid.uuid1()

test = 6

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
    config_node.summary()


if test==3:
    min=True
    config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [0.09167718645484463, 0.016581867845028825, 0.0005768263293848813, -0.016596000470601835, 0.09225401275224174], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.016581867845028825, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': 0.09167718645484463, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.016596000470601835, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 0.0005768263293848813, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0.0005626937038118712, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': -0.0005626937038118712, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.0005019000223479335, 'links': {0: 'CL0C0'}, 'gain': 0.8919595491257475}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 3.400675609195577e-05, 'links': {0: 'OL0C0'}, 'weights': [-0.06775603621786885]}}}
 
    ind, score = HPCTIndividual.run_from_config(config, min, render=True, seed=1, error_collector_type='InputsError', error_response_type='RootMeanSquareError', error_properties=None, error_limit=100, steps=500, hpct_verbose=False)
    
    print("Best Score: %0.3f" % score)
    # ind.summary()
    # print(ind.get_parameters_list())

if test==5:        
    min=True
    config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [0.09167718645484463, 0.016581867845028825, 0.0005768263293848813, -0.016596000470601835, 0.09225401275224174], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.016581867845028825, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': 0.09167718645484463, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.016596000470601835, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 0.0005768263293848813, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0.0005626937038118712, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': -0.0005626937038118712, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.0005019000223479335, 'links': {0: 'CL0C0'}, 'gain': 0.8919595491257475}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 3.400675609195577e-05, 'links': {0: 'OL0C0'}, 'weights': [-0.06775603621786885]}}}
    ind, score = PCTHierarchy.run_from_config(config, min, render=True, seed=1, error_collector_type='InputsError', error_response_type='RootMeanSquareError', error_properties=None, error_limit=100, steps=500, hpct_verbose=False)
    print("Best Score: %0.3f" % score)


if test==6:
    cm = ConnectionManager.getInstance()
    cm.set_port(6666)
    min=True
    config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'WebotsWrestler', 'name': 'WebotsWrestler', 'value': [-0.0, 0.0, -0.0, -0.0, 0.0, -0.0], 'links': {0: 'Action1', 1: 'Action2', 2: 'Action3', 3: 'Action4', 4: 'Action5', 5: 'Action6'}, 'env_name': 'WebotsWrestler', 'performance': 2.149, 'done': True}, 'pre1': {'type': 'IndexedParameter', 'name': 'LHipPitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'LKneePitch', 'value': 0.0, 'links': {0: 'WebotsWrestler'}, 'index': 1}, 'pre3': {'type': 'IndexedParameter', 'name': 'LAnklePitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 2}, 'pre4': {'type': 'IndexedParameter', 'name': 'RHipPitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 3}, 'pre5': {'type': 'IndexedParameter', 'name': 'RKneePitch', 'value': 0.0, 'links': {0: 'WebotsWrestler'}, 'index': 4}, 'pre6': {'type': 'IndexedParameter', 'name': 'RAnklePitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 5}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0.0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [0.3966908273483479, -0.14499343542419654]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [0, 0, 0, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0.0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.0, 'links': {0: 'CL0C0'}, 'gain': -0.2469704698731962}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': -0.0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-0.4959794866933991, -0.7366519577999016]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': -0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [0, 1, 0, 0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': -0.0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': -0.0, 'links': {0: 'CL0C1'}, 'gain': 0.453137041069354}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L0C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C2', 'value': 0.0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [0.19376194256004797, -0.4809641967711172]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C2', 'value': -0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [1, 1, 0, 1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C2', 'value': 0.0, 'links': {0: 'RL0C2', 1: 'PL0C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C2', 'value': -0.0, 'links': {0: 'CL0C2'}, 'gain': -0.22521351147985763}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L0C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C3', 'value': -0.0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-0.5513824762645159, -0.833993025497277]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C3', 'value': -0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [0, 1, 1, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C3', 'value': -0.0, 'links': {0: 'RL0C3', 1: 'PL0C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C3', 'value': -0.0, 'links': {0: 'CL0C3'}, 'gain': 8.589637172171094e-05}}}}, 'col4': {'col': 4, 'node': {'type': 'PCTNode', 'name': 'L0C4', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C4', 'value': -0.0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-1.1227165885642547, 0.3002880992470238]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C4', 'value': -0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [0, 0, 0, 1, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C4', 'value': -0.0, 'links': {0: 'RL0C4', 1: 'PL0C4'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C4', 'value': 0.0, 'links': {0: 'CL0C4'}, 'gain': -1.0546514050101221}}}}, 'col5': {'col': 5, 'node': {'type': 'PCTNode', 'name': 'L0C5', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C5', 'value': -0.0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-0.05203733904404315, -0.9069684322507601]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C5', 'value': 0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [0, 1, 1, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C5', 'value': -0.0, 'links': {0: 'RL0C5', 1: 'PL0C5'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C5', 'value': 0.0, 'links': {0: 'CL0C5'}, 'gain': -0.5870784571327743}}}}, 'col6': {'col': 6, 'node': {'type': 'PCTNode', 'name': 'L0C6', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C6', 'value': 0.0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [0.7866844357696494, 0.3098529521714545]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C6', 'value': -0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [1, 0, 0, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C6', 'value': 0.0, 'links': {0: 'RL0C6', 1: 'PL0C6'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C6', 'value': -0.0, 'links': {0: 'CL0C6'}, 'gain': -0.4435370238596815}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAVariable', 'name': 'RL1C0', 'value': -0.7835225545944999, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': -0.0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3', 4: 'PL0C4', 5: 'PL0C5', 6: 'PL0C6'}, 'weights': [1, 1, 1, 0, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': -0.0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0.0, 'links': {0: 'CL1C0'}, 'gain': -1.5664809090771636}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAVariable', 'name': 'RL1C1', 'value': -0.09078426133873872, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': -0.0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3', 4: 'PL0C4', 5: 'PL0C5', 6: 'PL0C6'}, 'weights': [1, 1, 0, 0, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0.0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': -0.0, 'links': {0: 'CL1C1'}, 'gain': -0.25675287991511975}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4', 5: 'OL0C5', 6: 'OL0C6'}, 'weights': [0.18510388753825763, -0.49389894215208135, 0.32059392077337623, -0.10533078947782826, 0.07548626300726557, -0.37043634913137413, 0.396509376693697]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4', 5: 'OL0C5', 6: 'OL0C6'}, 'weights': [-0.3239034730587389, 0.02599124375282727, 0.6492424802334008, -0.11715368518552849, -0.42008327417873426, -0.9418202494450519, -0.3862318164557935]}, 'post2': {'type': 'EAWeightedSum', 'name': 'Action3', 'value': 0.0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4', 5: 'OL0C5', 6: 'OL0C6'}, 'weights': [0.07556341378349078, 1.0044295458328305, 0.14716512695950196, -1.1688367179023418, 0.6724539259159428, 0.10136513418761281, 0.9852590407435039]}, 'post3': {'type': 'EAWeightedSum', 'name': 'Action4', 'value': 0.0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4', 5: 'OL0C5', 6: 'OL0C6'}, 'weights': [-0.16231614649505482, 0.5553604919750554, 0.3874508617159227, 0.7410367633561485, 1.0589899694324258, 1.847734511184337, 0.7476814117727033]}, 'post4': {'type': 'EAWeightedSum', 'name': 'Action5', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4', 5: 'OL0C5', 6: 'OL0C6'}, 'weights': [-0.13294559509020212, -0.32395564949593686, 0.55724790000176, 1.2492311232408904, -0.6098764646184718, -0.9109171762828597, 1.168843771670811]}, 'post5': {'type': 'EAWeightedSum', 'name': 'Action6', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4', 5: 'OL0C5', 6: 'OL0C6'}, 'weights': [0.4723809635755427, -0.9851636776923599, 0.7496632446166631, -0.9216107728136108, -1.1092427088964407, -0.5302694912593089, 0.09761569080690088]}}}
    ind, score = PCTHierarchy.run_from_config(config, min, render=True, seed=1, error_collector_type='InputsError', error_response_type='RootMeanSquareError', error_properties=None, error_limit=100, steps=500, hpct_verbose=False)
    print("Best Score: %0.3f" % score)


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

