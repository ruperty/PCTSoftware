
import time
import multiprocessing
import pickle

from deap import base, creator
import random

from epct.evolvers import EvolverWrapper, CommonToolbox
from pct.functions import HPCTFUNCTION

from eepct.hpct import HPCTIndividual
from eepct.hpct import HPCTEvolver
from eepct.hpct import HPCTArchitecture


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

if __name__ == "__main__":

    lower, upper = -1, 1 
    arch = HPCTArchitecture(lower_float=lower, upper_float=upper)
    arch.configure()

    # env = VelocityModel(name='VM', mass=250, num_links=2, indexes=4)
    env_name = 'CartPoleV1'
    env_inputs_indexes=[0,2,1,3]
    env_inputs_names=['IP', 'IV', 'IC', 'IF']
    references=[0]
    seed = 1

    error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'
    debug, pop_size, processes, runs, nevals, num_actions= 0, 100, 1, 1, 1, 1
    min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 5, 1, 5, 100
    zerolevel_inputs_indexes=None
    toplevel_inputs_indexes=None

    random.seed(seed)

    environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes,
        'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env_name, 'num_actions':num_actions, 'references':references}
    # evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25,  'attr_mut_pb':1, 'attr_cx_uniform_pb':0.5, 'structurepb':1}
    evolve_properties = {'attr_mut_pb':0.8,'structurepb':1, 'attr_cx_uniform_pb':0.5, 'alpha':0.5}

    hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit, 'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit, 'lower_float':-100, 'upper_float':100 }    

    #hpct_run_properties ={ 'hpct_verbose':False, 'debug':debug , 'runs':runs, 'nevals':nevals}    

    hpct_run_properties ={ 'error_collector_type':error_collector_type, 'error_response_type': error_response_type,
        'error_properties':error_properties, 'error_limit': error_limit, 'runs':runs, 'nevals':nevals,
        'history':False, 'hpct_verbose':False,  'debug':debug, 'seed':seed}    


    evolver_properties = {'environment_properties':environment_properties, 
        'evolve_properties':evolve_properties,  
        'hpct_structure_properties':hpct_structure_properties,
        'hpct_run_properties':hpct_run_properties,
        'arch': arch}

    evolver = HPCTEvolver(**evolver_properties)

    evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes, p_mutation=0.25)

    ind1 = evr.toolbox.individual()     

    for ctr in range(10):
        tic = time.process_time() 
        ind1.fitness.values = evr.toolbox.evaluate(ind1)
        print(ind1.get_preprocessor()[0].get_value())
        toc = time.process_time()
        elapsed = toc-tic
        #print(f'Evaluate time: {elapsed:4.4f}')
        #print (ind1.fitness)  

