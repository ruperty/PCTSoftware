

import time, random

from deap import base, creator
from epct.evolvers import CommonToolbox
from eepct.hpct import HPCTIndividual, HPCTEvolver, HPCTArchitecture, HPCTEvolverWrapper
from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTVARIABLE

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)




if __name__ == "__main__":

    lower, upper = -1, 1 
    arch = HPCTArchitecture(lower_float=lower, upper_float=upper)
    arch.configure()

    arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
    arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
    arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, {'lower': -5, 'upper': 5})
    
    env_name = 'CartPoleV1'
    env_inputs_indexes=[1, 0, 3, 2]
    env_inputs_names=['ICV', 'ICP', 'IPV', 'IPA']
    references=[0]

    error_collector_type , error_response_type = 'InputsError', 'RootMeanSquareError'
    seed, debug, pop_size, processes, runs, nevals, num_actions=1, 0, 20, 1, 500, 1, 1
    min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 5, 1, 5, 100
    zerolevel_inputs_indexes=None
    toplevel_inputs_indexes=None
    env_props={}
    min=True
    environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes, 'render':False, 
                              'early_termination': True, 'environment_properties': env_props, 'toplevel_inputs_indexes':toplevel_inputs_indexes, 
                              'env_inputs_names':env_inputs_names, 'env_name':env_name, 'num_actions':num_actions, 'references':references}
    hpct_run_properties ={ 'hpct_verbose':False, 'debug':debug , 'runs':runs, 'nevals':nevals, 'seed':seed,  'error_collector_type' :  'InputsError', 
                          'min': min, 'error_response_type' : 'RootMeanSquareError'}   
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
    evr = HPCTEvolverWrapper(evolver=evolver, min=min, pop_size=pop_size, toolbox=toolbox, processes=processes, p_crossover=0.8, p_mutation=0.5, display_env=False)

    test=1
    if test==1:
        print('Start evolve')
        verbose=  1
        deap_verbose=False #True #
        gens=10
        tic = time.perf_counter()
        top_ind=evr.run(gens=gens, deap_verbose=deap_verbose, evolve_verbose=verbose)
        toc = time.perf_counter()
        elapsed = toc-tic
        best=evr.best()
        print(f'Elapsed time: {elapsed:4.4f}')
        print("Best Score: %0.3f" % evr.best_score())
        print("Best Ind: ", best.get_parameters_list())
        best.set_suffixes()
        print("Best config: ", best.get_config())
        best.draw(file='hec.png', with_edge_labels=True, node_size=200, font_size=8)
        
    if test==2:
        config =  {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'CartPoleV1', 'name': 'CartPoleV1', 'value': [0.03498833197860944, 0.20994561633454428, 0.012668159509212712, -0.2705237130920193, 0.047656152654718356], 'links': {0: 'Action1'}, 'env_name': 'CartPole-v1', 'reward': 1.0, 'done': False, 'info': {}}, 'pre1': {'type': 'IndexedParameter', 'name': 'ICV', 'value': 0.20994561633454428, 'links': {0: 'CartPoleV1'}, 'index': 1}, 'pre2': {'type': 'IndexedParameter', 'name': 'ICP', 'value': 0.03498833197860944, 'links': {0: 'CartPoleV1'}, 'index': 0}, 'pre3': {'type': 'IndexedParameter', 'name': 'IPV', 'value': -0.2705237130920193, 'links': {0: 'CartPoleV1'}, 'index': 3}, 'pre4': {'type': 'IndexedParameter', 'name': 'IPA', 'value': 0.012668159509212712, 'links': {0: 'CartPoleV1'}, 'index': 2}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': -0.2705237130920193, 'links': {0: 'ICV', 1: 'ICP', 2: 'IPV', 3: 'IPA'}, 'weights': [0, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0.2705237130920193, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.05046166000036782, 'links': {0: 'CL0C0'}, 'gain': -0.1865332226280776}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -0.005282911840894066, 'links': {0: 'OL0C0'}, 'weights': [0.10469159835121472]}}}
        ind = HPCTIndividual.from_config(config)

        