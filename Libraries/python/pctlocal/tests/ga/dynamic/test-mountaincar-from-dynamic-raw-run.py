# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""


from pct.environments import MountainCarContinuousV0

from pct.architectures import LevelKey
from pct.architectures import DynamicArchitecture
from pct.structure import ArchitectureStructure


verbose=False
seed=None
render=True#False#True

runs=500

inputs =  [0, 1]
references =  [0.45]
top_inputs =  [0]
error_collector_type = 'ReferencedInputsError'
error_response_type = 'RootMeanSquareError'
error_properties = [['referenced_inputs','0&0.45']]
error_limit = 10
inputs_names = ['IP', 'IV']
loops = 1
early_termination=True

env = MountainCarContinuousV0(name='MountainCarContinuousV0', render=render, early_termination=early_termination)


config_test=20

move={'MountainCarContinuousV0': [-0.6, -0.5], 'Action1ws': [-0.4, -0.4], 
      'OL0C0sm': [-0.55, -0.2], 'OL0C1sm': [0, -0.2], 'OL0C2sm': [0.55, -0.2], 
      'OL1C0sm': [0, -0.1], 'IV': [-0.8, 0.05], 'IP': [-1.1, 0.5], 'CL1C0': [0, 0.1]}
move={'MountainCarContinuousV0': [-0.6, -0.5], 'Action1ws': [-0.4, -0.4], 
      'OL0C0sm': [-0.28, -0.25], 'OL0C1sm': [0.28, -0.25],  
      'OL1C0sm': [0, -0.1], 'IV': [-0.1, 0.0], 'IP': [-0.6, 0.5], 'CL1C0': [0, 0.1]}

arch_structure = None


modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
arch_structure = ArchitectureStructure(modes=modes)
plot=False


if config_test==20: 
    #runs = 1
    seed = 66
    loops = 6
    #raw =  [[[[1.198998468541923, 0.611754204266719, 1.7677170617308327]], [[3.4341117624938446, 0.9640180391471003], [-0.05887913748075457, 0.9825724309247841], [2.573053595563823, 0.38627004681749383]], [[1.137932637787607], [2.1164923802567945], [3.232824945210956]], [[3.0946849052258356, 3.1217341494218322, -0.45836455321778186]]], [[[0.5030156034214709]], [[3.9129702537620084, 0.4591226113143575]], [0.45]]]
    raw =  [[[[1.198998468541923, 1.7677170617308327]], [[3.4341117624938446, 0.9640180391471003],  [2.573053595563823, 0.38627004681749383]], [[1.137932637787607],  [3.232824945210956]], [[3.0946849052258356,  -0.45836455321778186]]], [[[1.0]], [[3.9129702537620084, 0.4591226113143575]], [0.45]]]
    

    plot=False
    plots=[]
    plots = [
        {'plot_items': {'IP':'ip', 'IV':'iv'},'title':'Inputs'},
        {'plot_items': {'OL0C1sm':'out1'}, 'title':'Output1'},
        {'plot_items': {'OL0C0sm':'out0', 'OL0C2sm':'out2'}, 'title':'Output'},
        {'plot_items': {'Action1ws':'act'}, 'title':'Action'}
        ]
    plots = [
        {'plot_items': {'IP':'ip', 'IV':'iv'},'title':'Inputs'},
        {'plot_items': {'RL1C0c':'ref0', 'PL1C0ws':'per0'}, 'title':'L1'},
        {'plot_items': {'RL0C0ws':'ref0', 'PL0C0ws':'per0'}, 'title':'C0'},
        {'plot_items': {'RL0C1ws':'ref0', 'PL0C1ws':'per0'}, 'title':'C1'},
        {'plot_items': {'CL0C0':'err00', 'CL0C1':'err01', 'CL1C0':'err1'}, 'title':'Error'},
        {'plot_items': {'OL0C0sm':'out0', 'OL0C1sm':'out1'}, 'title':'Outputs'},
        {'plot_items': {'Action1ws':'act'}, 'title':'Action'}
        ]
    
    

history=True

for seedn in range(seed, loops+seed, 1):
    score, last, hpct = DynamicArchitecture.run_raw(raw=raw, arch_structure=arch_structure, move=move, 
                env=env, runs=runs, inputs=inputs, error_properties=error_properties, inputs_names=inputs_names, 
                summary=False, verbose=verbose, seed=seedn, history=history, top_input_indexes=top_inputs,
                error_collector_type=error_collector_type, error_response_type=error_response_type, 
                draw=True, suffixes=True, error_limit =error_limit )
    
    print(f'seed {seedn} score {score:5.3f} last step {last}')

    #hpct.summary()
    if plot:
        for plot_item in plots:
            fig = hpct.hierarchy_plots(title=plot_item['title'], plot_items=plot_item['plot_items'])
            
        """
        plot_items = {'IT':'it', 'IV':'iv'}
        fig = hpct.hierarchy_plots(title='Inputs', plot_items=plot_items)
        
        plot_items = {'RL0C0c':'ref0', 'PL0C0ws': 'per0', 'IT':'it'}    
        fig = hpct.hierarchy_plots(title='Node0', plot_items=plot_items)
        
        plot_items = {'RL0C1c':'ref1', 'PL0C1ws': 'per1', 'IV':'iv'}    
        fig = hpct.hierarchy_plots(title='Node1', plot_items=plot_items)
        #print(hd['OL0C0ws'])
        """

env.close()

    

