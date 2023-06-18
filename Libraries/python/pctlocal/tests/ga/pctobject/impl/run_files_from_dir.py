
import argparse

from os import sep, listdir

from cutils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual, HPCTEvolveProperties
from pct.architectures import run_from_properties_file




def runit(filename, env_props, render=False, history=False, runs=None, early_termination = False):
    
    hep = HPCTEvolveProperties()
    hep.load_db(filename)

    error_collector_type = hep.db['error_collector_type']
    error_response_type = hep.db['error_response_type']
    error_limit = eval(hep.db['error_limit'])
    if runs==None:
        runs = eval(hep.db['runs'])
    config = eval(hep.db['config'])
    seed = eval(hep.db['seed'])
    # early_termination = eval(hep.db['early_termination'])

    hpct_verbose= False #True #False #
    
    ind, score = HPCTIndividual.run_from_config(config, min, render=render,  error_collector_type=error_collector_type, error_response_type=error_response_type, 
                                                error_properties=None, error_limit=error_limit, steps=runs, hpct_verbose=hpct_verbose, history=history, 
                                                environment_properties=env_props, seed=seed, early_termination=early_termination)
    
    print(f'Score={score:0.3f}')

        
    

    
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
    




