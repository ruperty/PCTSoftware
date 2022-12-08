#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""


import os
from pct.architectures import run_from_properties_file
from pct.putils import get_gdrive

render=True
summary=False
hpct_verbose=False
verbose=True
seed=None
plots = []
nevals = None
figsize=(14,12)
runs=500
plot=[]
move={}
root_dir=get_gdrive()
size = None
early_termination=False
print_properties=False
fseed=None

error_collector = None
error_response = None

prefix = 'data/ga/'

plots = [ {'plot_items': {'IPA':'ipa'}, 'title':'Inputs'},
          {'plot_items': {'reward':'reward'}, 'title':'Reward'}]

move={'CartPoleV1': [-0.6, -0.2],'ICV': [-0.45, 0], 'ICP': [-0.25,  0.1], 
  'IPV': [-0.05, 0.2],'IPA': [0.1, 0.3], 'OL0C0ws':[0.0,0], 
  #'RL0C0c':[-0.6,-0.4], 'PL0C0ws':[0.4,-0.5],  
  'Action1ws': [-1, 0]}

move={'ICV':[-0.17,-0.11],'ICP':[-0.05,-0.1],
      'IPV':[0.08,-0.02],'IPA':[0.2,0.05],
      'CartPoleV1':[-.7,-0.4], 'Action1ws':[-0.52,-0.25], 'CL1C0':[0.05,0],
      'OL0C0ws':[-0.25,-0.04], 'OL0C1ws':[0.26,-0.05], 'OL1C0ws':[0.1,0]}

plots=[]

test = 2


if test == 2:    
    dir = 'CartPoleV1/InputsError-RootMeanSquareError-Binary-WeightedSum-Std/'
    lower_limit=0.000
    upper_limit=0.112

    fseed='s012'
    #nevals=1
    #early_termination=True



    """
    plots = [ 
             {'plot_items': {'IT':'it','IV':'iv'}, 'title':'Inputs'},
             {'plot_items': {'PL1C0ws':'per1','RL1C0c':'ref1'}, 'title':'Goals1'},
             {'plot_items': {'PL0C0ws':'per0','RL0C0ws':'ref0'}, 'title':'Goals0'},
             {'plot_items': {'OL0C0sm':'out','CL0C0':'com'}, 'title':'Output0'},
             {'plot_items': {'Action1ws':'act'}, 'title':'Action'}
             ]
    nevals = 1
    """
    #seed = 15
 



def get_score(file):
    index1 = file.find('-')
    if file.find('--') > 0:
        index2 = file.find('-', index1+2, len(file)-1)
        score = file[file.find('-')+1: index2]
    else:
        score = file[index1+1: file.find('-', index1+1, len(file)-1)]

    return eval(score)

def get_fseed_in_filename(file):
    index = file.find('-', 5)
    fseed = file[index+1: index+5]
    
    return fseed
    
    
def multiple_files_in_folder(root_dir, prefix, dir, fseed):
    dir_path=''.join((root_dir, prefix, dir))
    
    for file in os.listdir(dir_path):
        if fseed == None:
            if size != None and file.find(size)<0:
                continue
                
            score = get_score(file)
            if score < lower_limit:
                continue
            if score > upper_limit:
                break
        else:            
            if fseed != get_fseed_in_filename(file):
                continue
        

        print(file)
        file_path=''.join((prefix, dir))
        
        hpct, sum, output = run_from_properties_file(root_dir=root_dir, path=file_path, 
                file=file, nevals=nevals, figsize=figsize,
                move=move, render=render, verbose=verbose, summary=summary, draw=True, runs=runs, 
                hpct_verbose=hpct_verbose, plots=plots, seed=seed, print_properties=print_properties,   
                early_termination=early_termination, error_collector_type=error_collector, 
                error_response_type=error_response)
        print(f'{output:4.3f}')
        if fseed != None:
            break


multiple_files_in_folder(root_dir, prefix, dir, fseed)







