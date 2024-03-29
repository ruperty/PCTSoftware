#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 11:59:42 2020

@author: ruperty
"""

    
import random
import numpy as np
from abc import ABC
from deap import tools

from epct.structure import BinaryOnes
from pct.functions import WeightedSum
from pct.architectures import LevelKey


class BaseParameterType(ABC):
    "Base class of a hierarchy parameter type. This class is not used direclty by developers, but defines the interface common to all."
    def __init__(self):
        pass

    def set_parameters(self, pars, globals):
        for par in pars:
            cmd = f'self.{par} = {pars[par]}'
            exec(cmd)
            
    def set_node_function(self, node, function, thislevel, targetlevel, targetprefix, column, num_target_indices, inputs, input_weights, by_column):
        func = node.get_function(function)
        prefix = function[0].capitalize()
        func.set_name(f'{prefix}L{thislevel}C{column}ws')

        """
        print('Base',func.get_name())        
        print('Base',inputs)        
        print('Base',input_weights)        
        print('Base',column)        
        print('Base',num_target_indices)        
        """
        weights=[]        
        for inputIndex in range(num_target_indices):
            if inputs==None:
                name=f'{targetprefix}L{targetlevel}C{inputIndex}ws'
            else:
                name=inputs[inputIndex]
            func.add_link(name)
            #print(name)
            if by_column:
                weights.append(input_weights[column][inputIndex])
            else:
                #print(inputIndex,column)
                weights.append(input_weights[inputIndex][column])                
        func.weights=np.array(weights)

    def has_changed(self, wts1, wts2):
        mutated = 0
        if wts1 != wts2:
            mutated = 1
        return mutated
    


class Binary(BaseParameterType):
    
    def __init__(self):
        self.ones=BinaryOnes.AT_LEAST_ONE
        self.attr_mut_pb=None
        self.attr_cx_uniform_pb=None

    def get_weights_list(self, num_inputs, num_columns):
        wts_list=[]
        for i in range(num_inputs):            
            if self.ones == BinaryOnes.ALL_ONES:
                wts = [1] * num_columns
            else:
                wts = [random.randint(0, 1) for iter in range(num_columns)]
                if self.ones == BinaryOnes.AT_LEAST_ONE:
                    if np.sum(wts) == 0:
                        index = random.randint(0, num_columns-1)
                        wts[index] = 1
        
            wts_list.append(wts)
         
        return wts_list
    
    def set_parameters(self, pars, globals):
        super().set_parameters(pars, globals)
        if self.attr_mut_pb==None:
            self.attr_mut_pb= globals['attr_mut_pb']
        if self.attr_cx_uniform_pb==None:
            self.attr_cx_uniform_pb= globals['attr_cx_uniform_pb']

    
    def mutate(self, wts):
        if self.ones == BinaryOnes.ALL_ONES or (self.ones == BinaryOnes.AT_LEAST_ONE and len(wts)==1):
            pass 
        else:
            weights, = tools.mutFlipBit(wts, self.attr_mut_pb)
            if self.ones == BinaryOnes.AT_LEAST_ONE:
                if np.sum(weights) == 0:
                    index = random.randint(0, len(weights)-1)
                    weights[index] = 1

    def mutate_binary_lists(self, lists):
        mut_pb = 0.5
        list = []
        #print('***1',lists)
        for item in lists:
            list.append(item[0])     
        #print('***2',list)
        list, = tools.mutFlipBit(list, mut_pb)
        #print('***3',list)
        if np.sum(list) == 0:
            index = random.randint(0, len(list)-1)
            list[index] = 1
        #print('***4',list)

        for i in range(len(list)):
            lists[i][0]=list[i]

        #print('***5',lists)
        


    def mate(self, wts1, wts2):
        #print('Binary mate')
        #print(wts2)
        #print(wts2)
        wts1, wts2 = tools.cxUniform(wts1, wts2, self.attr_cx_uniform_pb)
        

    def copy_data(self, from_wts, to_wts):
        
        #print(from_wts, to_wts)
        from_len=len(from_wts)
        to_len = len(to_wts)
        
        for ctr in range(min(from_len, to_len)):
            to_wts[ctr] = from_wts[ctr]
        
        if self.ones == BinaryOnes.AT_LEAST_ONE:
            if np.sum(to_wts) == 0:
                index = random.randint(0, len(to_wts)-1)
                to_wts[index] = 1
          
        
        #return to_wts


    class Factory:
        def create(self): return Binary()
        
        
class Float(BaseParameterType):
    
    def __init__(self):
        self.lower=None
        self.upper=None
        self.mu=None
        self.sigma=None
        self.attr_mut_pb=None
        self.alpha=None

    def get_weights_list(self,  num_lists, length):
        wts=[]
        for i in range(num_lists):
            wt = [random.uniform(self.lower, self.upper) for iter in range(length)]
            wts.append(wt)
        return wts      
    
    def set_parameters(self, pars, globals):
        super().set_parameters(pars, globals)
        if self.lower==None:
            self.lower = globals['lower_float']
        if self.upper==None:
            self.upper = globals['upper_float']
        if self.mu==None:
            self.mu = globals['mu']
        if self.sigma==None:
            self.sigma= globals['sigma']
        if self.alpha==None:
            self.alpha= globals['alpha']
        if self.attr_mut_pb==None:
            self.attr_mut_pb= globals['attr_mut_pb']

    def mutate(self, wts):
        weights, = tools.mutGaussian(wts, mu=self.mu, sigma=self.sigma, indpb=self.attr_mut_pb)

    def mate(self, wts1, wts2):
        #print('Float mate')
        #print(wts1, wts2)
        wts1, wts2 = tools.cxBlend(wts1, wts2, self.alpha)
        #print(wts1, wts2)
        
    def copy_data(self, from_wts, to_wts):
        
        #print(from_wts, to_wts)
        from_len=len(from_wts)
        to_len = len(to_wts)
        
        for ctr in range(min(from_len, to_len)):
            to_wts[ctr] = from_wts[ctr]
        
          
         

        
    class Factory:
        def create(self): return Float()


class Literal(BaseParameterType):
    
    def __init__(self):
        self.value=None

    def get_weights_list(self,  num_lists, length):
        return self.value      
    
    def set_node_function(self, node, function, thislevel, targetlevel, not_used, column, not_used1, inputs, weights, not_used2):
        
        func = node.get_function(function)
        prefix = function[0].capitalize()
        func.set_name(f'{prefix}L{thislevel}C{column}c')
        func.set_value(weights[column])
        """
        print('Literal',inputs)        
        print('Literal',weights)        
        prefix = function[0].capitalize()
        constant = Constant(weights[column], name=f'{prefix}L{thislevel}C{column}c')
        node.replace_function(function, constant, 0)
        """
        
    def copy_data(self, from_wts, to_wts):
        pass
   
    class Factory:
        def create(self): return Literal()
        
        
class ParameterFactory:
    factories = {}
    def addFactory(id, parameterFactory):
        ParameterFactory.factories.put[id] = parameterFactory
    addFactory = staticmethod(addFactory)
    
    # A Template Method:
    def createParameter(id):
        if not ParameterFactory.factories.__contains__(id):
            ParameterFactory.factories[id] = \
              eval(id + '.Factory()')
        return ParameterFactory.factories[id].create()
    
    createParameter = staticmethod(createParameter)        

class StructureDefinition():
    "StructureDefinition"
    def __init__(self, references=None, config=None, attr_mut_pb=None, lower_float=None, upper_float=None, levels_limit=None, 
                 columns_limit=None, sigma=None, mu=None, alpha=None, modes=None, **cargs):
        if config==None:
            self.config={'parameters': {'lower_float': -1, 'upper_float': 1, 
                         'modes' : {LevelKey.ZERO:3, LevelKey.N:3,LevelKey.TOP:4,LevelKey.ZEROTOP :4},
                         'levels_limit': 3, 'columns_limit': 3, 'attr_mut_pb': 1.0, 
                         'sigma': 0.8, 'mu': 0.5, 'alpha':0.6, 'attr_cx_uniform_pb':0.5}, 
                         LevelKey.ZERO: {'perception': {'type': 'Binary'}, 'output': {'type': 'Float'}, 'reference': {'type': 'Float'}, 'action': {'type': 'Binary'}}, 
                         LevelKey.N: {'perception': {'type': 'Binary'}, 'output': {'type': 'Float'}, 'reference': {'type': 'Float'}}, 
                         LevelKey.TOP: {'perception': {'type': 'Binary'}, 'output': {'type': 'Float'}, 'reference': {'type': 'Literal'}}}            
        else:
            self.config=config
        
        if references!=None:
            self.add_config_parameter(LevelKey.TOP , 'reference', 'value', references )

            
        if attr_mut_pb != None:
            self.config['parameters']['attr_mut_pb']=attr_mut_pb
        if lower_float!=None:                   
            self.config['parameters']['lower_float']=lower_float
        if upper_float!=None:  
            self.config['parameters']['upper_float']=upper_float
        if levels_limit!=None:  
            self.config['parameters']['levels_limit']=levels_limit
        if columns_limit!=None:    
            self.config['parameters']['columns_limit']=columns_limit
        if sigma!=None:  
            self.config['parameters']['sigma']=sigma
        if mu!=None:  
            self.config['parameters']['mu']=mu
        if alpha!=None:  
            self.config['parameters']['alpha']=alpha
        if modes!=None:  
            self.config['parameters']['modes']=modes


    def get_config(self):
        return self.config

    def add_config_type(self, level_key=None, function=None, type=None):
        ttype={'type': type}
        self.config[level_key][function]=ttype

    def add_structure_parameter(self, key=None, value=None):
        self.config['parameters'][key]=value
        
    def add_level_parameter(self, level=None, function=None, key=None, value=None):
        self.config[level][function][key]=value

    def add_config_parameter(self, level_key=LevelKey.N, function=None,  parameter_type=None, parameter_value=None):
        if not 'pars' in self.config[level_key][function]:
            self.config[level_key][function]['pars']={} #pars={'pars'}    
        self.config[level_key][function]['pars'][parameter_type]=parameter_value

    def get_config_parameter(self, level_key=LevelKey.N, function=None,  parameter_type=None):
        if not 'pars' in self.config[level_key][function]:
            return False
        return self.config[level_key][function]['pars'][parameter_type]
        
    def get_level0_config(self):
        return self.config['level0']

    def get_leveln_config(self):
        return self.config['leveln']

    def get_leveltop_config(self):
        return self.config['leveltop']
    
    def get_type(self, level_key, function):
        package = self.config[level_key][function]
        pars={} 
        if 'pars' in package.keys():
            pars = package['pars']
        
        return package['type'], pars

    def get_type_parameters(self, level, function):
        return self.config[level][function]

    def get_parameter(self, key):
        return self.config['parameters'][key]


    def set_node_function(self, node, function, levelkey, thislevel, targetlevel, targetprefix, column, num_target_indices, inputs, input_weights, by_column):
        type, type_parameters = self.get_type(levelkey, function)
        parameter = ParameterFactory.createParameter(type)
        parameter.set_node_function(node, function,  thislevel, targetlevel, targetprefix, column, num_target_indices, inputs, input_weights, by_column)
        
        
            
    def get_list(self, level_key, function,  num_lists, num_items):
        parameter = self.get_parameter_object(level_key, function)
        return parameter.get_weights_list(num_lists, num_items)

    
    def mutate_list(self, level, function, wts):
        parameter = self.get_parameter_object(level, function)
        return parameter.mutate(wts)

    def mutate_binary_lists(self, level, function, lists):
        parameter = self.get_parameter_object(level, function)
        parameter.mutate_binary_lists(lists)                

    def mate_lists(self, level, function, wts1, wts2):
        parameter = self.get_parameter_object(level, function)
        return parameter.mate(wts1, wts2)


    def copy_data(self, level, function, from_wts, to_wts):
        parameter = self.get_parameter_object(level, function)
        parameter.copy_data(from_wts, to_wts)
    
    def get_parameter_object(self, level_key, function):
        type, type_parameters = self.get_type(level_key, function)
        
        parameter = ParameterFactory.createParameter(type)
        parameter.set_parameters(type_parameters, self.config['parameters'])
        
        return parameter
        

    def get_level0(self, num_inputs, numColumnsThisLevel, numColumnsNextLevel, num_actions):
        config0=[]
        
        perception_list = self.get_list(LevelKey.ZERO,'perception', num_inputs, numColumnsThisLevel)
        output_list = self.get_list(LevelKey.ZERO,'output', num_actions, numColumnsThisLevel)       
        reference_list = self.get_list(LevelKey.ZERO,'reference', numColumnsThisLevel, numColumnsNextLevel)       
        action_list = self.get_list(LevelKey.ZERO,'action', num_actions, numColumnsThisLevel)

        config0.append(perception_list)
        config0.append(output_list[0])
        config0.append(reference_list)        
        config0.append(action_list)
        
        return config0
    
    
    def get_leveln(self, numColumnsThisLevel, numColumnsNextLevel, numColumnsPreviousLevel):
        config=[]
        
        perception_list = self.get_list(LevelKey.N,'perception', numColumnsPreviousLevel, numColumnsThisLevel)

        output_list = self.get_list(LevelKey.N,'output', numColumnsPreviousLevel, numColumnsThisLevel)
        
        reference_list = self.get_list(LevelKey.N,'reference', numColumnsThisLevel, numColumnsNextLevel)
        

        config.append(perception_list)
        config.append(output_list[0])
        config.append(reference_list)        
        
        return config
    
    def get_level0top(self, num_inputs, numColumnsThisLevel, num_actions):
        config0=[]
        
        perception_list = self.get_list(LevelKey.ZERO,'perception', num_inputs, numColumnsThisLevel)

        output_list = self.get_list(LevelKey.ZERO,'output', num_actions, numColumnsThisLevel)
        
        reference_list = self.get_list(LevelKey.TOP,'reference', 1, numColumnsThisLevel)
        
        action_list = self.get_list(LevelKey.ZERO,'action', num_actions, numColumnsThisLevel)

        config0.append(perception_list)
        config0.append(output_list[0])
        config0.append(reference_list)        
        config0.append(action_list)
        
        return config0
    
    def get_leveltop(self, numColumnsThisLevel, numColumnsPreviousLevel):
        config=[]
        
        perception_list = self.get_list(LevelKey.TOP,'perception', numColumnsPreviousLevel, numColumnsThisLevel)

        output_list = self.get_list(LevelKey.TOP,'output', 1, numColumnsThisLevel)
        
        reference_list = self.get_list(LevelKey.TOP,'reference', 1, numColumnsThisLevel)
        

        config.append(perception_list)
        config.append(output_list[0])
        config.append(reference_list)        
        
        return config
    
    # assume same for all levels and that datatypes are always floats
    def set_output_function(self, node,  thislevel, column, input_weights):
        func = node.get_function('output')
        func.set_name(f'OL{thislevel}C{column}ws')

        """
        print('Base',func.get_name())        
        print('Base',inputs)        
        print('Base',input_weights)        
        print('Base',column)        
        print('Base',num_target_indices)        
        """
        weights=[]        
        weights.append(input_weights[column])
        func.weights=np.array(weights)
   
    
    def set_action_function(self, hpct, env, numColumnsThisLevel,  weights):
        numActions = len(weights)
        for actionIndex in range(numActions):
            action = WeightedSum(weights=weights[actionIndex], name=f'Action{actionIndex+1}ws')
            for column in range(numColumnsThisLevel):
                action.add_link(f'OL0C{column}ws')
            hpct.add_postprocessor(action)
            env.add_link(action)


