# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

import os

from eepct.hpct import HPCTGenerateEvolvers


test = 2

if test == 1:
    file = 'configs'+ os.sep + 'configs-cp.csv'

if test == 2:
    file = 'configs'+ os.sep + 'configs-mc.csv'

if test == 3:
    file = 'configs'+ os.sep + 'configs-ww.csv'




hge = HPCTGenerateEvolvers()  

hge.process_csv(file)
