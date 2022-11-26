import array
import multiprocessing
import random
import sys
import time

if sys.version_info < (2, 7):
    print("mpga_onemax example requires Python >= 2.7.")
    exit(1)

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == "__main__":
    random.seed(64)
    
    # Process Pool of 4 workers
    pool = multiprocessing.Pool(processes=8)
    toolbox.register("map", pool.map)
    
    pop = toolbox.population(n=5000)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    print('Start evolve')
    tic = time.perf_counter()
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, 
                        stats=stats, halloffame=hof, verbose=False)
                        
    toc = time.perf_counter()
    elapsed = toc-tic
    print(f'Elapsed time: {elapsed:4.4f}')

    pool.close()