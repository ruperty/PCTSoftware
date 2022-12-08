#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 11:59:42 2020

@author: ruperty
"""

    
import enum
import random
import numpy as np
from abc import ABC
from deap import tools

from pct.architectures import BaseArchitecture
from pct.architectures import LevelKey
from pct.functions import IndexedParameter

from pct.functions import WeightedSum
from pct.nodes import PCTNode
from pct.functions import Constant
#from ga.tempepctconfig import ParameterFactory




class DynamicArchitecture(BaseArchitecture):
    "Dynamic Architecture"
    def __init__(self, name="dynamic", structure=None, config=None, env=None, input_indexes=None, history=False, error_collector=None, **cargs):
        inputs=[]
        for ctr in range(len(input_indexes)):
            ip = IndexedParameter(index=input_indexes[ctr], name=f'Input{ctr}', links=[env])
            inputs.append(ip)

        super().__init__(name, config, env, inputs, history, error_collector)
        self.structure=structure

    def __call__(self):
        #level0config = self.config['level0']
        levels = len(self.config)-1
        #print('levels', levels)
        if levels == 1:
            self.configure_zerotoplevel()
        else:           
            previous_columns=self.configure_zerothlevel()
            
            intermediate_levels = len(self.config)-3
            level=-1
            for level in range(intermediate_levels):
                leveln = self.config[f'level{level+1}']
                levelcolumns = self.configure_level(leveln, previous_columns, level+1)
                previous_columns=levelcolumns
            if intermediate_levels < 0:
                self.set_references()          
            else:
                level+=1
                self.configure_top_level(self.config[f'level{level+1}'], level+1, previous_columns)


    def configure_zerotoplevel(self):
        mode = self.structure.get_parameter('modes')[LevelKey.ZEROTOP]

        inputsIndex=0
        outputsIndex=1
        referencesIndex=2
        actionsIndex=3

        config=self.config['level0']
        level=0
        #numInputs= len(self.inputs)
        columns = len(config[inputsIndex][0])
        #print(config[0][0])
        #print('columns',columns)

        # create nodes
        for column in range(columns):
            node = PCTNode(build_links=True, mode=mode, name=f'L{level}C{column}', history=self.hpct.history)
            self.structure.set_node_function(node, 'reference', LevelKey.TOP , level, None, None, column, None, None, config[referencesIndex], True)            
            self.structure.set_node_function(node, 'perception', LevelKey.ZERO, level, None, None, column, len(self.inputs), self.inputs, config[inputsIndex], False)

            comparator_name=f'CL{level}C{column}'
            node.get_function("comparator").set_name(comparator_name)
            node.get_function("comparator").set_link(node.get_function("reference"))
            node.get_function("comparator").add_link(node.get_function("perception"))

            self.structure.set_output_function(node, level, column, config[outputsIndex])

            self.hpct.add_node(node, level, column)

        # configure actions
        numColumnsThisLevel = len(config[outputsIndex])
        self.structure.set_action_function(self.hpct, self.env, numColumnsThisLevel, config[actionsIndex])
        
        return numColumnsThisLevel
            
    def configure_zerothlevel(self):
        mode = self.structure.get_parameter('modes')[LevelKey.ZERO]

        inputsIndex=0
        outputsIndex=1
        referencesIndex=2
        actionsIndex=3

        config=self.config['level0']
        level=0
        columns = len(config[inputsIndex][0])
        #print(config[0][0])
        #print(columns)
        columnsNextLevel = len(config[referencesIndex][0])
        #print('columnsNextLevel',columnsNextLevel)

        # create nodes
        for column in range(columns):
            node = PCTNode(build_links=True, mode=mode, name=f'L{level}C{column}', history=self.hpct.history)
            self.structure.set_node_function(node, 'reference', LevelKey.ZERO, level, level+1, 'O', column, columnsNextLevel, None, config[referencesIndex], True)
            self.structure.set_node_function(node, 'perception', LevelKey.ZERO, level, None, None, column, len(self.inputs), self.inputs, config[inputsIndex], False)

            comparator_name=f'CL{level}C{column}'
            node.get_function("comparator").set_name(comparator_name)

            self.structure.set_output_function(node, level, column, config[outputsIndex])

            self.hpct.add_node(node, level, column)

        # configure actions
        numColumnsThisLevel = len(config[outputsIndex])
        self.structure.set_action_function(self.hpct, self.env, numColumnsThisLevel, config[actionsIndex])

        return numColumnsThisLevel

    def configure_level(self, config, numColumnsPreviousLevel, level):
        mode = self.structure.get_parameter('modes')[LevelKey.N]

        inputsIndex=0
        outputsIndex=1
        referencesIndex=2

        #numColumnsPreviousLevel=len(config[referencesIndex])
        numColumnsThisLevel = len(config[outputsIndex])
        columnsNextLevel = len(config[referencesIndex][0])
        
        # create nodes
        for column in range(numColumnsThisLevel):
            node = PCTNode(build_links=True, mode=mode, name=f'L{level}C{column}', history=self.hpct.history)
            self.structure.set_node_function(node, 'reference', LevelKey.N, level, level+1, 'O', column, columnsNextLevel, None, config[referencesIndex], True)
            self.structure.set_node_function(node, 'perception', LevelKey.N, level, level-1, 'P', column, numColumnsPreviousLevel, None, config[inputsIndex], False)

            comparator_name=f'CL{level}C{column}'
            node.get_function("comparator").set_name(comparator_name)

            self.structure.set_output_function(node, level, column, config[outputsIndex])

            self.hpct.add_node(node, level, column)

        return numColumnsThisLevel

    def configure_top_level(self, config, level, numColumnsPreviousLevel ):
        mode = self.structure.get_parameter('modes')[LevelKey.TOP]
        inputsIndex=0
        outputsIndex=1
        referencesIndex=2

        numColumnsThisLevel = len(config[referencesIndex])

        # create nodes
        for column in range(numColumnsThisLevel):
            node = PCTNode(build_links=True, mode=mode, name=f'L{level}C{column}', history=self.hpct.history)
            
            self.structure.set_node_function(node, 'reference', LevelKey.TOP , level, None, None, column, None, None, config[referencesIndex], None)
            self.structure.set_node_function(node, 'perception', LevelKey.TOP , level, level-1, 'P', column, numColumnsPreviousLevel, None, config[inputsIndex], False)

            comparator_name=f'CL{level}C{column}'
            node.get_function("comparator").set_name(comparator_name)
            node.get_function("comparator").set_link(node.get_function('reference'))
            node.get_function("comparator").add_link(node.get_function('perception'))
            
            self.structure.set_output_function(node, level, column, config[outputsIndex])

            self.hpct.add_node(node, level, column)


