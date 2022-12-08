# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""


import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
import random

from epct.evolvers import EvolverWrapper
from pct.environments import VelocityModel
from pct.architectures import LevelKey
from epct.structure  import BinaryOnes

#from epct.evolvers import DynamicEvolver
#from epct.structure import StructureDefinition

from temp.epctstruct import StructureDefinition
from temp.epctevolver import DynamicEvolver



inputs = [0]
references = [10]
num_actions=1
#seeds={'seed':None, 'eseed':11}
POPULATION_SIZE = 4 #20
MAX_GENERATIONS = 2 #10 

debug=0
verbose=1
deap_verbose=False
save_arch_all = False
save_arch_gen = False
attr_mut_pb=1
structurepb=1
runs=10
lower_float = -100
upper_float = 100
seed=1

env = VelocityModel(name='VModel', mass=75)

sdargs={'attr_mut_pb':attr_mut_pb}

structure = StructureDefinition(**sdargs)
structure.add_config_parameter(LevelKey.ZERO , 'action', 'ones', BinaryOnes.ALL_ONES)
structure.add_config_parameter(LevelKey.TOP , 'reference', 'value', references )

structure.add_structure_parameter('lower_float',lower_float)
structure.add_structure_parameter('upper_float', upper_float)
structure.add_structure_parameter('attr_cx_uniform_pb', 0.5)

 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 'structurepb':structurepb, 'error_limit':1000, 'runs':runs, 
        'debug':debug, 'hpct_verbose':False, 'seed':seed}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 0.9, 'p_mutation': 0.5, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen           }
evr = EvolverWrapper(**evwargs)



evr.run(gens=MAX_GENERATIONS, verbose=verbose, deap_verbose=deap_verbose)
print("Best Score: %0.5f" % evr.best_score())
print("Best Ind: ", evr.best())


best_of_gens = evr.get_best_of_gens()

""" 
sfig=stdev.create_plot(best_of_gens)    
anim = animation.FuncAnimation(sfig, stdev.animate, frames=stdev.frames, interval=250, repeat=False)
plt.show()
"""
