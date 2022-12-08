# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 20:20:48 2021

@author: ryoung
"""

from epct.properties import generate_evolvers

# removed RootSumSquaredError
# reomved Floats

envs = ['CartPoleV1', 'PendulumV0']
varieties ={'CartPoleV1': {'num_actions': 1, 'nevals':1, 
                           'options':[
                               {'name': 'Std', 'inputs':[1,0,3,2], 'references':[0],'inputs_names': '[ICV, ICP, IPV, IPA]'},
                               {'name': 'Topp1', 'inputs':[1,0,3,2], 'top_inputs':[2], 'references':[0],'inputs_names': '[ICV, ICP, IPV, IPA]'} ]},
            'PendulumV0': {'num_actions': 1, 'nevals':5,
                           'archs':[
                               {'name': 'Std', 'inputs':[2,3], 'references':[0,0], 'inputs_names': '[IV, IT]'},
                               #{'name': 'Topp1', 'inputs':[2,3], 'top_inputs':[3], 'references':[0], 'inputs_names': '[IV, IT]'} ,
                               #{'name': 'Topp2', 'inputs':[2,4], 'top_inputs':[4], 'references':[10], 'inputs_names': '[IV, IT]'} 
                               ]},
            'PendulumV0_1': {'num_actions': 1, 'nevals':5,
                           'archs':[
                               #{'name': 'Std', 'inputs':[3,4], 'references':[0,1], 'inputs_names': '[IV, IT]'},
                               #{'name': 'Topp3', 'inputs':[3,4], 'top_inputs':[4], 'references':[1], 'inputs_names': '[IV, IT]'} ,
                               #{'name': 'Topp4', 'inputs':[3,4], 'top_inputs':[4], 'references':[10], 'inputs_names': '[IV, IT]'} 
                               {'name': 'Topp5', 'inputs':[3,4], 'top_inputs':[4], 'references':[100], 'inputs_names': '[IV, IT]'} 
                               ]},
            'MountainCarContinuousV0': {'num_actions': 1, 'nevals':5,
                           'archs':[
                               {'name': 'Topp1', 'inputs':[0,1], 'top_inputs':[0], 'references':[0.45], 'inputs_names': '[IP, IV]'}
                               ]}
            }

collection = {'PendulumV0': { 'arch': {
                                'Std' : {'collectors': ['InputsError', 'RewardError'],
                                'responses': ['RootMeanSquareError' ],
                                'weights' : ['AllFloats', 'Binary'],
                                'structs' : ['SmoothWeightedSum']}
                                ,
                                'Topp1' : {'collectors': ['TopError', 'RewardError'],
                                'responses': ['RootMeanSquareError', 'SmoothError'],
                                'weights' : ['Binary','AllFloats'],
                                'structs' : ['WeightedSum','SmoothWeightedSum']}
                                ,
                                'Topp2' : {'collectors': ['TopError', 'RewardError'],
                                'responses': ['RootMeanSquareError', 'SmoothError'],
                                'weights' : ['Binary','AllFloats'],
                                'structs' : ['SmoothWeightedSum']}
                                }
                            },
            'PendulumV0_1': { 'arch': {
                                'Std' : {'collectors': ['TotalError'],
                                'responses': ['RootMeanSquareError'],
                                'weights' : ['Binary','AllFloats'],
                                'structs' : ['SmoothWeightedSum']}
                                ,
                                'Topp3' : {'collectors': ['TotalError', 'TopError', 'RewardError'],
                                'responses': ['RootMeanSquareError', 'SmoothError'],
                                'weights' : ['Binary','AllFloats'],
                                'structs' : ['SmoothWeightedSum']}
                                ,
                                'Topp4' : {'collectors': ['TotalError'],
                                'responses': ['RootMeanSquareError', 'SmoothError'],
                                'weights' : ['Binary','AllFloats'],
                                'structs' : ['SmoothWeightedSum']}
                                ,
                                'Topp5' : {'collectors': ['RewardError', 'TotalError', 'ReferencedInputsError'],
                                'responses': ['RootMeanSquareError', 'SmoothError'],
                                'weights' : ['Binary','AllFloats'],
                                'structs' : ['SmoothWeightedSum']}
                                }
                            },
            'MountainCarContinuousV0': { 'arch': {
                                'Topp1' : {'collectors': ['ReferencedInputsError', 'TopError', 'RewardError' ],
                                'responses': ['RootMeanSquareError', 'SmoothError', 'CurrentError'],
                                'weights' : ['Binary','AllFloats'],
                                'structs' : ['SmoothWeightedSum']}
                                }
                            }
             }

#collectors = ['TotalError', 'InputsError', 'TopError', 'RewardError']
#responses = ['RootMeanSquareError', 'CurrentError','SmoothError','RootSumSquaredError']
#weights = ['Binary','Floats','AllFloats']
#structs = ['WeightedSum','SmoothWeightedSum']

#properties = {'error:smooth_factor':0.9, 'error:referenced_inputs' : '0;1&0;100'}
properties = {'error:smooth_factor':0.9, 'error:referenced_inputs' : '0&0.45'}


configs = { 
          'PendulumV0_Std': {'seed': 1,'POPULATION_SIZE': 100,'MAX_GENERATIONS': 10,'attr_mut_pb':1,'structurepb':0.75,'runs':500, 
          'lower_float': -10,'upper_float': 10,'levels_limit': 5,'columns_limit': 8,
          'min_levels_limit': 1,'min_columns_limit': 1, 'error_limit': 100,'p_crossover': 0.9,'p_mutation': 0.5}
          ,
          'PendulumV0_1_Topp5': {'seed': 1,'POPULATION_SIZE': 1000,'MAX_GENERATIONS': 20,'attr_mut_pb':1,'structurepb':0.75,'runs':500, 
          'lower_float': -100,'upper_float': 100,'levels_limit': 2,'columns_limit': 1,
          'min_levels_limit': 2,'min_columns_limit': 1, 'error_limit': 1000,'p_crossover': 0.9,'p_mutation': 0.5}
          ,
          'MountainCarContinuousV0_Topp1': {'seed': 1,'POPULATION_SIZE': 100,'MAX_GENERATIONS': 10,'attr_mut_pb':1,'structurepb':0.75,'runs':500, 
          'lower_float': -1,'upper_float': 1,'levels_limit': 3,'columns_limit': 3, 'early_termination': True,
          'min_levels_limit': 2,'min_columns_limit': 1, 'error_limit': 10,'p_crossover': 0.9,'p_mutation': 0.5}           
          }


#envs = ['PendulumV0']
#envs = ['PendulumV0_1']

envs = ['MountainCarContinuousV0']

#collectors = ['InputsError']
#responses = ['SmoothError']
#weights = ['AllFloats']
#structs = ['SmoothWeightedSum']

            
            
iters = 100
generate_evolvers(iters, envs=envs, collection=collection, configs=configs, properties=properties, varieties=varieties)

# python run-dynamic-evolver-multi.py PendulumV0/InputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum-Topp1.properties -i 100      
            
             
           
                                  
    
                                                                   