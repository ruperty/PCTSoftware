

import time, random

from deap import base, creator
from epct.evolvers import CommonToolbox
from eepct.hpct import HPCTIndividual, HPCTEvolver, HPCTArchitecture, HPCTEvolverWrapper
from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTVARIABLE
from pct.webots import WebotsHelper

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMax)
min = True

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)




if __name__ == "__main__":

    lower, upper = -1, 1 
    arch = HPCTArchitecture(lower_float=lower, upper_float=upper)
    arch.configure()
    arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
    arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
    print(arch)

    env_name = 'WebotsWrestler'
    helper = WebotsHelper(name=env_name, mode=1)
    env_inputs_indexes=helper.get_sensor_indexes() 
    env_inputs_names=helper.get_sensor_names()
    references=helper.get_references()

    error_collector_type , error_response_type = 'InputsError', 'RootMeanSquareError'
    seed, debug, pop_size, processes, runs, nevals, num_actions=1, 0, 10, 1, 500, 1, helper.get_num_links()
    min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 6, 6, 6, 100
    zerolevel_inputs_indexes=None
    toplevel_inputs_indexes=None

    environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes, 'render':False, 'early_termination': False,
        'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env_name, 'num_actions':num_actions, 'references':references}
    hpct_run_properties ={'min':min, 'hpct_verbose':False, 'debug':debug , 'runs':runs, 'nevals':nevals, 'seed':seed,  'error_collector_type' :  'InputsError', 'error_response_type' : 'RootMeanSquareError'}   
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
    evr = HPCTEvolverWrapper(evolver, min, pop_size=pop_size, toolbox=toolbox, processes=processes, p_crossover=0.8, p_mutation=0.5, display_env=True)

    test=1
    if test==1:
        
        loops = 1
        for _ in range(loops):
            ind = evr.toolbox.individual()        
            print()
            print(ind.get_parameters_list())
            ind.summary()
            #print(ind.get_config())
            print(ind.formatted_config())
            
            while True:
                try:
                    out = ind()
                    #print(out)
                    loops+=1
                except Exception as ex:
                    print(f'loops={loops}')    
                    break
                
            # print(ind.get_config(zero=1))
            print(ind.formatted_config())

        

        