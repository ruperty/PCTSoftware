
from os import name
import random, enum, time, copy
from enum import IntEnum, auto
from deap import tools, algorithms
from dataclasses import dataclass

from pct.hierarchy import PCTHierarchy
from pct.nodes import PCTNode
from pct.errors import BaseErrorCollector
from pct.functions import FunctionFactory, CUF, FunctionsList
from pct.environments import EnvironmentFactory, OpenAIGym

from pct.functions import IndexedParameter
from epct.evolvers import BaseEvolver, CommonToolbox, EvolverWrapper, check_hash_file_exists
from epct.functions import EAFunctionFactory
from epct.structure import ParameterFactory
from pct.putils import stringListToListOfStrings


class HPCTARCH(IntEnum):
    PERCEPTION = auto()
    REFERENCE = auto()
    COMPARATOR = auto()
    OUTPUT = auto()
    ACTION = auto()
    ZERO = auto()
    N = auto()
    TOP = auto()
    ZEROTOP = auto()
    HIERARCHY = auto()
    LEVELS = auto()
    LEVEL = auto()
    VARIABLE_TYPE = auto()
    PARAMETER = auto()
    CONN = auto()
    EVOLVE = auto()
    FUNCTION_CLASS = auto()
    VARIABLE_PROPERTIES = auto()


class HPCTControlFunctionCollection(object):

    def __init__(self, reference=None, perception=None, comparator=None, output=None, action=None):
        self.reference = reference
        self.perception = perception
        self.output = output
        self.comparator = comparator
        self.action = action

    def __repr__(self):
        if self.reference is not None:
            r = f'Ref:{self.reference.__repr__()}'
        if self.perception is not None:
            p = f'Per:{self.perception.__repr__()}'
        if self.output is not None:
            o = f'Out:{self.output.__repr__()}'
        if self.comparator is not None:
            c = f'Com:{self.comparator.__repr__()}'
        if self.action is not None:
            a = f'Act:{self.action.__repr__()}'
            return ' '.join((r, p, c, o, a))

        return ' '.join((r, p, c, o))

    def get_function_properties(self, control_function_type):
        if control_function_type == HPCTARCH.REFERENCE:
            return self.reference.func_class, self.reference.var_type, self.reference.var_properties
        if control_function_type == HPCTARCH.PERCEPTION:
            return self.perception.func_class, self.perception.var_type, self.perception.var_properties
        if control_function_type == HPCTARCH.OUTPUT:
            return self.output.func_class, self.output.var_type, self.output.var_properties
        if control_function_type == HPCTARCH.COMPARATOR:
            return self.comparator.func_class, self.comparator.var_type, self.comparator.var_properties
        if control_function_type == HPCTARCH.ACTION:
            return self.action.func_class, self.action.var_type, self.action.var_properties

    def set_function_property(self, control_function_type, type, value):
        if control_function_type == HPCTARCH.REFERENCE:
            self.reference.set(type, value)
        if control_function_type == HPCTARCH.PERCEPTION:
            self.perception.set(type, value)
        if control_function_type == HPCTARCH.COMPARATOR:
            self.comparator.set(type, value)
        if control_function_type == HPCTARCH.OUTPUT:
            self.output.set(type, value)
        if control_function_type == HPCTARCH.ACTION:
            self.action.set(type, value)

    def set_function_properties(self, function):
        if function[0] == HPCTARCH.REFERENCE:
            self.reference.func_class, self.reference.var_type = function[1][
                HPCTARCH.FUNCTION_CLASS], function[1][HPCTARCH.VARIABLE_TYPE]
            if HPCTARCH.VARIABLE_PROPERTIES in function[1] != None:
                self.reference.var_properties = function[1][HPCTARCH.VARIABLE_PROPERTIES]

        if function[0] == HPCTARCH.PERCEPTION:
            self.perception.func_class, self.perception.var_type = function[1][
                HPCTARCH.FUNCTION_CLASS], function[1][HPCTARCH.VARIABLE_TYPE]
            if HPCTARCH.VARIABLE_PROPERTIES in function[1] != None:
                self.perception.var_properties = function[1][HPCTARCH.VARIABLE_PROPERTIES]

        if function[0] == HPCTARCH.OUTPUT:
            self.output.func_class, self.output.var_type = function[1][
                HPCTARCH.FUNCTION_CLASS], function[1][HPCTARCH.VARIABLE_TYPE]
            if HPCTARCH.VARIABLE_PROPERTIES in function[1] != None:
                self.output.var_properties = function[1][HPCTARCH.VARIABLE_PROPERTIES]

        if function[0] == HPCTARCH.COMPARATOR:
            self.comparator.func_class, self.comparator.var_type = function[1][
                HPCTARCH.FUNCTION_CLASS], function[1][HPCTARCH.VARIABLE_TYPE]
            if HPCTARCH.VARIABLE_PROPERTIES in function[1] != None:
                self.comparator.var_properties = function[1][HPCTARCH.VARIABLE_PROPERTIES]

        if function[0] == HPCTARCH.ACTION:
            self.action.func_class, self.action.var_type = function[1][
                HPCTARCH.FUNCTION_CLASS], function[1][HPCTARCH.VARIABLE_TYPE]
            if HPCTARCH.VARIABLE_PROPERTIES in function[1] != None:
                self.action.var_properties = function[1][HPCTARCH.VARIABLE_PROPERTIES]


@dataclass
class HPCTControlFunctionProperties(object):
    var_type : enum
    func_class : str 
    var_properties : dict

    # def __init__(self, properties=None):
    #     self.var_type = properties[HPCTARCH.VARIABLE_TYPE]
    #     self.func_class = properties[HPCTARCH.FUNCTION_CLASS]
    #     self.var_properties = properties[HPCTARCH.VARIABLE_PROPERTIES]

    def set(self, type, value):
        if type == HPCTARCH.VARIABLE_TYPE:
            self.var_type = value
        if type == HPCTARCH.FUNCTION_CLASS:
            self.func_class = value
        if type == HPCTARCH.VARIABLE_PROPERTIES:
            self.var_properties = value

    # HPCTControlFunctionProperties.from_properties
    @classmethod
    def from_properties(cls, properties):
        hpctcfp = cls(properties[HPCTARCH.VARIABLE_TYPE], properties[HPCTARCH.FUNCTION_CLASS], properties[HPCTARCH.VARIABLE_PROPERTIES])

        return hpctcfp
    # def __repr__(self):
    #     return f'("{self.var_type}","{self.func_class}",{self.var_properties})'


class HPCTArchitecture(object):

    def __init__(self, arch=None, mode=0, lower_float=-10, upper_float=10):
        if arch == None:
            if mode ==0:
                arch = {
                    HPCTARCH.HIERARCHY: {
                        HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES: {'lower': lower_float, 'upper': upper_float}},
                        HPCTARCH.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES: {'lower': lower_float, 'upper': upper_float}},
                        HPCTARCH.COMPARATOR: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'Subtract', HPCTARCH.VARIABLE_PROPERTIES: None},
                        HPCTARCH.OUTPUT: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAProportional', HPCTARCH.VARIABLE_PROPERTIES: {'lower': lower_float, 'upper': upper_float}},
                        HPCTARCH.ACTION: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES: {'lower': lower_float, 'upper': upper_float}},
                        HPCTARCH.LEVELS: {
                            HPCTARCH.ZERO: {HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES: None}},
                            HPCTARCH.N: {HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES: None}},
                            HPCTARCH.ZEROTOP: {HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES: None},
                                            HPCTARCH.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Literal', HPCTARCH.FUNCTION_CLASS: 'EAConstant', HPCTARCH.VARIABLE_PROPERTIES: None}},
                            HPCTARCH.TOP: {HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES: None},
                                        HPCTARCH.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Literal', HPCTARCH.FUNCTION_CLASS: 'EAConstant', HPCTARCH.VARIABLE_PROPERTIES: None}}
                        }}
            }

        self.arch = arch
        self.levels_zerotop = None
        self.levels_zero = None
        self.levels_top = None
        self.levels_n = None

    def __repr__(self):

        if self.levels_zerotop is not None:
            return f'ZeroTop:{self.levels_zerotop.__repr__()}'

        if self.levels_zero is not None:
            z = f'Zero:{self.levels_zero.__repr__()}'

        if self.levels_n is not None:
            n = f'N:{self.levels_n.__repr__()}'

        if self.levels_top is not None:
            t = f'Top:{self.levels_top.__repr__()}'

        if self.levels_n is None:
            return '\n'.join((z, t))

        return '\n'.join(( z, n, t))

    def configure(self, levels=None, additional=None):
        if additional is not None:
            self.arch = {**self.arch, **additional}
        if HPCTARCH.HIERARCHY in self.arch:
            hpctarch = HPCTControlFunctionCollection(
                reference=HPCTControlFunctionProperties.from_properties(
                    self.arch[HPCTARCH.HIERARCHY][HPCTARCH.REFERENCE]),
                perception=HPCTControlFunctionProperties.from_properties(
                    self.arch[HPCTARCH.HIERARCHY][HPCTARCH.PERCEPTION]),
                comparator=HPCTControlFunctionProperties.from_properties(
                    self.arch[HPCTARCH.HIERARCHY][HPCTARCH.COMPARATOR]),
                output=HPCTControlFunctionProperties.from_properties(
                    self.arch[HPCTARCH.HIERARCHY][HPCTARCH.OUTPUT]),
                action=HPCTControlFunctionProperties.from_properties(
                    self.arch[HPCTARCH.HIERARCHY][HPCTARCH.ACTION])
            )

            self.levels_zerotop = copy.deepcopy(hpctarch)
            self.levels_zero = copy.deepcopy(hpctarch)
            self.levels_top = copy.deepcopy(hpctarch)
            self.levels_n = copy.deepcopy(hpctarch)

            # if levels == 1:
            #     self.levels_zerotop = hpctarch
            # else:
            #     self.levels_zero = copy.deepcopy(hpctarch)
            #     self.levels_top = copy.deepcopy(hpctarch)
            #     self.levels_top.action = None
            # if levels > 2:
            #     self.levels_n = copy.deepcopy(hpctarch)
            #     self.levels_n.action = None

        if HPCTARCH.LEVELS in self.arch[HPCTARCH.HIERARCHY]:
            if self.levels_zero != None:
                if HPCTARCH.ZERO in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS]:
                    for function in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS][HPCTARCH.ZERO].items():
                        self.levels_zero.set_function_properties(function)

            if self.levels_n != None:
                if HPCTARCH.N in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS]:
                    for function in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS][HPCTARCH.N].items():
                        self.levels_n.set_function_properties(function)

            if self.levels_top != None:
                if HPCTARCH.TOP in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS]:
                    for function in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS][HPCTARCH.TOP].items():
                        self.levels_top.set_function_properties(function)

            if self.levels_zerotop != None:
                if HPCTARCH.ZEROTOP in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS]:
                    for function in self.arch[HPCTARCH.HIERARCHY][HPCTARCH.LEVELS][HPCTARCH.ZEROTOP].items():
                        self.levels_zerotop.set_function_properties(function)

    def get_function_properties(self, level_type, control_function_type):

        if level_type == HPCTARCH.ZEROTOP:
            return self.levels_zerotop.get_function_properties(control_function_type)

        if level_type == HPCTARCH.ZERO:
            return self.levels_zero.get_function_properties(control_function_type)

        if level_type == HPCTARCH.TOP:
            return self.levels_top.get_function_properties(control_function_type)

        if level_type == HPCTARCH.N:
            return self.levels_n.get_function_properties(control_function_type)

        return None, None

    def set(self, level_type, control_function_type, type, value):
        if level_type == HPCTARCH.ZEROTOP:
            self.levels_zerotop.set_function_property(
                control_function_type, type, value)

        if level_type == HPCTARCH.ZERO:
            self.levels_zero.set_function_property(
                control_function_type, type, value)

        if level_type == HPCTARCH.TOP:
            self.levels_top.set_function_property(
                control_function_type, type, value)

        if level_type == HPCTARCH.N:
            self.levels_n.set_function_property(
                control_function_type, type, value)


class HPCTIndividual(PCTHierarchy):

    def __init__(self, env=None, levels=0, cols=0, history=False, error_collector=None,
                 env_inputs=None, toplevel_inputs=None, zerolevel_inputs=None, levels_columns_grid=None,
                 lower_float=-1, upper_float=1, arch=None, references=None, num_actions=None):

        namespace = None
        if env is not None:
            namespace = env.namespace
        super().__init__(history=history, error_collector=error_collector, namespace=namespace)

        self.arch = arch
        self.lower_float, self.upper_float, self.references = lower_float, upper_float, references
        self.env_inputs, self.toplevel_inputs, self.zerolevel_inputs = env_inputs, toplevel_inputs, zerolevel_inputs

        if env is not None:
            self.add_preprocessor(env)
            for input in env_inputs:
                self.add_preprocessor(input)

            self.configure_nodes(levels_columns_grid)
            self.set_action_function(env, levels_columns_grid, num_actions)

    def set_action_function(self,  env, levels_columns_grid, num_actions):
        levels = len(levels_columns_grid)
        columns = levels_columns_grid[0]

        level_type = HPCTARCH.ZERO
        if levels == 1:
            level_type = HPCTARCH.ZEROTOP

        function_type = HPCTARCH.ACTION
        for actionIndex in range(num_actions):

            parameters, _ = self.get_function_parameters(
                level_type=level_type, function_type=function_type)
            parameters['targetcolumns'] = columns

            action = EAFunctionFactory.createFunctionWithNamespace('EAWeightedSum', namespace=self.namespace)
            action.set_name(f'Action{actionIndex+1}')
            action.create_properties(parameters)

            # for column in range(columns):
            #    action.add_link(f'OL0C{column}')
            self.add_postprocessor(action)
            env.add_link(action)

    def get_arch_parameter(self, level_type, function_type):

        fn_class, var_type, var_props = self.arch.get_function_properties(
            level_type, function_type)
        #print(var_type, var_props)
        parameter = self.get_parameter(var_type, var_props)

        return parameter


    def get_level_type(self, level):
        levels = self.get_levels()
        if levels == 1 and level == 0:
            return HPCTARCH.ZEROTOP

        if levels > 1 and level == 0:
            return HPCTARCH.ZERO

        if levels > 1 and level < levels-1:
            return HPCTARCH.N

        if levels > 1 and level == levels-1:
            return HPCTARCH.TOP

        return None

    def get_function_parameters(self, level_type=None, level=None, column=None, function_type=None, levels_grid=None, var_type=None, var_props=None):
        parameters = {}

        fn_class, var_type, var_props = self.arch.get_function_properties(
            level_type, function_type)
        #print(var_type, var_props)
        parameter = self.get_parameter(var_type, var_props)

        if function_type == HPCTARCH.ACTION:
            parameters['parameter'] = parameter
            parameters['targetprefix'] = 'O'
            parameters['targetlevel'] = 0
            return parameters, fn_class

        if function_type == HPCTARCH.PERCEPTION:
            if (level_type == HPCTARCH.TOP or level_type == HPCTARCH.ZEROTOP) and self.toplevel_inputs is not None:
                parameters['inputs'] = [self.toplevel_inputs[column]]
                parameters['targetcolumns'] = 1
                parameters['parameter'] = parameter
            elif level_type == HPCTARCH.ZEROTOP:
                parameters['inputs'] = self.env_inputs
                parameters['targetcolumns'] = len(self.env_inputs)
                parameters['parameter'] = parameter
            elif level_type == HPCTARCH.ZERO:
                parameters['inputs'] = self.zerolevel_inputs
                parameters['targetcolumns'] = len(self.zerolevel_inputs)
                parameters['parameter'] = parameter
            else:
                parameters['targetlevel'] = level-1
                parameters['targetprefix'] = 'P'
                parameters['targetcolumns'] = levels_grid[level-1]
                parameters['parameter'] = parameter
            return parameters, fn_class

        if function_type == HPCTARCH.REFERENCE:
            if level_type == HPCTARCH.N or level_type == HPCTARCH.ZERO:
                parameters['targetlevel'] = level+1
                parameters['targetprefix'] = 'O'
                parameters['targetcolumns'] = levels_grid[level+1]
                parameters['parameter'] = parameter
            if level_type == HPCTARCH.TOP or level_type == HPCTARCH.ZEROTOP:
                parameters['value'] = self.references[column]
            return parameters, fn_class

        if function_type == HPCTARCH.OUTPUT:
            parameters['targetlevel'] = level
            parameters['targetprefix'] = 'C'
            parameters['targetcolumn'] = column
            parameters['addlink'] = False
            parameters['parameter'] = parameter

        return parameters, fn_class

    def get_parameter(self, type, props):
        parameter = ParameterFactory.createParameter(type)
        parameter.set_properties(props)
        return parameter

    def create_node(self, level, column, level_type, levels_grid):
        #print(f'level {level}  column {column} ' )

        parameters, fn_class = self.get_function_parameters(
            level_type, level, column, HPCTARCH.PERCEPTION, levels_grid)
        perception = EAFunctionFactory.createFunctionWithNamespace(fn_class, namespace=self.namespace)
        perception.set_name(f'PL{level}C{column}')
        perception.create_properties(parameters)

        parameters, fn_class = self.get_function_parameters(
            level_type, level, column, HPCTARCH.REFERENCE, levels_grid)
        reference = EAFunctionFactory.createFunctionWithNamespace(fn_class, namespace=self.namespace)
        reference.set_name(f'RL{level}C{column}')
        reference.create_properties(parameters)

        fn_class, _, _ = self.arch.get_function_properties(
            level_type, HPCTARCH.COMPARATOR)
        comparator = FunctionFactory.createFunctionWithNamespace(fn_class, namespace=self.namespace)
        comparator.set_name(f'CL{level}C{column}')
        comparator.set_link(reference)
        comparator.add_link(perception)

        parameters, fn_class = self.get_function_parameters(
            level_type, level, column, HPCTARCH.OUTPUT, levels_grid)
        output = EAFunctionFactory.createFunctionWithNamespace(fn_class, namespace=self.namespace)
        output.set_name(f'OL{level}C{column}')
        output.create_properties(parameters)
        output.set_link(comparator)

        node = PCTNode(name=f'L{level}C{column}', history=self.history, perception=perception,
                       reference=reference, comparator=comparator, output=output, namespace=self.namespace)
        node.links_built = True

        return node

    def configure_nodes(self, levels_grid):
        # print(levels_grid)
        levels = len(levels_grid)
        if levels == 1:
            level_type = HPCTARCH.ZEROTOP
        else:
            level_type = HPCTARCH.ZERO

        for level, columns in enumerate(levels_grid):
            if level > 0:
                if level == levels-1:
                    level_type = HPCTARCH.TOP
                else:
                    level_type = HPCTARCH.N
            for column in range(columns):
                node = self.create_node(level, column, level_type, levels_grid)
                self.add_node(node, level, column)

        # self.summary()



    def validate(self):
        func = self.preCollection[0]
        func.validate(len(self.postCollection))
                    
        num_outputs = len(self.hierarchy[0])
        for func in self.postCollection:
            func.validate(num_outputs)
            
        num_lower_perceptions = len(self.preCollection)-1
        levels = self.get_levels()
        for level, nodes in enumerate(self.hierarchy):
            if level < levels-1:
                num_higher_outputs = len(self.hierarchy[level+1])
            else:
                num_higher_outputs = None
            if level > 0:    
                num_lower_perceptions = len(self.hierarchy[level-1])
            for node in nodes:
                node.validate(num_lower_perceptions, num_higher_outputs)


    def mutate(self, evolve_properties):
        if evolve_properties['attr_mut_pb'] == 0:
            return False
            
        mutated = 0
        for level in range(len(self.hierarchy)):
            for col in range(len(self.hierarchy[level])):
                    node = self.hierarchy[level][col]
                    mutated += node.get_function_from_collection(CUF.REFERENCE).mutate(evolve_properties)
                    mutated += node.get_function_from_collection(CUF.PERCEPTION).mutate(evolve_properties)
                    mutated += node.get_function_from_collection(CUF.OUTPUT).mutate(evolve_properties)

        for func in self.postCollection:
            mutated += func.mutate(evolve_properties)   

        return mutated > 0


    @classmethod
    def from_config(cls, config, namespace=None):
        hpct = HPCTIndividual()
        namespace = hpct.namespace
        #print(namespace)
        preCollection = []        
        coll_dict = config['pre']
        env_dict = coll_dict.pop('pre0')

        env = EnvironmentFactory.createEnvironmentWithNamespace(env_dict['type'], namespace=namespace)
        for key, link in env_dict['links'].items():
            env.add_link(link)
        preCollection.append(env)
        HPCTNode.collection_from_config(preCollection, coll_dict, namespace=namespace)
        
        hpct.preCollection=preCollection
                
        hpct.hierarchy=[]

        # do in order of perceptions from bottom 
        # then from top references, comparator and output

        for level_key in config['levels']:
            cols = []
            for nodes_key in config['levels'][level_key]['nodes']:
                node = HPCTNode.from_config(config['levels'][level_key]['nodes'][nodes_key]['node'], namespace=namespace, perception=True)
                cols.append(node)
            hpct.hierarchy.append(cols)

        for level_key, level_value in dict(reversed(list(config['levels'].items()))).items():
            cols = []
            for nodes_key, nodes_value in dict(reversed(list(level_value['nodes'].items()))).items():
                node = hpct.get_node(level_value['level'], nodes_value['col'])
                HPCTNode.from_config(config=nodes_value['node'], namespace=namespace, reference=True, comparator=True,  output=True, node=node)
                
        postCollection = []        
        coll_dict = config['post']
        HPCTNode.collection_from_config(postCollection, coll_dict, namespace=namespace)
        hpct.postCollection=postCollection

    
        return hpct


    @classmethod
    def run_from_config(cls, config, render=False,  error_collector_type=None, error_response_type=None, 
        error_properties=None, error_limit=100, steps=500, verbose=False, early_termination=False):
        ind = cls.from_config(config)
        env = ind.get_preprocessor()[0]
        env.set_render(render)
        env.early_termination = early_termination
        error_collector = BaseErrorCollector.collector(error_response_type, error_collector_type, error_limit, properties=error_properties)

        ind.set_error_collector(error_collector)
        ind.run(steps, verbose)
        env.close()
        
        score=ind.get_error_collector().error()
        
        return ind, score




class HPCTNode(PCTNode):

    @classmethod
    def collection_from_config(node, collection, coll_dict, namespace):
        #print("collection_from_config", coll_dict)
        for fndict_label in coll_dict:
            #print("fndict_label",fndict_label)

            fndict = coll_dict[fndict_label]
            #print(fndict)
            fnname = fndict.pop('type')
            #print(fndict)
            #func = eval(fnname).from_config(fndict, namespace)
            if fnname.startswith('EA'):
                func = EAFunctionFactory.createFunctionFromConfig(fnname, namespace, fndict)
            else:
                func = FunctionFactory.createFunctionFromConfig(fnname, namespace, fndict)

            collection.append(func)


    @classmethod
    def from_config(cls, config=None, namespace=None, node=None, reference=False, comparator=False, perception=False, output=False):

        if node is None:
            node = PCTNode(default=False, name=config['name'], namespace=namespace)

        namespace= node.namespace

        if reference:
            node.referenceCollection = []
            collection = node.referenceCollection
            coll_dict = config['refcoll']
            HPCTNode.collection_from_config(collection, coll_dict, namespace)

        if perception:
            node.perceptionCollection = []
            collection = node.perceptionCollection
            coll_dict = config['percoll']
            HPCTNode.collection_from_config(collection, coll_dict, namespace)

        if comparator:
            node.comparatorCollection = []
            collection = node.comparatorCollection
            coll_dict = config['comcoll']
            HPCTNode.collection_from_config(collection, coll_dict, namespace)

        if output:
            node.outputCollection = []
            collection = node.outputCollection
            coll_dict = config['outcoll']
            HPCTNode.collection_from_config(collection, coll_dict, namespace)

        node.links_built = True
        return node

class HPCTEvolver(BaseEvolver):

    def __init__(self, environment_properties=None, evolve_properties=None, arch=None,
                 hpct_structure_properties=None, hpct_run_properties=None, output_properties=None,
                 hpct_architecture_properties=None, **cargs):
        super().__init__()

        self.member = 0
        self.gen = 1

        self.evolve_properties={}
        self.evolve_properties['alpha'] = self.get_property_value('alpha', evolve_properties, 0.5)
        self.evolve_properties['mu'] = self.get_property_value('mu', evolve_properties, 0.1)
        self.evolve_properties['sigma'] = self.get_property_value('sigma', evolve_properties, 0.25)
        self.evolve_properties['indpb'] = self.get_property_value('indpb', evolve_properties, 1)
        self.evolve_properties['attr_mut_pb'] = self.get_property_value('attr_mut_pb', evolve_properties, 1)
        self.evolve_properties['attr_cx_uniform_pb'] = self.get_property_value('attr_cx_uniform_pb', evolve_properties, 0.5)
        self.evolve_properties['structurepb'] = self.get_property_value('structurepb', evolve_properties, 1)

        if 'structurepb' in  self.evolve_properties:
            self.structurepb = self.evolve_properties['structurepb']

        self.fig_file = None
        if output_properties:
            if 'save_arch_all' in output_properties:
                self.save_arch_all = output_properties['save_arch_all']
        else:
            self.save_arch_all = False

        self.env_name = environment_properties['env_name']
        self.references = environment_properties['references']
        self.env_inputs_names = environment_properties['env_inputs_names']
        self.env_inputs_indexes = environment_properties['env_inputs_indexes']
        self.env_inputs_names = environment_properties['env_inputs_names']
        self.toplevel_inputs_indexes = environment_properties['toplevel_inputs_indexes'] 
        self.zerolevel_inputs_indexes = environment_properties['zerolevel_inputs_indexes']
        self.num_actions = environment_properties['num_actions']
        self.render  = self.get_property_value('render', environment_properties, False)
        self.early_termination   = self.get_property_value('early_termination', environment_properties, False)


        self.min_levels_limit = self.get_property_value('min_levels_limit', hpct_structure_properties, 1)
        self.max_levels_limit = self.get_property_value('max_levels_limit', hpct_structure_properties, 2)
        self.min_columns_limit = self.get_property_value('min_columns_limit', hpct_structure_properties, 1)
        self.max_columns_limit = self.get_property_value('max_columns_limit', hpct_structure_properties, 3)

        # self. = self.get_property_value('', hpct_run_properties, '')

        self.error_collector_type = self.get_property_value('error_collector_type', hpct_run_properties, 'InputsError')
        self.error_response_type = self.get_property_value('error_response_type', hpct_run_properties, 'RootMeanSquareError')
        self.error_properties = self.get_property_value('error_properties', hpct_run_properties, 'error:smooth_factor,0.5')

        self.error_limit = self.get_property_value('error_limit', hpct_run_properties, 100)
        self.nevals = self.get_property_value('nevals', hpct_run_properties, 2)
        self.history = self.get_property_value('history', hpct_run_properties, False)
        self.runs = self.get_property_value('runs', hpct_run_properties, 500)
        self.seed = self.get_property_value('seed', hpct_run_properties, 2)
        self.hpct_verbose = self.get_property_value('hpct_verbose', hpct_run_properties, False)
        self.debug = self.get_property_value('debug', hpct_run_properties, 0)

        #self.individual_properties = individual_properties

        if arch==None:
            self.arch = HPCTArchitecture(arch=hpct_architecture_properties)
        else:
            self.arch = arch

    def get_property_value(self, type, collection, default):
        value = default
        if collection is not None and type in collection:
            value = collection[type]
        return value



    def create_inputs(self, env_inputs_indexes, env_inputs_names, toplevel_inputs_indexes, zerolevel_inputs_indexes, env):
        if toplevel_inputs_indexes is not None:
            toplevel_inputs = []
            if len(toplevel_inputs_indexes) != len(self.references):
                raise Exception(
                    f'HPCTEvolver.create_inputs: top level inputs {len(toplevel_inputs_indexes)}, should be equal to number of references {len(self.references)}')
        else:
            toplevel_inputs = None

        env_inputs = []
        zerolevel_inputs = []
        for ctr, input_index in enumerate(env_inputs_indexes):
            if env_inputs_names == None:
                input_name = f'Input{ctr}'
            else:
                input_name = env_inputs_names[ctr]

            ip = IndexedParameter(index=input_index, name=input_name, links=[env], namespace=env.namespace)
            env_inputs.append(ip)
            if toplevel_inputs_indexes != None:
                if input_index in toplevel_inputs_indexes:
                    toplevel_inputs.append(ip)
                if input_index in zerolevel_inputs_indexes:
                    zerolevel_inputs.append(ip)
            else:
                zerolevel_inputs.append(ip)

        return env_inputs, toplevel_inputs, zerolevel_inputs

    def get_grid(self, grid=None):
        if grid is None:
            grid = []
            levels = random.randint(self.min_levels_limit, self.max_levels_limit)
            for level in range(levels-1):
                columns = random.randint(
                    self.min_columns_limit, self.max_columns_limit)
                grid.append(columns)
            grid.append(len(self.references))

        return grid

    def evaluate(self, hpct):
        if self.save_arch_all:
            self.fig_file = f'arch-{self.gen:04}-{self.member:04}.png'

        score = 0
        if self.debug > 2:
            # hpct.summary()
            print(f'{self.gen:03} {self.member:03} {hpct.namespace}')
            print(hpct.get_parameters_list())

        env = hpct.get_preprocessor()[0]
        for i in range(self.nevals):
            if self.seed != None:
                env.set_seed(self.seed+i)
            env.reset(full=False)
            if i > 0:
                env.set_render(False)

            if self.fig_file != None:
                hpct.draw(file=self.fig_file)

            hpct.get_error_collector().reset()
            hpct.run(steps=self.runs, verbose=self.hpct_verbose)
            # if i==0:
            #     env.close()
            current_error=hpct.get_error_collector().error()
            score += current_error

        score = score / self.nevals
        if self.debug > 1:
            print(f'{self.gen:03} {self.member:03} score {score:5.3f}')

        self.member += 1

        return score,

    def create(self, cls, grid=None):
        error_collector = BaseErrorCollector.collector(self.error_response_type, self.error_collector_type, self.error_limit, properties=self.error_properties)
        levels_columns_grid = self.get_grid(grid)
        if levels_columns_grid[-1] != len(self.references):
            raise Exception(
                f'HPCTEvolver.create: top level nodes {levels_columns_grid[-1]}, should be equal to number of references {len(self.references)}')

        self.arch.configure(len(levels_columns_grid))
        env = EnvironmentFactory.createEnvironment(self.env_name)
        # testing only
        if self.env_name == 'VelocityModel':
            env.mass, env.num_links, env.indexes=250, 2, 4
            env.init_value()
        else:
            env.render=self.render
            env.set_name(self.env_name)
            env.early_termination = self.early_termination
        # env=copy.deepcopy(self.env_name)
        # namespace = uuid.uuid1()
        #print(namespace)
        # env.namespace = namespace

        env_inputs, self.toplevel_inputs, self.zerolevel_inputs = self.create_inputs(self.env_inputs_indexes, self.env_inputs_names,
            self.toplevel_inputs_indexes, self.zerolevel_inputs_indexes, env)


        return cls(env=env, env_inputs=env_inputs, toplevel_inputs=self.toplevel_inputs,
                   zerolevel_inputs=self.zerolevel_inputs, history=self.history, error_collector=error_collector,
                   levels_columns_grid=levels_columns_grid, 
                #     env_inputs_names=self.env_inputs_names, 
                   arch=self.arch,
                   references=self.references, num_actions=self.num_actions)  # , lower_float=self.lower_float, upper_float=self.upper_float)

    def mate(self, indvidual1, indvidual2):
        child1 = CommonToolbox.getInstance().get_toolbox().clone(indvidual1) 
        child2 = CommonToolbox.getInstance().get_toolbox().clone(indvidual2)
        child1.change_namespace() 
        child2.change_namespace() 
        child1.checklinks = True
        child2.checklinks = True

        # return child1, child2

        # actions, at level 0
        child1actions = child1.get_postprocessor()
        child2actions = child2.get_postprocessor()
        #parameter = child1.get_arch_parameter(HPCTARCH.ZERO, HPCTARCH.ACTION)
        for ctr in range(self.num_actions):
            child1actions[ctr].mate(child2actions[ctr],  self.evolve_properties)
     
        # perceptions and outputs at all levels
        for level_lists in zip(child1.hierarchy,child2.hierarchy):
            #print(level_lists)
            for node in zip(level_lists[0], level_lists[1]):
                #print(node)
                # perceptions
                #parameter = child1.get_arch_parameter(child1.get_level_type(level), HPCTARCH.PERCEPTION)
                node[0].get_function_from_collection(CUF.PERCEPTION).mate(node[1].get_function_from_collection(CUF.PERCEPTION),  self.evolve_properties)

               # output
                #parameter = child1.get_arch_parameter(child1.get_level_type(level), HPCTARCH.OUTPUT)
                node[0].get_function_from_collection(CUF.OUTPUT).mate(node[1].get_function_from_collection(CUF.OUTPUT), self.evolve_properties)

        # references at all levels except top
        level=0
        stop_level = min(child1.get_levels(), child2.get_levels())-1
        for level_lists in zip(child1.hierarchy,child2.hierarchy):
            if stop_level == level:
                break
            #print(level_lists)
            for node in zip(level_lists[0], level_lists[1]):
                ref0 = node[0].get_function_from_collection(CUF.REFERENCE)
                ref1 = node[1].get_function_from_collection(CUF.REFERENCE)
                ref0.mate(ref1, self.evolve_properties)
                # node[0].get_function_from_collection(CUF.REFERENCE).mate(node[1].get_function_from_collection(CUF.REFERENCE), self.evolve_properties)

            level+=1


        if self.debug > 1:
            print(f'mate indvidual1 ', indvidual1.get_grid(), indvidual1.namespace)
            print(f'mate indvidual2 ', indvidual2.get_grid(), indvidual2.namespace)

        if self.debug>2:
            print('mate b4',indvidual1.namespace, indvidual1.get_parameters_list())
            print('mate b5',child1.namespace, child1.get_parameters_list())
            print('mate b4',indvidual2.namespace, indvidual2.get_parameters_list())
            print('mate b5',child2.namespace, child2.get_parameters_list())


        return child1, child2


    def mutate(self, hpct, choice=None, remove_level=None, remove_nodes=None, add_level=None, add_nodes=None):
        tb = CommonToolbox.getInstance().get_toolbox()
        mutant = tb.clone(hpct)
        mutant.change_namespace()
        mutant.reset_checklinks()
        mutated_structure = 0
        mutated=False

        if self.debug > 1:
            print(f'member {self.member:03}', mutant.get_grid(), mutant.namespace)
        if self.debug > 2:
            print('mut b4',mutant.get_parameters_list())

        mutated = mutant.mutate(self.evolve_properties)

        if random.random() < self.structurepb:
            mutated_structure = self.mutate_structure(mutant, choice, remove_level, remove_nodes, add_level, add_nodes)

        if mutated or mutated_structure>0:
            self.mutate_sum += 1

        if mutated_structure>0:
            self.mutate_structure_sum += 1

        if self.debug > 1:
            print(f'member {self.member:03}', mutant.get_grid(), mutant.namespace)
        if self.debug>2:
            print('mut b5',mutant.get_parameters_list())

        return mutant, 


    def add_nodes(self, individual, num_nodes, level, levels_columns_grid):  
        existing_columns = levels_columns_grid[level]

        if level==0:
            level_type = HPCTARCH.ZERO
        else:
            level_type = HPCTARCH.N

        # create nodes
        for column in range(existing_columns, existing_columns+num_nodes):
            node = individual.create_node(level, column, level_type, levels_columns_grid)            
            #node.summary()
            individual.add_node(node, level, column)

        if level==0:
            parameter = individual.get_arch_parameter(HPCTARCH.ZERO, HPCTARCH.ACTION)
            for action in  individual.get_postprocessor():
                action.add_connections(num_nodes, level,  parameter, 'O')
        else:
            # lower reference
            parameter = individual.get_arch_parameter(level_type, HPCTARCH.REFERENCE)
            for column in range(individual.get_columns(level-1)):
                node = individual.get_node(level-1, column)
                func = node.get_function_from_collection(CUF.REFERENCE)
                func.add_connections(num_nodes, level,  parameter, 'O')

        # higher perceptions
        level_type = individual.get_level_type(level+1)
        if (level_type == HPCTARCH.TOP or level_type == HPCTARCH.ZEROTOP) and self.toplevel_inputs is not None:
            # don't change top inputs
            pass
        else:
            parameter = individual.get_arch_parameter(individual.get_level_type(level+1), HPCTARCH.PERCEPTION)
            for column in range(individual.get_columns(level+1)):
                node = individual.get_node(level+1, column)
                func = node.get_function_from_collection(CUF.PERCEPTION)
                func.add_connections(num_nodes, level,  parameter, 'P')
        


    def add_level(self, individual, num_columns, level, levels_columns_grid):  
        levels=len(levels_columns_grid)
        # flist = FunctionsList.getInstance()

        new_levels = levels+1
        individual.insert_level(level)
        levels_columns_grid.insert(level, num_columns)
        levels_offset=2 if new_levels==2 else 3

        if new_levels==2:
            adjust_top_connections = num_columns - len(self.zerolevel_inputs)
        else:
            adjust_top_connections = num_columns - levels_columns_grid[-levels_offset]  

        # change top level nodes and function names
        top_level = new_levels-1
        for column in range(levels_columns_grid[-1]):
            node = individual.get_node(top_level, column)
            suffix = f'L{top_level}C{column}'
            node.get_function_from_collection(CUF.REFERENCE).set_name(f'R{suffix}')
            node.set_name(suffix)
            perception = node.get_function_from_collection(CUF.PERCEPTION)
            perception.set_name(f'P{suffix}')
            node.get_function_from_collection(CUF.COMPARATOR).set_name(f'C{suffix}')
            node.get_function_from_collection(CUF.OUTPUT).set_name(f'O{suffix}')

        # create nodes at new level
        level_type = individual.get_level_type(level)
        for column in range(num_columns):
            node = individual.create_node(level, column, level_type, levels_columns_grid)            
            #node.summary()
            individual.add_node(node, level, column)

        # top level change links
        for column in range(levels_columns_grid[-1]):
            node = individual.get_node(top_level, column)
            # suffix = f'L{top_level}C{column}'
            # node.get_function_from_collection(CUF.REFERENCE).set_name(f'R{suffix}')
            # node.set_name(suffix)
            perception = node.get_function_from_collection(CUF.PERCEPTION)
            # perception.set_name(f'P{suffix}')

            level_type = individual.get_level_type(top_level)
            if (level_type == HPCTARCH.TOP or level_type == HPCTARCH.ZEROTOP) and self.toplevel_inputs is not None:
                # don't change top inputs
                pass
            else:
                parameter = individual.get_arch_parameter(individual.get_level_type(level), HPCTARCH.PERCEPTION)
                if adjust_top_connections <0:
                    if len(perception.weights) - abs(adjust_top_connections)  <=0:
                        raise Exception(f'add_level: too many connections {abs(adjust_top_connections)} for {len(perception.weights)}')
                    perception.remove_connections(abs(adjust_top_connections))
                if adjust_top_connections >0:
                    perception.add_connections(adjust_top_connections, new_levels-2, parameter, 'P')
                #change the perception links
                perception.reset_links('P', level)

            # node.get_function_from_collection(CUF.COMPARATOR).set_name(f'C{suffix}')
            # node.get_function_from_collection(CUF.OUTPUT).set_name(f'O{suffix}')


        # lower level adjust connections
        adjust_lower_connections = num_columns - levels_columns_grid[-1]  
        if new_levels>2:
            # references
            lower_level = new_levels-levels_offset
            for column in range(levels_columns_grid[-levels_offset]):
                node = individual.get_node(lower_level, column)
                reference = node.get_function_from_collection(CUF.REFERENCE)

                parameter = individual.get_arch_parameter(individual.get_level_type(level), HPCTARCH.REFERENCE)
                if adjust_lower_connections <0:
                    reference.remove_connections(abs(adjust_lower_connections))
                if adjust_lower_connections >0:
                    reference.add_connections(adjust_lower_connections, new_levels-2, parameter, 'O')
        else:
            # actions
            # lower actions
            for action in  individual.get_postprocessor():
                # if adjust_lower_connections>0:
                parameter = individual.get_arch_parameter(HPCTARCH.ZERO, HPCTARCH.ACTION)
                action.reset_connections(num_columns, level,  parameter, 'O')
                # if adjust_lower_connections<0:
                #     action.remove_connections(abs(adjust_lower_connections))



    def remove_level(self, individual, level):
        levels_columns_grid = individual.get_grid()
        num_old_columns = levels_columns_grid[level]
        individual.remove_level(level)
        levels_columns_grid = individual.get_grid()

        adjust_top_perception_connections = levels_columns_grid[level-1] - num_old_columns 
        for column in range(levels_columns_grid[-1]):
            # rename top nodes
            node = individual.get_node(level, column)
            node.name = f'L{level}C{column}'
            # rename functions
            suffix = f'L{level}C{column}'
            node.get_function_from_collection(CUF.REFERENCE).set_name(f'R{suffix}')
            perception = node.get_function_from_collection(CUF.PERCEPTION)
            perception.set_name(f'P{suffix}')
            node.get_function_from_collection(CUF.COMPARATOR).set_name(f'C{suffix}')
            node.get_function_from_collection(CUF.OUTPUT).set_name(f'O{suffix}')

            if level==0:
                level_type = individual.get_level_type(level)
                if level_type == HPCTARCH.ZEROTOP:
                    if self.toplevel_inputs is None:
                        #parameter = individual.get_arch_parameter(level_type, HPCTARCH.PERCEPTION)
                        parameters, _ = individual.get_function_parameters(level_type, level, column, HPCTARCH.PERCEPTION, levels_columns_grid)
                        perception.clear_links()
                        perception.create_properties(parameters)
                    else:
                        # do not change top level perceptions
                        pass
                else:
                    raise Exception(f'TBI')

            else:
                level_type = individual.get_level_type(level)
                if (level_type == HPCTARCH.TOP or level_type == HPCTARCH.ZEROTOP) and self.toplevel_inputs is not None:
                    # don't change top inputs
                    pass
                else:
                    parameter = individual.get_arch_parameter(level_type, HPCTARCH.PERCEPTION)
                    if adjust_top_perception_connections <0:
                        perception.remove_connections(abs(adjust_top_perception_connections))
                    if adjust_top_perception_connections >0:
                        perception.add_connections(adjust_top_perception_connections, level-1, parameter, 'P')
                    perception.reset_links('P', level-1)


        adjust_lower_connections = levels_columns_grid[-1] - num_old_columns
        if level==0:
            # lower actions
            parameter = individual.get_arch_parameter(HPCTARCH.ZERO, HPCTARCH.ACTION)
            for action in  individual.get_postprocessor():
                if adjust_lower_connections>0:
                    action.add_connections(adjust_lower_connections, level,  parameter, 'O')
                if adjust_lower_connections<0:
                    action.remove_connections(abs(adjust_lower_connections))
        else:
            # lower references
            num_new_columns = levels_columns_grid[level]
            lower_level = level-1
            for column in range(levels_columns_grid[lower_level]):
                node = individual.get_node(lower_level, column)
                reference = node.get_function_from_collection(CUF.REFERENCE)

                if adjust_lower_connections <0:
                    reference.remove_connections(abs(adjust_lower_connections))
                if adjust_lower_connections >0:
                    parameter = individual.get_arch_parameter(individual.get_level_type(lower_level), HPCTARCH.REFERENCE)
                    reference.add_connections(adjust_lower_connections, lower_level+1, parameter, 'O')


    def remove_nodes(self, individual, level, num_nodes):
        #levels_columns_grid = individual.get_grid()
        individual.remove_nodes(level, num_nodes)
        levels_columns_grid = individual.get_grid()

        # perceptions at higher level
        higher_level = level+1
        level_type = individual.get_level_type(higher_level)
        if (level_type == HPCTARCH.TOP or level_type == HPCTARCH.ZEROTOP) and self.toplevel_inputs is not None:
            # don't change top level perceptions
            pass
        else:
            for column in range(levels_columns_grid[higher_level]):
                node = individual.get_node(higher_level, column)
                perception = node.get_function_from_collection(CUF.PERCEPTION)
                if self.debug>1:
                    print(f'Remove {num_nodes} connections from {len(perception.weights)} links')
                    if num_nodes == len(perception.weights):
                        print(individual.get_parameters_list())
                        individual.summary()
                        pass                        
                if num_nodes > len(perception.weights):
                    print(individual.get_parameters_list())
                    individual.summary()
                perception.remove_connections(num_nodes)

        if level==0:
            # lower actions
            for action in  individual.get_postprocessor():
                action.remove_connections(num_nodes)
        else:
            # references of lower level
            lower_level = level-1
            for column in range(levels_columns_grid[lower_level]):
                node = individual.get_node(lower_level, column)
                reference = node.get_function_from_collection(CUF.REFERENCE)
                reference.remove_connections(num_nodes)



    def mutate_structure(self, individual, choice=None, remove_level=None, remove_nodes=None, add_level=None, add_nodes=None):

        if isinstance(individual.get_postprocessor()[0].get_links()[0], str):
            pass
        else:
            if individual.get_postprocessor()[0].get_links()[0].get_name() == 'OL1C0':
                raise Exception('Wrong action connection')

        mutated_structure = False
        if choice is None:
            choice = random.randint(1,4)
        if self.debug>1:
            print('choice',choice)
        levels = individual.get_levels()
        levels_columns_grid = individual.get_grid()
        #print(levels_columns_grid)
        if choice == 1 :
            upper_levels_limit = levels-2
            if upper_levels_limit >= 0:
                if add_level is None:
                    add_level = random.randint(0, levels-2)
                # can't add to top level
                if add_level+1 < levels:
                    max_columns_limit = self.max_columns_limit
                    columns = individual.get_columns(add_level)
                    if columns < max_columns_limit:
                        if add_nodes is None:
                            add_nodes = random.randint(1, max_columns_limit-columns)
                        if self.debug>1:
                            print(f'Add {add_nodes} nodes to level {add_level}' )
                            if add_nodes==1 and add_level==0:                                
                                print(individual.get_parameters_list())
                                individual.summary()
                                #individual.draw(file='hpct-level0nodes1.png', with_edge_labels=True)

                        self.add_nodes(individual, add_nodes, add_level, levels_columns_grid)            
                        mutated_structure = True

        if choice == 2 :
            max_levels_limit = self.max_levels_limit
            if levels < max_levels_limit:
                if add_nodes is None:
                    add_nodes = random.randint(1, self.max_columns_limit)
                if self.debug>1:
                    print(f'Add level {levels-1} with {add_nodes} node(s)' )
                self.add_level(individual, add_nodes, levels-1, levels_columns_grid)
                mutated_structure = True
                #struct, mutated_structure = cs.add_level(num_columns=num_columns)

        if choice == 3 :
            min_levels_limit = self.min_levels_limit
            if levels > min_levels_limit:
                remove_level = levels-2
                if self.debug>1:                    
                    print(f'Remove level {remove_level} from {levels} levels {levels_columns_grid}' )
                self.remove_level(individual, remove_level)
                mutated_structure = True
                #struct, mutated_structure = cs.remove_level()

        if choice == 4 :
            upper_levels_limit = levels-2
            if upper_levels_limit >= 0:
                if remove_level is None:
                    remove_level = random.randint(0, upper_levels_limit)
                upper_node_limit =  levels_columns_grid[remove_level]-1
                if upper_node_limit > 0:
                    min_columns_limit = self.min_columns_limit
                    columns = levels_columns_grid[remove_level]               
                    if columns > min_columns_limit:
                        if remove_nodes is None:
                            remove_nodes = random.randint(1, upper_node_limit)
                        if self.debug>1:
                            print(f'Remove {remove_nodes} node(s) from level {remove_level}')
                            # if remove_nodes==3 and remove_level==0:                                
                            #     print(individual.get_parameters_list())
                            #     individual.summary()
                        self.remove_nodes(individual, remove_level, remove_nodes)
                        mutated_structure = True
                        #struct, mutated_structure = cs.remove_nodes(level=remove_level, num_nodes=remove_nodes)

        if individual.get_postprocessor()[0].get_links()[0].get_name() == 'OL1C0':
            raise Exception('Wrong action connection')

        return mutated_structure



    def create_plot(self):
        return 0

    def animate(self, epoch):
        pass


class HPCTEvolverWrapper(EvolverWrapper):

    def run(self, gens=25, verbose=False, deap_verbose=False, log=False):
        log_string = ''
        
        if self.save_arch_all:
            self.evolver.set_save_arch_all(self.save_arch_all)
            self.evolver.set_gen(0)

        self.pop = self.toolbox.population(n=self.pop_size)
        self.genealogy.update(self.pop)

        if verbose>0:
            logs = 'gen   pop   min       mean      max        mut  muts  timing'
            print(logs)
        if log:
            logs = 'gen   pop   min       mean      max        mut  muts  timing'
            log_string = ''.join((log_string, '# ', logs, '\n'))

        self.best_of_gens=[]
        top_ind = tools.selBest(self.pop, k=1)[0]
        self.best_of_gens.append(top_ind)

        for gen in range(1, gens+1, 1):
            self.evolver.set_gen(gen)
            tic = time.perf_counter()
            self.pop, logbook = algorithms.eaSimple(self.pop, self.toolbox, cxpb=self.p_crossover,
                    mutpb=self.p_mutation,  ngen=1, halloffame=self.hof, stats=self.stats, verbose=deap_verbose)
            toc = time.perf_counter()
            timeperpop = (toc-tic)/self.pop_size
            self.timing_sum += timeperpop
            self.evolver.member=0
            if gen == 1:
                log_stats = self.collect_stats( 0, 0, logbook, timeperpop, verbose, log)
                if log:
                    log_string = ''.join((log_string, log_stats))

            log_stats = self.collect_stats( gen, 1, logbook, timeperpop, verbose, log)

            if verbose>2:
                print('pop ***')
                for pop in self.pop:
                    print(pop)

            top_ind = tools.selBest(self.pop, k=1)[0]
            if verbose>1:
                print ( f'[{top_ind}]')
            else:
                if verbose>0:
                    print()
                if log:
                    log_string = ''.join((log_string, log_stats, '\n'))

            self.best_of_gens.append(top_ind)
            # if self.display_env and gen == gens:
            if self.display_env:

                if self.save_arch_gen:
                    self.evolver.fig_file = f'fig{gen:03}.png'

                print(f'Displaying gen {gen}')

                ind, score = HPCTIndividual.run_from_config(top_ind.get_config(), render=True,  error_collector_type=self.evolver.error_collector_type, 
                    error_response_type=self.evolver.error_response_type, error_properties=self.evolver.error_properties, 
                    error_limit=100, steps=500, verbose=False, early_termination=self.evolver.early_termination)

                self.evolver.fig_file = None


                # newind = CommonToolbox.getInstance().get_toolbox().clone(top_ind)
                # newind.change_namespace() 
                # environment = newind.get_preprocessor()[0]
                # if hasattr(environment, 'env'):
                #     if isinstance(environment, OpenAIGym):
                #         environment.set_render(True)
                #         if self.save_arch_gen:
                #             self.evolver.fig_file = f'fig{gen:03}.png'
                #         # if gen == 1:
                #         #     best = self.best_of_gens[0]
                #         #     environment_zero = best.get_preprocessor()[0]
                #         #     print('Displaying gen 0')
                #         #     environment_zero.set_render(True)
                #         #     self.evolver.evaluate(best)
                #         #     print('>> Press enter to continue:')
                #         #     input()
                #         #     print('Displaying gen 0')
                #         #     environment_zero.set_render(True)
                #         #     self.evolver.evaluate(best)
                #         #     environment_zero.set_render(False)
                #         #     print(best, best.get_parameters_list())
                #         print(f'Displaying gen {gen}')
                #         self.evolver.evaluate(newind)
                #         self.evolver.fig_file = None
                #         environment.set_render(False)
                #         environment.close()
                #         print(top_ind, top_ind.get_parameters_list())

        return self.timing_sum/gens, log_string





class HPCTEvolveProperties(object):


    def __init__(self):
        # self.properties = {}
        self.environment_properties = {} 
        self.evolve_properties = {}  
        self.hpct_structure_properties = {}
        self.hpct_run_properties = {}
        self.file_properties = {}
        self.wrapper_properties = {}
     

    def set_property_value(self, properties_var=None, existing_var=False, var=None, property_name=None,  
        int_convert=False, float_convert=False, eval_convert=False, stringList=False, default=None):

        if stringList:
            properties_var[property_name] = stringListToListOfStrings(self.db[property_name], ',')
            return

        if existing_var:
            if var == None:
                if int_convert:
                    properties_var[property_name] = int(self.db[property_name])
                else:
                    properties_var[property_name] = self.db[property_name]
            else:
                properties_var[property_name] = var
        else:
            if property_name in self.db:
                if eval_convert:
                    properties_var[property_name] = eval(self.db[property_name])
                elif float_convert:
                    properties_var[property_name] = float(self.db[property_name])                    
                elif int_convert:
                    properties_var[property_name] = int(self.db[property_name])
                else:
                    properties_var[property_name] = self.db[property_name]
            else:
                properties_var[property_name] = default


    def load_db(self, file):
        from jproperties import Properties

        # read properties from file
        configs = Properties()
        with open(file, 'rb') as config_file:
            configs.load(config_file)

        items_view = configs.items()
        self.db = {}
        for item in items_view:
            self.db[item[0]] = item[1].data


    def get_error_properties(self):

        error_properties = []
        for property in range(1, 100):
            property_key = f'property{property}'
            if property_key in self.db:
                property_string = self.db[property_key]
                strarr = property_string.split(':')
                if strarr[0] == 'error':
                    parr = strarr[1].split(',')
                    prop=[]
                    prop.append(parr[0])
                    prop.append(parr[1])
                    error_properties.append(prop)
        return error_properties
        
    def collect_types_strings(self):
        types_strings={}
        for type in range(1, 100):
            type_key = f'type{type}'
            if type_key in self.db:
                types_strings[type_key]=self.db[type_key]

        return types_strings

    def collect_configs_strings(self):
        configs_strings={}
        for config in range(1, 100):
            config_key = f'config{config}'
            if config_key in self.db:
                configs_strings[config_key]=self.db[config_key]

        return configs_strings

    #@classmethod
    def load_properties(self, file=None, nevals=None, seed=None, print_properties=False,
                        gens=None, pop_size=None, evolve=False):

        self.load_db(file)

        # evolve arguments
        self.set_property_value(properties_var=self.wrapper_properties, existing_var=True, var=pop_size, property_name='pop_size', int_convert=True)
        self.set_property_value(properties_var=self.wrapper_properties, existing_var=True, var=gens, property_name='gens', int_convert=True)
        self.set_property_value(properties_var=self.wrapper_properties, property_name='p_crossover', float_convert=True)
        self.set_property_value(properties_var=self.wrapper_properties, property_name='p_mutation', float_convert=True)
        self.set_property_value(properties_var=self.evolve_properties, property_name='attr_mut_pb', float_convert=True)
        self.set_property_value(properties_var=self.evolve_properties, property_name='structurepb', float_convert=True)


        # if evolve:
        #     raw = None
        # else:
        #     if 'raw' in db.keys():
        #         raw = eval(db['raw'])
        #     else:
        #         fh = open(file, "r")
        #         for _ in range(5):
        #             line = fh.readline()
        #             #print('<',line,'>')
        #             if line.startswith('# Best individual'):
        #                 break
        #         line = fh.readline()
        #         #print(line[2:])
        #         raw = eval(line[2:])
        #         fh.close()
        # self.file_properties['raw'] = raw

        self.file_properties['desc'] = self.db['desc']

        self.set_property_value(properties_var=self.environment_properties, property_name='early_termination', eval_convert=True, default=False)
        self.set_property_value(properties_var=self.environment_properties, property_name='env_inputs_indexes', eval_convert=True)
        self.set_property_value(properties_var=self.environment_properties, property_name='references', eval_convert=True)
        self.set_property_value(properties_var=self.environment_properties, property_name='toplevel_inputs_indexes', eval_convert=True)
        self.set_property_value(properties_var=self.environment_properties, property_name='zerolevel_inputs_indexes', eval_convert=True)
        self.set_property_value(properties_var=self.environment_properties, property_name='env_inputs_names', stringList=True)
        self.set_property_value(properties_var=self.environment_properties, property_name='env_name')
        self.set_property_value(properties_var=self.environment_properties, property_name='num_actions', int_convert=True)

        self.set_property_value(properties_var=self.hpct_structure_properties, property_name='min_levels_limit', int_convert=True, default=1)
        self.set_property_value(properties_var=self.hpct_structure_properties, property_name='min_columns_limit', int_convert=True, default=1)
        self.set_property_value(properties_var=self.hpct_structure_properties, property_name='max_levels_limit', int_convert=True, default=1)
        self.set_property_value(properties_var=self.hpct_structure_properties, property_name='max_columns_limit', int_convert=True, default=1)
        self.set_property_value(properties_var=self.hpct_structure_properties, property_name='lower_float', float_convert=True)
        self.set_property_value(properties_var=self.hpct_structure_properties, property_name='upper_float', float_convert=True)
        self.set_property_value(properties_var=self.hpct_structure_properties, property_name='mode', eval_convert=True)

        self.hpct_structure_properties['types_strings'] = self.collect_types_strings()
        self.hpct_structure_properties['configs_strings'] = self.collect_configs_strings()

        error_properties = self.get_error_properties()
        self.hpct_run_properties['error_properties'] = error_properties
        self.set_property_value(properties_var=self.hpct_run_properties, property_name='error_collector_type',  default='TotalError')
        self.set_property_value(properties_var=self.hpct_run_properties, property_name='error_response_type',  default='RootSumSquaredError')
        self.set_property_value(properties_var=self.hpct_run_properties, existing_var=True, var=nevals, property_name='nevals', int_convert=True, default=1)
        self.set_property_value(properties_var=self.hpct_run_properties, existing_var=True, var=seed, property_name='seed', int_convert=True)
        self.set_property_value(properties_var=self.hpct_run_properties, property_name='error_limit', float_convert=True)
        self.set_property_value(properties_var=self.hpct_run_properties, property_name='runs', int_convert=True)


        if print_properties:
            print('Properties:')
            print(f'Description = {self.db["desc"]}, inputs = {self.environment_properties["env_name"]}')
            print(f'inputs = {self.environment_properties["env_inputs_indexes"]}, references = {self.environment_properties["references"]}, top_inputs = {self.environment_properties["toplevel_inputs_indexes"]}')
            print(f'names = {self.environment_properties["env_inputs_names"]}, early_termination = {self.environment_properties["early_termination"]}')
            print(f'error_collector = {self.hpct_run_properties["error_collector_type"]}, error_response = {self.hpct_run_properties["error_response_type"]}, error_limit = {self.hpct_run_properties["error_limit"]}')
            print(f'pop_size = {self.wrapper_properties["pop_size"]}, gens = {self.wrapper_properties["gens"]}, attr_mut_pb = {self.evolve_properties["attr_mut_pb"]}, structurepb = {self.evolve_properties["structurepb"]}, lower_float = {self.hpct_structure_properties["lower_float"]}, upper_float = {self.hpct_structure_properties["upper_float"]}')
            print(f'p_crossover = {self.wrapper_properties["p_crossover"]}, p_mutation = {self.wrapper_properties["p_mutation"]}')
            print(f'seed = {self.hpct_run_properties["seed"]}, nevals = {self.hpct_run_properties["nevals"]}, runs = {self.hpct_run_properties["runs"]}, mode = {self.hpct_structure_properties["mode"]}')
            # if raw != None:
            #     print(raw)

        

    # Cell
    def setup_environment(self, properties, render=False, seed=None, early_termination=None,
            error_collector_type=None, error_response_type=None):

        if error_collector_type == None:
            error_collector_type = properties['error_collector_type']
        if error_response_type == None:
            error_response_type = properties['error_response_type']
        if early_termination == None:
            early_termination = properties['early_termination']

        env_name = properties['env_name']
        error_limit = properties['error_limit']
        error_properties = properties['error_properties']
        if seed == None:
            seed = properties['seed']


        env = EnvironmentFactory.createEnvironment(env_name)
        env.render=render
        env.set_name(env_name)
        env.early_termination = early_termination

        if env == None:
            env = EnvironmentFactory.createEnvironment('DummyModel')

        error_collector = BaseErrorCollector.collector(error_response_type, error_collector_type, error_limit, properties=error_properties)
        if seed != None:
            env.set_seed(seed)
        env.reset()

        return env, error_collector


    # def get_types_string(self):
    #     types_string=""
    #     types_strings = self.hpct_structure_properties['types_strings'] 
    #     for type_key, type_value in types_strings.items():
    #         types_string+=type_value
    #         type_list = stringListToListOfStrings(type_value, ',')
    #         lk = eval(type_list[0])
    #         #print(lk, type_list[1], type_list[2])
    #         # structure.set_config_type(lk, type_list[1], type_list[2])

    #     return types_string

    def get_configs_string(self):
        configs_string=""
        configs_strings = self.hpct_structure_properties['configs_strings']
        for config_key, config_value  in configs_strings.items():
            configs_string+=config_value
            config_list = stringListToListOfStrings(config_value,',')
            lk = eval(config_list[0])
            bk = eval(config_list[3])
            #print(lk, config_list[1], config_list[2], bk)
            # structure.set_config_parameter(lk, config_list[1], config_list[2], bk)

        return configs_string

    def create_hash_string(self, properties_string, configs_string):

        hs = ''.join((f'{self.environment_properties["env_inputs_indexes"]}{self.environment_properties["references"]}{self.environment_properties["toplevel_inputs_indexes"]}',
            f'{properties_string}{self.file_properties["desc"]}{self.hpct_run_properties["error_response_type"]}{self.hpct_run_properties["error_collector_type"]}',
            f'{configs_string}{self.hpct_structure_properties["mode"]}{self.hpct_run_properties["seed"]}{self.wrapper_properties["pop_size"]}',
            f'{self.wrapper_properties["gens"]}{self.evolve_properties["attr_mut_pb"]}{self.evolve_properties["structurepb"]}',
            f'{self.hpct_run_properties["runs"]}{self.hpct_structure_properties["lower_float"]}{self.hpct_structure_properties["upper_float"]}',
            f'{self.hpct_structure_properties["max_levels_limit"]}{self.hpct_structure_properties["max_columns_limit"]}',
            f'{self.hpct_structure_properties["min_levels_limit"]}{self.hpct_structure_properties["min_columns_limit"]}',
            f'{self.hpct_run_properties["error_limit"]}{self.wrapper_properties["p_crossover"]}{self.wrapper_properties["p_mutation"]}'))
      
        return  hs 

    def get_verbose_property(self, key, verbose, default=False):
        value = default
        if key in verbose:
            value = verbose[key]
        return value

    def write_output(self, output, out_dir, env_name, desc, hash_num, overwrite):

        if output:
            import os
            dir1 = out_dir + env_name
            if not os.path.isdir(dir1):
                os.mkdir(dir1)
            dir2 = dir1+os.sep+desc
            if not os.path.isdir(dir2):
                os.mkdir(dir2)
            exists, fname = check_hash_file_exists(dir2, hash_num)
            if exists and not overwrite:
                print(f'Skipping file {fname}')
                return True, None
                # return None,None,None
    
            return False, dir2

        return False, None


    def evolve_from_properties_file(self, file=None, verbose=None, env_name=None, seed=None,
            test=False, gens=None, pop_size=None, nevals = None, move=None, out_dir=None, node_size=200,
            parallel=False, video_wrap=False, log=False, figsize=(12,12), summary=False, draw_file=None, with_edge_labels=True,
            print_properties=False, overwrite=False, output=False, toolbox=None, processes=1):

        import hashlib
        self.load_properties(file, print_properties=print_properties, evolve=True)

        if gens is None:
            gens = self.wrapper_properties['gens']

        if seed is None:
            seed = self.hpct_run_properties['seed']
        # modes_list = properties['modes']
       
        # types_string = self.get_types_string()
        configs_string= self.get_configs_string()

        properties_string=""
        #print(error_properties)
        for property in self.hpct_run_properties['error_properties']:
            property_string = property[0]+property[1]
            properties_string+=property_string

        #print(structure.get_config())
        # env factory
        env_name = self.environment_properties['env_name']
        env = EnvironmentFactory.createEnvironment(env_name)
        env.set_name(env_name)
        namespace=env.namespace

        if video_wrap:
            env.set_video_wrap(video_wrap)
            env.create_env(seed)

        debug = self.get_verbose_property( 'debug', verbose, default=0)
        hpct_verbose = self.get_verbose_property ('hpct_verbose', verbose)

        self.hpct_run_properties['hpct_verbose']=hpct_verbose
        self.hpct_run_properties['debug']= debug  

        save_arch_all = self.get_verbose_property( 'save_arch_all', verbose)
        save_arch_gen = self.get_verbose_property( 'save_arch_gen', verbose)
        display_env = self.get_verbose_property( 'display_env', verbose)
        evolve_verbose = self.get_verbose_property( 'evolve_verbose', verbose)
        deap_verbose = self.get_verbose_property( 'deap_verbose', verbose)

        desc = self.file_properties['desc']
        # create hash
        #print(modes_list)
        hash_string = self.create_hash_string(properties_string, configs_string)
        #print(hash_string)
        hash_num = hashlib.md5(hash_string.encode()).hexdigest()
        #print(hash_num)


        skip, dir = self.write_output(output, out_dir, env_name, desc, hash_num, overwrite)
        if skip:
            return None,None,None


        arch = HPCTArchitecture(mode=self.hpct_structure_properties["mode"], lower_float=self.hpct_structure_properties["lower_float"], upper_float=self.hpct_structure_properties["upper_float"])
        arch.configure()
        
        evolver_properties = {'environment_properties':self.environment_properties, 
        'evolve_properties':self.evolve_properties,  
        'hpct_structure_properties':self.hpct_structure_properties,
        'hpct_run_properties':self.hpct_run_properties,
        'arch': arch}

        random.seed(seed)
        evolver = HPCTEvolver(**evolver_properties)
        # print(evolver_properties)
        
        self.wrapper_properties['evolver']=evolver
        self.wrapper_properties['save_arch_all']=save_arch_all
        self.wrapper_properties['save_arch_gen']=save_arch_gen
        self.wrapper_properties['display_env']=display_env
        self.wrapper_properties['select']={'selection_type':'tournament'}
        self.wrapper_properties['processes']=processes
        self.wrapper_properties['toolbox']=toolbox        
        evr = HPCTEvolverWrapper(**self.wrapper_properties)

        if test:
            #meantime = evr.run(gens=int(db['MAX_GENERATIONS']), verbose=verbose['evolve_verbose'], deap_verbose=verbose['deap_verbose'])
            raw= [777] #evr.best()
            score = 47.2345 #evr.best_score()
            print("Best Score: %0.5f" % score)
            print("Best Ind: ", raw)
            #print(f'Mean time: {meantime:6.3f}')

        else:
            meantime, log_string = evr.run(gens=gens, verbose=evolve_verbose, deap_verbose=deap_verbose, log=log)
            best= evr.best()
            score = evr.best_score()
            s1 = f'Best Score: {score:0.5f}'
            s2 = f'Best Ind: {best.get_parameters_list()}'
            s3 = f'Mean time: {meantime:6.3f}'
            if log:
                log_string = ''.join((log_string, '# ', s1, '\n# ', s2, '\n# ', s3, '\n'))
            if evolve_verbose:
                print(s1)
                print(s2)
                print(s3)

            # draw architecture
            if draw_file is not None:
                if move == None:
                    move={}
                best.draw(file=draw_file, with_edge_labels=with_edge_labels, node_size=node_size, figsize=figsize)

        # write results
        output_file = None
        if output:
            import os
            struct = best.get_grid()
            levels = len(struct)
            cols = max(struct)
            if seed == None:
                seed = 'N'
            # delim = os.sep
            # file = delim.join((root_dir, path, file))
            file_contents =  self.get_file_contents(file)

            output_file = dir+os.sep +f'ga-{score:07.3f}-s{seed:03}-{levels}x{cols}-m{self.hpct_structure_properties["mode"]}-{hash_num}.properties'
            if print_properties:
                print(output_file)
            f = open(output_file, "w")
            from datetime import datetime   
            dateTimeObj = datetime.now()
            f.write(f'# Date {dateTimeObj}\n')
            f.write('# Result'+'\n')
            f.write('# Best individual'+'\n')
            f.write(f'raw = {best.get_parameters_list()}'+'\n')
            f.write(f'score = {score:0.5f}'+'\n')
            f.write(f'# Time  {meantime:0.4f}'+'\n')
            f.write(file_contents.replace(f'seed = {int(self.hpct_run_properties["seed"])}', f'seed = {seed}')+'\n')
            if log:
                f.write(log_string)

            f.close()
        env.close()

        return output_file, evr, score

    def get_file_contents(self, file):
        from io import StringIO
        file_str = StringIO()
        with open(file, 'r') as f:
            for line in f:
                if line.startswith('# Date') or line.startswith('# Result') or line.startswith('# Best individual') or line.startswith('raw') or line.startswith('score')or line.startswith('# Time'):
                    pass
                else:
                    file_str.write(line)

        return file_str.getvalue()




class HPCTGenerateEvolvers(object):
    def __init__(self, iters=1, envs=None, collection=None, configs=None, properties=None, varieties=None):
        import os
        for env in envs:
            if not os.path.isdir(env):
                os.mkdir(env)

        for env in envs:
            num_actions = varieties[env]['num_actions']
            nevals = varieties[env]['nevals']
            archs = varieties[env]['archs']
            for arch in archs:
                key = '_'.join((env,arch['name']))
                print(key)
                config = configs[key]
                self.generate_option_files(iters, env, num_actions, arch, config, nevals, properties, collection)

    def generate_option_files(self, iters, env, num_actions, arch, config, nevals, properties, collection):
        import os
        arch_name = arch['name']
        # inputs_names = arch['inputs_names']
        ppars = ''

        collectors=collection[env]['arch'][arch_name]['collectors']
        responses=collection[env]['arch'][arch_name]['responses']
        structs=collection[env]['arch'][arch_name]['structs']


        for collector in collectors:
            for response in responses:
                    for struct in structs:
                        desc, filename = self.description(collector,response,  f'Mode{struct["mode"]:02}', arch_name)
                        fpars = self.fixed_parameters(env, arch, num_actions)
                        cpars = self.configurable_parameters( config, collector, response, nevals)
                        ppars = self.additional_properties(properties, response, collector)
                        spars = self.structure_parameters(collector,response,  struct, arch_name)
                        # display = f'### Display\n\ninputs_names = {inputs_names}\n'
                        
                        text = '\n'.join((desc, fpars, cpars, ppars, spars))
                        filepath = f'{env}{os.sep}{filename}.properties'
                        self.write_to_file(filepath, text)
                        cmd = f'python run-dynamic-evolver-multi.py {filepath} -i {iters}'
                        print(cmd, end='\n')

    def additional_properties(self, properties, response, collector):
        ppars = ''
        
        if len(properties)>0:
            ppars='### Additional properties\n\n'

        ctr = 1
        for  prop in properties:
            value = properties[prop]
            if response == 'SmoothError' and prop == 'error:smooth_factor':
                propstr = f'property{ctr} = {prop},{value}'        
                ppars = ''.join((ppars, propstr, '\n'))
                ctr+=1
            
            if collector == 'ReferencedInputsError' and  prop == 'error:referenced_inputs':
                propstr = f'property{ctr} = {prop},{value}'        
                ppars = ''.join((ppars, propstr, '\n'))
                ctr+=1
                

        return ppars                        


    def write_to_file(self, file, text):
        f = open(file, "w")
        f.write(text)
        f.close()

    def structure_parameters(self, collector,response,  struct, arch):
        header = '### Structure\n\n'
        header = header + '# modes - pattern of nodes at particular levels, zero, n, top and zerotop\n'
        header = header + '# the mode numbers refer to:\n'
        header = header + '# 0 - per:bin-ws, ref:flt-ws, com:sub, out:flt-ws\n'

        mode = 0
        # if struct == 'SmoothWeightedSum':
        #     modes = [6, 6, 5, 5]
            
        mstr = f'mode = {mode}'
        type_num = 1
        types = ''

        for type in struct['types']:
            types = ''.join((types, f'type{type_num} = HPCTARCH.{type[0].name} HPCTARCH.{type[1].name} HPCTARCH.{type[2].name} {type[3]}\n'))

        # if weight == 'Floats' or weight == 'AllFloats':
        #     types = ''.join((types, f'type{type_num} = [LevelKey.ZERO, perception, Float]\n'))
        #     type_num += 1
        #     types = ''.join((types, f'type{type_num} = [LevelKey.N, perception, Float]\n'))
        #     type_num += 1
        #     types = ''.join((types, f'type{type_num} = [LevelKey.TOP, perception, Float]\n'))
        #     type_num += 1

        # if weight == 'AllFloats':
        #     types = ''.join((types, f'type{type_num} = [LevelKey.ZERO, action, Float]\n'))
        #     type_num += 1
            
        # if struct == 'SmoothWeightedSum':
        #     types = ''.join((types, f'type{type_num} = [LevelKey.ZERO, output, Smooth]\n'))
        #     type_num += 1
        #     types = ''.join((types, f'type{type_num} = [LevelKey.N, output, Smooth]\n'))
        #     type_num += 1
        #     types = ''.join((types, f'type{type_num} = [LevelKey.TOP, output, Smooth]\n'))
        #     type_num += 1

        types = types + '\n\n\n\n'
            
        
        rtn = '\n'.join((header, mstr, types))
        return rtn


    def configurable_parameters(self,  config, collector, response, nevals):  
        header = ''.join(("### Configurable parameters\n\n# Randomisation seed to reproduce results\n# Size of population\n", 
                        "# Number of generations\n# Probability that an attribute will be mutated\n# Probability that the structure will be mutated\n",
                        "# Number of runs of environment\n# Lower limit of float values\n# Upper limit of float values\n",
                        "# Initial limit of levels\n# Initial limit of columns\n# Lower limit of levels\n# Lower limit of columns\n",
                        "# Limit of error on which to terminate individual evaluation\n# Probability for crossover\n# Probability for mutating an individual\n# Number of times the evaulation is run (with different random seeds)\n# Type of errors collected\n# Error function\n\n"))

        text = ''
        for key in config.keys():
            value = config[key]
            text = ''.join((text, key, ' = ', f'{value}', '\n'))
        
        text = ''.join((header, text, f'nevals = {nevals}\nerror_collector = {collector}\nerror_response = {response}\n'))
        
        #f'seed = {seed}\nPOPULATION_SIZE = {POPULATION_SIZE}\nMAX_GENERATIONS = {MAX_GENERATIONS}\nattr_mut_pb={attr_mut_pb}\nstructurepb={structurepb}\nruns={runs}\nlower_float = {lower_float}\nupper_float = {upper_float}\nlevels_limit = {levels_limit}\ncolumns_limit = {columns_limit}\nerror_limit = {error_limit}\np_crossover = {p_crossover}\np_mutation = {p_mutation}\nnevals = {nevals}\nerror_collector = {error_collector}\nerror_response = {error_response}\n'
        return text
        

    def description(self, collector,response, mode, arch):
        filename = '-'.join((arch, collector,response, mode))
        rtn = ''.join(('\n### Description:\n\n','desc = ', filename,'\n'))
        return rtn, filename

    def fixed_parameters(self, env, option, num_actions):  
            
        header = '### Environment parameters\n\n# Full list of input indexes from environment\n# List of input indexes from environment for zero level if not full\n# List of input indexes from environment for top level# List of reference values\n# Number of actions\n# Display names for environment inputs\n\n'
        text1 = f'env_name = {env}\n' 
        text1 = text1 + f'env_inputs_indexes = {self.get_parameter(option, "env_inputs_indexes")}\n'
        text1 = text1 + f'zerolevel_inputs_indexes = {self.get_parameter(option, "zerolevel_inputs_indexes")}\n'
        text1 = text1 + f'toplevel_inputs_indexes = {self.get_parameter(option, "toplevel_inputs_indexes")}\n'
        text1 = text1 + f'references = {self.get_parameter(option, "references")}\n'
        text1 = text1 + f'num_actions = {num_actions}\n'
        text1 = text1 + f'env_inputs_names = {self.get_parameter(option, "env_inputs_names")}\n'

        return ''.join((header,text1))    

    def get_parameter(self, pdict, name, default=None):
        if name in pdict:
            return pdict[name]

        return default