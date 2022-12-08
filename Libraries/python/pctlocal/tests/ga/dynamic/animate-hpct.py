#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""


import matplotlib.animation as animation
import matplotlib.pyplot as plt
from pct.architectures import load_properties
from pct.architectures import setup_environment
from pct.architectures import create_hierarchy
from pct.putils import Counter
from pct.putils import get_gdrive
from pct.plotting import SubPlotter
from pct.plotting import run_hpct_animation

window = 30
"""
plotter = SubPlotter(10, 8, "MyData", [
                                      ["Goal1", "t", "y", 2, window, 511, ['RL1C0c', 'PL1C0ws']], 
                                      ["Goal0", "t", "y", 2, window, 512, ['RL0C0ws', 'PL0C0ws']],
                                      ["Outputs", "t", "y", 2, window, 513, ['OL0C0sm', 'OL1C0sm']],
                                      ["Action", "t", "y", 1, window, 514, ['Action1ws']],
                                      ["Reward", "t", "r", 1, window, 515, ['reward']] 
                                      ])
"""
move={}
figsize=(10,10)
draw = True
runs=500
verbose=False

test=5

if test ==1 :

    plotter = SubPlotter(10, 12, "MyData", [
                                          ["Goal1", "t", "y", 2, window, 511, ['RL1C0c', 'PL1C0ws']], 
                                          ["Goal0", "t", "y", 2, window, 512, ['RL0C0ws', 'PL0C0ws']],
                                          ["Outputs", "t", "y", 2, window, 513, ['OL1C0sm', 'OL0C0sm']],
                                          ["Action", "t", "y", 1, window, 514, ['Action1ws']] 
                                          ])

    path = 'data/ga/PendulumV0/Topp2-TopError-RootMeanSquareError-AllFloats-SmoothWeightedSum'   
    file = 'ga-001.334-s010-2x1.properties'


if test ==2 :
    plotter = SubPlotter(10, 12, "MyData", [
                                          ["Goal00", "t", "y", 2, window, 421, ['RL0C0ws', 'PL0C0ws']],
                                          ["Goal01", "t", "y", 2, window, 422, ['RL0C1ws', 'PL0C1ws']],
                                          ["Goal1", "t", "y", 2, window, 412, ['RL1C0c', 'PL1C0ws']], 
                                          ["Outputs", "t", "y", 2, window, 413, ['OL1C0sm', 'OL0C0sm']],
                                          ["Action", "t", "y", 1, window, 414, ['Action1ws']] 
                                          ])

    path = 'data/ga/PendulumV0_1/Topp3-TopError-SmoothError-AllFloats-SmoothWeightedSum'   
    file = 'ga-000.000-s038-2x2-6655.properties'



if test ==3 :
    plotter = SubPlotter(10, 10, "MyData", [
                                          ["Goal1", "t", "y", 2, window, 411, ['RL1C0c', 'PL1C0ws']], 
                                          ["Goal0", "t", "y", 2, window, 412, ['RL0C0ws', 'PL0C0ws']],
                                          ["Outputs", "t", "y", 2, window, 413, ['OL1C0sm', 'OL0C0sm']],
                                          ["Action", "t", "y", 1, window, 414, ['Action1ws']] 
                                          ])

    path = 'data/ga/PendulumV0/Topp2-TopError-RootMeanSquareError-Binary-SmoothWeightedSum'   
    file = 'ga-001.322-s056-2x1-6655.properties'

    move={'IV':[-0.05,0.3],'IT':[0.1,0.3],'OL1C0sm':[0.0,-0.2],'OL0C0sm':[0.0,-0.2],
          'PendulumV0':[-0.3,-0.25], 'Action1ws':[-0.5,-0.2]}

    draw = False#True
    figsize=(10,10)



if test == 4 :
    window = 100
    file = 'ga-002.436-s006-2x2-6655.properties'
    plotter = SubPlotter(10, 10, file, [
        ["Goal1", "t", "y", 2, window, 421, ['RL1C0c', 'PL1C0ws']], 
        ["Goal0", "t", "y", 2, window, 422, ['RL0C0ws', 'PL0C0ws']],
        ["Outputs", "t", "y", 2, window, 412, ['OL1C0sm', 'OL0C0sm']],
        ["Action", "t", "y", 1, window, 413, ['Action1ws']] ,
        ["Reward", "t", "r", 1, window, 414, ['reward']] 
        ])

    path = 'data/ga/PendulumV0_1/Topp5-TotalError-RootMeanSquareError-Binary-SmoothWeightedSum'   
    draw = False
    move={'IV':[-0.05,0.4],'IT':[0.1,0.3],'OL0C0sm':[0,-0.1], 'PendulumV0_1':[-.4,-0.25], 'Action1ws':[-0.425,-0.1]}
    runs=1000



if test == 5 :
    window = 100
    file = 'ga-000.749-s001-3x3-6655-04c3b2898d85049f8c26f644f8eda182.properties'
    """
    plotter = SubPlotter(10, 10, file, [
        ["Goal1", "t", "y", 2, window, 421, ['RL1C0c', 'PL1C0ws']], 
        ["Goal0", "t", "y", 2, window, 422, ['RL0C0ws', 'PL0C0ws']],
        ["Outputs", "t", "y", 2, window, 412, ['OL1C0sm', 'OL0C0sm']],
        ["Action", "t", "y", 1, window, 413, ['Action1ws']] ,
        ["Reward", "t", "r", 1, window, 414, ['reward']] 
        ])
    """
    
    plotter = SubPlotter(10, 10, file, [
        ["Reward", "t", "r", 1, window, 111, ['reward']] 
        ])
    path = 'data/ga/MountainCarContinuousV0/Topp1-ReferencedInputsError-RootMeanSquareError-Binary-SmoothWeightedSum'   
    draw = True
    move={'IV':[-0.05,0.4],'IT':[0.1,0.3],'OL0C0sm':[0,-0.1], 'PendulumV0_1':[-.4,-0.25], 'Action1ws':[-0.425,-0.1]}
    move={}
    verbose=True
    runs=500



render = True

root_dir=get_gdrive()
properties = load_properties(root_dir, path, file, print_properties=True)    
env, error_collector = setup_environment(properties, render=render)
hpct = create_hierarchy(env, error_collector, properties, history=True, suffixes=True)

#move={}
   


if draw :
    hpct.draw(move=move, figsize=figsize, with_edge_labels=True, node_size=300, font_size=8)

#hpct.summary()

counter = Counter(runs,  display=1000, pause=True)
    
run_hpct_animation(hpct, counter=counter, plotter=plotter, verbose=verbose)
plt.show()








