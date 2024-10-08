#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""




from pct.putils import Timer
from pct.hierarchy import PCTHierarchy
from cutils.paths import get_root_path, get_gdrive
from pct.environment_processing import EnvironmentProcessingFactory

# base = 'steady'
# target = 'variable'


base = 'variable'
# target = 'variable'
target = 'steady'


if base == 'steady':
    filepath = "G:\\My Drive\\data\\ga\\WindTurbine\\RewardError-SummedError-Mode05\\ga--1362.401-s003-4x3-m005-WT0538-bddf277b0f729cc630efacf91b9f494f.properties"

if base == 'variable':
    filepath = "G:\\My Drive\\data\\ga\\WindTurbine\\RewardError-SummedError-Mode02\\ga--2629.009-s001-5x5-m002-WT0416-31ecb19201d49e8c6f9dd1e172bd6944.properties"

verbosed = {'debug': 0, 'hpct_verbose':0}


drive = get_gdrive()
root_path=get_root_path()
results_props = {'comparisons' : True, 'comparisons_print_plots': False}
env_name = 'WindTurbine'
args = {'file': filepath, 'env_name':env_name, 'verbosed':verbosed, 'drive':drive, 'root_path':root_path, 'max' : True} | results_props

environment_properties={'series': target, 'zero_threshold': 1, 'reward_type': 'power', 'keep_history': True, 'range': 'test'}

env_proc = EnvironmentProcessingFactory.createEnvironmentProcessing(f'{env_name}EnvironmentProcessing')
env_proc.set_properties(args=args)

timer = Timer()
timer.start()
env_proc.get_experiment()
rtn = env_proc.results(filepath=filepath, environment_properties=environment_properties)


# print(f'Score={score:0.3f}')
timer.stop()
print(f'Mean time: {timer.mean()}')









