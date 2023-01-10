
import time
import warnings
import os
import numpy.testing as npt
from deap import base
from deap import creator
from epct.evolvers import evolve_from_properties_file
from epct.evolvers import CommonToolbox

warnings.simplefilter(action='ignore', category=UserWarning)

online=False
debug=False
output=False
out_dir=None

#| gui
online=True
debug=False

if online and not debug:
    verbose = {'evolve_verbose':1}
    print_properties=True
    gens=None
    pop_size=None
    output=True
    #gens=1
    #pop_size = 4
    if os.name=='nt':
        out_dir='c:/tmp/'
    else:
        out_dir='/mnt/c/tmp'
else:
    gens=1
    pop_size = 4
    verbose = {}
    print_properties=True

move={'OL0C0ws':[0.25,0], 'CL0C0':[0.25,0]}
filename = 'testfiles/ga-001.444-3344-397818342161201780.properties'

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

if hasattr(creator, 'FitnessMin'):
    del creator.FitnessMin
    del creator.Individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

tic = time.perf_counter()
out,evr,score = evolve_from_properties_file(file=filename, gens=gens, pop_size=pop_size, 
    out_dir=out_dir, draw=True, verbose=verbose, print_properties=print_properties, 
    move=move, output=output, overwrite=True, toolbox=toolbox)
toc = time.perf_counter()

elapsed = toc-tic
print(f'Evolve time: {elapsed:4.2f}')

sfig=evr.create_stats_plot(evr.stats_history)

print(score)

if online and not debug:
    #assert score == 1.4439277168113878
    #assert score == 2.497800695219841
    npt.assert_almost_equal(score,  47.102084829889066)
    #npt.assert_almost_equal(score, 2.730255138400179)
else:
    npt.assert_almost_equal(score,  47.102084829889066)
    #assert score == 47.314969196199557

print(score)

move={'OL0C0sm':[0.25,0], 'CL0C0':[0.25,0]}
filename = 'testfiles/ga-000.110-s029-1x1-6655--1760182505815353182.properties'

toolbox = base.Toolbox()

tic = time.perf_counter()
out,evr,score = evolve_from_properties_file(file=filename, gens=gens, pop_size=pop_size, out_dir=out_dir, 
    draw=True, figsize=(14,12), verbose=verbose, print_properties=print_properties, move=move, 
    output=output, overwrite=True, toolbox=toolbox)
toc = time.perf_counter()

elapsed = toc-tic
print(f'Evolve time: {elapsed:4.2f}')

sfig=evr.create_stats_plot(evr.stats_history)

print(score)

if online and not debug:
    #assert score == 0.1104365333118583
    #assert score == 0.10916236281693095
    npt.assert_almost_equal(score, 0.11202464496789143)    
else:
    #assert score == 9.222988568285782
    #assert score == 6.313868582375436
    #assert score == 20.85836482794505
    npt.assert_almost_equal(score, 18.17885814419378)

#| hide
import nbdev; nbdev.nbdev_export()
