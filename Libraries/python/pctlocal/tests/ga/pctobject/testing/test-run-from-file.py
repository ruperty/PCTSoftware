#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""




from pct.putils import Timer
from pct.hierarchy import PCTHierarchy

plots = []
file = "G:\\My Drive\\data\\ga\\MicroGrid\\RewardError-RootMeanSquareError-Mode04\\ga-000.017-s001-3x5-m004-MG0001-9b7851aa082d1178ee05750f4b5815ce.properties"
timer = Timer()
timer.start()
hierarchy, score = PCTHierarchy.run_from_file(file, env_props=None, seed=1, render=False, move=None, min=True, plots=plots, history=False, 
                                              hpct_verbose= False, runs=None, plots_dir=None, early_termination=False)
print(f'Score={score:0.3f}')
timer.stop()
print(f'Mean time: {timer.mean()}')









