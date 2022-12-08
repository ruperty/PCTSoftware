#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 11:59:42 2020

@author: ruperty
"""

   
    
import random


from epct.configs import BaseConfiguration
from epct.configs import ConfigurationStructure


        
class DynamicConfigurationStructure(ConfigurationStructure):

    def __init__(self, structure=None, **cargs):
        if structure==None:
            self.structure={}
        else:
            self.structure=structure

    def from_raw(self, raw):

        config = BaseConfiguration.from_raw(raw)
        levels = len(config)-1
        num_inputs=len(config['level0'][0])
        self.structure['num_inputs']=num_inputs
        num_actions=len(config['level0'][3])
        self.structure['num_actions']=num_actions

        grid=[]
        for level in range(levels):
            grid.append(len(config[f'level{level}'][1]))
        self.structure['grid']=grid
        references = config[f'level{levels-1}'][2]
        self.structure['references']=references
        return self.structure

 

class DynamicConfiguration(BaseConfiguration):
    "DynamicConfiguration"
    def __init__(self, num_inputs=1, num_actions=1, references=None,
                 structure=None, grid=None,  **cargs):

        #self.inputs=inputs
        self.num_inputs=num_inputs
        self.num_actions=num_actions
        self.references=references
        self.config={}
        self.structure=structure
        self.grid=grid
        """
        self.lower_float=lower_float
        self.upper_float=upper_float
        self.config['parameters']['lower_float']=lower_float
        self.config['parameters']['upper_float']=upper_float
        """

    def __call__(self):

        if self.grid==None:
            grid=[]
            levels = random.randint(0, self.structure.get_parameter('levels_limit'))
            for level in range(levels-1):
                columns = random.randint(1, self.structure.get_parameter('columns_limit'))
                grid.append(columns)
            grid.append(len(self.references))
        else:
            grid=self.grid
        
        
        levels = len(grid)
        #print(grid)
        if levels == 1:
            level0 = self.level0topconfig(grid[0])
            self.config['level0']=level0
            return self.config
        else:
            level0 = self.level0config(grid[0], grid[1])

        self.config['level0']=level0

        if levels > 2:
            for level in range(1,levels-1, 1):
                numColumnsThisLevel=grid[level]
                numColumnsPreviousLevel=grid[level-1]
                numColumnsNextLevel = grid[level+1]
                self.config[f'level{level}']=self.levelnconfig(numColumnsThisLevel, numColumnsNextLevel, numColumnsPreviousLevel)

        if levels > 1:
            self.config[f'level{len(grid)-1}'] = self.leveltopconfig(grid[-1], grid[-2])

        return self.config

    def level0config(self, numColumnsThisLevel, numColumnsNextLevel):
        return self.structure.get_level0(self.num_inputs,numColumnsThisLevel, numColumnsNextLevel, self.num_actions)

    def level0topconfig(self, num_columns):
        return self.structure.get_level0top(self.num_inputs,num_columns, self.num_actions)

    def levelnconfig(self, numColumnsThisLevel, numColumnsNextLevel, numColumnsPreviousLevel):
        return self.structure.get_leveln(numColumnsThisLevel, numColumnsNextLevel, numColumnsPreviousLevel)

    def leveltopconfig(self, numColumnsThisLevel, numColumnsPreviousLevel):
        return self.structure.get_leveltop(numColumnsThisLevel, numColumnsPreviousLevel)