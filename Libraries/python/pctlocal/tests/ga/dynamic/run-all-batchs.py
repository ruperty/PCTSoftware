#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""


import os
from pct.architectures import run_from_properties_file
from pct.putils import get_gdrive

render=False
summary=False
hpct_verbose=False
verbose=False
seed=1
plots = []
nevals = 2
runs=500
plot=[]
move={}
root_dir=get_gdrive()
size = None
early_termination=False
print_properties=False
fseed=None
draw=False
print_properties=False

error_collector = 'RewardError'
error_response = 'CurrentError'

prefix = 'data'+os.sep+'ga'+os.sep

env='MountainCarContinuousV0-1'

omit = 'RewardError'
    
    
def runs_batches(root_dir, prefix, env, omit):
    dir_path=os.sep.join((root_dir, prefix, env))
    print(dir_path)
    for dir in os.listdir(dir_path):
        if dir.find(omit)>=0:
            continue
        print(dir)
        full_dir = os.sep.join((root_dir, prefix, env, dir))
    
        for file in os.listdir(full_dir):
            pass
            #print(file)
            
            file_path=os.sep.join((prefix, env, dir))
            hpct, sum, output = run_from_properties_file(root_dir=root_dir, path=file_path, file=file, nevals=nevals, 
                    move=move, render=render, verbose=verbose, summary=summary, draw=draw, runs=runs, 
                    plots=plots, seed=seed, print_properties=print_properties, early_termination=early_termination,
                    error_collector_type=error_collector, error_response_type=error_response)
            
            if sum == 0:
                print('>>', file, f'{output:4.3f}')

runs_batches(root_dir, prefix, env, omit)







