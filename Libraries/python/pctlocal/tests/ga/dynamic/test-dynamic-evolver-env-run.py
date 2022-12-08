# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""


import argparse
import os
import time
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

from deap import base
from deap import creator

from epct.evolvers import evolve_from_properties_file
from epct.evolvers import CommonToolbox
from pct.putils import get_gdrive


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

if False:
    #file = 'CartPoleV1/TopError-RootSumSquaredError-AllFloats-WeightedSum-Topp1.properties'
    #file = 'PendulumV0_1/Topp5-ReferencedInputsError-SmoothError-AllFloats-SmoothWeightedSum.properties'
    #file =     'testfiles/ga-001.444-3344-397818342161201780.properties'
    #file = 'PendulumV0/Std-RewardError-RootMeanSquareError-Binary-SmoothWeightedSum.properties'
    #file = 'MountainCarContinuousV0/Topp1-ReferencedInputsError-RootMeanSquareError-Binary-SmoothWeightedSum.properties'
    
    #file = 'MountainCarContinuousV0/Topp1-ReferencedInputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum.properties'
    #file =     'testfiles/ga-000.326-s066-2x3-6655-a6abebd2c88246e9f77dd8623eac6e3e.properties'

    file = 'CartPoleV1/InputsError-RootMeanSquareError-Binary-WeightedSum-Std.properties'

    debug = 0
    verbose = True
    render=False
    gens = 2
    pop = 4
    gens = 10
    pop = 100
    
    test=False
    overwrite = False
    start=12
    iters=1
    history=False

else:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the properties file name")
    
    parser.add_argument("-v", "--verbose", help="print output ", action="store_true")
    parser.add_argument("-hi","--history", help="plot stats history", action="store_true")
    parser.add_argument("-o", "--overwrite", help="overwrite existing file", action="store_true")
    parser.add_argument("-r", "--render", help="display environment run after each generation", action="store_true")
    parser.add_argument("-t", "--test", help="test run", action="store_true")
    
    parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
    parser.add_argument('-p', '--pop', type=int, help="population size", default=100)
    parser.add_argument('-g', '--gens', type=int, help="number of generations")
    parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
    parser.add_argument('-m', '--multi', type=int, help="number of processors, for multiprocessing", default=1)
    parser.add_argument('-d', '--debug', type=int, help="debug level, 0 - 3", default=0)
    
    args = parser.parse_args()
    file = args.file
    debug = args.debug
    verbose = args.verbose
    
    render=args.render
    gens = args.gens
    pop = args.pop 
    test=args.test
    overwrite =args.overwrite 
    start=args.start
    iters=args.iters
    history=args.history
    processes=args.multi
    
verbosed = {'debug':debug, 'evolve_verbose':verbose, 'deap_verbose': False, 'save_arch_all': False,
           'save_arch_gen':  False, 'display_env':render, 'deap_verbose':False, 'hpct_verbose':False}

#move={'OL0C0sm':[0.2,0]}
move={}
out_dir=get_gdrive()+ 'data' +os.sep+'ga'+os.sep

for seed in range(start,iters+start,1):
    tic = time.perf_counter()
    out,evr,score=evolve_from_properties_file(out_dir=out_dir, file=file,  verbose=verbosed, seed=seed, 
        gens=gens, pop_size=pop, test=test, move=move, draw=False, print_properties=verbose, 
        output=True, overwrite=overwrite, log=True, toolbox=toolbox, processes=processes)
    
    #out,evr,score = evolve_from_properties_file(file=file, gens=gens, pop_size=pop, out_dir='.',
    #    draw=True, verbose=verbosed, print_properties=True, move=move, output=False, summary=True)
    
    if out != None:
        toc = time.perf_counter()
        elapsed = toc-tic        
        if render:
            for ctr, best in enumerate(evr.best_of_gens):
                print(ctr, best)
        if verbose:
            print(f'Evolve time: {elapsed:4.2f}')
        if history:
            sfig=evr.create_stats_plot(evr.stats_history)





