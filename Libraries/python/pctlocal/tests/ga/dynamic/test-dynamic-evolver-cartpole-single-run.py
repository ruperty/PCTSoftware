# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""


import os
from jproperties import Properties

from pct.putils import stringIntListToListOfInts
from pct.putils import stringListToListOfStrings
from pct.putils import listNumsToString
from pct.putils import get_drive
from pct.environments import CartPoleV1
from pct.architectures import LevelKey
from epct.evolvers import EvolverWrapper
from epct.configs import DynamicConfiguration


from epct.evolvers import DynamicEvolver
from epct.structure import StructureDefinition

#from temp.epctevolver import DynamicEvolver
#from temp.epctstruct import StructureDefinition

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)


inputs = [1,0,3,2]
references = [0]
num_actions=1

#seeds={'seed':None, 'eseed':2} 
seeds={'seed':None, 'eseed':4} 

#random.seed(seeds['seed'])

POPULATION_SIZE = 100
MAX_GENERATIONS = 10
debug=0
verbose=1
deap_verbose=False
save_arch_all = False
save_arch_gen = False
display_env=True
deap_verbose=False

attr_mut_pb=1
structurepb=0.75
runs=500
lower_float = -10
upper_float = 10

env = CartPoleV1(name='CartpoleV1')

sdargs={'attr_mut_pb':attr_mut_pb, 'lower_float':lower_float, 'upper_float': upper_float, 
        'levels_limit': 5, 'columns_limit': 8}

structure = StructureDefinition(references=references,**sdargs)

#structure.add_config_parameter(LevelKey.TOP , 'perception', 'ones', BinaryOnes.AT_LEAST_ONE )


print(structure.get_config())
 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 'structurepb':structurepb, 'error_limit':100, 'runs':runs, 
        'debug':debug,  'seed':seeds['eseed'], 'hpct_verbose':False}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 0.9, 'p_mutation': 0.5, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen, 'display_env':display_env,
         'select':{'selection_type':'tournament', 'tournsize':25} }
evr = EvolverWrapper(**evwargs)



meantime = evr.run(gens=MAX_GENERATIONS, verbose=verbose, deap_verbose=deap_verbose)
raw=evr.best()
print("Best Score: %0.5f" % evr.best_score())
print("Best Ind: ", raw)
print(f'Mean time: {meantime:6.3f}')

best_of_gens = evr.get_best_of_gens()




env.close()
move={}
DynamicConfiguration.draw_raw(raw, move=move, summary=False)


