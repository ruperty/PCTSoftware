#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:01:52 2020

@author: ruperty
"""


#from epct.configs import BaseConfiguration
from pct.environments import VelocityModel
from pct.architectures import LevelKey
from epct.evolvers import EvolverWrapper
from deap import creator

from temp.epctevolver import DynamicEvolver
#from temp.epctstruct import StructureDefinition
#from temp.epctstruct import BinaryOnes


from epct.structure  import BinaryOnes
from epct.structure import StructureDefinition
#from epct.evolvers import DynamicEvolver

inputs = [0]
references = [10]
num_actions=1
seeds={'seed':None, 'eseed':None} # grid [1]
POPULATION_SIZE = 2
debug=0
save_arch_all = False
save_arch_gen = False
attr_mut_pb=1
structurepb=1
runs=10
lower_float = -10
upper_float = 10

env = VelocityModel(name='VModel')

sdargs={'attr_mut_pb':attr_mut_pb}

structure = StructureDefinition(**sdargs)
structure.add_config_parameter(LevelKey.ZERO , 'action', 'ones', BinaryOnes.ALL_ONES)
#structure.add_config_parameter('0', 'perception', 'ones', BinaryOnes.ALLOW_ALL_ZEROS)
structure.add_config_parameter(LevelKey.TOP , 'reference', 'value', references )

structure.add_structure_parameter('lower_float',lower_float)
structure.add_structure_parameter('upper_float', upper_float)
structure.add_structure_parameter('attr_cx_uniform_pb', 0.5)


move={}
figsize=(12,12)
layout={'r':2,'c':1,'p':1, 'o':0}


 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 
        #'alpha':0.6, 'mu':0.5, 'sigma':0.8, 'indpb':0.5,
        'structurepb':structurepb, 'error_limit':100, 'runs':runs, 
        'debug':debug, 'seed':seeds['eseed'], 'hpct_verbose':False}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 1.0, 'p_mutation': 1.0, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen, 
         'select':{'selection_type':'tournament', 'tournsize':25} }
evr = EvolverWrapper(**evwargs)


test = 2




if test==1:
   #[1]
   raw = [[[[1]], [36.07749913455225], [[2.5]], [1]]]

   move={'VModel': [-0.3, -0.4], 'Action1ws': [-1, 0], 'Action2ws': [-0.3, 0], 
         'Input0': [0, 0], 'Input1': [0.8, 0],  'CL0C0': [-0.24, 0]}
   
if test==2:
   #[3, 1] 1 actions
   raw = [[[[1, 0, 1], [1, 0, 0]], [-0.2564132888753856, 0.7368909157301906, -0.23848416591046973], 
           [[-0.7960511956521692], [-0.5013385711146268], [0.46236743355884835]], [[1, 1, 1]]], 
          [[[1], [1], [1]], [-0.6807915752839235], [666]]]
   move={'VModel': [-0.3, -0.2], 'Action1ws': [0, 0],
         'OL0C0ws': [-0.5, 0], 'OL0C1ws': [0.025, 0], 'OL0C2ws': [0.55, 0],
         'RL0C0ws': [-0.1, 0],  'RL0C2ws': [0.1, 0],
         'Input0': [-0.4, 0], 'Input1': [0.2, 0]}
   figsize=(16,16)

if test==3:
   #[3, 1] 2 actions
   raw = [[[[1, 0, 1], [1, 0, 0]], [-0.2564132888753856, 0.7368909157301906, -0.23848416591046973], 
           [[-0.18369789005097203], [-0.6358486724444425], [0.7349181885380365]], [[1, 1, 1], [1, 1, 1]]], 
          [[[1], [1], [1]], [-0.7466015348994606], [666]]]
   
   move={'VModel': [0, -0.2], 'Action1ws': [-0.5, 0], 'OL0C0ws': [-0.55, 0], 
       'OL0C2ws': [0.55, 0], 'Input0': [-0.4, 0], 'Input1': [0.2, 0]}

if test==4:
    #[3, 2, 1] 2 actions
    raw = [[[[1, 0, 0], [0, 1, 1]], [0.7965959400638762, -0.838370705633998, 0.10854093635657214], 
            [[0.4069607845874941, -0.09595815909994854], [0.4501307371644181, -0.6856856768067483], [-0.5239755950669345, -0.7781049440439707]], 
            [[1, 1, 1], [1, 1, 1]]], 
           [[[0, 1], [0, 1], [0, 1]], [0.779152111526018, 0.5451604763676756], 
            [[0.41760144958495693], [-0.9894567895029012]]], 
           [[[1], [1]], [0.6916129364328345], [666]]]
    move={'VModel': [0, -0.2], 'Action1ws': [-0.5, 0], 'OL0C0ws': [-0.35, 0], 'OL0C2ws': [0.35, 0], 
          'OL1C0ws': [-0.2, 0], 'OL1C1ws': [0.2, 0],
          'Input0': [-0.4, 0], 'Input1': [0, 0]}
    figsize=(16,16)


if test==5:
    inputs = [0]
    references = [666, 777]
    raw = [[[[1, 1]], [0.15618260226894076, -0.5878035357209965], [666, 777], [[1, 1]]]]
    move={'VModel': [0, -0.2], 'Action1ws': [-0.2, 0], 'OL0C0ws': [-0.5, 0], 
       'OL0C1ws': [0.75, 0], 'Input0': [-0.4, 0]}
    
    
    
if test==6:
    inputs = [0]
    references = [666, 777]
    raw= [[[[1, 0, 0]], [0.6078006254420971, -0.04847352758224743, 0.22791766811872827], [[0.07738701715535701, 0.7807609840249787], [0.268905565766697, 0.1908730116813393], [-0.20768004708353027, -0.09401026883836794]], [[1, 1, 1], [1, 1, 1]]], [[[1, 0], [1, 0], [0, 1]], [-0.3474132949034705, 0.18191888693611502], [[-0.8300224772493561, 0.30960327801351095], [-0.1864425242296428, 0.10253547125595253]]], [[[0, 1], [1, 0]], [0.025769282714127595, -0.9404961754348353], [666, 777]]]


if test==7:
    # [2,1,2]
    inputs = [0]
    references = [666, 777]
    structure.add_config_parameter('top', 'reference', 'value', references )
    raw = [[[[0, 1]], [0.7286678846318877, 0.9497141212733313], [[-0.9607385812593965], [-0.6253852785486784]], [[1, 1], [1, 1]]], [[[1], [1]], [-0.11691663774434402], [[0.22066632403366881, 0.6605789556551689]]], [[[1, 0]], [-0.8514380143565361, -0.5825333806464852], [666, 777]]]

if test==8:
    raw = [[[[1, 0], [1, 1]], [0.7993565392695623, -0.9638140327190565], [[0.9740994358560522, 0.5654007514587511, -0.3218087042981326], [-0.5739404072383725, 0.34891013944752647, 0.6754021403079287]], [[1, 1], [1, 1]]], [[[1, 1, 0], [1, 0, 0]], [-0.6606117164112248, 0.8219755670161357, -0.5740636100171517], [[-0.2637840011887018], [-0.3194295299960239], [-0.41756942517773066]]], [[[1], [1], [1]], [-0.9217244028061788], [666, 777]]]

if test==9:
    raw=[[[[1, 1, 0], [1, 0, 1]], [-0.48047494851346295, 0.13099776334257873, -0.35077345929643533], [[-0.8379916225308663], [-0.08900762540145002], [-0.2022517079600037]], [[1, 1, 1], [1, 1, 1]]], [[[1], [1], [1]], [0.1250522596145356], [[-0.9625150221772281]]], [[[1]], [-0.378130910153365], [666]]]

if test==10: # force num_nodes = 2
    raw = [[[[1], [1]], [0.28764570736866624], [[-0.3151498114317244]], [[1], [1]]], [[[1]], [-0.36781950459402113], [666]]]

#single = False
single = True

if single:
    #ind1 = creator.Individual([[[[1]], [-0.034876650898288286], [10], [[1]]]])

    ind1 = evr.toolbox.individual()
    print(ind1)
    ind1.fitness.values = evr.toolbox.evaluate(ind1)
    print (ind1.fitness)          

else:
    for ctr in range(40):
        ind1 = evr.toolbox.individual()
        print(ind1)
        ind1.fitness.values = evr.toolbox.evaluate(ind1)
        print ('Fitness ****',ind1.fitness)          


"""
config = BaseConfiguration.from_raw( raw)
pa = DynamicArchitecture(structure=structure, config=config, env=env, input_indexes=inputs) #, error_collector=te)
pa()
hpct = pa.get_hierarchy()
#hpct.set_order('Down')
#hpct.summary()
hpct.draw(move=move, figsize=figsize, with_edge_labels=True, layout=layout)
"""



    
    
    
    
    
    
    
    
    
    