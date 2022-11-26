
import time
import multiprocessing
import pickle

from deap import tools
import random
from deap import base
from deap import creator

from epct.evolvers import CommonToolbox

from epkg.wrappers import SigmoidWrapper
from epkg.evolvers import Evolver
from epkg.evolvers import SigmoidObject
#from epkg.evolvers import CommonToolbox

individual_properties = {'range_limit':20, 'goal':20, 'evaluate_factor':5, 'evaluate_divisor':5, 'scale_limit':5}

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FooIndividual", SigmoidObject, fitness=creator.FitnessMin)#, properties=individual_properties)


toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)


if __name__ == "__main__":
    #processes=4
    #pool = multiprocessing.Pool(processes=processes)
    #toolbox.register("map", pool.map)

    random.seed(1)
    pop_size=100
    gens=100
    processes=1

    evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25, 'indpb':1, 'individual_properties': individual_properties}
    evolver = Evolver(**evolve_properties)
    #evolver.set_toolbox(toolbox)
    wrap = SigmoidWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes)

    #print(dir(creator.FooIndividual))
    test=2
    if test ==1 :
        pop=wrap.create_population()

        print([[p.range, p.scale] for p in pop])

        score, = wrap.toolbox.evaluate(pop[0])
        print(f'score {score:4.3f}')

        print('mutate')
        print(pop[0])
        mutant = wrap.toolbox.mutate(pop[0])
        print(pop[0])
        print(mutant)

        print('mate')
        print(pop[1], pop[2])
        ind1, ind2 = wrap.toolbox.mate(pop[1],pop[2])
        print(pop[1], pop[2])
        print(ind1, ind2)

    if test==2:


        print('Start evolve')
        deap_verbose=False #True #
        tic = time.perf_counter()
        top_ind=wrap.run(gens=gens, deap_verbose=deap_verbose)
        toc = time.perf_counter()
        elapsed = toc-tic
        print(f'Elapsed time: {elapsed:4.4f}')
        print(top_ind)    

    if test==3:
        so = creator.FooIndividual([2,2])
        
        with open('pickled.dat', 'w') as pfile:
            pickle.dump(so, pfile)

