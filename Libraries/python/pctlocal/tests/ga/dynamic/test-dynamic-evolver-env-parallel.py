# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""


import sys
import time
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

from epct.evolvers import evolve_from_properties_file

# python -m scoop test-dynamic-evolver-env-scoop.py

#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))

# test-dynamic-evolver-cartpole-run.py cp.properties, 1 1 True True
# filename, loops, start, single, test, pop, gens

if __name__ == '__main__':

    args = ['testfiles/ga-000.110-s029-1x1-6655--1760182505815353182.properties', '1', '1', 'True', 'False', '100', '10']
    
    parallel=True
    display_env = False
    debug = 0
    
    nargs = len(sys.argv)
    for index in range(1, nargs-1, 1):
        args[index-1]=sys.argv[index]
        
    #print(args)
    
    pop_size=None
    gens=10
    
    filename = args[0]
    loops = eval(args[1])
    start=eval(args[2])
    single = eval(args[3])
    test=eval(args[4])
    if len(args)>5:
        pop_size = eval(args[5])
    if len(args)>6:
        gens= eval(args[6])
        
    verbose = {'debug':debug, 'evolve_verbose':1, 'deap_verbose': False, 'save_arch_all': False,
               'save_arch_gen':  False, 'display_env':display_env, 'deap_verbose':False, 'hpct_verbose':False}
    
    move={'OL0C0sm':[0.2,0]}
    

    if single:
        tic = time.perf_counter()
        out,evr,score=evolve_from_properties_file(filename, verbose=verbose, gens=gens, pop_size=pop_size, test=test, move=move, 
                                    parallel=parallel, draw=True, print_properties=True)
        if out != None:
            toc = time.perf_counter()
            elapsed = toc-tic        
            print(f'Evolve time: {elapsed:4.2f}')
            sfig=evr.create_stats_plot(evr.stats_history)
    else:
        for seed in range(start,loops+start,1):
            evolve_from_properties_file(filename, verbose=verbose, seed=seed, test=test, move=move,parallel=parallel)
    



