#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 11:59:42 2020

@author: ruperty
"""

    
import random
from deap import creator

from epct.evolvers import BaseEvolver
from epct.configs import BaseConfiguration
from pct.architectures import ControlUnitIndices
from pct.architectures import LevelKey

from epct.structure import BinaryOnes

from pct.errors import BaseErrorCollector

from temp.pctarch import DynamicArchitecture
from temp.epctconfig import DynamicConfigurationStructure
from temp.epctconfig import DynamicConfiguration



