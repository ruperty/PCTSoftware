# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""


# python examples/generate-arc.py > configs/ar/cmds-dims_only.txt
# python examples/generate-arc.py > configs/ar/cmds-simple.txt
# python examples/generate-arc.py >> configs/ar/cmds-simple.txt

# python examples/generate-arc.py -f configs-simple-00000001.csv -c 00000001 -p simple-00000001 -sm -ii 61 -pop 1000
# python examples/generate-arc.py -f configs-simple-00000001.csv -c 00000001 -p simple-00000001 -sm -ii 61 > configs/ar/cmds-simple.txt
# python examples/generate-arc.py -f configs-simple-00000001.csv -c 00000001 -p simple -sm -ii 61 -a "-i 5" >> configs/ar/cmds-simple.txt

# python examples/generate-arc.py -f configs-simple-00000002.csv -c 00000002 -p simple -sm -ii 81  >> configs/ar/cmds-simple.txt
# python examples/generate-arc.py -f configs-simple-00000002.csv -c 00000002 -p simple -sm -ii 81 -a "-i 5" >> configs/ar/cmds-simple.txt

# python examples/generate-arc.py -f configs-simple-00000003.csv -c 00000003 -p simple -sm -ii 101  >> configs/ar/cmds-simple.txt
# python examples/generate-arc.py -f configs-simple-00000003.csv -c 00000003 -p simple -sm -ii 101 -a "-i 5" >> configs/ar/cmds-simple.txt

# python examples/generate-arc.py -f configs-simple-00000003.csv -c 00000003 -p simple-00000003 -sm -ii 101  >> configs/ar/cmds-simple.txt
# python examples/generate-arc.py -f configs-simple-00000003.csv -c 00000003 -p simple-00000003 -sm -ii 101 -a "-i 5" >> configs/ar/cmds-simple.txt

# All
"""

Simple
AverageMaxOfDiff
python examples/generate-arc.py -f configs-simple-00000001.csv -c 00000001 -p simple-00000001 -ii 61 -a "-i 3" -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000001',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5, 'atARCdisplay': 0.5}, 'fitness': 'AverageMaxOfDiff'}" > configs/ar/cmds-simple.txt
python examples/generate-arc.py -f configs-simple-00000002.csv -c 00000002 -p simple-00000002 -ii 91 -a "-i 3" -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000002',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5, 'atARCdisplay': 0.5}, 'fitness': 'AverageMaxOfDiff'}" >> configs/ar/cmds-simple.txt
python examples/generate-arc.py -f configs-simple-00000003.csv -c 00000003 -p simple-00000003 -ii 121 -a "-i 3" -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000003',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5, 'atARCdisplay': 0.5}, 'fitness': 'AverageMaxOfDiff'}" >> configs/ar/cmds-simple.txt
python examples/generate-arc.py -f configs-simple-00000004.csv -c 00000004 -p simple-00000004 -ii 151 -a "-i 3" -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000004',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5, 'atARCdisplay': 0.5}, 'fitness': 'AverageMaxOfDiff'}" >> configs/ar/cmds-simple.txt
python examples/generate-arc.py -f configs-simple-00000005.csv -c 00000005 -p simple-00000005 -ii 251 -a "-i 3" -macl 1 -mall 1 -o -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000005',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5}, 'fitness': 'Euclidean'}" >> configs/ar/cmds-simple.txt

Euclidean
python examples/generate-arc.py -f configs-simple-00000001.csv -c 00000001 -p simple-00000001 -ii  61 -a "-i 3" -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000001',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5 }, 'fitness': 'Euclidean'}" > configs/ar/cmds-simple.txt

python examples/generate-arc.py -f configs-simple-00000004.csv -c 00000004 -p simple-00000004 -ii 151 -a "-i 3" -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000004',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5 }, 'fitness': 'Euclidean'}" >> configs/ar/cmds-simple.txt

python examples/generate-arc.py -f configs-simple-00000006.csv -c 00000006 -p simple-00000006 -ii 301 -a "-i 3" -sm -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000006',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5 }, 'fitness': 'Euclidean'}" >> configs/ar/cmds-simple.txt

python examples/generate-arc.py -f configs-simple-00000007.csv -c 00000007 -p simple-00000007 -mall 1 -macl 1 -ii 401 -a "-i 3" -sm -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000007',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5 }, 'fitness': 'Euclidean'}" >> configs/ar/cmds-simple.txt
python examples/generate-arc.py -f configs-simple-00000007.csv -c 00000007 -p simple-00000007 -pl scFitness -mall 1 -macl 1 -ii 401 -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000007',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5 }, 'fitness': 'Euclidean'}" >> configs/ar/cmds-simple.txt

python examples/generate-arc.py -f configs-simple-00000010.csv -c 00000010 -p simple-00000010 -mall 1 -macl 1 -ii 351 -a "-i 3" -sm -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000010',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5 }, 'fitness': 'Euclidean'}" >> configs/ar/cmds-simple.txt


Train
Simple
AverageMaxOfDiff
python examples/generate-arc.py -f configs-train-5582e5ca.csv -p train-5582e5ca -ii 201 -a "-i 3" -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_training_', 'code':'5582e5ca',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5, 'atARCdisplay': 0.5}, 'fitness': 'AverageMaxOfDiff'}" > configs/ar/cmds-train.txt
python examples/generate-arc.py -f configs-train-5582e5ca.csv -p train-5582e5ca -ii 201 -a "-i 3 -t macl10" -mall 100 -macl 10 -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_training_', 'code':'5582e5ca',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5, 'atARCdisplay': 0.5}, 'fitness': 'AverageMaxOfDiff'}" > configs/ar/cmds-train.txt

Euclidean
python examples/generate-arc.py -f configs-train-5582e5ca.csv -p train-5582e5ca -ii 201 -a "-i 3 -t macl10" -mall 10 -macl 10 -ep "{ 'dir': '/tmp/arc-prize-2024', 'file_prefix':'arc-agi_training_', 'code':'5582e5ca',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env', 'inputs'], 'tolerances': {'atARCresolved': 0.5 }, 'fitness': 'Euclidean'}" > configs/ar/cmds-train.txt



"""





from os import sep
import argparse
from eepct.hpct import HPCTGenerateEvolvers
from socket import gethostname    

def process(filename,common_configs, args, cmd, initial_index, batch, single_multi=False):
    file = 'configs'+ sep + filename

    hge = HPCTGenerateEvolvers(common_configs=common_configs, single_multi=single_multi)  
    hge.process_csv(file, args, cmdline=cmd, initial_index=initial_index, batch=batch, single_multi=single_multi)





if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-c', '--code', type=str, help="ARC code")
    parser.add_argument('-a', '--aargs', type=str, help="additional arguments", default="")
    parser.add_argument('-r', '--refs', type=str, help="references", default="")
    parser.add_argument('-ep', '--env_props', type=str, help="environment properties", default=None)
    parser.add_argument('-p', '--project', type=str, help="project name")
    parser.add_argument('-sm', '--single_multi', help="single or multi", action="store_true")
    parser.add_argument('-el', '--error_limit', type=int, help="error limit", default=1000)
    parser.add_argument('-ei', '--einitial', type=int, help="error initial", default=100)
    parser.add_argument('-ii', '--initial_index', type=int, help="initial index", default=1)
    parser.add_argument('-pop', '--pop_size', type=int, help="pop size", default=100)
    parser.add_argument('-g', '--gens', type=int, help="gens", default=50)  
    parser.add_argument('-s', '--seed', type=int, help="seed", default=1)
    parser.add_argument("-o", "--overwrite", help="overwrite existing results file", action="store_true")
    parser.add_argument('-mill', '--min_levels_limit', type=int, help="initial index", default=1)
    parser.add_argument('-mall', '--max_levels_limit', type=int, help="initial index", default=4)    
    parser.add_argument('-micl', '--min_columns_limit', type=int, help="initial index", default=1)
    parser.add_argument('-macl', '--max_columns_limit', type=int, help="initial index", default=4)
    parser.add_argument('-pl', '--plots', type=str, help="plots", default="scEdges,scZero,scFitness")

    args = parser.parse_args()

    min_levels_limit = args.min_levels_limit
    max_levels_limit = args.max_levels_limit
    min_columns_limit = args.min_columns_limit
    max_columns_limit = args.max_columns_limit
    error_limit = args.error_limit
    einitial = args.einitial
    initial_index = args.initial_index
    pop_size = args.pop_size
    gens = args.gens
    file = args.file
    seed = args.seed
    aargs = args.aargs
    project = args.project
    code = args.code
    single_multi = args.single_multi
    overwrite = args.overwrite
    ow = ""
    if overwrite:
        ow = "-o"
    references = None
    if args.refs != "":
        references = eval(args.refs)
    plots = args.plots
    env_props = args.env_props
    if env_props is not None:
        env_props = eval(env_props)

    cmd='impl.evolve'
    # initial_index=1
    batch = 60
    num_evals = 1
    env = 'ARC'
    arch_name = 'ARC'
    error_collector = 'FitnessError'
    evolve_termination_value = 0
    error_response = 'MovingAverageError'
    runs = '750'

# if project == 'dims_only':
#     runs = 500
#     initial_index = 1
#     filename = 'ar' + sep +'configs-dims-only.csv'
#     args = f'-b -pl scEdges,scZero -p {project} -o'
#     # properties = { 'code':'007bbfb7',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env']}
#     common_configs = {'env' : env, 'seed': seed, 'arch_name' : arch_name, 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
#                     'attr_mut_pb' : 1, 'structurepb' : 1, 'runs' : runs, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 
#                     'max_levels_limit': 4, 'min_columns_limit': 1, 'max_columns_limit': 4, 'early_termination': True, 'p_crossover': 0.9, 
#                     'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': 10000, # 'environment_properties': properties, 
#                     'error_properties':{'error:history': 10, 'error:initial': 100}, 'error_collector': error_collector, 'references': [0]}

#     process(filename,common_configs, args, cmd, initial_index, batch)

# if project == 'simple':

    filename = f'ar{sep}{file}'
    args = f'-b -pl {plots} -p {project} {aargs} {ow}'
    # args = f'-b -pl scEdges,scZero,scFitness -p s-{code}-test -i 5'


    # properties = { 'dir': f'C:/Users/{user}/Versioning/python/nbdev/epct/nbs/testfiles/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000001',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env']}
    common_configs = {'env' : env, 'seed': seed, 'arch_name' : arch_name, 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
                    'attr_mut_pb' : 1, 'structurepb' : 1, 'lower_float' : -1, 'upper_float' : 1, 'runs': runs, 'environment_properties': env_props, 
                    'min_levels_limit': min_levels_limit, 'max_levels_limit': max_levels_limit, 'min_columns_limit': min_columns_limit, 'max_columns_limit': max_columns_limit, 'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': error_limit , 'error_properties':{'error:history': 10, 'error:initial': einitial}, 
                    'error_collector': error_collector, 'error_response': error_response, 'references': references}

    process(filename,common_configs, args, cmd, initial_index, batch, single_multi=single_multi)
    print()

