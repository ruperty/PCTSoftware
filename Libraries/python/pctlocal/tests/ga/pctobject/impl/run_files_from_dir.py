
import argparse

from os import sep, listdir

from cutils.paths import  get_gdrive
from eepct.hpct import HPCTEvolveProperties
from pct.architectures import run_from_properties_file

from pct.hierarchy import PCTHierarchy



def runit(filename, env_props, render=False, history=False, runs=None, early_termination = False):
    
    hep = HPCTEvolveProperties()
    hep.load_db(filename)

    error_collector_type = hep.db['error_collector_type'].strip()
    error_response_type = hep.db['error_response_type']
    error_limit = eval(hep.db['error_limit'])
    error_properties = hep.get_error_properties()

    if runs==None:
        runs = eval(hep.db['runs'])
    config = eval(hep.db['config'])
    seed = eval(hep.db['seed'])
    # early_termination = eval(hep.db['early_termination'])

    hpct_verbose= False #True #False #
    
    ind, score = PCTHierarchy.run_from_config(config, min, render=render,  error_collector_type=error_collector_type, error_response_type=error_response_type, 
                                                error_properties=error_properties, error_limit=error_limit, steps=runs, hpct_verbose=hpct_verbose, history=history, 
                                                environment_properties=env_props, seed=seed, early_termination=early_termination)
    
    print(f'Score={score:0.3f}')

# python -m impl.run_files_from_dir -d "/mnt/c/Users/ruper/My Drive/data/ga/MountainCarContinuousV0/MC03-ReferencedInputsError-RootMeanSquareError-Mode01/0c4be8064cb284e7bd5bc0c3248ee554"
    

# python -m impl.run_files_from_dir -d "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\cdf7cc1497ad143c0b04a3d9e72ab783" 
# python -m impl.run_files_from_dir -d "/mnt/c/Users/ruper/My Drive/data/ga/MountainCarContinuousV0/MC08-ReferencedInputsError-RootMeanSquareError-Mode04/cdf7cc1497ad143c0b04a3d9e72ab783" 

# python -m impl.run_files_from_dir -d "/mnt/c/Users/ruper/My Drive/data/ga/MountainCarContinuousV0/MC00-ReferencedInputsError-RootMeanSquareError-Mode00/fc21f334f54a2f9b44275c793465158e" 

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, help="directory of files")
    parser.add_argument('-r', '--runs', type=int, help="number of runs", default="500")
    parser.add_argument('-e', '--early', help="early termination", action="store_true")

    args = parser.parse_args()
    dir = args.dir 
    runs = args.runs 
    early = args.early 


    # dir = "C:\\Users\\ruper\\My Drive\\data\\ga\\CartPoleV1\\Std03-InputsError-RootMeanSquareError-Mode00\\e951b3484d28b6fa411d2879d3269abf"
    # dir = '/mnt/c/Users/ruper/My Drive/data/ga/CartPoleV1/Std03-InputsError-RootMeanSquareError-Mode00/e951b3484d28b6fa411d2879d3269abf/'
    # dir = '/mnt/c/Users/ruper/My Drive/data/ga/CartPoleV1/Std00-InputsError-RootMeanSquareError-Mode00/fb22a9790da95d15522361084ca466ab/'
    env_props={}

    for file in listdir(dir):
        if file.endswith(".config"):
            # print(file)
            runit(dir+sep+file, env_props, render=True, runs=runs, early_termination=early)
    




