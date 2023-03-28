
#| include: false
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
draw=False
output=False
out_dir=None

#| gui
online=True
debug=False
draw=True

if online and not debug:
    verbose = {'evolve_verbose':1}
    print_properties=True
    gens=None
    pop_size=None
    #output=True
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

move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
          'Pendulum':[-.5,-0.25], 'Action1ws':[-0.4,0]}
filename = 'testfiles/ga-000.270-s009-1x2-3344-859779289552369250.properties'

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

if hasattr(creator, 'FitnessMin'):
    del creator.FitnessMin
    del creator.Individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

tic = time.perf_counter()
out,evr,score = evolve_from_properties_file(file=filename, gens=gens, pop_size=pop_size, out_dir=out_dir, 
    draw=draw, verbose=verbose, print_properties=print_properties, move=move, output=output, toolbox=toolbox)
toc = time.perf_counter()

elapsed = toc-tic
print(f'Evolve time: {elapsed:4.2f}')

sfig=evr.create_stats_plot(evr.stats_history)

print(score)

if online and not debug:
    #assert score == 0.26978597182270175
    #assert score == 0.26894295091129783
    npt.assert_almost_equal(score, 2.1899479885177566)
else:
    #assert score == 0.8850472758783118
    #assert score == 2.6363647691355183
    npt.assert_almost_equal(score, 2.1899479885177566)

move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
          'Pendulum':[-.5,-0.25], 'Action1ws':[-0.4,0]}
#filename = 'testfiles/ga-000.825-s008-1x2-6655-5991537330581304229.properties'
filename = 'testfiles/ga-001.882-s009-1x2-6655-1660c5b8a2ceb3bd7749d80b07132506.properties'

toolbox = base.Toolbox()

tic = time.perf_counter()
out,evr,score = evolve_from_properties_file(file=filename, gens=gens, pop_size=pop_size, out_dir=out_dir, 
    draw=draw, figsize=(14,14), verbose=verbose, print_properties=print_properties, move=move, 
    output=output, toolbox=toolbox)
toc = time.perf_counter()

elapsed = toc-tic
print(f'Evolve time: {elapsed:4.2f}')

sfig=evr.create_stats_plot(evr.stats_history)

print(score)

if online and not debug:
    #assert score == 0.8254670799410004
    #assert score == 0.6311335956974932
    npt.assert_almost_equal(score, 2.273327359300754)
else:
    #assert score == 2.071381553474449
    #assert score == 4.464886695620801
    npt.assert_almost_equal(score,  7.6551149763049935  )

#| hide
import nbdev; nbdev.nbdev_export()
