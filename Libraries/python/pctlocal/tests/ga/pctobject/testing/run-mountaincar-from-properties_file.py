#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""



from pct.architectures import run_from_properties_file
from utils.paths import get_gdrive
import os


seed=None
figsize=(14, 14)
verbose=True
plots = []
nevals = None
root_dir=get_gdrive()
prefix = 'data/ga/'
env = 'MountainCarContinuousV0/'
type = 'Topp1-ReferencedInputsError-RootMeanSquareError-Binary-SmoothWeightedSum/'
funcdata = False #True #False

if funcdata:
    move={'MountainCarContinuousV0': [-0.6, -0.5], 'Action1ws': [-0.4, -0.4], 
      'OL0C0sm\n0.93': [-0.28, -0.25], 'OL0C1sm\n0.51': [0.28, -0.25],  
      'OL1C0sm\n0.47': [0, -0.1], 'IV': [-0.1, 0.0], 'IP': [-0.6, 0.5], 'CL1C0': [0, 0.1]}
else:
    move={'MountainCarContinuousV0': [-0.6, -0.5], 'Action1ws': [-0.4, -0.4], 
      'OL0C0sm': [-0.28, -0.25], 'OL0C1sm': [0.28, -0.25],  
      'OL1C0sm': [0, -0.1], 'IV': [-0.1, 0.0], 'IP': [-0.6, 0.5], 'CL1C0': [0, 0.1]}


test=21


if test==20:
    # only works with plenty of momentum
    file = 'ga-000.158-s045-1x1-6655--219450010485841347.properties'
    plots = [{'plot_items': {'IP':'ip', 'IV':'iv'}, 'title':'Inputs'},
             {'plot_items': {'CL0C0':'err'}, 'title':'Error'},
             {'plot_items': {'RL0C0c':'ref', 'PL0C0ws': 'per'}, 'title':'Goal'}]  
    nevals=1
    #seed = 58
    
if test==21:
    # only works with plenty of momentum
    file = 'ga-000.334-s005-2x2-6655-0e807ca9d92dc8b7f825dfb5d7fe79c2.properties'
    plots = [{'plot_items': {'IP':'ip', 'IV':'iv'}, 'title':'Inputs'},
             {'plot_items': {'CL0C0':'err'}, 'title':'Error'},
             {'plot_items': {'RL1C0c':'ref', 'PL1C0ws': 'per'}, 'title':'Goal'}]  
    
    
    plots = [
        {'plot_items': {'IP':'ip', 'IV':'iv'},'title':'Inputs'},
        {'plot_items': {'RL1C0c':'ref1', 'PL1C0ws':'per1'}, 'title':'L1'},
        {'plot_items': {'RL0C0ws':'ref0', 'PL0C0ws':'per0'}, 'title':'C0'},
        {'plot_items': {'RL0C1ws':'ref0', 'PL0C1ws':'per0'}, 'title':'C1'},
        {'plot_items': {'CL0C0':'err00', 'CL0C1':'err01', 'CL1C0':'err1'}, 'title':'Error'},
        {'plot_items': {'OL0C0sm':'out0', 'OL0C1sm':'out1'}, 'title':'Output'},
        {'plot_items': {'Action1ws':'act'}, 'title':'Action'}
        ]
    
    plots = []

    
    nevals=1
    #seed = 58
    
    
    
file_path=os.sep.join((prefix, env, type))
render = False
draw_file="mc.png"
hpct, score_sum, output = run_from_properties_file(root_dir=root_dir, path=file_path, file=file, 
    nevals=nevals, move=move, plots=plots, seed=seed, print_properties=True, verbose=verbose, 
    draw=True, early_termination=True, figsize=figsize, render =render, draw_file=draw_file, funcdata=funcdata)








