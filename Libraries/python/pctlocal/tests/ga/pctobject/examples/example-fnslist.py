
from pct.functions import Proportional, WeightedSum, Constant, Variable, Integration 
from pct.nodes import PCTNode
from pct.putils import UniqueNamer, FunctionsList, get_drive
from pct.architectures import DynamicArchitecture

from epct.configs import DynamicConfiguration

import uuid

class mfn(object):
    "A function that subtracts one value from another. Parameter: None. Links: Two links required to each the values to be subtracted."
    def __init__(self, name="mfn", new_name=True, namespace=None, **cargs):

        if namespace ==None:
            namespace = uuid.uuid1()
        self.namespace=namespace

        if new_name:
            self.name = UniqueNamer.getInstance().get_name(namespace, name)
        else:
            self.name = name                

        FunctionsList.getInstance().add_function(namespace, self)

    def get_name(self):
        return self.name  

# class UniqueNamer:
#     "A utility for ensuring the names of functions are unique."
#     __instance = None
#     @staticmethod 
#     def getInstance():
#       """ Static access method. """
#       if UniqueNamer.__instance == None:
#          UniqueNamer()
#       return UniqueNamer.__instance

#     def __init__(self):
#       """ Virtually private constructor. """
#       if UniqueNamer.__instance != None:
#          raise Exception("This class is a singleton!")
#       else:
#          UniqueNamer.__instance = self
#       self.names = {}

#     def clear(self):
#       self.names = {}

#     def get_name(self, namespace=None, name=None):

#         if namespace in self.names:
#             namespace_list = self.names[namespace]
#         else:
#             namespace_list = {}
#             self.names[namespace] = namespace_list

#         if name in namespace_list: 
#             num = namespace_list[name]+1
#             namespace_list[name]=num
#             name = f'{name}{num}'
#         #else:
#         namespace_list[name]=0
#         return name
    
#     def report(self,  namespace=None, name=None,):

#         if namespace is None:
#             for namespace, namespace_list in self.names.items():
#                 print(namespace, len(namespace_list))
#                 for name in namespace_list:
#                     print("*** ", name)
#         else:
#             if namespace in self.names:
#                 namespace_list = self.names[namespace]
#                 if name == None:
#                     print(len(namespace_list))
#                     for nname in namespace_list:
#                         print("*** ", nname, namespace_list[nname])
#                 else:
#                     print("*** ", name, namespace_list[name])


# class FunctionsList:
#     "A utility for storing functions created, keyed on the function name."
#     __instance = None
#     @staticmethod 
#     def getInstance():
#       """ Static access method. """
#       if FunctionsList.__instance == None:
#          FunctionsList()
#       return FunctionsList.__instance
#     def __init__(self):
#       """ Virtually private constructor. """
#       if FunctionsList.__instance != None:
#          raise Exception("This class is a singleton!")
#       else:
#          FunctionsList.__instance = self
#       self.functions = {}

#     def clear(self, namespace):
#       self.functions[namespace] = {}
    
#     def add_function(self, namespace=None, func=None):
#         if namespace in self.functions:
#             namespace_list = self.functions[namespace]
#         else:
#             namespace_list = {}
#             self.functions[namespace]=namespace_list

#         name = func.get_name()
#         namespace_list[name]=func
        
#         return name

#     def remove_function(self, namespace=None, name=None):
#         self.functions[namespace].pop(name)
        
#     def get_function(self, namespace=None, name=None):        
#         if namespace in self.functions:
#             namespace_list = self.functions[namespace]
#         else:
#             return name
        
#         if isinstance(name, str) and name in namespace_list: 
#             func = namespace_list[name]
#         else:
#             func = name

#         return func
    
#     def report(self, namespace=None, name=None):
#         if namespace is None:
#             for namespace, namespace_list in self.functions.items():
#                 print(len(namespace_list), namespace)
#                 for name, function in namespace_list.items():
#                     print("*** ", name, [function])
#                     print(function)
#         else:   
#             if namespace in self.functions:
#                 namespace_list = self.functions[namespace]
#             else:
#                 raise Exception(f"Namespace {namespace} not found in report")

#             if name == None:
#                 print(len(namespace_list), namespace)
#                 for name, function in namespace_list.items():
#                     print("*** ", name, [function])
#                     print(function)
#             else:
#                 print("*** ", name, [namespace_list[name]])
#                 print(namespace_list[name])            


if __name__ == "__main__":


    test=12
    if test==13:
        user = "ruper"
        cwd = os.getcwd()
        if 'ryoung' in  cwd:
            user  = "ryoung"
        print(user)
        
    if test==12:
        import os
        user = "ruper"
        cwd = os.getcwd()
        if 'ryoung' in  cwd:
            user  = "ryoung"
            
        from pct.architectures import run_from_properties_file
        print(get_drive())
        runs=500
        render=False
        draw=False
        
        root_dir = '/mnt/c'
        path =  'Users/'+user+'/Versioning/python/nbdev/epct/nbs/'
        filename = 'testfiles/ga-001.444-3344-397818342161201780.properties'
        nevals = 1
        move={'OL0C0ws':[0.25,0], 'CL0C0':[0.25,0]}
        plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
            {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
        hpct = run_from_properties_file(root_dir=root_dir, path=path, file=filename,  nevals=nevals, move=move, draw=draw,
                                plots_figsize=(12,5), figsize=(10,10), render=render, runs=runs, plots=plots, 
                                    print_properties=True)
    if test==11:
        from epct.functions import EAConstant, EAProportional
        eac = EAConstant()
        eac.set_name(f'RL1C2')
        parameters={'value':1.2 }
        eac.create_properties(parameters)
        eac.summary()

        from epct.structure import ParameterFactory

        namespace=eac.namespace
        print(namespace)
        gap = EAProportional(namespace=namespace)
        level=2
        column=1
        gap.set_name(f'OL{level}C{column}')
        parameter = ParameterFactory.createParameter('Float')
        parameter.lower=-10
        parameter.upper=10

        parameters={'targetlevel':1, 'targetprefix':'C', 'targetcolumn':3, 'parameter':parameter, 'addlink': True }
        gap.create_properties(parameters)
        gap.summary()

    if test==10:
        dc = DynamicConfiguration.convert_to_raw_from_proportional_raw(
        [[[[1, 0], [1, 0], [1, 0], [1, 1]], [-6.546736285882238, -9.103232717855912], [[1, 1]]], [[[0, 1]], [0.889772263378402], [[1], [-1.6252635774790236]], [0]]],
        verbose=True)
        move={'Input0':[-0.7,0.1],'Input1':[-0.3,-0.05],'Input2':[0.18,-0.12],'Input3':[0.6,-0.2],'World':[-.9,-0.25],
          'Action1ws':[-0.515,-0.1], 'OL0C0ws':[-0.25,0], 'OL0C1ws':[0.25,0]}
        DynamicArchitecture.draw_raw(dc, move=move, summary=False)

    if test==9:
        from pct.environments import PendulumV0
        from pct.functions import Constant
        from pct.architectures import ProportionalArchitecture

        pen = PendulumV0(name='Pendulum',render=True)
        namespace = pen.namespace
        print(namespace)
        inputs=[2, 3]
        config = {'level0': [[[0, 0, 1], [0, 0, 1]], [74.7727669099358, 37.42447782017047, 70.45900090605967], [[1, 0, 1]]], 'level1': [[[1, 0, 1], [1, 1, 1]], [0.028281504070566288, 0.29618653732851286], [[-49.05302284318027, 46.949638698585005], [-96.63198831250754, -29.78373183094591], [-3.8249493797145107, -60.95121501461629]]], 'level2': [[[1, 0], [0, 1]], [0.633350421196448, 0.5607290603484817], [[41.217164164869104, -76.70635343790484], [83.21744682425535, -96.9311066757899]], [1, 2]], 'parameters': {}}
        for key in config.keys():
            print(key, config[key])
        pa = ProportionalArchitecture(config=config, env=pen, input_indexes=inputs, namespace=namespace)
        pa()
        hpct = pa.get_hierarchy()
        hpct.draw(move={'Pendulum': [-0.2, -0.3],'Input0': [-0.3, 0], 'Input1': [0.3, 0]})

    if test==8:
        FunctionsList.getInstance().get_function(name="cos_angle1").set_name("cos_angle2")

    if test==7:
        node = PCTNode()
        FunctionsList.getInstance().report() 

    if test==6:

        from pct.functions import Constant
        from pct.hierarchy import PCTHierarchy
        pre=Constant(5, name='precon')
        namespace=pre.namespace
        post=Constant(10, name='postcon', namespace=namespace)
        hpct = PCTHierarchy(3,3, pre=[pre], post=[post], history=True, clear_names=False, links="dense", namespace=namespace)
        FunctionsList.getInstance().report() 
        hpct()


    if test==5:
        integrator = Integration(3, 10)
        ns=integrator.namespace
        cons = Constant(5, namespace=ns)
        integrator.add_link(cons)
        config = integrator.get_config()
        inte = Integration.from_config(config, namespace=ns)
        print(inte())
        target = {'type': 'Integration', 'name': 'integration', 'value': 1.5, 'links': {0: 'constant'}, 'gain': 3, 'slow': 10}
        #print(target)
        assert inte.get_config() == target

    if test==4:
        const = Constant(1, name='const')
        ns = const.namespace
        pr = Proportional(name='pr', links=const, namespace=ns)
        pr.summary()
        pr = Proportional(gain=10, name='pr', links='const', namespace=ns)
        pr.summary()
        assert pr() == 10

    if test==3:
        wts=[1,1,1]
        ws = WeightedSum(weights=wts)
        ns = ws.namespace
        ws.add_link(Constant(10, namespace=ns))
        ws.add_link(Constant(5, namespace=ns))
        ws.add_link(Constant(20, namespace=ns))
        assert ws() == 35
        c = ws.get_config()
        print(c)
        ws1 = WeightedSum.from_config(c, namespace=ns)
        ws1.get_config()

    if test==2:

        # r = Variable(0, name="velocity_reference")
        # p = Constant(10, name="constant_perception")
        # o = Integration(10, 100, name="integrator")
        # integratingnode = PCTNode(reference=r, perception=p, output=o, name="integratingnode", history=True)
        import json
        # integratingnode.save("inode.json")
        nnode = PCTNode.load("inode.json")
        print(nnode.get_config())

    if test==1:
        prop = mfn()
        prop1 = mfn()
        namespace = prop.namespace
        prop2 = mfn(namespace=namespace)
        prop3 = mfn(name='xx')
        prop3 = mfn(name='xx', namespace=prop1.namespace)
        prop3 = mfn(name='xx', namespace=prop2.namespace)


        UniqueNamer.getInstance().report(name='xx', namespace=prop2.namespace)
        print()
        UniqueNamer.getInstance().report(namespace=prop2.namespace)

        #FunctionsList.getInstance().report(namespace=namespace)
        FunctionsList.getInstance().report()

