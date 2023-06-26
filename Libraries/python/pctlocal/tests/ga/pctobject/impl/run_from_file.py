
import argparse

from os import sep, listdir

from cutils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual, HPCTEvolveProperties




def runit(filename, env_props, render=False, history=False, runs=None, early_termination = False):
    
    hep = HPCTEvolveProperties()
    hep.load_db(filename)

    error_collector_type = hep.db['error_collector_type']
    error_response_type = hep.db['error_response_type']
    error_limit = eval(hep.db['error_limit'])
    error_properties = hep.get_error_properties()

    if runs==None:
        runs = eval(hep.db['runs'])
    config = eval(hep.db['config'])
    seed = eval(hep.db['seed'])
    # early_termination = eval(hep.db['early_termination'])

    hpct_verbose= False #True #False #
    
    ind, score = HPCTIndividual.run_from_config(config, min, render=render,  error_collector_type=error_collector_type, error_response_type=error_response_type, 
                                                error_properties=error_properties, error_limit=error_limit, steps=runs, hpct_verbose=hpct_verbose, history=history, 
                                                environment_properties=env_props, seed=seed, early_termination=early_termination)
    
 

# py -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.548-s013-2x2-m004-5a08e6cdc09769db0267a14f0634b051.properties"
# py -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC06-ReferencedInputsError-RootMeanSquareError-Mode03\ga-000.554-s068-2x2-m003-5342c97128d9ad23a0fea14a6d9c05e5.properties"
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-r', '--runs', type=int, help="number of runs", default="500")
    parser.add_argument('-e', '--early', help="early termination", action="store_true")
    parser.add_argument('-d', '--display', help="display environment", action="store_false")

    args = parser.parse_args()
    file = args.file 
    runs = args.runs 
    early = args.early 
    render = args.display


    # file = 'G:\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode03\ga-000.631-s066-2x2-m003-eb57dceed66c7697c01c54617cb106ff.properties'
    # file = 'G:\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.548-s013-2x2-m004-5a08e6cdc09769db0267a14f0634b051.properties'

    # runit(dir+sep+file, env_props, render=True, runs=runs, early_termination=early)
    
    score = HPCTIndividual.run_from_file(file, render=render, history=False, move=None, plots=None, hpct_verbose= False, runs=None, outdir=None, early_termination=early)
     
    
    print(f'Score={score:0.3f}')




