#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:01:52 2020

@author: ruperty
"""



from pct.environments import MountainCarContinuousV0
from pct.architectures import LevelKey
from pct.architectures import DynamicArchitecture
from pct.structure import ArchitectureStructure
from epct.evolvers import EvolverWrapper
from epct.configs import DynamicConfiguration
from epct.structure import BinaryOnes

from deap import creator

from epct.evolvers import DynamicEvolver
from epct.structure import StructureDefinition

inputs = [0, 1]
references = [0.45]
top_inputs=[0]
num_actions=1
seeds={'seed':None, 'eseed':1} 
POPULATION_SIZE = 2
debug=0

display_env=True
save_arch_all = False
save_arch_gen = False
hpct_verbose=False


error_collector_type ='ReferencedInputsError'
error_response_type = 'CurrentError'

attr_mut_pb=1

structurepb=0.75
runs=500
lower_float = -1
upper_float = 1

env = MountainCarContinuousV0(name='CartpoleV1', render=True, early_termination=True)

sdargs={'attr_mut_pb':attr_mut_pb, 'lower_float':lower_float, 'upper_float': upper_float, 
        'levels_limit': 5, 'columns_limit': 8}


structure = StructureDefinition(references=references,**sdargs)
#structure.set_config_parameter(LevelKey.TOP , 'perception', 'ones', BinaryOnes.AT_LEAST_ONE )

structure.set_config_type(LevelKey.ZERO, 'action', 'Float')
structure.set_config_type(LevelKey.ZERO, 'perception', 'Float')
structure.set_config_type(LevelKey.N, 'perception', 'Float')
structure.set_config_type(LevelKey.TOP, 'perception', 'Float')
structure.set_config_type(LevelKey.ZERO, 'output', 'Smooth')
structure.set_config_type(LevelKey.N, 'output', 'Smooth')
structure.set_config_type(LevelKey.TOP, 'output', 'Smooth')

structure.set_structure_parameter('top_inputs', top_inputs)


modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
arch_structure = ArchitectureStructure(modes=modes)
structure.arch_structure=arch_structure



print(structure.get_config())

error_properties = [['referenced_inputs','0&0.45']]

move={}
figsize=(12,12)
layout={'r':2,'c':1,'p':1, 'o':0}
 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 'structurepb':structurepb, 'error_limit':100, 'runs':runs, 
        'error_collector_type':error_collector_type, 'error_response_type':error_response_type,
        'error_properties': error_properties,
        'debug':debug, 'seed':seeds['eseed'], 'hpct_verbose':hpct_verbose}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 1.0, 'p_mutation': 1.0, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen, 
         'display_env':display_env,'select':{'selection_type':'tournament', 'tournsize':25} }
evr = EvolverWrapper(**evwargs)


test = 1



if test==1:
   raw = [[[[-0.6054973800569653]], [[0.14732165967500344, 0.9765613163013146]], [[0.06060438938016721]], [[-0.2772875786304368]]], [[[0.8662427129590583]], [[1.8401224243845018, 0.3945183636711995]], [0.45]]]
   
   raw=[[[[1.868050274735844, 0.6527020349693591, 0.34830602849372827]], [[0.30580494940160385, 0.5811240762433265], [0.8373683873238282, 0.8071273289614824], [-0.4078546538336969, 0.4997999222368016]], [[1.4957228630115247], [0.4430861079291004], [0.7993565392695623]], [[0.03750203156944254, 1.0752092008943261, -0.34451858980746497]]], [[[2.200594188589861]], [[0.6574252886779938, 0.9413554854741091]], [0.45]]]
    
   move={'Input0':[-0.3,0.1],'Input1':[-0.3,-0.05],'World':[-.3,-0.25],
          'Action1ws':[-0.2,-0.2], 'OL0C0sm':[0,-0.2], 'OL1C0sm':[0,-0.2]}
   move={}
    
#single = False
single = True

if single:
    DynamicArchitecture.draw_raw(raw, move=move, arch_structure=arch_structure,  
        inputs=inputs, top_input_indexes=top_inputs, summary=False)
    
    ind1 = creator.Individual(raw)
    ind1.fitness.values = evr.toolbox.evaluate(ind1)
    print (ind1.fitness)          # (2.73, 0.2)


else:
    for ctr in range(40):
        ind1 = evr.toolbox.individual()
        print(ctr, ind1)
        
        ind1.fitness.values = evr.toolbox.evaluate(ind1)
        #print (ind1.fitness.valid)    # True
        print (ind1.fitness)          # (2.73, 0.2)
        
        #evr.evolver.mutate_sum=0
        #evr.evolver.mutate_structure_sum=0
        #inda1= evr.toolbox.mutate(ind1)
        #print(ctr, 'mutated', evr.evolver.mutate_sum)
        #print('mutated struct', evr.evolver.mutate_structure_sum)
        print()




env.close()


    
    
    
    
    
    
    
    
    
    