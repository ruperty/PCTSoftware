# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""


# python examples/generate-generic.py -f configs.csv 




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
    parser.add_argument('-a', '--aargs', type=str, help="additional arguments", default="")
    parser.add_argument('-r', '--refs', type=str, help="references", default="")
    parser.add_argument('-ep', '--env_props', type=str, help="environment properties", default=None)
    parser.add_argument('-p', '--project', type=str, help="project name")
    parser.add_argument('-sm', '--single_multi', help="single or multi", action="store_true")
    parser.add_argument('-el', '--error_limit', type=int, help="error limit", default=1000)
    parser.add_argument('-ei', '--einitial', type=int, help="error initial", default=100)
    parser.add_argument('-ii', '--initial_index', type=int, help="initial index", default=1)
    parser.add_argument('-pop', '--pop_size', type=int, help="pop size", default=100)
    parser.add_argument('-g', '--gens', type=int, help="gens", default=10)  
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
    env = 'GenericGym'



    filename = f'gen{sep}{file}'
    args = f'-b -pl {plots} -p {project} {aargs} {ow}'
    # args = f'-b -pl scEdges,scZero,scFitness -p s-{code}-test -i 5'

    common_configs = {'env' : env, 'seed': seed, 'pop_size' : pop_size, 'gens': gens, 
                    'attr_mut_pb' : 1, 'structurepb' : 1, 'lower_float' : -1, 'upper_float' : 1,  'environment_properties': env_props, 
                    'min_levels_limit': min_levels_limit, 'max_levels_limit': max_levels_limit, 'min_columns_limit': min_columns_limit, 'max_columns_limit': max_columns_limit, 
                    'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': error_limit , 'error_properties':{'error:history': 10, 'error:initial': einitial}, 
                     'references': references}

    process(filename,common_configs, args, cmd, initial_index, batch, single_multi=single_multi)
    print()

