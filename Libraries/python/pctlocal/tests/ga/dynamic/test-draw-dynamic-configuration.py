#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:01:52 2020

@author: ruperty
"""

# https://matplotlib.org/3.1.0/gallery/color/named_colors.html


from epct.configs import BaseConfiguration
from epct.configs import DynamicConfigurationStructure

from pct.structure import ArchitectureStructure
from pct.environments import VelocityModel
from epct.structure  import BinaryOnes
from pct.architectures import LevelKey


#from temp.epctstruct import StructureDefinition
#from temp.pctarch import DynamicArchitecture

from epct.structure import StructureDefinition
from pct.architectures import DynamicArchitecture

inputs = [1, 3]
references = [666]

env = VelocityModel(name='MountainCarContinuousV0')

#structure = StructureDefinition()
#structure.add_config_parameter(LevelKey.ZERO, 'action', 'ones', BinaryOnes.ALL_ONES)
#structure.add_config_parameter(LevelKey.TOP, 'reference', 'value', references )


structure = ArchitectureStructure()
move={}
figsize=(12,12)
layout={'r':2,'c':1,'p':1, 'o':0}

test = 12


if test==1:
   #[1]
   raw = [[[[1.1], [1.2]], [0.5219248898251512], [666], [[1.3], [1.4]]]]
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
    raw = [[[[1.1, 0.2, 0.3], [0, 1, 1]], [0.7965959400638762, -0.838370705633998, 0.10854093635657214], 
            [[0.4069607845874941, -0.09595815909994854], [0.4501307371644181, -0.6856856768067483], [-0.5239755950669345, -0.7781049440439707]], 
            [[1, 1, 1], [1, 1, 1]]], 
           [[[0, 1], [0, 1], [0, 1]], [0.779152111526018, 0.5451604763676756], 
            [[0.41760144958495693], [-0.9894567895029012]]], 
           [[[1], [1]], [0.6916129364328345], [666]]]
    move={'VModel': [0, -0.2], 'Action1ws': [-0.5, 0], 'OL0C0ws': [-0.35, 0], 'OL0C2ws': [0.35, 0], 
          'OL1C0ws': [-0.2, 0], 'OL1C1ws': [0.2, 0],
          'Input0': [-0.4, 0], 'Input1': [0, 0]}
    figsize=(20,20)


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
    inputs = [1,0,3,2]
    references = [0]
    num_actions=1
    raw = [[[[0, 0, 1, 0, 0, 1, 1, 0], [0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0], [0, 1, 1, 0, 0, 1, 1, 1]], [9.953124009261686, 9.913832833123983, 6.804310989857235, 4.156192429958988, -3.6944556596890017, -5.406681967841889, -4.219201053715958, -8.595530008801482], [[5.32575772820814, -1.992003901630179, 6.931672437623572, -2.26972936588131, 9.160847666396272, 6.946195466056089, -9.98910125888859, -5.805651705407778], [8.205438562083629, -0.6002544797266722, 9.607178823485842, -2.051512238414377, -8.539233123326042, 2.5890982446804838, 5.570217173533017, -4.604488262997146], [-8.257116032956597, -3.3482874907330418, 9.281524331875282, 5.160810339875177, -7.640166411608984, -5.0722410221374, -7.9790738208658984, -8.802131941178466], [5.940430236879482, -6.446437436032677, 1.1859028322078977, -1.0515024499795693, -6.186311694192678, 4.637884314287007, -7.380658325667606, 2.8743024742233416], [-7.669840247205888, -1.5848876550715811, -5.742686539818211, -4.604100456188034, 9.41858112437383, 6.0682300616414295, -3.91709700258021, 7.697302254979416], [-5.785795571311212, -2.1145072585589126, 7.087538034024611, 2.8367131318092103, -7.993344956322341, 9.786033950203446, -5.7351326284495485, -4.834448842767591], [5.453793795456463, -3.4208914890454007, -4.073504748021072, -8.532028932231517, -8.197656540761395, 1.65469596335104, -5.139741597248753, 2.025676871638776], [-2.565919068135436, -0.9358379055230195, 9.18269344974626, -0.3255093347490998, 1.491424908598951, 7.330513356044445, -6.343445684426296, -6.917293621478784]], [[1, 1, 1, 1, 1, 1, 1, 1]]], [[[0, 0, 0, 0, 0, 1, 1, 0], [1, 0, 0, 0, 0, 1, 0, 1], [1, 1, 1, 1, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 0, 0], [0, 1, 1, 1, 0, 0, 0, 1], [0, 1, 1, 0, 0, 0, 1, 1]], [4.740109897325178, 8.00391762498758, 4.7417626883312, 4.073812384835547, 5.86533352186968, 8.300051591040798, -2.9633180670549253, 3.70291910667396], [[-4.464080062231776], [-6.617421789045725], [-0.9870109749806399], [-4.496743541101833], [-5.718392456934431], [-1.7203039850967983], [2.514671164747373], [-0.12249266026209504]]], [[[1], [1], [1], [1], [1], [1], [1], [1]], [2.985727308916079], [0]]]

if test==9:    
    inputs = [1,0,3,2]
    references = [0]
    num_actions=1
    raw=[[[[0, 1], [1, 1], [1, 0], [1, 1]], [5.8763461493110825, 0.1136743553379631], [[9.026256011619111], [7.518837500570186]], [[1, 1]]], [[[1], [1]], [1.251970881114719], [0]]]


if test==11:    
    inputs = [1,0,3,2]
    references = [0]
    num_actions=1
    raw=[[[[1, 0], [1, 0], [1, 0], [1, 1]], [-6.546736285882238, -9.103232717855912], [[1], [-1.6252635774790236]], [[1, 1]]], [[[0], [1]], [0.889772263378402], [0]]]


if test==12:    
    inputs =  [0, 1]    
    references = [0]
    inputs_names =  ['IP', 'IV']
    top_inputs =  [0]    
    layout=None
    raw=[[[[1.198998468541923, 0.611754204266719, 1.7677170617308327]], [[3.4341117624938446, 0.9640180391471003], [-0.05887913748075457, 0.9825724309247841], [2.573053595563823, 0.38627004681749383]], [[1.137932637787607], [2.1164923802567945], [3.232824945210956]], [[3.0946849052258356, 3.1217341494218322, -0.45836455321778186]]], [[[0.5030156034214709]], [[3.9129702537620084, 0.4591226113143575]], [0.45]]]
    
    
    modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
    structure = ArchitectureStructure(modes=modes)
    
    figsize=(12,14)
    move={'MountainCarContinuousV0': [-0.6, -0.5], 'Action1ws': [-0.3, -0.3], 
          'OL0C0sm': [-0.55, -0.2], 'OL0C1sm': [0, -0.2], 'OL0C2sm': [0.55, -0.2], 
          'OL1C0sm': [0, -0.1], 'IV': [-0.8, 0.05], 'IP': [-1.1, 0.5], 'CL1C0': [0, 0.1]}


config = BaseConfiguration.from_raw( raw)
#print(config)
pa = DynamicArchitecture(structure=structure, config=config, env=env, input_indexes=inputs, top_input_indexes=top_inputs, suffixes=True, inputs_names=inputs_names) #, error_collector=te)
pa()
hpct = pa.get_hierarchy()
#hpct.set_order('Down')

#hpct.summary()




"""
hpct.get_preprocessor()[1].set_name('ICV')
hpct.get_preprocessor()[2].set_name('ICP')
hpct.get_preprocessor()[3].set_name('IPV')
hpct.get_preprocessor()[4].set_name('IPA')

move={'CartpoleV1': [-0.3, -0.4],'ICV': [-0.25, -0.15], 'ICP': [-0.08,  -0.15], 
      'IPV': [-0.05, -0.15],'IPA': [0.1, -0.15], 'OL0C0p': [-0.25, -0.05], 
      'OL0C1p': [0.27, -0.05], 'OL1C0p': [0.2, 0], 'Action1ws': [-0.4, -0.2]}
"""
if layout == None:
    hpct.draw(move=move, figsize=figsize, with_edge_labels=True)
else:
    hpct.draw(move=move, figsize=figsize, with_edge_labels=True, layout=layout)

#move={'CartpoleV1': [-0.3, -0.2],'ICV': [-0.25, 0], 'ICP': [-0.08,  0], 
#      'IPV': [-0.05, 0],'IPA': [0.1, 0], 'Action1ws': [-0.4, 0]}

#hpct.draw_nodes()
#hpct.draw_nodes(move=move)






    
    
    
    
    
    
    
    
    
    