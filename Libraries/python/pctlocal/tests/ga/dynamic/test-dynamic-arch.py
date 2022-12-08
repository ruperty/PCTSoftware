#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 19:45:13 2021

@author: ruperty
"""


from pct.structure import ArchitectureStructure
from pct.architectures import LevelKey
from pct.environments import VelocityModel


from pct.architectures import DynamicArchitecture
#from pct.structure import StructureDefinition

#from temp.pctarch import DynamicArchitecture
#from temp.epctstruct import StructureDefinition

references = [666]
inputs = [0]


env = VelocityModel(name='VModel')

modes =  {LevelKey.ZERO:3, LevelKey.N:3,LevelKey.TOP:5,LevelKey.ZEROTOP :5}
structure = ArchitectureStructure(modes=modes)

#structure = ArchitectureStructure()

#structure = StructureDefinition()
#structure.add_config_parameter(LevelKey.ZERO, 'action', 'ones', BinaryOnes.ALL_ONES)
#structure.add_config_parameter(LevelKey.TOP, 'reference', 'value', references )


config = {'parameters': {}, 'level0': [[[1.0864011617580416, -1.0342161642584196], [-8.899524671308557, -8.976856229389936]], [-0.7295091920311653, -4.460573287694404], [0, 0], [[-4.146713118740296, 1.2794655139677662]]]}


print(config)
#config = {'level0': [[[1]], [62.82423385532463], [[0]], [1]], 'parameters': {}}

for key in config.keys():
    print(key, config[key])
pa = DynamicArchitecture(structure=structure, config=config, env=env, input_indexes=inputs) #, error_collector=te)
pa()
hpct = pa.get_hierarchy()
#hpct.summary()

#hpct.run(steps=1, verbose=True)
move={'VModel': [-0.2, -0.3],'Input0': [-0.3, 0],'OL0C0ws': [-0.4, 0],'OL0C1ws': [0.6, 0]}
hpct.draw(move=move, with_edge_labels=True, figsize=(10,10))
