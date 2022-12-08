#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""



from pct.architectures import run_from_properties_file

from pct.putils import get_gdrive
import os



seed=None
plots = []
nevals = 1
draw=True
root_dir=get_gdrive()
runs=1
figsize=(8,8)

prefix = 'data/ga/'
env = 'CartPoleV1/'
type = 'Default/'
move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
          'CartPoleV1':[-.5,-0.25], 'Action1ws':[-0.4,0]}

test=10

if test==10:
    file = 'ga-001.444-3344-397818342161201780.properties'
    
    move={'CartPoleV1': [-1, -0.2],'ICV': [-0.45, 0], 'ICP': [-0.25,  0.1], 
      'IPV': [-0.05, 0.2],'IPA': [0.1, 0.3], 'OL0C0ws':[0.0,0], 
      'RL0C0c':[-0.6,-0], 'PL0C0ws':[0.4,-0.5],  
      'Action1ws': [-0.9, 0]}
    #move={'CartPoleV1': [-1, -0.2],'ICV': [-0.45, 0], 'ICP': [-0.25,  0.1], 
    #  'IPV': [-0.05, 0.2],'IPA': [0.15, 0.3],  
    #  'Action1ws': [-0.75, 0]}
    
    #plots = [ {'plot_items': {'IPA':'pa','IPV':'pv','ICP':'cp','ICV':'cv'}, 'title':'Inputs'}]
    #plots = [ {'plot_items': {'IPA':'pa'}, 'title':'Inputs'}]
    
    plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'}]
    
    plots = []

    #plots = [ {'plot_items': {'IV':'iv','IT':'it'}, 'title':'Input'}]  
    #nevals=1

    
    
file_path=os.sep.join((prefix, env, type))
    
hpct, score_sum, output = run_from_properties_file(root_dir=root_dir, path=file_path, file=file, 
            nevals=nevals, move=move, figsize=figsize, draw=draw, runs=runs,
            plots=plots, seed=seed, print_properties=True)








