

import time
import warnings
import os
import numpy.testing as npt
from deap import base
from deap import creator
from epct.evolvers import evolve_from_properties_file
from epct.evolvers import CommonToolbox

warnings.simplefilter(action='ignore', category=UserWarning)


#| gui
online=True
debug=False
draw=True

if online and not debug:
    verbose = {'evolve_verbose':1, 'display_env': True}
    print_properties=True
    gens=None
    pop_size=None
    
    #output=True
    #gens=1
    #pop_size = 4
else:
    gens=1
    pop_size = 4
    verbose = {}
    print_properties=True

figsize=(12,14)
move={'MountainCarContinuousV0': [-0.6, -0.5], 'Action1ws': [-0.3, -0.3], 
      'OL0C0sm': [-0.55, -0.2], 'OL0C1sm': [0, -0.2], 'OL0C2sm': [0.55, -0.2], 
      'OL1C0sm': [0, -0.1], 'IV': [-0.8, 0.05], 'IP': [-1.1, 0.5], 'CL1C0': [0, 0.1]}
move={}
filename = 'testfiles/MountainCar/ga-000.326-s066-2x3-6655-a6abebd2c88246e9f77dd8623eac6e3e.properties'
# great! ga-000.401-s093-2x1-6655-2b4b558d02b2661881f9a5109fedca77.properties 

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

if hasattr(creator, 'FitnessMin'):
    del creator.FitnessMin
    del creator.Individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

tic = time.perf_counter()
out,evr,score = evolve_from_properties_file(file=filename, gens=gens, pop_size=pop_size, draw=draw,
    move=move, verbose=verbose, print_properties=print_properties,toolbox=toolbox)
toc = time.perf_counter()

elapsed = toc-tic
print(f'Evolve time: {elapsed:4.2f}')

sfig=evr.create_stats_plot(evr.stats_history)

print(score)

