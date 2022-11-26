
from deap import tools
from deap import creator
from deap import algorithms
from deap import base
import numpy as np
import random
import multiprocessing

from epkg.evolvers import SigmoidObject


class SigmoidWrapper(object):
    
    def __init__(self, evolver=None, pop_size=10, toolbox=None, processes=1,
        select={'selection_type':'tournament', 'tournsize':None}, p_crossover = 0.9, p_mutation = 0.1):
        #creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        #creator.create("FooIndividual", SigmoidObject, fitness=creator.FitnessMin, properties=individual_properties)

        self.toolbox=toolbox
        self.evolver=evolver        
        self.pop_size=pop_size
        self.p_crossover = p_crossover   # probability for crossover
        self.p_mutation = p_mutation   # probability for mutating an individual
        
        if processes>1:
            pool = multiprocessing.Pool(processes=processes)
            toolbox.register("map", pool.map)

        #toolbox.register("indices", sigmoid_parameters, 2)
        #toolbox.register("individual", tools.initIterate, creator.FooIndividual, toolbox.indices)

        toolbox.register("individual", self.create(), creator.FooIndividual)

        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.evaluate())
        toolbox.register("mate", self.mate())
        toolbox.register("mutate", self.mutate())

        self.hof = tools.HallOfFame(1)

        if select['selection_type'] == 'tournament':
            if 'tournsize' in select.keys():
                tournsize=select['tournsize']
            else:
                tournsize=None           
            if tournsize==None:
                tournsize=(int)(pop_size/4)
            toolbox.register("select", tools.selTournament, tournsize=tournsize)


        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("mean", np.mean)
        self.stats.register("min", np.min)
        self.stats.register("max", np.max)
        self.stats.register("std", np.std)
        #self.evolver.set_toolbox(toolbox)

    def create(self):
        return self.evolver.create

    def evaluate(self):
        return self.evolver.evaluate

    def mate(self):
        return self.evolver.mate

    def mutate(self):
        return self.evolver.mutate

    def create_population(self):
        self.pop = self.toolbox.population(n=self.pop_size)
        return self.pop


    def run(self, gens=25, verbose=False, deap_verbose=False, log=False):

        self.pop = self.create_population()
        self.pop, logbook = algorithms.eaSimple(self.pop, self.toolbox, cxpb=self.p_crossover,
                    mutpb=self.p_mutation,  ngen=gens, halloffame=self.hof, stats=self.stats, verbose=deap_verbose)
        top_ind = tools.selBest(self.pop, k=1)[0]      

        return top_ind