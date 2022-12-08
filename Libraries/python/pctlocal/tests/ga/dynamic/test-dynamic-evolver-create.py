#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:09:59 2020

@author: ruperty
"""


    
from epct.configs import BaseConfiguration
from pct.environments import VelocityModel
from pct.architectures import  LevelKey
from epct.evolvers import EvolverWrapper
from epct.structure import BinaryOnes
from epct.configs import DynamicConfigurationStructure


#from temp.pctarch import DynamicArchitecture
#from temp.epctevolver import DynamicEvolver
#from temp.epctstruct import StructureDefinition


from epct.structure import StructureDefinition
#from pct.architectures import BinaryOnes
from pct.architectures import DynamicArchitecture
from epct.evolvers import DynamicEvolver


from pct.structure import ArchitectureStructure


test = 8

inputs = [0, 1]
references = [666]
num_actions=2

if test == 1:
    #inputs = [0]
    seeds={'seed':None, 'eseed':1} # grid [1]
if test == 2:
    seeds={'seed':None, 'eseed':5} # grid [3, 1]
    num_actions=1

if test == 3:
    seeds={'seed':None, 'eseed':5} # grid [3, 1]
if test == 4:
    seeds={'seed':None, 'eseed':9} # grid [3, 2, 1]

if test == 5:
    inputs = [0]
    references = [666, 777]
    num_actions=1
    seeds={'seed':None, 'eseed':10} # grid [2]


if test == 6:
    inputs = [0, 1]
    references = [666, 777]
    num_actions=2
    seeds={'seed':None, 'eseed':11} # grid [3, 2, 2]

if test == 7:
    inputs = [0]
    references = [10]
    num_actions=1
    seeds={'seed':None, 'eseed':10} # grid [2]


if test == 8:
    top_inputs = [3]
    inputs = [1, 0, 3, 2]
    references = [0]
    num_actions=1
    seeds={'seed':None, 'eseed':1} 



#random.seed(seeds['seed'])

POPULATION_SIZE = 2
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual
MAX_GENERATIONS = 25


debug=0
save_arch_all = False
save_arch_gen = False
smooth = False 

env = VelocityModel(name='VM')

structure = StructureDefinition()
structure.set_structure_parameter('lower_float',-100)
structure.set_structure_parameter('upper_float',100)

if smooth:
    structure.set_config_type(LevelKey.ZERO, 'action', 'Float')
    structure.set_config_type(LevelKey.ZERO, 'perception', 'Float')
    structure.set_config_type(LevelKey.N, 'perception', 'Float')
    structure.set_config_type(LevelKey.TOP, 'perception', 'Float')
    structure.set_config_type(LevelKey.ZERO, 'output', 'Smooth')
    structure.set_config_type(LevelKey.N, 'output', 'Smooth')
    structure.set_config_type(LevelKey.TOP, 'output', 'Smooth')

    structure.set_config_parameter(LevelKey.TOP, 'reference', 'value', references )
    modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
    arch_structure = ArchitectureStructure(modes=modes)
    structure.arch_structure=arch_structure

else:
    structure.set_config_parameter(LevelKey.ZERO , 'action', 'ones', BinaryOnes.ALL_ONES)
    structure.set_config_parameter(LevelKey.TOP, 'reference', 'value', references )    
    structure.set_structure_parameter('top_inputs', top_inputs)
    arch_structure = ArchitectureStructure()
 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 
        #'alpha':0.6, 'mu':0.5, 'sigma':0.8, 'structurepb':0.5, 'error_limit':100, 'indpb':1, 
        'runs':500, 
        'debug':debug, 'seed':seeds['eseed'], 'hpct_verbose':False}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 0.9, 'p_mutation': 0.5, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen, 
         'select':{'selection_type':'tournament', 'tournsize':25} }
evr = EvolverWrapper(**evwargs)

num_inputs = len(inputs)

test=1
loops  = 5

if test==1:
    # create
    for _ in range(loops):
        ind1 = evr.toolbox.individual()
        print()
        print(ind1)
        config = BaseConfiguration.from_raw( ind1)
        cs = DynamicConfigurationStructure()

        struct = cs.from_raw(ind1)
        print()
        print(struct)
        if num_inputs != struct['num_inputs'] and len(struct['grid'])==1:
            print('WARNING')
            break
        #print(config)
        env.reset()
        pa = DynamicArchitecture(structure=arch_structure, config=config, env=env, input_indexes=inputs, top_input_indexes=top_inputs)         
        pa()
        hpct = pa.get_hierarchy()
        #hpct.summary()
        hpct.draw(with_edge_labels=True)
    
    
    
if test==10:
    ds = StructureDefinition()

    ds.add_structure_parameter('lower_float', -10)
    ds.add_structure_parameter('upper_float', 10)
    ds.add_structure_parameter('levels_limit', 3)
    ds.add_structure_parameter('columns_limit', 10)
    
    ds.add_config_type('0', 'perception', 'Binary')    
    ds.add_config_type('0', 'output', 'float')
    ds.add_config_type('0', 'reference', 'float')
    ds.add_config_type('0', 'action', 'Binary')
    
    ds.add_config_type('n', 'perception', 'Binary')
    ds.add_config_type('n', 'output', 'float')
    ds.add_config_type('n', 'reference', 'float')
    
    ds.add_config_type('top', 'perception', 'Binary')
    ds.add_config_type('top', 'output', 'float')
    ds.add_config_type('top', 'reference', 'literal')

    #ds.add_config_parameter('0', 'perception', 'ones', 'all')
    #ds.add_config_parameter('0', 'perception', 'x', 'y')

    print(ds.get_config())

