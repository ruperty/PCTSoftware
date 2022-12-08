#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:56:21 2020

@author: ruperty
"""


from epct.configs import DynamicConfiguration
from epct.configs import BaseConfiguration
from pct.architectures import LevelKey
from pct.architectures import DynamicArchitecture
from epct.structure  import BinaryOnes
from pct.structure  import ArchitectureStructure

import random

from epct.structure  import StructureDefinition

#from temp.epctstruct import StructureDefinition


random.seed(1)

debug=False

test=1

structure = StructureDefinition()
structure.set_config_parameter(LevelKey.ZERO, 'action', 'ones', BinaryOnes.ALL_ONES)
structure.set_structure_parameter('lower_float',-100)
structure.set_structure_parameter('upper_float',100)
arch_structure = ArchitectureStructure()


if test==1:
    ttest=5

    if ttest==1:
        inputs=[2]
        num_actions=1
        grid=[2] 
        references=[2,1]
        
        pc = DynamicConfiguration(num_inputs=len(inputs), num_actions=num_actions, grid=grid, 
                                  references=references)
        config = pc()
        #if debug: 
        print('config', len(config), config)
        print()
        
    if ttest==2:
        inputs=[2]
        num_actions=2
        grid=[1] 
        references=[2]
        
        pc = DynamicConfiguration(num_inputs=len(inputs), num_actions=num_actions, grid=grid, 
                                  references=references)
        config = pc()
        print('config', len(config), config)
        print()
        
    if ttest==3:
        inputs=[2, 3]
        num_actions=2
        grid=[2, 3, 2] 
        references=[333, 444]
        
        pc = DynamicConfiguration(num_inputs=len(inputs), num_actions=num_actions, grid=grid, 
                                  references=references)
        config = pc()
        print('config', len(config), config)


    if ttest==4:
        inputs=[1, 0, 3, 2]
        num_actions=1
        grid=[2, 1] 
        references=[333]
        structure.set_config_parameter(LevelKey.TOP, 'reference', 'value', references )

        pc = DynamicConfiguration(num_inputs=len(inputs), num_actions=num_actions, grid=grid, 
                                  references=references, structure=structure)
        config = pc()
        print('config', len(config), config)

    if ttest==5:
        # smooth 
        inputs=[2, 3]
        num_actions=2
        grid=[2, 3, 2] 
        references=[333, 444]
        
        structure.set_config_type(LevelKey.ZERO, 'output', 'Smooth')
        structure.set_config_type(LevelKey.N, 'output', 'Smooth')
        structure.set_config_type(LevelKey.TOP, 'output', 'Smooth')

        structure.set_config_parameter(LevelKey.TOP, 'reference', 'value', references )

        pc = DynamicConfiguration(num_inputs=len(inputs), num_actions=num_actions, grid=grid, 
                                  references=references, structure=structure)
        
        modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
        arch_structure = ArchitectureStructure(modes=modes)
        structure.arch_structure=arch_structure

        
        config = pc()
        #print('config', len(config), config)
        for level in config:
            print(level, config[level])
        


    if ttest==6:
        # smooth 
        inputs=[2]
        num_actions=2
        grid=[1] 
        references=[2]
        
        structure.set_config_type(LevelKey.ZERO, 'output', 'Smooth')
        #structure.set_config_type(LevelKey.N, 'output', 'Smooth')
        #structure.set_config_type(LevelKey.TOP, 'output', 'Smooth')
        structure.set_config_parameter(LevelKey.TOP, 'reference', 'value', references )

        pc = DynamicConfiguration(num_inputs=len(inputs), num_actions=num_actions, grid=grid, 
                                  references=references, structure=structure)
        modes =  {LevelKey.ZERO:6, LevelKey.N:6,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
        arch_structure = ArchitectureStructure(modes=modes)
        structure.arch_structure=arch_structure
        print(structure.get_config())

        config = pc()
        print('config', len(config), config)
        print()

    raw  = DynamicConfiguration.dict_to_raw(config)
    DynamicArchitecture.draw_raw(raw, arch_structure=arch_structure, structure=structure, 
                                  figsize=(12,12), summary=True)


if test==2:

    orig_config = {'parameters': {}, 'level0': [[[1, 0, 1]], [241.64006427764332, 15.711983735211517, 59.066023814182955], [[1, 0, 0]]], 'level1': [[[0, 0, 1], [1, 1, 1]], [-28.939441716645348, 71.78038808899879], [[-39.10349458380049, 22.045694371271942], [36.97327980164832, 69.47037895335438], [37.24898485777277, 27.288736567555148]]], 'level2': [[[1, 0]], [-70.09742737637771], [[1], [13.536911135358622]], [1]]}

    config = {'parameters': {'lower_float': -100, 'upper_float': 100}, 'level0': [[[1, 0, 1]], [-48.23682528100597, 57.54240653885029, 67.89788408381847], [[0, 1, 1]]], 'level1': [[[0, 0, 1]], [75.77861886070627], [[-2.481296741140355], [-80.38067579432438], [65.80705878985557]], [1]]}

    print(orig_config)
    print(config)
    BaseConfiguration.copy_data_from_larger(orig_config, config)
    print(config)







if test==3:

    from pct.environments import VelocityModel
    from epct.batch import initial_config
    from pct.putils import FunctionsList
    from epct.batch import change_structure
    from epct.batch import testing_structure
    from epct.batch import create_new_config
    from epct.batch import testing_config
    from epct.batch import create_new_arch


    modes= ['addnode', 'addlevel', 'removelevel', 'removenodes']
    raws = [    
    [[[[[1]], [67.35416681586418], [[1]], [666]]], [88], 0, 0, 0, 1], # inputs, num_nodes, level, remove_level, remove_nodes
    [[[[[1, 0]], [-4.29964834890464, 37.05412979575067], [[1, 0]]], [[[0, 1]], [84.49448300658264], [[-63.929079254529306], [-83.97596112397123]], [666]]],[8],2 ,0, 0, 1],
    [[[[[1, 0], [1, 1]], [45.40338888303913, -47.49060200982651], [[0, 1], [1, 1]]], [[[1, 0], [0, 1], [0, 1]], [-49.86213601067775, -76.52517617113793, 58.46471448110918], [[49.31092547776123, 36.80491803735387, 19.930679352838013], [44.05156655365113, -66.73470627728699, 89.76250108960434]]], [[[0, 1, 1], [0, 1, 1]], [28.227094017927726, -54.93595393165438], [[50.66033945625355, -3.2482803501785895], [0.026979212227075777, 61.38056695171272], [-88.54417981589538, 24.60208702256068]], [666, 777]]],[88,99],2 ,1, 1, 2],
    [[[[[0, 1, 1, 0, 0, 1, 1, 1, 0]], [-32.47526289613046, -92.89691840748627, -56.06602116364752, -86.82578498433813, -63.17198029235773, -7.0074710904952155, -58.98919746226241, -55.57230503909434, -84.16854557282132], [[1, 1, 1, 1, 1, 1, 1, 0, 1]], [666, 999, 999, 999, 999, 999, 999, 999, 999]]],[88],0, 0, 0, 1],
    [[[[[1, 0], [1, 1]], [45.40338888303913, -47.49060200982651], [[0, 1], [1, 1]]], [[[0, 0], [0, 1], [0, 1]], [-49.86213601067775, -76.52517617113793, 58.46471448110918], [[49.31092547776123, 36.80491803735387, 19.930679352838013], [44.05156655365113, -66.73470627728699, 89.76250108960434]]], [[[0, 1, 1], [0, 1, 1]], [28.227094017927726, -54.93595393165438], [[50.66033945625355, -3.2482803501785895], [0.026979212227075777, 61.38056695171272], [-88.54417981589538, 24.60208702256068]], [666, 777]]],[88,99],4, 1, 1, 1],
    [[[[[0, 1], [0, 1]], [43.10316736228367, -35.24781902464089], [[1, 0]]], [[[1, 0]], [-22.743072513747563], [[29.475237757888237], [-56.48433098799168]], [9]]],[88,99],2, 0, 0, 1],
    [[[[[1, 0], [1, 1]], [45.40338888303913, -47.49060200982651], [[0, 1], [1, 1]]], [[[0, 0], [0, 1], [0, 1]], [-49.86213601067775, -76.52517617113793, 58.46471448110918], [[49.31092547776123, 36.80491803735387, 19.930679352838013], [44.05156655365113, -66.73470627728699, 89.76250108960434]]], [[[0, 1, 1], [0, 1, 1]], [28.227094017927726, -54.93595393165438], [[50.66033945625355, -3.2482803501785895], [0.026979212227075777, 61.38056695171272], [-88.54417981589538, 24.60208702256068]], [666, 777]]],[88,99],2, 0, 0, 1]
    ]
    
    for mode in modes:
        for i in range(len(raws)):
            print(mode, i+1)
            FunctionsList.getInstance().clear()
            env = VelocityModel(name='VMorig')
            orig_config = initial_config(env, raws[i])
            struct = change_structure(mode, raws[i], i+1)
            testing_structure(mode, struct, i+1)
            config=create_new_config(orig_config, mode, struct)
            testing_config(mode, config, i+1)
            create_new_arch(config, env, raws[i][1])
            print()




















