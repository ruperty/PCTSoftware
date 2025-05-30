# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

"""



# LunarLanderContinuousV2

python examples/generate-generic.py -e GenericGym -f gen/LL-RewardSummed.csv -sm -mall 8 -macl 8 -pl "scEdges,scError,scReward" -p Reward-Summed -a "-i 3 -o" -pop 1000 -n 3 > configs/gen/LL-RewardSummed.txt
python examples/generate-generic.py -e GenericGym -f gen/LL-InputsRMS.csv -sm  -mall 8 -macl 8 -el 1000 -pl "scEdges,scError,scReward" -p Inputs-RMS -a "-i 3 -o" -pop 1000 -n 3 -ii 21 > configs/gen/LL-InputsRMS.txt
python examples/generate-generic.py -e GenericGym -f gen/LL-RefInputsRMS.csv -sm -mall 8 -macl 8 -pl "scEdges,scError,scReward" -p RefInputs-RMS -a "-i 3 -o" -pop 1000 -n 3 -ii 41 > configs/gen/LL-RefInputsRMS.txt
python examples/generate-generic.py -e GenericGym -f gen/LL-RefInputsSmooth.csv -sm -mall 8 -macl 8 -pl "scEdges,scError,scReward" -p RefInputs-Smooth -a "-i 3 -c 3 -o" -pop 1000 -n 3 -ii 61 > configs/gen/LL-RefInputsSmooth.txt
python examples/generate-generic.py -e GenericGym -f gen/LL-InputsCurrentRMS.csv -sm  -mall 8 -macl 8 -pl "scEdges,scError,scReward" -p Inputs-CurrentRMS -a "-i 3 -c 3 -o" -pop 1000 -n 3 -ii 81 > configs/gen/LL-InputsCurrentRMS.txt
python examples/generate-generic.py -e GenericGym -f gen/LL-RefInputsCurrentRMS.csv -sm  -mall 8 -macl 8 -pl "scEdges,scError,scReward" -p RefInputs-CurrentRMS -a "-i 3 -c 3 -o" -pop 1000 -n 3 -ii 101 > configs/gen/LL-RefInputsCurrentRMS.txt



python examples/generate-generic.py -e GenericGym -f gen/LL-RefInputsSmooth.csv -mall 1 -macl 8 -pl "scEdges,scError,scReward" -p RefInputs-Smooth -a "-c 3 -o" -pop 10 -ii 1061 > configs/gen/LL-RefInputsSmooth1061.txt



# CartPoleV1

python examples/generate-generic.py -e GenericGym -f gen/configs-cp.csv -mall  1 -macl 1 -pl "scEdges,scError" -a "-i 3" -p all > configs/gen/cmds-cp-all.txt

python examples/generate-generic.py -e GenericGym -f gen/configs-cp-total.csv -mall  1 -macl 1 -pl "scEdges,scError" -a "-i 3" -p total > configs/gen/cmds-cp.txt
python examples/generate-generic.py -e GenericGym -f gen/configs-cp-inputs.csv -mall  1 -macl 1 -pl "scEdges,scError" -ii 9 -a "-i 3" -p inputs >> configs/gen/cmds-cp.txt
python examples/generate-generic.py -e GenericGym -f gen/configs-cp-reward.csv -mall  1 -macl 1 -pl "scEdges,scError" -ii 17 -a "-i 3" -p inputs >> configs/gen/cmds-cp.txt

# WindTurbine
python examples/generate-generic.py -e WindTurbine -f wt/configs-wt-refinp-rms-test.csv

# MountainCarContinuousV0

python examples/generate-generic.py -e MountainCarContinuousV0 -f mc/configs-mc.csv




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
    parser.add_argument('-e', '--env', type=str, help="environment name")
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-a', '--aargs', type=str, help="additional arguments", default="")
    parser.add_argument('-r', '--refs', type=str, help="references", default="")
    parser.add_argument('-ep', '--env_props', type=str, help="environment properties", default=None)
    parser.add_argument('-p', '--project', type=str, help="project name")
    parser.add_argument('-sm', '--single_multi', help="single or multi", action="store_true")
    parser.add_argument('-el', '--error_limit', type=int, help="error limit", default=None)
    parser.add_argument('-ei', '--einitial', type=int, help="error initial", default=100)
    parser.add_argument('-ii', '--initial_index', type=int, help="initial index", default=1)
    parser.add_argument('-pop', '--pop_size', type=int, help="pop size", default=100)
    parser.add_argument('-g', '--gens', type=int, help="gens", default=10)  
    parser.add_argument('-s', '--seed', type=int, help="seed", default=1)
    parser.add_argument('-o', '--overwrite', help="overwrite existing results file", action="store_true")
    parser.add_argument('-mill', '--min_levels_limit', type=int, help="initial index", default=1)
    parser.add_argument('-mall', '--max_levels_limit', type=int, help="initial index", default=4)    
    parser.add_argument('-micl', '--min_columns_limit', type=int, help="initial index", default=1)
    parser.add_argument('-macl', '--max_columns_limit', type=int, help="initial index", default=4)
    parser.add_argument('-pl', '--plots', type=str, help="plots", default="")
    parser.add_argument('-b', '--batch', type=int, help="batch size", default=8)
    parser.add_argument('-n', '--nevals', type=int, help="number of evaluations", default=1)

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
    batch = args.batch
    num_evals = args.nevals
    env = args.env


    args = f'-b  {aargs} {ow}'
    if plots != "":
        args = args + f' -pl {plots}'
    if project is not None:
        args = args + f' -p {project}'


    common_configs = {'env' : env, 'seed': seed, 'pop_size' : pop_size, 'gens': gens, 
                    'attr_mut_pb' : 1, 'structurepb' : 1, 'lower_float' : -10, 'upper_float' : 10,  'environment_properties': env_props, 
                    'min_levels_limit': min_levels_limit, 'max_levels_limit': max_levels_limit, 'min_columns_limit': min_columns_limit, 'max_columns_limit': max_columns_limit, 
                    'early_termination': True, 'p_crossover': 0.9, 
                    'p_mutation': 0.9, 'num_evals': num_evals, 'error_limit': error_limit , 'error_properties':{'error:history': 10, 'error:initial': einitial}, 
                     'references': references}

    print()
    process(file,common_configs, args, cmd, initial_index, batch, single_multi=single_multi)
    print()

