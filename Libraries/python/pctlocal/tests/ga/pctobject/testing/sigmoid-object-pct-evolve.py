
import time
import multiprocessing
import pickle

from deap import tools
import random
from deap import base
from deap import creator

from epct.evolvers import EvolverWrapper
from epct.evolvers import CommonToolbox

from epkg.evolvers import Evolver
from epkg.evolvers import SigmoidObject

individual_properties = {'range_limit':20, 'goal':20, 'evaluate_factor':5, 'evaluate_divisor':5, 'scale_limit':5}

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", SigmoidObject, fitness=creator.FitnessMin)


toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)



if __name__ == "__main__":

    random.seed(1)
    pop_size=500
    gens=40
    processes=8

    evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25, 'indpb':1, 'individual_properties': individual_properties}
    evolver = Evolver(**evolve_properties)
    #evolver.set_toolbox(toolbox)
    evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes)

    #print(dir(creator.FooIndividual))
    test=2

    if test==2:

        print('Start evolve')
        verbose=False #False #True #
        deap_verbose=False #True #
        tic = time.perf_counter()
        top_ind=evr.run(gens=gens, deap_verbose=deap_verbose, verbose=verbose)
        toc = time.perf_counter()
        elapsed = toc-tic
        print(f'Elapsed time: {elapsed:4.4f}')
        print("Best Score: %0.3f" % evr.best_score())
        print("Best Ind: ", evr.best())
        #print(top_ind)    
