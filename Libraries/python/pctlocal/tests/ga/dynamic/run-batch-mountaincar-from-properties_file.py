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

plots = [ {'plot_items': {'reward':'err'}, 'title':'Reward'}]
move={'IV':[0.2,0],'IP':[-0.2,0.1],'OL0C0sm':[0,-0.2],'OL1C0sm':[0,-0.2], 'MountainCarContinuousV0':[-.4,-0.25], 'Action1ws':[-0.45,-0.3]}


test = 2


if test == 2:    
    ttest = 5
    if ttest == 1:    
        dir = 'MountainCarContinuousV0xx/Topp1-ReferencedInputsError-CurrentError-AllFloats-SmoothWeightedSum/'
        fseed='s001'
        #nevals=1
        early_termination=True
        plots = [ {'plot_items': {'IP':'ip'}, 'title':'Inputs'},
                  {'plot_items': {'reward':'err'}, 'title':'Reward'}]

    if ttest == 4:    
        dir = 'MountainCarContinuousV0-1/Topp1-ReferencedInputsError-RootMeanSquareError-Binary-SmoothWeightedSum/'

        lower_limit=0.325
        upper_limit=0.332
        #seed=10
        nevals=1
        error_collector = 'RewardError'
        error_response = 'CurrentError'
        early_termination=True

    if ttest == 5:    
        dir = 'MountainCarContinuousV0-1/Topp1-ReferencedInputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        # great! ga-000.326-s066-2x3-6655-a6abebd2c88246e9f77dd8623eac6e3e.properties vel 8 5   
        figsize=(12,14)
        move={'IV':[0.15,0.2],'IP':[-0.8,0.1],
              'OL0C0sm':[-0.4,-0.2],'OL0C1sm':[0,-0.2],'OL0C2sm':[0.4,-0.2],
              'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}
        # great! ga-000.330-s064-3x3-6655-345d7433a4d8b74a5176c7538bef9c98.properties vel -100 -25
        # great! ga-000.401-s093-2x1-6655-2b4b558d02b2661881f9a5109fedca77.properties vel -3 -2 s94
        move={'IV':[0.2,0],'IP':[-0.2,0.1],'OL0C0sm':[0,-0.2],'OL1C0sm':[0,-0.2],
              'MountainCarContinuousV0':[-.4,-0.25], 'Action1ws':[-0.45,-0.3]}
        
        lower_limit=0.401
        upper_limit=0.401
        #fseed='s066'
        #seed=94
        nevals=1
        runs=1
        error_collector = 'RewardError'
        error_response = 'CurrentError'
        early_termination=True
        plots = [ 
                {'plot_items': {'IP':'ip'}, 'title':'Inputs'},
                {'plot_items': {'OL0C0sm':'out'}, 'title':'Output'},
                {'plot_items': {'reward':'err'}, 'title':'Reward'}
                ]
        plots=[]


if test == 1:    
    ttest = 1
    if ttest == 1:    
        dir = 'MountainCarContinuousV0/Topp1-ReferencedInputsError-CurrentError-AllFloats-SmoothWeightedSum/'
        fseed='s001'
        #nevals=1
        early_termination=True
        plots = [ {'plot_items': {'IP':'ip'}, 'title':'Inputs'},
                  {'plot_items': {'reward':'err'}, 'title':'Reward'}]

    if ttest == 2:    
        dir = 'MountainCarContinuousV0/Topp1-ReferencedInputsError-CurrentError-Binary-SmoothWeightedSum/'

    if ttest == 3:    
        dir = 'MountainCarContinuousV0-1/Topp1-ReferencedInputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.325
        upper_limit=0.326
        seed=10
        #nevals=10
        render=True#False
        #size='2x3'
        #runs=1


    if ttest == 4:    
        dir = 'MountainCarContinuousV0-1/Topp1-ReferencedInputsError-RootMeanSquareError-Binary-SmoothWeightedSum/'
        lower_limit=0.334
        upper_limit=0.334
        #seed=22
        nevals=1
        render=True#False
        #size='5x3'
        runs=210

    if ttest == 5:    
        dir = 'MountainCarContinuousV0/Topp1-ReferencedInputsError-SmoothError-AllFloats-SmoothWeightedSum/'

    if ttest == 6:    
        dir = 'MountainCarContinuousV0-1/Topp1-ReferencedInputsError-SmoothError-Binary-SmoothWeightedSum/'
        lower_limit=0.0
        upper_limit=0.07
        #seed=56

    if ttest == 7:    
        dir = 'MountainCarContinuousV0/Topp1-RewardError-CurrentError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.0
        upper_limit=0.0
        fseed='s001'


    if ttest == 8:    
        dir = 'MountainCarContinuousV0/Topp1-RewardError-CurrentError-Binary-SmoothWeightedSum/'

    if ttest == 9:    
        dir = 'MountainCarContinuousV0/Topp1-RewardError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
    if ttest == 10:
        dir = 'MountainCarContinuousV0/Topp1-RewardError-RootMeanSquareError-Binary-SmoothWeightedSum/'
    if ttest == 11:    
        dir = 'MountainCarContinuousV0/Topp1-RewardError-SmoothError-AllFloats-SmoothWeightedSum/'



    if ttest == 12:    
        dir = 'MountainCarContinuousV0/Topp1-RewardError-SmoothError-Binary-SmoothWeightedSum/'
        lower_limit=0.0
        upper_limit=0.0
        nevals=1
        fseed='s006'

    if ttest == 13:    
        dir = 'MountainCarContinuousV0/Topp1-TopError-CurrentError-AllFloats-SmoothWeightedSum/'
    if ttest == 14:    
        dir = 'MountainCarContinuousV0/Topp1-TopError-CurrentError-Binary-SmoothWeightedSum/'



    if ttest == 15:    
        dir = 'MountainCarContinuousV0-1/Topp1-TopError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.16
        upper_limit=0.17
        #seed=1
        #nevals=1
        render=True#False

    if ttest == 16:    
        dir = 'MountainCarContinuousV0/Topp1-TopError-RootMeanSquareError-Binary-SmoothWeightedSum/'

    if ttest == 17:    
        dir = 'MountainCarContinuousV0-1/Topp1-TopError-SmoothError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.0
        upper_limit=0.000
        #seed=56

    if ttest == 18:    
        dir = 'MountainCarContinuousV0/Topp1-TopError-SmoothError-Binary-SmoothWeightedSum/'

 
    
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







