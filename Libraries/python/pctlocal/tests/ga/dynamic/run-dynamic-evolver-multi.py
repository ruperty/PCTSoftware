# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""

from  multiprocessing import Pool
import numpy as np
import argparse
import os
import time
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

from epct.evolvers import evolve_from_properties_file
from pct.putils import get_gdrive





def evolve(args):
    seed=args['seed']
    file=args['file']
    verbosed=args['verbosed']
    gens=args['gens']
    pop=args['pop']
    verbose=args['verbose']
    overwrite=args['overwrite']
    #{'seed': i, 'file': args.file, 'verbosed':args.verbosed, 'gens':args.gens, 'pop':args.pop, 
    #           'test':args.test, 'overwrite':args.overwrite, 'move':move, 'verbose': args.verbose}
    
    print(f'Start seed {seed}')
    tic = time.perf_counter()
    
    out_dir=get_gdrive()+ 'data' +os.sep+'ga'+os.sep
    out,evr,score=evolve_from_properties_file(out_dir=out_dir,file=file, verbose=verbosed, seed=seed, gens=gens, pop_size=pop, 
          output=True, draw=False, print_properties=verbose, overwrite=overwrite, log=True)
    if out != None:
        toc = time.perf_counter()
        elapsed = toc-tic        
        print(f'Seed {seed} Evolve time: {elapsed:4.2f}')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the properties file name")
    
    parser.add_argument("-v", "--verbose", help="print output ", action="store_true")
    parser.add_argument("-hi","--history", help="plot stats history", action="store_true")
    parser.add_argument("-o", "--overwrite", help="overwrite existing file", action="store_true")
    parser.add_argument("-r", "--render", help="display environment run after each generation", action="store_true")
    #parser.add_argument("-t", "--test", help="test run", action="store_true")
    
    parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
    parser.add_argument('-p', '--pop', type=int, help="population size", default=100)
    parser.add_argument('-g', '--gens', type=int, help="number of generations")
    parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
    parser.add_argument('-d', '--debug', type=int, help="debug level, 0 - 3", default=0)
    
    args = parser.parse_args()
    start=args.start
    iters=args.iters
        
    verbosed = {'debug':args.debug, 'evolve_verbose':args.verbose, 'deap_verbose': False, 'save_arch_all': False,
               'save_arch_gen':  False, 'display_env':args.render, 'deap_verbose':False, 'hpct_verbose':False}
        
    list=[]
    for i in range(start, iters+start, 1):
        arg = {'seed': i, 'file': args.file, 'verbosed':verbosed, 'gens':args.gens, 'pop':args.pop, 
               'overwrite':args.overwrite, 'verbose': args.verbose}
        list.append(arg) 
    
    p = Pool()
    p.map(evolve, list)
    
    p.close()
    p.join()





