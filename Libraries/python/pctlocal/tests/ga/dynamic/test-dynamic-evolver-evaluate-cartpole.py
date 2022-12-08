#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:01:52 2020

@author: ruperty
"""


#from epct.configs import BaseConfiguration
from pct.environments import CartPoleV1
from pct.architectures import LevelKey
from pct.architectures import DynamicArchitecture
from epct.evolvers import EvolverWrapper
from epct.configs import DynamicConfiguration
from epct.structure import BinaryOnes

from deap import creator

#from temp.epctevolver import DynamicEvolver
#from temp.epctstruct import StructureDefinition

from epct.evolvers import DynamicEvolver
from epct.structure import StructureDefinition

inputs = [1, 0, 3, 2]
references = [0]
num_actions=1
seeds={'seed':None, 'eseed':2} 
POPULATION_SIZE = 2
debug=0

display_env=True
save_arch_all = False
save_arch_gen = False
hpct_verbose=False



attr_mut_pb=1

structurepb=0.5
runs=500
lower_float = -10
upper_float = 10

env = CartPoleV1(name='CartpoleV1', render=True)

sdargs={'attr_mut_pb':attr_mut_pb, 'lower_float':lower_float, 'upper_float': upper_float, 
        'levels_limit': 5, 'columns_limit': 8}


structure = StructureDefinition(references=references,**sdargs)
structure.set_config_parameter(LevelKey.TOP , 'perception', 'ones', BinaryOnes.AT_LEAST_ONE )

top_inputs=[2]
structure.set_structure_parameter('top_inputs', top_inputs)

print(structure.get_config())



move={}
figsize=(12,12)
layout={'r':2,'c':1,'p':1, 'o':0}


 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 'structurepb':structurepb, 'error_limit':100, 'runs':runs, 
        'debug':debug, 'seed':seeds['eseed'], 'hpct_verbose':hpct_verbose}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 1.0, 'p_mutation': 1.0, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen, 
         'display_env':display_env,'select':{'selection_type':'tournament', 'tournsize':25} }
evr = EvolverWrapper(**evwargs)


test = 5

move={}

if test==1:
   raw = [[[[1, 0], [1, 0], [1, 0], [1, 1]], [-6.546736285882238, -9.103232717855912], [[1], [-1.6252635774790236]], [[1, 1]]], [[[0], [1]], [0.889772263378402], [0]]]
   move={'Input0':[-0.7,0.1],'Input1':[-0.3,-0.05],'Input2':[0.18,-0.12],'Input3':[0.6,-0.2],'World':[-.9,-0.25],
          'Action1ws':[-0.515,-0.1], 'OL0C0ws':[-0.25,0], 'OL0C1ws':[0.25,0]}
   #move={'VModel': [-0.3, -0.4], 'Action1ws': [-1, 0], 'Action2ws': [-0.3, 0], 
   #      'Input0': [0, 0], 'Input1': [0.8, 0],  'CL0C0': [-0.24, 0]}
   
   
if test==2:
   raw =    [[[[1], [1], [0], [1]], [2.306991093978107], [0], [[1]]]]
   
if test==3:
    raw = [[[[1], [0], [1], [1]], [-1.1076644566332312], [0], [[1]]]]
    move={'Input0':[-0.7,0.6],'Input1':[-0.3,0.4],'Input2':[0.18,0.2],'Input3':[0.7,0],
          'World':[-.5,-0.25], 'Action1ws':[-0.5,0]}
   
if test==4:
    raw = [[[[7.658684867984963], [1.1130313365600184], [7.751568016823082], [5.629262405947559]], [-2.9429894771355043], [0], [[1]]]]
    move={'Input0':[-0.7,0.6],'Input1':[-0.3,0.4],'Input2':[0.18,0.2],'Input3':[0.7,0],
          'World':[-.5,-0.25], 'Action1ws':[-0.5,0]}

if test==5:
    raw = [[[[0, 1, 0, 0, 1], [1, 0, 1, 0, 1]], [-7.390763134694144, -4.22946131797576, -2.6514551094159504, 2.047097465890523, 9.924490487532584], [[0.31913045492552616, 4.980614361186383, 1.8376074914935807, 10.33629085115888], [3.930936802863756, 7.268792496029049, 3.602639441097349, 0.9746193680409186], [11.668694650866918, 3.484610237081074, -2.2993959876025487, 1.1184730431872736], [-0.39480897744503185, -7.87109374771551, 1.7108190065881006, 0.7845719437972605], [-4.9611725023749464, -5.557452972684743, -5.411082463107778, -9.014812688394297]], [[1, 1, 0, 1, 0]]], [[[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 1, 1, 0], [0, 1, 1, 0]], [-5.8034035076364265, -2.291608497336007, 15.715273398275786, -0.8609185685242312], [[-5.477891508620873, 2.3898095558832626, 1.768818808472001, 4.948935403661013, -0.11656144406349167, -4.133095816527465], [1.7821009965718533, 15.3279029447039, 9.140767797984429, -1.5767240350255767, -0.9886670543662466, 0.4214626848894809], [10.820693421264084, -8.747857021831276, 5.8806687094987735, -3.9793271642650754, 7.400233550893851, -0.17151697735885607], [-10.055527743891897, -6.084897775577392, -3.0724768431518528, -8.116442760603242, 2.5192278437434563, -6.103558843831634]]], [[[1, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0], [1, 0, 1, 1, 0, 0], [0, 1, 1, 0, 0, 1]], [-5.86874814110375, -6.0736405617550435, -4.075552014503511, 0.8965475061840357, 7.048739594438536, 4.787497995464191], [[10.968581289356118, 0.3831515037373321], [-3.4574770351576563, 9.22365620162302], [-0.06804511734518676, -6.797843565594787], [6.856161507420422, 4.949063441384439], [10.324460788843554, 8.641684171882218], [-7.767682087438846, -9.097265690010348]]], [[[1, 0], [1, 1], [1, 1], [1, 0], [1, 1], [1, 0]], [3.788763323584753, 0.9184198674837507], [[-8.80074299877353], [1.4342450471773631]]], [[[1]], [-2.1175756325138453], [0]]]

    #raw = [[[[1, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 0, 1]], [-7.3115544209730725, -4.814801610789455, -1.8504850505436092, 1.5097436630314793, 10.299759822420393], [[-0.6808282191767624, 3.6451407409008256, 1.1911106858156733, 10.391488929635244], [3.4258065539919444, 6.856536619001108, 3.581441744584704, 1.2665707739053698], [11.624486443337348, 4.847172214194358, -3.6687515823602936, 0.6505548013578566], [-1.5005008849741208, -6.719649466538843, 1.1077134638656028, 1.7198648494212945], [-5.6029296382647935, -5.433697066366367, -4.955966065153415, -9.413480616565941]], [[0, 0, 1, 0, 1]]], [[[0, 0, 1, 1], [1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 0, 1], [1, 0, 0, 1]], [-6.476817712683923, -0.297249141358612, 14.812191053945833, -1.5334810554313087], [[-5.520012570465779, 2.2008219392607913, 1.0374809935952438, 3.553149050097314, -0.6355685044808759, -5.772763920936141], [2.2235900815225325, 15.389139864494267, 8.35152985330945, -2.2757660193331253, 0.35152241119591743, 1.7598293312964497], [9.37192152663802, -8.574431164576078, 5.172845545421129, -5.097714742004729, 5.438160223206797, 0.8701425912739751], [-10.21306171125734, -5.788798814353219, -2.9423807629838965, -8.875925101666, 1.301640787654513, -7.269527948609644]]], [[[0, 1, 0, 0, 0, 1], [0, 1, 1, 0, 1, 1], [0, 1, 0, 0, 1, 1], [1, 0, 0, 1, 1, 0]], [-5.873093879003811, -6.531984052816905, -4.032811234520666, 0.1724607100767237, 5.894505203688475, 3.345704124635132], [[10.696023451260467, 0.3087797380814479, 8.43160056170888, -5.64626011582914, 0.8741970559592964, -5.171074209433108, 6.01022834611793, -8.735415347312276], [-3.4545355761808683, 8.925613805578347, 0.7008026391912381, -0.72494299670403, -3.3109136478080643, 9.537494546597426, 9.457833173321838, -0.16344074854794677], [-0.24191141890262813, -7.346273209661396, -1.4985857326802883, -6.258575426670276, 1.212925864604573, -2.4452371611344725, 7.475079535171293, 3.448107898123709], [6.062612792958465, 3.9576245882678567, -5.131842398234701, -0.3171239970687658, -3.1984401699179577, -1.0969450608683662, -8.425195224016715, 7.195646622478172], [9.31951962691005, 8.85141585996196, -6.855083981748389, -8.941180801122755, -0.5500283477144983, 7.079759521226244, 2.1942479789034373, 2.869365172157929], [-9.148974295605983, -9.304622111549786, 8.698869939615882, -0.4534283436727975, -0.8267975124877154, -0.6595950172807754, -1.413623207378551, -1.8841759598483332]]], [[[1, 0, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 1, 0], [1, 1, 1, 1, 0, 1, 0, 1], [1, 0, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 0]], [3.788763323584753, 0.9184198674837507, -7.810434503505865, 9.602664247370491, 5.218231691615745, 2.257104435424811, 9.461369196111168, 9.954551184561154], [[-8.80074299877353], [1.4342450471773631], [0.4576537518746804], [-4.280651350906197], [1.1058037882037048], [-5.4832940411510345], [3.118090505832418], [-7.093664902322951]]], [[[1]], [-2.475324911797964], [0]]]

 
    move={}

    
#single = False
single = True

if single:
    DynamicArchitecture.draw_raw(raw, move=move, inputs=inputs, top_input_indexes=top_inputs, summary=False)
    ind1 = creator.Individual(raw)
    ind1.fitness.values = evr.toolbox.evaluate(ind1)
    #print (ind1.fitness.valid)    # True
    print (ind1.fitness)          # (2.73, 0.2)


else:
    for ctr in range(40):
        ind1 = evr.toolbox.individual()
        print(ctr, ind1)
        
        ind1.fitness.values = evr.toolbox.evaluate(ind1)
        #print (ind1.fitness.valid)    # True
        print (ind1.fitness)          # (2.73, 0.2)
        
        #evr.evolver.mutate_sum=0
        #evr.evolver.mutate_structure_sum=0
        #inda1= evr.toolbox.mutate(ind1)
        #print(ctr, 'mutated', evr.evolver.mutate_sum)
        #print('mutated struct', evr.evolver.mutate_structure_sum)
        print()




env.close()


    
    
    
    
    
    
    
    
    
    