#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:01:52 2020

@author: ruperty
"""


#from epct.configs import BaseConfiguration
from pct.environments import VelocityModel
from pct.architectures import LevelKey
from epct.structure  import BinaryOnes
from epct.evolvers import EvolverWrapper
from deap import creator

#from temp.epctevolver import DynamicEvolver
#from temp.epctstruct import StructureDefinition
#from temp.epctstruct import BinaryOnes


from epct.structure import StructureDefinition
from epct.evolvers import DynamicEvolver
from pct.structure import ArchitectureStructure

inputs = [1, 3, 0, 2]
references = [666]
num_actions=1
seeds={'seed':None, 'eseed':5} # grid [1]
POPULATION_SIZE = 2
debug=3
save_arch_all = False
save_arch_gen = False
attr_mut_pb=1
structurepb=1
lower_float = -10
upper_float = 10
sigma = 10

test = 11
single = False
#single = True
loops = 1

smooth = False 

if single:
    smooth = False
    inputs = [1, 3]
    
if single and test == 11:
    inputs = [1, 3, 4]
    


env = VelocityModel(name='VModel')

sdargs={'attr_mut_pb':attr_mut_pb, 'lower_float':lower_float, 'upper_float': upper_float, 'sigma':sigma }
structure = StructureDefinition(**sdargs)

if smooth:
    structure.set_config_type(LevelKey.ZERO, 'action', 'Float')
    structure.set_config_type(LevelKey.ZERO, 'perception', 'Float')
    structure.set_config_type(LevelKey.N, 'perception', 'Float')
    structure.set_config_type(LevelKey.TOP, 'perception', 'Float')
    structure.set_config_type(LevelKey.ZERO, 'output', 'Smooth')
    structure.set_config_type(LevelKey.N, 'output', 'Smooth')
    structure.set_config_type(LevelKey.TOP, 'output', 'Smooth')

    structure.set_config_parameter(LevelKey.TOP, 'reference', 'value', references )
    modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
    arch_structure = ArchitectureStructure(modes=modes)
    structure.arch_structure=arch_structure

else:
    structure.set_config_parameter(LevelKey.ZERO , 'action', 'ones', BinaryOnes.ALL_ONES)
    #structure.add_config_parameter('0', 'perception', 'ones', BinaryOnes.ALLOW_ALL_ZEROS)
    structure.set_config_parameter(LevelKey.TOP , 'reference', 'value', references )
    structure.set_structure_parameter('top_inputs', [2])

move={}
figsize=(12,12)
layout={'r':2,'c':1,'p':1, 'o':0}


 
evargs={'inputs': inputs, 'env':env, 'num_actions':num_actions, 'references':references, 
        'structure':structure, 
        #'alpha':0.6, 'mu':0.5, 'sigma':0.8, 'indpb':0.5,
        'structurepb':structurepb, 'error_limit':100, 'runs':500, 
        'debug':debug, 'seed':seeds['eseed'], 'hpct_verbose':False}    
stdev = DynamicEvolver(**evargs)

evwargs={'evolver':stdev, 'pop_size':POPULATION_SIZE, 'p_crossover': 1.0, 'p_mutation': 1.0, 
         'save_arch_all': save_arch_all, 'save_arch_gen':save_arch_gen, 
         'select':{'selection_type':'tournament', 'tournsize':25} }
evr = EvolverWrapper(**evwargs)





if test==1:
   #[1]
   raw = [[[[1], [1]], [0.5219248898251512], [666], [[1], [1]]]]

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


if test==11:
    inputs = [0,1,2]
    raw=[[[[1, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 0, 1]], [-7.3115544209730725, -4.814801610789455, -1.8504850505436092, 1.5097436630314793, 10.299759822420393], [[-0.6808282191767624, 3.6451407409008256, 1.1911106858156733, 10.391488929635244], [3.4258065539919444, 6.856536619001108, 3.581441744584704, 1.2665707739053698], [11.624486443337348, 4.847172214194358, -3.6687515823602936, 0.6505548013578566], [-1.5005008849741208, -6.719649466538843, 1.1077134638656028, 1.7198648494212945], [-5.6029296382647935, -5.433697066366367, -4.955966065153415, -9.413480616565941]], [[0, 0, 1, 0, 1]]], [[[0, 0, 1, 1], [1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 0, 1], [1, 0, 0, 1]], [-6.476817712683923, -0.297249141358612, 14.812191053945833, -1.5334810554313087], [[-5.520012570465779, 2.2008219392607913, 1.0374809935952438, 3.553149050097314, -0.6355685044808759, -5.772763920936141], [2.2235900815225325, 15.389139864494267, 8.35152985330945, -2.2757660193331253, 0.35152241119591743, 1.7598293312964497], [9.37192152663802, -8.574431164576078, 5.172845545421129, -5.097714742004729, 5.438160223206797, 0.8701425912739751], [-10.21306171125734, -5.788798814353219, -2.9423807629838965, -8.875925101666, 1.301640787654513, -7.269527948609644]]], [[[0, 1, 0, 0, 0, 1], [0, 1, 1, 0, 1, 1], [0, 1, 0, 0, 1, 1], [1, 0, 0, 1, 1, 0]], [-5.873093879003811, -6.531984052816905, -4.032811234520666, 0.1724607100767237, 5.894505203688475, 3.345704124635132], [[10.696023451260467, 0.3087797380814479, 8.43160056170888, -5.64626011582914, 0.8741970559592964, -5.171074209433108, 6.01022834611793, -8.735415347312276], [-3.4545355761808683, 8.925613805578347, 0.7008026391912381, -0.72494299670403, -3.3109136478080643, 9.537494546597426, 9.457833173321838, -0.16344074854794677], [-0.24191141890262813, -7.346273209661396, -1.4985857326802883, -6.258575426670276, 1.212925864604573, -2.4452371611344725, 7.475079535171293, 3.448107898123709], [6.062612792958465, 3.9576245882678567, -5.131842398234701, -0.3171239970687658, -3.1984401699179577, -1.0969450608683662, -8.425195224016715, 7.195646622478172], [9.31951962691005, 8.85141585996196, -6.855083981748389, -8.941180801122755, -0.5500283477144983, 7.079759521226244, 2.1942479789034373, 2.869365172157929], [-9.148974295605983, -9.304622111549786, 8.698869939615882, -0.4534283436727975, -0.8267975124877154, -0.6595950172807754, -1.413623207378551, -1.8841759598483332]]], [[[1, 0, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 1, 0], [1, 1, 1, 1, 0, 1, 0, 1], [1, 0, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 0]], [3.788763323584753, 0.9184198674837507, -7.810434503505865, 9.602664247370491, 5.218231691615745, 2.257104435424811, 9.461369196111168, 9.954551184561154], [[-8.80074299877353], [1.4342450471773631], [0.4576537518746804], [-4.280651350906197], [1.1058037882037048], [-5.4832940411510345], [3.118090505832418], [-7.093664902322951]]], [[[1]], [-2.475324911797964], [0]]]



if single:
    ind1 = creator.Individual(raw)
    
    #print('ind1 ')
    #for level in ind1:
    #    print('*',level )
    #print()
    
    inda1= evr.toolbox.mutate(ind1)
    #print('inda1')
    #for level in inda1[0]:
    #    print('*',level )

    print('mutated', evr.evolver.mutate_sum)
    print('mutated struct', evr.evolver.mutate_structure_sum)
    print(inda1)
else:
    for ctr in range(loops):
        ind1 = evr.toolbox.individual()
        print(ctr, 'loop', ind1)
        evr.evolver.mutate_sum=0
        evr.evolver.mutate_structure_sum=0
        inda1= evr.toolbox.mutate(ind1)
        print(ctr, 'mutated', evr.evolver.mutate_sum)
        print('mutated struct', evr.evolver.mutate_structure_sum)
        print()


"""
config = BaseConfiguration.from_raw( raw)
pa = DynamicArchitecture(structure=structure, config=config, env=env, input_indexes=inputs) #, error_collector=te)
pa()
hpct = pa.get_hierarchy()
#hpct.set_order('Down')
#hpct.summary()
hpct.draw(move=move, figsize=figsize, with_edge_labels=True, layout=layout)
"""



    
    
    
    
    
    
    
    
    
    