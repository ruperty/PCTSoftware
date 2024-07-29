# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""


# python examples/generate-arc.py > configs/ar/test-cmds.txt


from os import sep

from eepct.hpct import HPCTGenerateEvolvers

test = 'simple'

args = "-i 1 -s 93"
cmd='impl.evolve'
initial_index=1
# initial_index=1
batch = 10

if test == 'dims_only':

    filename = 'ar' + sep +'configs-dims-only.csv'
    args = "-b -pl scEdges,scZero -p dims-only -o"
    num_evals = 1
    pop_size =  100
    gens = 25
    evolve_termination_value = 0
    properties = { 'code':'007bbfb7',  'dataset': 'train', 'control_set': ['dims'], 'input_set': ['env']}
    common_configs = {'env' : 'ARC', 'seed': 1, 'arch_name' : 'ARC', 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
                    'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 100, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 
                    'max_levels_limit': 2, 'min_columns_limit': 1, 'max_columns_limit': 2, 'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': 10000, 'environment_properties': properties}

if test == 'simple':

    initial_index=20
    filename = 'ar' + sep +'configs-simple.csv'
    args = "-b -pl scEdges,scZero -p simple -o"
    num_evals = 1
    pop_size =  100
    gens = 25
    evolve_termination_value = 0
    properties = { 'dir': 'C:/Users/ryoung/Versioning/python/nbdev/epct/nbs/testfiles/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000001',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env']}
    common_configs = {'env' : 'ARC', 'seed': 1, 'arch_name' : 'ARC', 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
                    'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 100, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 
                    'max_levels_limit': 2, 'min_columns_limit': 1, 'max_columns_limit': 2, 'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': 10000, 'environment_properties': properties}


file = 'configs'+ sep + filename

hge = HPCTGenerateEvolvers(common_configs=common_configs)  
hge.process_csv(file, args, cmdline=cmd, initial_index=initial_index, batch=batch)
