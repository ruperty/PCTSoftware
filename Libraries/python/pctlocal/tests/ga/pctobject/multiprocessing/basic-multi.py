
import multiprocessing
import random
import time

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


def evaluate(individual):
    a = sum(individual)
    b = len(individual)
    return a, 1. / b


IND_SIZE = 50
toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                toolbox.attr_float, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    evolve()

def evolve():
    pop_size = 1000
    ngen=100
    verbose=False

    pop = toolbox.population(n=pop_size)
      
    print('Start evolve')
    tic = time.perf_counter()
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen, verbose=verbose)
    toc = time.perf_counter()
    elapsed = toc-tic
    print(f'Elapsed time: {elapsed:4.4f}')



if __name__ == "__main__":
    processes=8
    pool = multiprocessing.Pool(processes=processes)
    toolbox.register("map", pool.map)

    main()



