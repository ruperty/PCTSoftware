# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

import os

from eepct.hpct import HPCTGenerateEvolvers

args = "-i 1 -s 93"
test = 5
cmd='impl.evolve_multi'
initial_index=1

if test == 1:
    file = 'configs'+ os.sep + 'configs-cp.csv'

if test == 2:
    file = 'configs'+ os.sep + 'configs-mc.csv'

if test == 3:
    file = 'configs'+ os.sep + 'configs-ww.csv'

if test == 4:
    file = 'configs'+ os.sep + 'configs-pm.csv'

if test == 5:
    file = 'configs'+ os.sep + 'configs-wt.csv'
    # args = "-b -l -o -pl \"[ {'plot_items': {'IYE':'ye'}, 'title':'YawError'},  {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]\" -p evolve-batch -i 3 -c 2"
    args = "-b -l -o -pl scEdges -p test-evolve"
    cmd='impl.evolve_multi_wt'
    # initial_index=1000

hge = HPCTGenerateEvolvers()  
hge.process_csv(file, args, cmdline=cmd, initial_index=initial_index)
