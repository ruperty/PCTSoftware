# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

# python examples/generate-evolver-properties-csv.py > configs/wt/variable-cmds.txt
# python examples/generate-evolver-properties-csv.py > configs/wt/steady-cmds.txt
# python examples/generate-evolver-properties-csv.py > configs/wt/steady-cmds-700.txt
# python examples/generate-evolver-properties-csv.py > configs/wt/variable-cmds-700.txt


from os import sep

from eepct.hpct import HPCTGenerateEvolvers

test = 'arc'
# test = 'WindTurbine'
# test = 'MicroGrid'


args = "-i 1 -s 93"
cmd='impl.evolve_multi'
initial_index=1
# initial_index=1
batch = 10

if test == 1:
    file = 'configs'+ sep + 'configs-cp.csv'

if test == 2:
    file = 'configs'+ sep + 'configs-mc.csv'

if test == 3:
    file = 'configs'+ sep + 'configs-ww.csv'

if test == 4:
    file = 'configs'+ sep + 'configs-pm.csv'

if test == 'WindTurbine':
    test = "variable"
    # test = "steady"
    batch = 10
    pop_size = 100
    gens = 10

    if initial_index == 1:
        common_configs = {'env' : 'WindTurbine', 'num_actions' : 1, 'seed': 1, 'arch_name' : 'WT', 'pop_size' : pop_size, 'gens': gens, 
                        'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 1000, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 2, 
                        'max_levels_limit': 5, 'min_columns_limit': 2, 'max_columns_limit': 5, 'early_termination': False, 'p_crossover': 0.9, 
                        'p_mutation': 0.75, 'num_evals': 1}

    if initial_index == 701:
        common_configs = {'env' : 'WindTurbine', 'num_actions' : 1, 'seed': 1, 'arch_name' : 'WT',  'gens': gens, 'error_limit': None,
                        'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 1000, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 2, 
                        'min_columns_limit': 2, 'early_termination': False, 'p_crossover': 0.9, 'error_properties': None,
                        'p_mutation': 0.75, 'num_evals': 1, 'zerolevel_inputs_indexes':None, 'toplevel_inputs_indexes':None}


    if initial_index == 1:
        filename = 'wt' + sep +'configs-wt-0001-0616-'+test+'.csv'
        # args = "-b -pl scEdges -p evolve1 -rp \"{'comparisons' : True, 'comparisons_print_plots': True}\" -c 6 "
        args = "-b -pl scEdges -p evolve1-batch -rp \"{'comparisons' : True, 'comparisons_print_plots': True}\" -c 6 -s 2 -i 4"
        # args = "-b -o -pl scEdges -p test-evolve -rp \"{'comparisons' : True, 'comparisons_print_plots': True}\" -c 3 -s 1 -i 3"
        # args = "-b -l -o -pl scEdges -p evolve" 

    if initial_index == 701:
        filename = 'wt' + sep +'configs-wt-0701-0732-'+test+'.csv'
        args = "-b -pl scEdges -p evolve1-added -rp \"{'comparisons' : True, 'comparisons_print_plots': True}\" -c 6 -s 1 -i 1"

if test == 'MicroGrid':

    filename = 'configs-mg.csv'       
    args = "-b -o -x"
    num_evals = 1
    pop_size =  4
    gens = 1
    #day_mode = 'ordered'
    day_mode = [5]
    common_configs = {'env' : 'MicroGrid', 'num_actions' : 4, 'seed': 1, 'arch_name' : 'MG', 'pop_size' : pop_size, 'gens': gens, 
                    'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 24, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 2, 
                    'max_levels_limit': 5, 'min_columns_limit': 2, 'max_columns_limit': 5, 'early_termination': False, 'p_crossover': 0.9, 
                    'p_mutation': 0.75, 'num_evals': num_evals, 'error_limit': None, 'error_properties' : None, 
                    'environment_properties': {'iterations' : 24, 'day_mode' : day_mode, 'initial_day' :1 }}
                    # 'environment_properties': {'iterations' : 24, 'initial_seed' : 1, 'day_mode' : 'ordered', 'initial_day' :1 }}


if test == 'arc':

    filename = 'ar' + sep +'configs-arc.csv'
    args = "-b -pl scEdges -p test-evolve"
    num_evals = 1
    pop_size =  100
    gens = 10
    properties = {'dir': 'C:/packages/arc-prize-2024/training', 'code':'1_007bbfb7.dat', 'fitness_type': 'dim_only'}
    common_configs = {'env' : 'ARC', 'num_actions' : 2, 'seed': 1, 'arch_name' : 'ARC', 'pop_size' : pop_size, 'gens': gens, 
                    'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : 100, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 
                    'max_levels_limit': 2, 'min_columns_limit': 1, 'max_columns_limit': 2, 'early_termination': False, 'p_crossover': 0.9, 
                    'p_mutation': 0.75, 'num_evals': num_evals, 'error_limit': 10000,  'arch_types': '',
                    'environment_properties': properties}



file = 'configs'+ sep + filename

hge = HPCTGenerateEvolvers(common_configs=common_configs)  
hge.process_csv(file, args, cmdline=cmd, initial_index=initial_index, batch=batch)
