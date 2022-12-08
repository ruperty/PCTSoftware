#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 19:58:30 2021

@author: ruperty
"""

from epct.configs import DynamicConfiguration

from pct.architectures import LevelKey
from pct.environments import DummyModel
from epct.structure  import BinaryOnes
from epct.configs import BaseConfiguration
from pct.architectures import DynamicArchitecture
from epct.structure import StructureDefinition


dc = DynamicConfiguration.convert_to_raw_from_proportional_raw(
    [[[[1, 0], [1, 0], [1, 0], [1, 1]], [-6.546736285882238, -9.103232717855912], [[1, 1]]], [[[0, 1]], [0.889772263378402], [[1], [-1.6252635774790236]], [0]]],
    verbose=True)


print()
print(dc)

move={'Input0':[-0.7,0.1],'Input1':[-0.3,-0.05],'Input2':[0.18,-0.12],'Input3':[0.6,-0.2],'World':[-.9,-0.25],
          'Action1ws':[-0.515,-0.1], 'OL0C0ws':[-0.25,0], 'OL0C1ws':[0.25,0]}


DynamicConfiguration.draw_raw(dc, move=move, summary=False)


# [[[[1, 0], [1, 0], [1, 0], [1, 1]], [-6.546736285882238, -9.103232717855912], [[1], [-1.6252635774790236]], [[1, 1]]], [[[0], [1]], [0.889772263378402], [0]]]





