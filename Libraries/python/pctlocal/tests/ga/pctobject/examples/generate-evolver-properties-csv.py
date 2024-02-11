# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

import os

from eepct.hpct import HPCTGenerateEvolvers

args = "-i 1 -s 93"
test = 5
cmd='impl.evolve_multi'
initial_index=1

if test == 1:
    file = 'configs'+ os.sep + 'configs-cp.csv'

if test == 2:
    file = 'configs'+ os.sep + 'configs-mc.csv'

if test == 3:
    file = 'configs'+ os.sep + 'configs-ww.csv'

if test == 4:
    file = 'configs'+ os.sep + 'configs-pm.csv'

if test == 5:
    common_configs = {'env' : 'WindTurbine', 'num_actions' : 1, 'seed': 1, 'arch_name' : 'WT', 'pop_size' : 100, 'gens': 10, 'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 1000, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 2, 'max_levels_limit': 5, 'min_columns_limit': 2, 'max_columns_limit': 5, 'early_termination': False, 'p_crossover': 0.9, 'p_mutation': 0.75, 'num_evals': 1}
    # common_configs = {}

    file = 'configs'+ os.sep + 'configs-wt.csv'
    # file = 'configs'+ os.sep + 'configs-wt-reward-sum.csv'

    # args = "-b -l -o -pl scEdges -p evolve-batch -c 3 -s 1 -i 3"
    args = "-b -o"
    cmd='impl.evolve_multi_wt'
    # initial_index=1000

hge = HPCTGenerateEvolvers(common_configs=common_configs)  
hge.process_csv(file, args, cmdline=cmd, initial_index=initial_index)
