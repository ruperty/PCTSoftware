# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:23:58 2020

@author: rupert
"""


from pct.environments import PendulumV0

from pct.architectures import LevelKey
from pct.architectures import DynamicArchitecture
from pct.structure import ArchitectureStructure


verbose=False
seed=None
render=True#False#True

runs=500
inputs=[2,3]
error_collector_type ='InputsError'
error_response_type = 'RootMeanSquareError'
inputs_names=['IV', 'IT']
loops = 1

env = PendulumV0(name='PendulumV0', render=render, early_termination=False)


config_test=23

move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}

if config_test==1: 
    raw=[[[[9.477514382636144, 2.278686427103339], [1.9658023343231577, -0.32840366520171715]], [8.495722620222262, 5.4191839146355605], [0, 0], [[1, 0]]]]
    

if config_test==2: 
    raw = [[[[-5.909649528826087, -4.67381334002868], [-6.984489989401268, -3.0953766317133224]], [-1.2600169671254136, 0.5354891039492525], [0, 0], [[1, 0]]]]


if config_test==3: 
    raw = [[[[-2.744243249061846, -2.993052230211862], [2.6417690964379723, -5.993040691149572]], [1.18277335831221, -2.0844325534664456], [0, 0], [[0, 1]]]]


# InErr-Rms-Flts ga-000.809-s009-1x2-3344-7111951246514006343.properties
# suceeds if has momentum e.g. seeds 12, 19, 20
if config_test==4: 
    runs=500
    loops = 3
    seed = 18
    raw = [[[[1.3934327893200846, -3.5906852558471747], [3.6762210434477036, 8.482459777049534]], 
            [7.136806050884725, -9.046649865675267], [0, 0], [[1, 0]]]]

# removed one node for above
if config_test==5: 
    runs=500
    loops = 1
    seed = 12
    raw = [[[[1.3934327893200846], [3.6762210434477036]], [7.136806050884725], [0], [[1]]]]
    move={'IV':[-0.5,0.5],'IT':[0.55,0.5],          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}

# Default ga-004.694-s027-1x2-3344--6233767676388718113.properties
# keeps velocity at zero though pointing down
if config_test==6: 
    error_collector_type ='TotalError'
    error_response_type = 'RootSumSquaredError'
    seed = 27
    loops = 3
    raw = [[[[0, 1], [0, 0]], [-7.490082048936612, 5.873140253310572], [0, 0], [[0, 1]]]]


# InErr-Rms ga-000.793-s057-1x2-3344--1603152508696519723.properties
# suceeds if has momentum
if config_test==7: 
    seed = 57
    loops = 5
    raw = [[[[0, 1], [1, 1]], [9.494146275141079, 5.456583533202007], [0, 0], [[1, 1]]]]

# InErr-Rms-Alo ga-000.793-s057-1x2-3344-2972144816251611205.properties
# same as previous
if config_test==8: 
    seed = 57
    loops = 3
    raw = [[[[0, 1], [1, 1]], [9.494146275141079, 5.456583533202007], [0, 0], [[1, 1]]]]


if config_test==9: 
    seed = 12
    loops = 1
    raw = [[[[-13.170852779030238, 3.6586390171612475], [-2.9676382065231435, -3.4162186913680825]], [-6.967143801073124, 0.06548777212716497], [0, 0], [[5.232075295832819, 7.965520639105748]]]]


# InErr-Rms-AllFlts ga-000.270-s009-1x2-3344--6832704055390970200.properties
# works well for 9, 10, 11
# 12 is best
if config_test==10: 
    seed = 12
    loops = 1
    raw = [[[[1.0864011617580416, -1.0342161642584196], [-8.899524671308557, -8.976856229389936]], [-0.7295091920311653, -4.460573287694404], [0, 0], [[-4.146713118740296, 1.2794655139677662]]]]


arch_structure = None

if config_test>=20: 
    modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
    arch_structure = ArchitectureStructure(modes=modes)
    plot=False


# Rms-AllFlts-Sm-Three ga-000.311-s002-1x3-6655-7462452875783963726.properties
# Interestingly with the wrong inputs, error and reference 
# this continuously swings around
if config_test==20: 
    runs = 1
    move={'IV':[-0.95,0.75],'IT':[-0.15,0.6],'OL0C0sm':[-0.7,0],'OL0C2sm':[0.7,0],
          'PendulumV0':[-.75,0.3], 'Action1ws':[-0.5,0.2]}
    seed = 12
    loops = 1
    raw = [[[[-1.368260426322016, 0.1724264458685155, 0.08722530221997006], 
             [-0.3850286648119032, 0.26428958833832633, -0.11102962444023638], 
             [-0.17683951643121804, -0.2411264943076289, -0.9543451344795024]], 
            [[-6.034270774706741, 0.12543906678849756], [5.765429132709796, 0.40779876723996744], [-10.058876939288458, 0.3599319704005053]], 
            [1, 0, 0], [[-2.5216109946841394, -0.7584677596234357, 8.177208949292822]]]]
    

# Rms-AllFlts-Sm-Three ga-000.311-s002-1x3-6655-7462452875783963726.properties
if config_test==21: 
    #runs = 1
    inputs=[0,1,2]
    error_collector_type ='TotalError'
    error_response_type = 'RootMeanSquareError'
    inputs_names=['ICT', 'IST', 'IV']
    
    move={'ICT':[-0.95,0.8],'IST':[-0.4,0.7],'IV':[0.15,0.6],'OL0C0sm':[-0.7,0],'OL0C2sm':[0.7,0],
          'PendulumV0':[-1.5,0.3], 'Action1ws':[-0.5,0.2]}

    seed = 2
    loops = 1
    raw = [[[[-1.368260426322016, 0.1724264458685155, 0.08722530221997006], [-0.3850286648119032, 0.26428958833832633, -0.11102962444023638], [-0.17683951643121804, -0.2411264943076289, -0.9543451344795024]], [[-6.034270774706741, 0.12543906678849756], [5.765429132709796, 0.40779876723996744], [-10.058876939288458, 0.3599319704005053]], [1, 0, 0], [[-2.5216109946841394, -0.7584677596234357, 8.177208949292822]]]]

# Rms-AllFlts-Sm-Three ga-000.311-s002-1x3-6655-7462452875783963726.properties
if config_test==22: 
    #runs = 1
    inputs=[0,1,2]
    error_collector_type ='TotalError'
    error_response_type = 'RootMeanSquareError'
    inputs_names=['ICT', 'IST', 'IV']
    
    move={'ICT':[-0.95,0.8],'IST':[-0.4,0.7],'IV':[0.15,0.6],'OL0C0sm':[-0.7,0],'OL0C2sm':[0.7,0],
          'PendulumV0':[-1.5,0.3], 'Action1ws':[-0.5,0.2]}
    seed=57
    loops = 1
    raw = [[[[-2.0568957279349243, 0.7935910239595161, -0.8283745733765602], [3.0526595551630784, -2.3467060571703375, 1.8922026544895072], [-0.9144229383235083, 0.6600287951771658, 0.5454123311580075]], [[-13.617436564586423, 0.8589923276759401], [-5.046423193076034, 0.7522068394952924], [-0.3666086406681157, 0.8332770664160627]], [1, 0, 0], [[9.968277028488513, -0.1790587783619302, 6.776571864045582]]]]


# InErr-Rms-AllFlts-Sm-Theta ga-000.523-s057-1x1-6655--7487932617301201865.properties
if config_test==23: 
    #runs = 1
    inputs=[3]
    error_collector_type ='TotalError'
    error_response_type = 'RootMeanSquareError'
    inputs_names=['IT']
    
    #move={'ICT':[-0.95,0.8],'IST':[-0.4,0.7],'IV':[0.15,0.6],'OL0C0sm':[-0.7,0],'OL0C2sm':[0.7,0],
    #      'PendulumV0':[-1.5,0.3], 'Action1ws':[-0.5,0.2]}
    move={}

    seed = 58
    loops = 1
    #raw = [[[[1.9103802256306466]], [[12.435438353702377, 0.9982937371425193]], [0], [[8.015508203461325]]]]
    raw = [[[[1.9103802256306466]], [[12.435438353702377, 0.0017]], [0], [[8.015508203461325]]]]
    #raw = [[[[1.9103802256306466]], [[12.435, 0.998]], [0], [[8]]]]
    plot=True
    plots = [{'plot_items': {'IT':'it'}, 'title':'Inputs'},
             {'plot_items': {'RL0C0c':'ref0', 'PL0C0ws': 'per0'}, 'title':'Node'},
             {'plot_items': {'OL0C0sm':'out'}, 'title':'Output'}]
    
    

history=True

for seedn in range(seed, loops+seed, 1):
    score, last, hpct = DynamicArchitecture.run_raw(raw=raw, arch_structure=arch_structure, move=move, env=env, runs=runs, inputs=inputs, 
                inputs_names=inputs_names, summary=False, verbose=verbose, seed=seedn, history=history,
                error_collector_type=error_collector_type, error_response_type=error_response_type, draw=True, suffixes=True)
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

    

