# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 20:20:48 2021

@author: ryoung
"""

from eepct.hpct import HPCTGenerateEvolvers


from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTVARIABLE

from pct.functions import HPCTFUNCTION

# removed RootSumSquaredError
# reomved Floats


varieties ={'CartPoleV1': {'num_actions': 1, 'nevals':1, 
                           'archs':[
                               {'name': 'Std00', 'env_inputs_indexes':[1,0,3,2], 'references':[0],'env_inputs_names': '[ICV, ICP, IPV, IPA]'},
                               {'name': 'Std01', 'env_inputs_indexes':[1,0,3,2], 'references':[0],'env_inputs_names': '[ICV, ICP, IPV, IPA]'},
                               {'name': 'Std02', 'env_inputs_indexes':[1,0,3,2], 'references':[0],'env_inputs_names': '[ICV, ICP, IPV, IPA]'}
                            #    ,
                            #    {'name': 'Topp1', 'inputs':[1,0,3,2], 'top_inputs':[2], 'references':[0],'inputs_names': '[ICV, ICP, IPV, IPA]'} 
                            ]}
                            ,
            'WebotsWrestler': {'num_actions': 6, 'nevals':1,
                           'archs':[
                               {'name': 'WW01-01', 'env_inputs_indexes':[0,1,2,3,4,5], 'references':[0], 'env_inputs_names': '[ LHipPitch, LKneePitch, LAnklePitch, RHipPitch, RKneePitch, RAnklePitch]'},
                               {'name': 'WW01-02', 'env_inputs_indexes':[0,1,2,3,4,5], 'references':[0.5], 'env_inputs_names': '[ LHipPitch, LKneePitch, LAnklePitch, RHipPitch, RKneePitch, RAnklePitch]'}                               
                               ]}
                            ,
            'MountainCarContinuousV0': {'num_actions': 1, 'nevals':5,
                           'archs':[
                               {'name': 'Topp1', 'env_inputs_indexes':[0,1], 'top_inputs':[0], 'references':[0.45], 'env_inputs_names': '[IP, IV]'}
                               ]}
            }

collection = {
            'CartPoleV1': { 'arch': {
                                    'Std00' : {'collectors': ['InputsError' , 'TotalError'],
                                    'responses': ['RootMeanSquareError'],
                                    'structs' : [{'mode': 0, 'types':[] }, 
                                                 {'mode': 1, 'types':[] }, {'mode': 2, 'types':[] }, {'mode': 3, 'types':[] }]
                                    },
                                    # 'structs' : [{'mode': 0, 'types':[[HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.TYPE, 'Float'], 
                                    #                                   [HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.FUNCTION_CLASS, 'EAVariable'], 
                                    #                                   [HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, { 'lower': -1,'upper': 1}],
                                    #                                   [HPCTLEVEL.TOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.TYPE, 'Float'], 
                                    #                                   [HPCTLEVEL.TOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.FUNCTION_CLASS, 'EAVariable'],
                                    #                                   [HPCTLEVEL.TOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, { 'lower': -1,'upper': 1}]] }, 
                                    #              {'mode': 1, 'types':[] }, {'mode': 2, 'types':[] }, {'mode': 3, 'types':[] }]
                                    # },
                                    'Std01' : {'collectors': ['InputsError' , 'TotalError'],
                                    'responses': ['RootMeanSquareError'],
                                    'structs' : [{'mode': 0, 'types':[] }, {'mode': 1, 'types':[] }, {'mode': 2, 'types':[] }, {'mode': 3, 'types':[] }]
                                    },
                                    'Std02' : {'collectors': ['InputsError' , 'TotalError'],
                                    'responses': ['RootMeanSquareError'],
                                    'structs' : [{'mode': 0, 'types':[[HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary'], 
                                                    [HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary']] }, 
                                                 {'mode': 1, 'types':[[HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary'], 
                                                    [HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary']] }                                                 
                                                ]
                                    }
                                }
                        }
                            ,
            'WebotsWrestler': { 'arch': {
                                    'WW01-01' : {'collectors': ['RewardError' ],
                                    'responses': ['CurrentError'],
                                    'structs' : [{'mode': 1, 
                                                'types':[[HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.TYPE, 'Float'], 
                                                                        [HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.FUNCTION_CLASS, 'EAVariable'], 
                                                                        [HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, { 'lower': -1,'upper': 1}],
                                                                        [HPCTLEVEL.TOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.TYPE, 'Float'], 
                                                                        [HPCTLEVEL.TOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.FUNCTION_CLASS, 'EAVariable'],
                                                                        [HPCTLEVEL.TOP, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, { 'lower': -1,'upper': 1}]]
                                                }]}
                                    ,
                                    'WW01-02' : {'collectors': ['RewardError' ],
                                    'responses': ['CurrentError'],
                                    'structs' : [{'mode': 1, 'types':[]  }]}
                                    }

                            }
                            ,
            'MountainCarContinuousV0': { 'arch': {
                                'Topp1' : {'collectors': ['ReferencedInputsError', 'TopError', 'RewardError' ],
                                'responses': ['RootMeanSquareError', 'SmoothError', 'CurrentError'],
                                'structs' : [{'mode': 0, 'types':[]}]}
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
          'CartPoleV1_Std00': {'seed': 1,'pop_size': 100,'gens': 10,'attr_mut_pb':0.8,'structurepb':1,'runs':500, 
          'lower_float': -1,'upper_float': 1,'max_levels_limit': 5,'max_columns_limit': 5, 'early_termination': True,
          'min_levels_limit': 1,'min_columns_limit': 1, 'error_limit': 100,'p_crossover': 0.8,'p_mutation': 0.5}
          ,
          'CartPoleV1_Std01': {'seed': 1,'pop_size': 100,'gens': 10,'attr_mut_pb':0.8,'structurepb':1,'runs':500, 
          'lower_float': -1,'upper_float': 1,'max_levels_limit': 1,'max_columns_limit': 1, 'early_termination': True,
          'min_levels_limit': 1,'min_columns_limit': 1, 'error_limit': 100,'p_crossover': 0.8,'p_mutation': 0.5}
          ,
          'CartPoleV1_Std02': {'seed': 1,'pop_size': 100,'gens': 10,'attr_mut_pb':0.8,'structurepb':1,'runs':500, 
          'lower_float': -1,'upper_float': 1,'max_levels_limit': 1,'max_columns_limit': 1, 'early_termination': True,
          'min_levels_limit': 1,'min_columns_limit': 1, 'error_limit': 100,'p_crossover': 0.8,'p_mutation': 0.5}
          ,
          'WebotsWrestler_WW01-01': {'seed': 1,'pop_size': 100,'gens': 25,'attr_mut_pb':1,'structurepb':1,'runs':1000000, 
          'lower_float': -1,'upper_float': 1,'max_levels_limit': 10,'max_columns_limit': 10, 'early_termination': True,
          'min_levels_limit': 2,'min_columns_limit': 2, 'error_limit': 100,'p_crossover': 0.9,'p_mutation': 0.5}           
          ,
          'WebotsWrestler_WW01-02': {'seed': 1,'pop_size': 1000,'gens': 10,'attr_mut_pb':1,'structurepb':1,'runs':1000000, 
          'lower_float': -1,'upper_float': 1,'max_levels_limit': 10,'max_columns_limit': 10, 'early_termination': True,
          'min_levels_limit': 2,'min_columns_limit': 2, 'error_limit': 100,'p_crossover': 0.9,'p_mutation': 0.75}           
          ,
          'MountainCarContinuousV0_Topp1': 
          {'seed': 1,'pop_size': 100,'gens': 10,'attr_mut_pb':1,'structurepb':0.75,'runs':500, 
          'lower_float': -1,'upper_float': 1,'max_levels_limit': 3,'max_columns_limit': 3, 'early_termination': True,
          'min_levels_limit': 2,'min_columns_limit': 1, 'error_limit': 10,'p_crossover': 0.9,'p_mutation': 0.5}           
          }


envs = ['CartPoleV1', 'MountainCarContinuousV0']
envs = ['CartPoleV1']
envs = ['WebotsWrestler']


            
            
iters = 100


if __name__ == "__main__":


    hge = HPCTGenerateEvolvers(iters, envs=envs, collection=collection, configs=configs, properties=properties, varieties=varieties)

# python run-dynamic-evolver-multi.py PendulumV0/InputsError-RootMeanSquareError-AllFloats-SmoothWeightedSum-Topp1.properties -i 100      
            
             
           
                                  
    
                                                                   