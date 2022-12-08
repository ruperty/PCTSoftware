#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:01:52 2020

@author: ruperty
"""

# https://matplotlib.org/3.1.0/gallery/color/named_colors.html


#from epct.configs import BaseConfiguration
from pct.environments import VelocityModel
from epct.evolvers import EvolverWrapper
from epct.structure  import BinaryOnes
from pct.architectures import LevelKey

#from temp.epctevolver import DynamicEvolver
#from temp.epctstruct import StructureDefinition


from epct.structure import StructureDefinition
from pct.architectures import DynamicArchitecture
from epct.evolvers import DynamicEvolver
from pct.structure import ArchitectureStructure


inputs = [1, 3]
references = [666]
num_actions=2
seeds={'seed':None, 'eseed':4} # grid [1]
POPULATION_SIZE = 2
debug=0
save_arch_all = False
save_arch_gen = False
attr_mut_pb=0.5
attr_cx_pb=0.9
structurepb=1
lower_float = -100
upper_float = 100

smooth = True 

env = VelocityModel(name='VModel')

sdargs={'attr_mut_pb':attr_mut_pb, 'attr_cx_pb':attr_cx_pb, 'lower_float':lower_float, 'upper_float': upper_float }
structure = StructureDefinition(**sdargs)

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
    structure.add_config_parameter(LevelKey.ZERO, 'action', 'ones', BinaryOnes.ALL_ONES)
    #structure.add_config_parameter('0', 'perception', 'ones', BinaryOnes.ALLOW_ALL_ZEROS)
    structure.add_config_parameter(LevelKey.TOP, 'reference', 'value', references )




move={}
figsize=(12,12)
layout={'r':2,'c':1,'p':1, 'o':0}
 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 
        'structurepb':structurepb, 'error_limit':100, 'runs':500, 
        'debug':debug, 'seed':seeds['eseed'], 'hpct_verbose':False}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 1.0, 'p_mutation': 1.0, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen, 
         'select':{'selection_type':'tournament', 'tournsize':25} }
evr = EvolverWrapper(**evwargs)


test = 1

def print_ind(name, ind):
    print(name)
    for level in range(len(ind)):
        print('*',level, ind[level] )

if test ==1:
    ind1 = evr.toolbox.individual()
    ind2 = evr.toolbox.individual()



single = False
#single = True

if single:
    
    print_ind('ind1', ind1)
    print_ind('ind2', ind2)
    
    mated1, mated2 = evr.toolbox.mate(ind1, ind2)

    print_ind('mated1', mated1)
    print_ind('mated2', mated2)

else:
    for ctr in range(100):
        print('*** ', ctr, ' ***')
        ind1 = evr.toolbox.individual()
        ind2 = evr.toolbox.individual()
        print_ind('ind1', ind1)
        print_ind('ind2', ind2)
        
        mated1, mated2 = evr.toolbox.mate(ind1, ind2)
    
        print_ind('mated1', mated1)
        print_ind('mated2', mated2)
 

"""
config = BaseConfiguration.from_raw( raw)
pa = DynamicArchitecture(structure=structure, config=config, env=env, input_indexes=inputs) #, error_collector=te)
pa()
hpct = pa.get_hierarchy()
#hpct.set_order('Down')
#hpct.summary()
hpct.draw(move=move, figsize=figsize, with_edge_labels=True, layout=layout)
"""



    
    
    
    
    
    
    
    
    
    