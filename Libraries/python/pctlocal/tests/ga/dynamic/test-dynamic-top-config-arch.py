#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:56:21 2020

@author: ruperty
"""


from epct.configs import DynamicConfiguration
from pct.architectures import LevelKey
from pct.architectures import DynamicArchitecture
from epct.structure  import BinaryOnes
from pct.structure  import ArchitectureStructure

import random

from epct.structure  import StructureDefinition

#from temp.epctstruct import StructureDefinition

def run_test(pars, move):
    structure = StructureDefinition()
    structure.set_config_parameter(LevelKey.ZERO, 'action', 'ones', BinaryOnes.ALL_ONES)
    structure.set_config_parameter(LevelKey.TOP , 'perception', 'ones', BinaryOnes.AT_LEAST_ONE )
    structure.set_structure_parameter('lower_float',-10)
    structure.set_structure_parameter('upper_float',10)
    #print(structure.get_config())
    arch_structure = ArchitectureStructure()

    
    inputs=pars['inputs']
    num_inputs=len(inputs)
    #num_top_inputs=0
    
        
    num_actions=pars['num_actions']
    grid=pars['grid']
    references=pars['references']

    structure.set_config_parameter(LevelKey.TOP, 'reference', 'value', pars['references'])

    pc = DynamicConfiguration(num_inputs=len(inputs), num_actions=num_actions, grid=grid, 
                              references=references, structure=structure)
    config = pc()
    print('config', len(config), config)
    raw  = DynamicConfiguration.dict_to_raw(config)
    DynamicArchitecture.draw_raw(raw, arch_structure=arch_structure, figsize=(12,14), summary=summary, move=move)

    top_inputs=None
    if 'top_inputs' in pars:
        top_inputs=pars['top_inputs']
        structure.set_structure_parameter('top_inputs', top_inputs)

    top_pc = DynamicConfiguration(num_inputs=num_inputs, num_actions=num_actions, grid=grid, references=references, structure=structure)
    top_config = top_pc()
    print('config', len(top_config), top_config)

    #summary=True
    raw  = DynamicConfiguration.dict_to_raw(top_config)
    DynamicArchitecture.draw_raw(raw, arch_structure=arch_structure, figsize=(12,12), inputs=inputs,
                                 top_input_indexes=top_inputs, summary=summary, move=move)
    print()
    

random.seed(1)

debug=False

test=1



summary=False

#ttest=4

move=[
      {'Input0':[-0.7,0.6],'Input1':[-0.3,0.4],'Input2':[0.18,0.2],'Input3':[0.6,0],
           'OL0C0ws': [-0.25, 0], 'OL0C1ws': [0.25, 0], 'World':[-.75,-0.25], 'Action1ws':[-0.5,0]},
      {'Input0':[-0.7,0.6], 'OL0C0ws': [-0.5, 0], 'OL0C1ws': [0.5, 0], 'World':[-.75,-0.25], 'Action1ws':[-0.5,0]},
      {'Input0':[-0.7,0.6], 'OL0C0ws': [-0.5, 0], 'OL0C1ws': [0.5, 0], 'World':[-.75,-0.25], 'Action1ws':[-0.5,0]},
      {'PL1C0ws':[-0.2,0],'PL1C1ws':[0.0,0.2],'Input0':[-1.2,0.6],'Input1':[-0.8,0.3],'Input2':[-0.4,0],'Input3':[0.2,0],
           'OL0C0ws': [-0.6, 0], 'OL0C1ws': [0, 0], 'OL0C2ws': [0.6, 0],  'OL1C0ws': [-0.3, 0], 'OL1C1ws': [0.3, 0],'World':[-.9,-0.25], 'Action1ws':[-0.5,0]},
      {'PL1C0ws':[-0.2,0],'PL1C1ws':[0.0,0.2],'Input0':[-1.2,0.6],'Input1':[-0.8,0.3],'Input2':[-0.4,0],'Input3':[0.2,0],
           'OL0C0ws': [-0.6, 0], 'OL0C1ws': [0, 0], 'OL0C2ws': [0.6, 0],  'OL1C0ws': [-0.3, 0], 'OL1C1ws': [0.3, 0],'World':[-.9,-0.25], 'Action1ws':[-0.5,0]},
      {},
      {}
      ]


#if ttest==4:

pars = [ 
        {'inputs': [1, 0, 3, 2], 'top_inputs':[2], 'num_actions':1, 'grid':[2, 1], 'references':[333]}, 
        {'inputs': [2], 'top_inputs':[2], 'num_actions':1, 'grid':[2], 'references':[2,1]},        
        {'inputs': [1], 'top_inputs':[2], 'num_actions':1, 'grid':[2], 'references':[2,1]},        
        {'inputs': [1,2,0,3], 'top_inputs':[3], 'num_actions':1, 'grid':[3, 2], 'references':[22,33]},
        {'inputs': [1,2,0,3], 'top_inputs':[1,3], 'num_actions':2, 'grid':[3, 2], 'references':[22,33]},
        {'inputs': [1,2,0,3],  'num_actions':2, 'grid':[3, 2], 'references':[22,33]},                                
        {'inputs': [1,2,0,3], 'top_inputs':[1,3], 'num_actions':1, 'grid':[2], 'references':[22,33]}
        ]
    
for i in range(len(pars)):
    if i != 6:
        continue
    run_test(pars[i], move[i])    





















