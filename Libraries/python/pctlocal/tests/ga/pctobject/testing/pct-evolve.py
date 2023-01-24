
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
    # arch.set(HPCTARCH.ZERO, HPCTARCH.ACTION, HPCTARCH.VARIABLE_PROPERTIES, {'lower': lower, 'upper': upper})
    # arch.set(HPCTARCH.ZERO, HPCTARCH.REFERENCE, HPCTARCH.VARIABLE_PROPERTIES, {'lower': lower, 'upper': upper})
    # arch.set(HPCTARCH.TOP, HPCTARCH.OUTPUT, HPCTARCH.VARIABLE_PROPERTIES, {'lower': lower, 'upper': upper})
    # arch.set(HPCTARCH.N, HPCTARCH.REFERENCE, HPCTARCH.VARIABLE_PROPERTIES, {'lower': lower, 'upper': upper})
    # arch.set(HPCTARCH.N, HPCTARCH.OUTPUT, HPCTARCH.VARIABLE_PROPERTIES, {'lower': lower, 'upper': upper})
    # arch.set(HPCTARCH.ZERO, HPCTARCH.PERCEPTION, HPCTARCH.VARIABLE_TYPE, 'Binary')

    # env = VelocityModel(name='VM', mass=250, num_links=2, indexes=4)
    env_name = 'VelocityModel'
    env_inputs_indexes=[0,2,1,3]
    env_inputs_names=['IP', 'IV', 'IC', 'IF']
    references=[11, 2]

    test=1
    if test ==1 :
        # choice 2 [2] Add level 0 with 5 nodes
        sd = 2
        no_inputs=False #True
    if test ==2:
        # choice 2 [4, 4, 2] Add level 2 with 3 nodes
        sd=16
        no_inputs=True

    error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'
    seed, debug, pop_size, processes, runs, nevals, num_actions=sd, 3, 100, 1, 500, 3, 2
    min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 5, 1, 5, 100
    #min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 2, 1, 3, 100

    if no_inputs:
        zerolevel_inputs_indexes=None
        toplevel_inputs_indexes=None
    else:
        zerolevel_inputs_indexes=[0,1]
        toplevel_inputs_indexes=[2,3]

    random.seed(seed)

    # individual_properties = {'range_limit':20, 'goal':20, 'evaluate_factor':5, 'evaluate_divisor':5, 'scale_limit':5}
    environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes,
        'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env_name, 'num_actions':num_actions, 'references':references}
    # evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25, 'indpb':1, 'attr_mut_pb':1, 'attr_cx_uniform_pb':0.5, 'structurepb':1}
    evolve_properties = {'attr_mut_pb':0.8,'structurepb':1, 'attr_cx_uniform_pb':0.5, 'alpha':0.5}

    hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit, 'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit, 'lower_float':-100, 'upper_float':100 }    
    #hpct_structure_properties ={  'lower_float':-100, 'upper_float':100 }    
    # hpct_run_properties ={ 'error_collector_type':error_collector_type, 'error_response_type': error_response_type,
    #     'error_properties':error_properties, 'error_limit': error_limit, 'runs':runs, 'nevals':nevals,
    #     'history':False, 'hpct_verbose':False,  'debug':debug, 'seed':seed}    

    hpct_run_properties ={ 'hpct_verbose':False, 'debug':debug , 'runs':runs, 'nevals':nevals}    

    evolver_properties = {'environment_properties':environment_properties, 
        'evolve_properties':evolve_properties,  
        'hpct_structure_properties':hpct_structure_properties,
        'hpct_run_properties':hpct_run_properties,
        # 'individual_properties': individual_properties, 
        'arch': arch}

    evolver = HPCTEvolver(**evolver_properties)

    evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes, p_mutation=0.25)

    test=10
    
    if test==1:
        ind = evr.toolbox.individual()
        ind.set_suffixes()
        ind.summary()
        ind.draw(file='hpct.png', with_edge_labels=True)
        config = ind.get_parameters_list()
        print(config)


    if test==2:
        ind1 = evr.toolbox.individual()     
        #ind1.summary()  
        tic = time.process_time() 
        ind1.fitness.values = evr.toolbox.evaluate(ind1)
        toc = time.process_time()
        elapsed = toc-tic
        print(f'Evaluate time: {elapsed:4.4f}')
        print (ind1.fitness)  

    if test==3:
        ind = evr.toolbox.individual()   
        #FunctionsList.getInstance().report()
        print(ind.get_grid())

        ind.draw(file='hpct_b4_mutate.png', node_size=200)
        #print(id(ind.get_preprocessor()[1]))
        # print(ind.get_preprocessor()[0].__repr__())
        # ind.get_preprocessor()[0].summary()
        #ind.summary()    
        func1 = ind.get_node(0,0).get_function_from_collection(CUF.COMPARATOR)
        #print(func1.get_name(), func1.__repr__())
        #ind1 = evr.toolbox.individual()   
        #ind1.summary()    
        #ind.run(steps=3, verbose=True)

        tic = time.process_time() 
        ind1 = evr.toolbox.mutate(ind)[0]
        toc = time.process_time()

        grid = ind1.get_grid()
        print(grid)        
        config = ind1.get_config()
        func = ind1.get_node(0,0).get_function_from_collection(CUF.COMPARATOR)
        #print(func.get_name(), func.__repr__())

        #FunctionsList.getInstance().report()

        func1 = ind.get_node(0,0).get_function_from_collection(CUF.COMPARATOR)
        #print(func1.get_name(), func1.__repr__())

        func = ind.get_node(0,0).get_function_from_collection(CUF.OUTPUT)
        print('Ind output')
        print(func.get_name(), func.__repr__())
        print(func)
        print('Ind action')
        action0 = ind.get_postprocessor()[0]
        print(action0.get_name(), action0.__repr__())
        action0.summary()
        link = action0.get_links()[0]
        print(link, link.__repr__())
        #link.summary()


        ind.run(steps=3, verbose=True)
        #ind.summary()
        #ind1.summary()    

        func = ind.get_node(0,0).get_function_from_collection(CUF.OUTPUT)
        print('Ind output')
        print(func.get_name(), func.__repr__())
        func.summary()
        # func = ind.get_node(0,1).get_function_from_collection(CUF.OUTPUT)
        # print(func.get_name(), func.__repr__())
        # func.summary()

        print('Ind action')
        action0 = ind.get_postprocessor()[0]
        print(action0.get_name(), action0.__repr__())
        action0.summary()
        link = action0.get_links()[0]
        print(link.get_name(), link.__repr__())
        link.summary()

        print()
        func1 = ind1.get_node(0,0).get_function_from_collection(CUF.OUTPUT)
        print('Ind1 output')
        print(func1.get_name(), func1.__repr__())
        func1.summary()

        # func1 = ind1.get_node(0,1).get_function_from_collection(CUF.OUTPUT)
        # print(func1.get_name(), func1.__repr__())
        # func1.summary()
        print('Ind action')
        action0 = ind.get_postprocessor()[0]
        print(action0.get_name(), action0.__repr__())
        action0.summary()
        link = action0.get_links()[0]
        print(link.get_name(), link.__repr__())
        link.summary()


        print('Ind1 action')
        action0 = ind1.get_postprocessor()[0]
        print(action0.get_name(), action0.__repr__())
        action0.summary()
        link = action0.get_links()[0]
        print(link, link.__repr__())
        #link.summary()



        elapsed = toc-tic
        #print(id(ind1.get_preprocessor()[1]))
        #print(ind1.get_preprocessor()[0].__repr__())
        #ind1.get_preprocessor()[0].summary()
        #ind1.summary() 
        print(f'Mutate time: {elapsed:4.4f}')
        ind1.draw(file='hpct_b5_mutate.png', node_size=200)

        #print (ind1.fitness)  




    if test==4:
        ind = evr.toolbox.individual()   
        print(ind.get_preprocessor()[0])
        print(len(ind.get_preprocessor()[0].get_links()))
        # ind1 = evr.toolbox.mutate(ind)[0]
        # print(ind1.get_preprocessor()[0].__repr__())
        # print(ind1.get_preprocessor()[0])

        ind = evr.toolbox.individual()   
        print(ind.get_preprocessor()[0])
        print(len(ind.get_preprocessor()[0].get_links()))
        # ind1 = evr.toolbox.mutate(ind)[0]
        # print(ind1.get_preprocessor()[0].__repr__())
        # print(ind1.get_preprocessor()[0])

    if test==5:
        ind1 = evr.toolbox.individual()   
        #ind.draw(file='hpct_b4_mutate.png', node_size=200)

        ind2 = evr.toolbox.individual()   

        tic = time.process_time() 
        child1, child2 = evr.toolbox.mate(ind1, ind2)
        toc = time.process_time()


        elapsed = toc-tic
        print(f'Mate time: {elapsed:4.4f}')

    if test==6:
        #pop = evr.toolbox.population(n=pop_size)
        for ctr in range(100):
            
            ind = evr.toolbox.individual(grid=[1,2])     
            #ind1.summary()  
            ind1 = evr.toolbox.mutate(ind, choice=1)[0]
            ind1.fitness.values = evr.toolbox.evaluate(ind1)        
            print(ctr, ind1.fitness.values)

    if test==7:
        evolver.debug=0

        for seed in range(1000):
            random.seed(seed)
            print('Start evolve', seed)            
            ind = evr.toolbox.individual(grid=[1, 2])     
            ind1 = evr.toolbox.mutate(ind, choice=1, add_level=0, add_nodes=1)[0]


    if test==8:
        evolver.debug=2
        random.seed(1)
        ind = evr.toolbox.individual(grid=[4, 5, 1, 2])     
        #ind.draw(file='t8_hpct_b4_mutate.png', node_size=200)
        ind.summary()
        ind1 = evr.toolbox.mutate(ind, choice=4, remove_level=1, remove_nodes=2)[0]
        #ind1.draw(file='t8_hpct_b5_mutate.png', node_size=200)
        print(ind1.get_grid())
        ind1.fitness.values = evr.toolbox.evaluate(ind1)        


    if test==9:
        random.seed(2)
        ind = evr.toolbox.individual(grid=[4, 4, 1, 2])     
        ind.summary()
        ind.draw(file='t9_ind.png', node_size=200)
        # ind.fitness.values = evr.toolbox.evaluate(ind)        

        #FunctionsList.getInstance().report()
        ind1 = evr.toolbox.mutate(ind, choice=3, remove_level=2)[0]
        #FunctionsList.getInstance().report()
        ind1.summary()
        ind1.draw(file='t9_ind1.png', node_size=200)
        ind1.fitness.values = evr.toolbox.evaluate(ind1)        



    if test==10:
        evolver.debug=0

        for seed in range(1):
            random.seed(3)
            print('Start evolve', seed)
            verbose=  True #False #True #
            deap_verbose=False #True #
            gens=10
            tic = time.perf_counter()
            top_ind=evr.run(gens=gens, deap_verbose=deap_verbose, verbose=verbose)
            toc = time.perf_counter()
            elapsed = toc-tic
            best=evr.best()
            print(f'Elapsed time: {elapsed:4.4f}')
            print("Best Score: %0.3f" % evr.best_score())
            print("Best Ind: ", best.get_parameters_list())
            print("Best grid: ", best.get_grid())
            best.summary()
            #print(top_ind)    



    if test==11:
        evolver.debug=0

        for seed in range(1000):
            random.seed(seed)
            print('Start evolve', seed)  

            #ind1 = evr.toolbox.individual(grid=[5, 1, 2])   
            ind1 = evr.toolbox.individual()   
            ind2 = evr.toolbox.individual()               

            child1, child2 = evr.toolbox.mate(ind1, ind2)

            child1_1 = evr.toolbox.mutate(child1)[0]
            child2_1 = evr.toolbox.mutate(child2)[0]

            child1_1.fitness.values = evr.toolbox.evaluate(child1_1)   
            child2_1.fitness.values = evr.toolbox.evaluate(child2_1)   

            print(child1_1.fitness.values, child2_1.fitness.values)



    if test==12:
        evolver.debug=2
        seed = 10
        random.seed(seed)
        print('Start evolve', seed)  

        ind1 = evr.toolbox.individual(grid=[5, 1, 2])   
        ind2 = evr.toolbox.individual()   
        
        # ind1.draw(file='ind1.png', node_size=200)
        # ind2.draw(file='ind2.png', node_size=200)

        child1, child2 = evr.toolbox.mate(ind1, ind2)

        child1.draw(file='child1.png', node_size=200)
        child2.draw(file='child2.png', node_size=200)

        child1_1 = evr.toolbox.mutate(child1, choice=1, add_level=1, add_nodes=2)[0]
        child2_1 = evr.toolbox.mutate(child2, choice=1, add_level=1, add_nodes=2)[0]

        child1_1.draw(file='child1_1.png', node_size=200)
        child2_1.draw(file='child2_1.png', node_size=200)


        child1_1.fitness.values = evr.toolbox.evaluate(child1_1)   
        child2_1.fitness.values = evr.toolbox.evaluate(child2_1)   
        print(child1_1.fitness.values, child2_1.fitness.values)

        # clhild1.fitness.values = evr.toolbox.evaluate(child1)   
        # child2.fitness.values = evr.toolbox.evaluate(child2)   
        # print(chid1.fitness.values, child2.fitness.values)



    if test==13:
        evolver.debug=3
        random.seed(2)
        ind = evr.toolbox.individual()     
        for i in range(100):
            print('ctr', i, ind.get_grid())
            ind = evr.toolbox.mutate(ind)[0]
            # if i == 6:
            #     ind.summary()
            ind.validate()

            ind.fitness.values = evr.toolbox.evaluate(ind)
            print('score', ind.fitness.values)     

