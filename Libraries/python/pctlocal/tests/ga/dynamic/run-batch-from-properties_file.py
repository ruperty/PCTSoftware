#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""


import os
from pct.architectures import run_from_properties_file
from pct.putils import get_gdrive


summary=False
verbose=False
seed=None
plots = []
nevals = None
runs=500
plot=[]
move={}
root_dir=get_gdrive()
size = None


prefix = 'data/ga/'

test = 30


if test == 30:    
    ttest = 1
    if ttest == 1:    
        dir = 'MountainCarContinuousV0/Topp1-ReferencedInputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.332
        upper_limit=0.403
        #seed=56
        size='2x1'

    if ttest == 4:    
        dir = 'MountainCarContinuousV0/Topp1-ReferencedInputsError-SmoothError-Binary-SmoothWeightedSum/'
        lower_limit=0.0
        upper_limit=0.07
        #seed=56

    if ttest == 7:    
        dir = 'MountainCarContinuousV0/Topp1-TopError-SmoothError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.0
        upper_limit=0.000
        #seed=56

if test == 29:    
    ttest = 2
    if ttest == 1:    
        dir = 'PendulumV0/Std-RewardError-RootMeanSquareError-Binary-SmoothWeightedSum/'
        lower_limit=1.81
        upper_limit=2.3
    
    if ttest == 2:    
        dir = 'PendulumV0/Std-RewardError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        lower_limit=1.3
        upper_limit=1.7

    if ttest == 3:    
        dir = 'PendulumV0/Std-InputsError-RootMeanSquareError-Binary-SmoothWeightedSum/'
        lower_limit=0.83
        upper_limit=0.85

    if ttest == 4:    
        dir = 'PendulumV0/Std-InputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.805
        upper_limit=0.825



if test == 28:    
    ttest = 7
    if ttest == 1:    
        dir = 'PendulumV0_1/Topp5-ReferencedInputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        lower_limit=0
        upper_limit=3
    if ttest == 2:    
        dir = 'PendulumV0_1/Topp5-ReferencedInputsError-RootMeanSquareError-Binary-SmoothWeightedSum/'
        lower_limit=0
        upper_limit=3.02
    if ttest == 3:    
        dir = 'PendulumV0_1/Topp5-ReferencedInputsError-SmoothError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.3
        upper_limit=0.52
    if ttest == 4:    
        dir = 'PendulumV0_1/Topp5-ReferencedInputsError-SmoothError-Binary-SmoothWeightedSum/'
        lower_limit=0.3
        upper_limit=0.5
        #nevals=1
        #runs=1000
        
    if ttest == 5:    
        dir = 'PendulumV0_1/Topp5-TotalError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
        lower_limit=0
        upper_limit=1.7
    if ttest == 6:    
        dir = 'PendulumV0_1/Topp5-TotalError-RootMeanSquareError-Binary-SmoothWeightedSum/'
        # check out this one
        lower_limit=2.42
        upper_limit=2.44
        move={'IV':[-0.4,0.5],'IT':[0.1,0.3],'OL0C0sm':[-0.275,-0.1],'OL0C1sm':[0.275,-0.1], 'PendulumV0_1':[-.4,-0.25], 'Action1ws':[-0.4,0]}
        nevals=1
        runs=1
    if ttest == 7:    
        dir = 'PendulumV0_1/Topp5-TotalError-SmoothError-AllFloats-SmoothWeightedSum/'
        lower_limit=0.038
        upper_limit=0.040
    if ttest == 8:    
        dir = 'PendulumV0_1/Topp5-TotalError-SmoothError-Binary-SmoothWeightedSum/'
        # check out these
        lower_limit=0.4
        upper_limit=0.44
        #move={'IV':[-0.4,0.5],'IT':[0.1,0.3],'OL0C0sm':[-0.275,-0.1],'OL0C1sm':[0.275,-0.1], 'PendulumV0_1':[-.4,-0.25], 'Action1ws':[-0.4,0]}
        move={'IV':[-0.4,0.5],'IT':[0.1,0.3],'OL0C0sm':[0,-0.1], 'PendulumV0_1':[-.4,-0.25], 'Action1ws':[-0.4,-0.2]}
    
    
        #seed=66
        #nevals=1
        #runs=1000
        #verbose=True



if test == 27:
    #dir = 'PendulumV0_1/Topp5-TotalError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
    dir = 'PendulumV0_1/Topp5-TotalError-RootMeanSquareError-Binary-SmoothWeightedSum/'

    lower_limit=0
    upper_limit=55.6
    #seed=63
    nevals=1
    verbose=True

if test == 26:
    #dir = 'PendulumV0_1//'
    #dir = 'PendulumV0_1/Topp4-TotalError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
    #dir = 'PendulumV0_1/Topp4-TotalError-RootMeanSquareError-Binary-SmoothWeightedSum/'
    dir = 'PendulumV0_1/Topp4-TotalError-SmoothError-AllFloats-SmoothWeightedSum/'

    
    
    lower_limit=0
    upper_limit=0.01
    #seed=63
    #nevals=1
    #verbose=True


if test == 25:
    #dir = 'PendulumV0/Topp2-RewardError-SmoothError-AllFloats-SmoothWeightedSum/'
    #dir = 'PendulumV0/Topp2-RewardError-SmoothError-Binary-SmoothWeightedSum/'
    #dir = 'PendulumV0//'
    #dir = 'PendulumV0/Topp2-TopError-RootMeanSquareError-Binary-SmoothWeightedSum/'
    #dir = 'PendulumV0/Topp2-TopError-SmoothError-AllFloats-SmoothWeightedSum/'
    
    dir = 'PendulumV0/Topp2-TopError-SmoothError-Binary-SmoothWeightedSum/'
    
    lower_limit=0.44
    upper_limit=0.44
    #seed=41
    #nevals=1
    #verbose=True



if test == 24:
    #dir = 'PendulumV0_1/Topp4-TotalError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'
    #dir = 'PendulumV0_1/Topp4-TotalError-RootMeanSquareError-Binary-SmoothWeightedSum/'
    #dir = 'PendulumV0_1/Topp4-TotalError-SmoothError-AllFloats-SmoothWeightedSum/'
    dir = 'PendulumV0_1/Topp4-TotalError-SmoothError-Binary-SmoothWeightedSum/'

    lower_limit=0.0
    upper_limit=0.7
    seed=80
    #nevals=1
    #verbose=True


if test == 23:
    #dir = 'PendulumV0_1/Topp3-InputsError-RootMeanSquareError-Binary-SmoothWeightedSum/'   
    #dir = 'PendulumV0_1/Topp3-InputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'   

    #dir = 'PendulumV0_1/Topp3-InputsError-SmoothError-AllFloats-SmoothWeightedSum/'   
    #  ??  dir = 'PendulumV0_1/Topp3-RewardError-RootMeanSquareError-Binary-SmoothWeightedSum/'   

    # not good dir = 'PendulumV0_1/Topp3-TopError-RootMeanSquareError-Binary-SmoothWeightedSum/'   

    dir = 'PendulumV0_1/Topp3-TopError-SmoothError-AllFloats-SmoothWeightedSum/'

    lower_limit=0.013
    upper_limit=0.013
    #seed=1
    #nevals=1
    #verbose=True

    
if test == 22:
    # reject zero wts dir = 'PendulumV0/TopError-SmoothError-AllFloats-SmoothWeightedSum-Std/'    
    # ok dir = 'PendulumV0/InputsError-RootMeanSquareError-AllFloats-WeightedSum-Topp1/'   
    # poor dir = 'PendulumV0/InputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum-Topp1/'   
    # poor dir = 'PendulumV0/InputsError-RootMeanSquareError-Floats-WeightedSum-Std/'   
    # some good seed 99 dir = 'PendulumV0/InputsError-SmoothError-AllFloats-SmoothWeightedSum-Std/'   
    #dir = 'PendulumV0/TopError-RootSumSquaredError-Floats-SmoothWeightedSum-Std/'   
  
    #dir = 'PendulumV0/Topp1-TopError-RootMeanSquareError-Binary-SmoothWeightedSum/'   
  
    # look at s10, s54
    #dir = 'PendulumV0/Topp2-TopError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'   
  
    # not good dir = 'PendulumV0/Topp2-RewardError-RootMeanSquareError-Binary-SmoothWeightedSum/'   
    # not good dir = 'PendulumV0/Topp2-RewardError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'   
  
    # not good dir = 'PendulumV0/Topp2-TopError-RootMeanSquareError-Binary-SmoothWeightedSum/'   
    
    dir = 'PendulumV0/Topp2-InputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum/'   
  
    
    lower_limit=4.995
    upper_limit=4.997
    move={'IV':[-0.5,0.5],'IT':[0,0.3], 'PendulumV0':[-0.5,-0.25], 'Action1ws':[-0.3,0]}
    
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
    
    
if test == 21:
    dir = 'PendulumV0/TotalError-RootMeanSquareError-Floats-WeightedSum-Std/'
    
    lower_limit=0.002
    upper_limit=0.005
    move={'OL0C0ws':[0.25,0]}
    plots = [ {'plot_items': {'CL0C0':'err'}, 'title':'Error'}]
    nevals = 1

if test == 20:
    dir = 'CartPoleV1/TotalError-RootMeanSquareError-AllFloats-SmoothWeightedSum-Std/'
    dir = 'CartPoleV1/TotalError-RootMeanSquareError-Floats-SmoothWeightedSum-Std/'
    dir = 'CartPoleV1/TotalError-RootMeanSquareError-Binary-SmoothWeightedSum-Topp1/'
    dir = 'CartPoleV1/TotalError-RootMeanSquareError-AllFloats-SmoothWeightedSum-Topp1/'

    
    
    lower_limit=0.0
    upper_limit=0.5
    move={'OL0C0sm':[0.25,0]}
    plots = [ {'plot_items': {'CL0C0':'err'}, 'title':'Error'}]


if test == 1:
    dir = 'PendulumV0/InErr-Rms-AllFlts-Sm/'
    lower_limit=0.96
    upper_limit=1.2

if test == 2:
    dir = 'MountainCarV0/Rms-AllFlts-Sm/'
    lower_limit=0.120
    upper_limit=0.160
    
    
if test == 3:
    dir = 'PendulumV0/Reward-Curr/'
    lower_limit=0.1
    upper_limit=0.4
    #move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
    #      'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    #seed=12
    #nevals = 3
    
if test == 4:
    dir = 'PendulumV0/Reward-Curr-Sm/'
    lower_limit=0.1
    upper_limit=0.4
    #move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
    #      'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
   

    
if test == 5:
    dir = 'PendulumV0/Reward-Curr-AllFlts-Sm/'
    lower_limit=0
    upper_limit=0
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    seed=12
    nevals = 3
    
if test == 6:
    dir = 'PendulumV0/Reward-Rms/'
    lower_limit=0
    upper_limit=0.5
    nevals=5
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}

if test == 7:
    dir = 'PendulumV0/Reward-Rms-Sm/'
    lower_limit=0
    upper_limit=6
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}

if test == 8:
    dir = 'PendulumV0/Reward-Rms-AllFlts-Sm/'
    lower_limit=0
    upper_limit=0.5
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    #seed=12
    #nevals = 3


if test == 9:
    dir = 'PendulumV0/Reward-Sme-Sm/'
    lower_limit=0.2
    upper_limit=0.4
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    #move={}
    #seed=60
    #nevals = 1
    plots = [ {'plot_items': {'OL0C0sm':'out','CL0C0':'com'}, 'title':'Output0'},
             {'plot_items': {'OL0C1sm':'out','CL0C1':'com'}, 'title':'Output1'},
             {'plot_items': {'PL0C0ws':'per0','PL0C1ws':'per1'}, 'title':'Percs'},
         {'plot_items': {'IT':'it','IV':'iv'}, 'title':'Inputs'},
         {'plot_items': {'Action1ws':'act'}, 'title':'Action'}]
    
if test == 10:
    dir = 'PendulumV0/Reward-Sme/'
    lower_limit=0.004
    upper_limit=0.01
    seed=85
    nevals = 3
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}


if test == 11:
    dir = 'CartPoleV1/InErr-Rms-Top/'
    lower_limit=0.00
    upper_limit=0.17
    #seed=85
    #nevals = 3
    #move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
    #      'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    move={}


if test == 12:
    dir = 'PendulumV0/InErr-Rms-TopP/'
    lower_limit=0.00
    upper_limit=1.952
    #move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
    #      'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    move={}


if test == 13:
    dir = 'PendulumV0/InErr-Rms-Topp-Sm/'
    lower_limit=0.7
    upper_limit=0.8
    #move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
    #      'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    move={}



if test == 14:
    dir = 'PendulumV0/Reward-Curr-Sm-Topp/'
    lower_limit=0.0
    upper_limit=0.05

if test == 15:
    # look at 0.284
    dir = 'PendulumV0/Reward-Sme-Sm-Topp/'
    lower_limit=0.26
    upper_limit=0.3
    nevals=5
    seed=19
    
    plots = [ 
             {'plot_items': {'IT':'it','IV':'iv'}, 'title':'Inputs'},
             {'plot_items': {'PL1C0ws':'per1','RL1C0c':'ref1'}, 'title':'Goals1'},
             {'plot_items': {'PL0C0ws':'per0','RL0C0ws':'ref0'}, 'title':'Goals0'},
             {'plot_items': {'OL0C0sm':'out','CL0C0':'com'}, 'title':'Output0'},
             {'plot_items': {'Action1ws':'act'}, 'title':'Action'}
             ]

if test == 16:
    dir = 'PendulumV0/Reward-Sme-Topp/'
    lower_limit=0.0
    upper_limit=0.4

if test == 17:
    dir = 'PendulumV0/Reward-Rms-Sm-Topp/'
    lower_limit=5.8
    upper_limit=5.9
    seed=24
    nevals=1
    plots = [ 
             {'plot_items': {'IT':'it','IV':'iv'}, 'title':'Inputs'},
             {'plot_items': {'PL1C0ws':'per1','RL1C0c':'ref1'}, 'title':'Goals1'},
             {'plot_items': {'Action1ws':'act'}, 'title':'Action'}
             ]

if test == 18:
    dir = 'PendulumV0/toterr-rms-bin-sm-topp/'
    lower_limit=0.73
    upper_limit=0.765


if test == 19:
    dir = 'PendulumV0/toterr-sme-bin-sm-topp/'
    lower_limit=0.1
    upper_limit=0.19
    nevals = 1


def get_score(file):
    index1 = file.find('-')
    if file.find('--') > 0:
        index2 = file.find('-', index1+2, len(file)-1)
        score = file[file.find('-')+1: index2]
    else:
        score = file[index1+1: file.find('-', index1+1, len(file)-1)]

    return eval(score)


dir_path=''.join((root_dir, prefix, dir))

for file in os.listdir(dir_path):
    #score = eval(file.split('-')[1])
    if size != None and file.find(size)<0:
        continue
        
    score = get_score(file)
    if score < lower_limit:
        continue
    if score > upper_limit:
        break
    print(file)
    file_path=''.join((prefix, dir))
    
    hpct = run_from_properties_file(root_dir=root_dir, path=file_path, file=file, nevals=nevals, move=move,
            verbose=verbose, summary=summary, draw=True, runs=runs, plots=plots, seed=seed, print_properties=True)
    print()








