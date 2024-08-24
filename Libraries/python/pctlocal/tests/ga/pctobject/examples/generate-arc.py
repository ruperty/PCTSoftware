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

python examples/generate-arc.py -f configs-simple-00000001.csv -c 00000001 -p simple-00000001 -sm -ii 61 > configs/ar/cmds-simple.txt
python examples/generate-arc.py -f configs-simple-00000002.csv -c 00000002 -p simple-00000002 -sm -ii 91 >> configs/ar/cmds-simple.txt
python examples/generate-arc.py -f configs-simple-00000003.csv -c 00000003 -p simple-00000003 -sm -ii 121 >> configs/ar/cmds-simple.txt


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

    # user = 'ruper' if gethostname() == 'DESKTOP-5O07H5P' else 'ryoung'

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-c', '--code', type=str, help="ARC code")
    parser.add_argument('-a', '--aargs', type=str, help="additional arguments", default="")
    parser.add_argument('-r', '--refs', type=str, help="references", default="")
    parser.add_argument('-p', '--project', type=str, help="project name")
    parser.add_argument('-sm', '--single_multi', help="single or multi", action="store_true")
    parser.add_argument('-el', '--error_limit', type=int, help="error limit", default=1000)
    parser.add_argument('-ei', '--einitial', type=int, help="error initial", default=100)
    parser.add_argument('-ii', '--initial_index', type=int, help="initial index", default=1)
    parser.add_argument('-pop', '--pop_size', type=int, help="pop size", default=100)
    parser.add_argument('-g', '--gens', type=int, help="gens", default=50)  
    parser.add_argument('-s', '--seed', type=int, help="seed", default=1)
    parser.add_argument("-o", "--overwrite", help="overwrite existing results file", action="store_true")

    args = parser.parse_args()


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
    args = f'-b -pl scEdges,scZero,scFitness -p {project} {aargs} {ow}'
    # args = f'-b -pl scEdges,scZero,scFitness -p s-{code}-test -i 5'


    # properties = { 'dir': f'C:/Users/{user}/Versioning/python/nbdev/epct/nbs/testfiles/arc-prize-2024', 'file_prefix':'arc-agi_simple_', 'code':'00000001',  'dataset': 'train', 'control_set': ['cells'], 'input_set': ['env']}
    common_configs = {'env' : env, 'seed': seed, 'arch_name' : arch_name, 'pop_size' : pop_size, 'gens': gens, 'evolve_termination_value': evolve_termination_value,
                    'attr_mut_pb' : 1, 'structurepb' : 1, 'lower_float' : -1, 'upper_float' : 1, 'min_levels_limit': 1, 'runs': runs,
                    'max_levels_limit': 4, 'min_columns_limit': 1, 'max_columns_limit': 4, 'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': error_limit , 'error_properties':{'error:history': 10, 'error:initial': einitial}, 
                    'error_collector': error_collector, 'error_response': error_response, 'references': references}

    process(filename,common_configs, args, cmd, initial_index, batch, single_multi=single_multi)
    print()

