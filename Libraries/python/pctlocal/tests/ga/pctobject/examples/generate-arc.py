# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""


# python examples/generate-arc.py > configs/ar/cmds-dims_only.txt
# python examples/generate-arc.py > configs/ar/cmds-simple.txt
# python examples/generate-arc.py >> configs/ar/cmds-simple.txt

from os import sep

from eepct.hpct import HPCTGenerateEvolvers

def process(filename,common_configs, args, cmd, initial_index, batch):
    file = 'configs'+ sep + filename

    hge = HPCTGenerateEvolvers(common_configs=common_configs)  
    hge.process_csv(file, args, cmdline=cmd, initial_index=initial_index, batch=batch)


from socket import gethostname    
user = 'ruper' if gethostname() == 'DESKTOP-5O07H5P' else 'ryoung'

project = 'simple'
# project = 'dims_only'

args = "-i 1 -s 93"
cmd='impl.evolve'
# initial_index=1
batch = 60
num_evals = 1
pop_size =  100
gens = 50
env = 'ARC'
seed =  1
arch_name = 'ARC'
error_collector = 'FitnessError'
evolve_termination_value = 0

if project == 'dims_only':
    runs = 500
    initial_index = 1
    filename = 'ar' + sep +'configs-dims-only.csv'
    args = f'-b -pl scEdges,scZero -p {project} -o'
    # properties = { 'code':'007bbfb7',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env']}
    common_configs = {'env' : env, 'seed': seed, 'arch_name' : arch_name, 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
                    'attr_mut_pb' : 1, 'structurepb' : 1, 'runs' : runs, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 
                    'max_levels_limit': 4, 'min_columns_limit': 1, 'max_columns_limit': 4, 'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': 10000, # 'environment_properties': properties, 
                    'error_properties':{'error:history': 10, 'error:initial': 100}, 'error_collector': error_collector, 'references': [0]}

    process(filename,common_configs, args, cmd, initial_index, batch)



# if project == 'dims_only1':

#     filename = 'ar' + sep +'configs-dims-only-sum.csv'
#     args = f'-b -pl scEdges,scZero -p {project} -o'
#     initial_index=1
#     qty = 7

#     ls = [ ['env'] , ['env', 'inputs'] ]
#     for input_set in ls:
#         for index in range(2):
#             if index == 0:
#                 properties = { 'code':'007bbfb7',  'dataset': 'train', 'control_set': ['dims'], 'input_set': input_set, 'index' : 0}
#             else:
#                 properties = { 'code':'007bbfb7',  'dataset': 'train', 'control_set': ['dims'], 'input_set': input_set}

#             common_configs = {'env' : 'ARC', 'seed': 1, 'arch_name' : 'ARC', 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
#                     'attr_mut_pb' : 1, 'structurepb' : 0.9, 'runs' : runs, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 
#                     'max_levels_limit': 2, 'min_columns_limit': 1, 'max_columns_limit': 2, 'early_termination': True, 'p_crossover': 0.9, 
#                     'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': 10000, 'environment_properties': properties, 'error_properties':{'error:history': 20, 'error:initial': 100}}

#             process(filename,common_configs, args, cmd, initial_index, batch)
#             initial_index += qty

if project == 'simple':
    code = '00000003'

    if code == '00000001':
        initial_index=61
    elif code == '00000002':
        initial_index=81
    elif code == '00000003':
        initial_index=101
        pop_size =  1000

    elif code == '00000004':
        initial_index=121

    filename = f'ar{sep}configs-simple-{code}.csv'
    args = f'-b -pl scEdges,scZero,scFitness -p simple-{code} -o'
    runs = 300

    # properties = { 'dir': f'C:/Users/{user}/Versioning/python/nbdev/epct/nbs/testfiles/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000001',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env']}
    common_configs = {'env' : env, 'seed': seed, 'arch_name' : arch_name, 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
                    'attr_mut_pb' : 1, 'structurepb' : 1, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 
                    'max_levels_limit': 4, 'min_columns_limit': 1, 'max_columns_limit': 4, 'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': 10000, # 'environment_properties': properties,
                    'error_properties':{'error:history': 10, 'error:initial': 100}, 'error_collector': error_collector, 'references': [0]}

    process(filename,common_configs, args, cmd, initial_index, batch)
    print()

