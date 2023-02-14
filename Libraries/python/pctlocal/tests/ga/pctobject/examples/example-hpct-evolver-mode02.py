

import time, random

from deap import base, creator
from epct.evolvers import CommonToolbox
from eepct.hpct import HPCTIndividual, HPCTEvolver, HPCTArchitecture, HPCTEvolverWrapper
from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTVARIABLE
from eepct.hpct import Memory

from pct.putils import FunctionsList

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)




if __name__ == "__main__":

    lower, upper = -1, 1 
    arch = HPCTArchitecture(mode=2, lower_float=lower, upper_float=upper)
    arch.configure()

    env_name = 'CartPoleV1'
    env_inputs_indexes=[1, 0, 3, 2]
    env_inputs_names=['ICV', 'ICP', 'IPV', 'IPA']
    references=[0]

    error_collector_type , error_response_type = 'InputsError', 'RootMeanSquareError'
    pop_size, processes, runs, nevals, num_actions= 10, 1, 500, 1, 1
    min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 5, 1, 5, 100
    zerolevel_inputs_indexes=None
    toplevel_inputs_indexes=None
    seed=1
    debug=0
                
        
    environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes, 'render':False, 'early_termination': False,
        'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env_name, 'num_actions':num_actions, 'references':references}
    hpct_run_properties ={ 'hpct_verbose':False, 'debug':debug , 'runs':runs, 'nevals':nevals, 'seed':seed,  'error_collector_type' :  'InputsError', 'error_response_type' : 'RootMeanSquareError'}   
    evolve_properties = {'attr_mut_pb':0.8,'structurepb':1} #, 'attr_cx_uniform_pb':0.5, 'alpha':0.5} 
    hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit, 'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit }    
  

    evolver_properties = {'environment_properties':environment_properties, 
        'evolve_properties':evolve_properties,  
        'hpct_structure_properties':hpct_structure_properties,
        'hpct_run_properties':hpct_run_properties,
        'arch': arch}

    random.seed(seed)
    evolver = HPCTEvolver(**evolver_properties)
    #print(evolver_properties)
    evr = HPCTEvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes, p_crossover=0.8, p_mutation=0.5, display_env=True, local_out_dir='output')

    test=1

    if test==1:
        ind = evr.toolbox.individual()          
        ind1, = evr.toolbox.mutate(ind)
        
    if test==2:
        ind1 = evr.toolbox.individual()          
        ind2 = evr.toolbox.individual()          
        ind21,ind22 = evr.toolbox.mate(ind1, ind2)
        

        