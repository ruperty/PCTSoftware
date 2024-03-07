# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

import os

from eepct.hpct import HPCTGenerateEvolvers

# test = 'WindTurbine'
test = 'MicroGrid'


args = "-i 1 -s 93"
cmd='impl.evolve_multi'
initial_index=1
batch = 20

if test == 1:
    file = 'configs'+ os.sep + 'configs-cp.csv'

if test == 2:
    file = 'configs'+ os.sep + 'configs-mc.csv'

if test == 3:
    file = 'configs'+ os.sep + 'configs-ww.csv'

if test == 4:
    file = 'configs'+ os.sep + 'configs-pm.csv'

if test == 'WindTurbine':
    test = 4
    batch = 20

    cmd='impl.evolve_multi_wt'
    common_configs = {'env' : 'WindTurbine', 'num_actions' : 1, 'seed': 1, 'arch_name' : 'WT', 'pop_size' : 100, 'gens': 10, 
                    'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 1000, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 2, 
                    'max_levels_limit': 5, 'min_columns_limit': 2, 'max_columns_limit': 5, 'early_termination': False, 'p_crossover': 0.9, 
                    'p_mutation': 0.75, 'num_evals': 1}

    if test == 1:
        filename = 'configs-wt-0001-0616-steady.csv'
        args = "-b -l -o -pl scEdges -p evolve-batch -c 6 -s 1 -i 3"
        # args = "-b -l -o -pl scEdges -p evolve" 

    if test == 2:
        filename = 'configs-wt-1000-1083-steady-w2test.csv'       
        initial_index=2000
        args = "-b -l -o -pl scEdges -p test-evolve -c 3 -s 1 -i 3"

    if test == 3:

        filename = 'configs-wt-0001-0616-variable.csv'       
        # args = "-b -l -o -pl scEdges -p test-evolve -c 8 -s 1 -i 3"
        # args = "-b -l -o -pl scEdges -p test-evolve -c 8 -s 1 -i 3"
        # args = "-b -l -o -pl scEdges -p evolve-batch -c 8 -s 1 -i 3"
        # args = "-b -l -o -pl scEdges -p evolve" 

    if test == 4:
        # common_configs['pop_size'] = 1000
        # common_configs['gens'] = 2
        # filename = 'configs-wt-2000-mode04-scActBinSig-variable.csv'       
        filename = 'configs-wt-2000-mode04-scActBinSig-steady.csv'       
        initial_index=2000
        args = "-b -l -o -pl scEdges -p evolve-misc -c 4 -s 1 -i 9"
        # args = "-b -l -o -pl scEdges -p evolve-misc "


if test == 'MicroGrid':

    filename = 'configs-mg.csv'       
    args = "-b -o"
    
    common_configs = {'env' : 'MicroGrid', 'num_actions' : 4, 'seed': 1, 'arch_name' : 'MG', 'pop_size' : 4, 'gens': 2, 
                    'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 24, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 2, 
                    'max_levels_limit': 5, 'min_columns_limit': 2, 'max_columns_limit': 5, 'early_termination': False, 'p_crossover': 0.9, 
                    'p_mutation': 0.75, 'num_evals': 1, 'error_limit': None, 'error_properties' : None, 'environment_properties': {'iterations' : 24, 'initial_seed' : 1, 'initial_day' : 1, 'day' : 1}}

file = 'configs'+ os.sep + filename

hge = HPCTGenerateEvolvers(common_configs=common_configs)  
hge.process_csv(file, args, cmdline=cmd, initial_index=initial_index, batch=batch)
