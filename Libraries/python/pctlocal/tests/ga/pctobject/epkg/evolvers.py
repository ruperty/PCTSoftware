import random

from deap import tools
from pct.putils import sigmoid
from epct.evolvers import BaseEvolver

from epct.evolvers import CommonToolbox

#from app import clone


def sigmoid_parameters(n):
    return  [random.uniform(0, 1) for iter in range(n)]

class SigmoidObject(object):
    
    def __init__(self, x, properties):
        self.range_limit=properties['range_limit']
        self.goal=properties['goal']
        self.evaluate_factor=properties['evaluate_factor']
        self.evaluate_divisor=properties['evaluate_divisor']
        self.scale_limit=properties['scale_limit']
        
        self.range = x[0]*self.range_limit
        self.scale = x[1]*self.scale_limit

    def __str__(self) -> str:
        return f'SigmoidObject: range {self.range:4.3f} scale {self.scale:4.3f}'

    def list(self):
        return [self.range, self.scale]

    def set(self, rs):
        self.range=rs[0]
        self.scale=rs[1]

    def get_range(self):
        return self.range

    
    def evaluate(self):
        
        shift = 0
        upper = 0
        lower = 0
        zero = 0
        
        goal = self.goal * self.evaluate_factor
        upper =shift + sigmoid(goal, self.range, self.scale)
        lower = shift + sigmoid(self.goal/self.evaluate_divisor, self.range, self.scale)
        zero = sigmoid(0, self.range, self.scale)

        score = abs(self.goal - upper) + abs(self.goal/2 - lower) + shift - zero
        return score,


"""
class CommonToolbox:
    "Toolbox"
    __instance = None
    @staticmethod
    def getInstance():
      ### Static access method. ###
      if CommonToolbox.__instance == None:
         CommonToolbox()
      return CommonToolbox.__instance
    def __init__(self):
      ### Virtually private constructor. ###
      if CommonToolbox.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         CommonToolbox.__instance = self
      self.toolbox = None


    def set_toolbox(self, toolbox):
        self.toolbox=toolbox

    def get_toolbox(self):
        return self.toolbox
"""

class Evolver(BaseEvolver):
        
    def __init__(self, alpha=0, mu=0.1, sigma=0.25, indpb=0.2, individual_properties=None, **cargs):
        super().__init__()
        self.alpha=alpha
        self.mu=mu
        self.sigma=sigma
        self.indpb=indpb
        self.individual_properties=individual_properties

    #def set_toolbox(self, toolbox):
    #    self.toolbox=toolbox

    def evaluate(self, individual):
        return individual.evaluate()

    def create(self, cls):
        #new_individial = SigmoidObject(sigmoid_parameters(2), properties=self.individual_properties)
        #new_individial.append(random.uniform(0, self.range_limit))
        #new_individial.append(random.uniform(0, self.scale_limit))

        return cls(sigmoid_parameters(2), properties=self.individual_properties)

        #return cls(new_individial)

    def mate(self, indvidual1, indvidual2):
        ind1, ind2 = tools.cxBlend(indvidual1.list(), indvidual2.list(), self.alpha)
        if ind1[0]<0 or ind2[0]<0 :
            if ind1[0]<0 :
               ind1[0]=abs(ind1[0])     
            if ind2[0]<0 :
               ind2[0]=abs(ind2[0]) 

        if ind1[1]<0 or ind2[1]<0 :
            if ind1[1]<0 :
               ind1[1]=abs(ind1[1])     
            if ind2[1]<0 :
               ind2[1]=abs(ind2[1]) 
        
        indvidual1.set(ind1)
        indvidual2.set(ind2)

        return indvidual1, indvidual2

    def mutate(self, ind):
        tb = CommonToolbox.getInstance().get_toolbox()
        mutant = tb.clone(ind)
        #mutant = self.toolbox.clone(ind)
        rs, = tools.mutGaussian([ind.range, ind.scale], mu=self.mu, sigma=self.sigma, indpb=self.indpb)      
        #scale = tools.mutGaussian(ind.scale, mu=self.mu, sigma=self.sigma, indpb=self.indpb)      

        mutant.range=rs[0]
        mutant.scale=rs[1]

        return mutant, 

    def create_plot(self):
        return 0
    
    def animate(self, epoch):
        pass