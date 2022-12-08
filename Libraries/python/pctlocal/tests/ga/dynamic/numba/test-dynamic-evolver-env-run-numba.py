# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""

from numba import jit


import argparse
import time
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

from epct.evolvers import evolve_from_properties_file

if True:
    file = '../CartPoleV1/TopError-RootSumSquaredError-AllFloats-WeightedSum-Topp1.properties'
    debug = 0
    verbose = True
    render=False
    gens = 3
    pop = 4
    test=False
    overwrite = True
    start=1
    iters=5
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
    
verbosed = {'debug':debug, 'evolve_verbose':verbose, 'deap_verbose': False, 'save_arch_all': False,
           'save_arch_gen':  False, 'display_env':render, 'deap_verbose':False, 'hpct_verbose':False}

#move={'OL0C0sm':[0.2,0]}
move={}


@jit(nopython=True)
def evolve(file, verbose, seed, gens, pop_size, test, move, draw, print_properties, overwrite, log):
    out,evr,score=evolve_from_properties_file(file, verbose=verbosed, seed=seed, gens=gens, pop_size=pop, 
          test=test, move=move, draw=False, print_properties=verbose, overwrite=overwrite, log=True)

    return out,evr,score


mtic = time.perf_counter()

for seed in range(start,iters+start,1):
    tic = time.perf_counter()
    out,evr,score=evolve(file, verbose=verbosed, seed=seed, gens=gens, pop_size=pop, 
          test=test, move=move, draw=False, print_properties=verbose, overwrite=overwrite, log=True)
    if out != None:
        toc = time.perf_counter()
        elapsed = toc-tic        
        if verbose:
            print(f'Evolve time: {elapsed:4.2f}')
        if history:
            sfig=evr.create_stats_plot(evr.stats_history)


mtoc = time.perf_counter()
elapsed = mtoc-mtic        
print(f'Evolve all time: {elapsed:4.2f}')





