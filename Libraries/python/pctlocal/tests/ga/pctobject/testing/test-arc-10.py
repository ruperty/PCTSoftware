#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""




from pct.putils import Timer, PCTRunProperties
from pct.hierarchy import PCTHierarchy
from pct.errors import BaseErrorCollector

plots = []
render=True
runs=10
early_termination = True
hpct_verbose = False
history = False
suffixes=False
# file = "G:\\My Drive\\data\\ga\\MicroGrid\\RewardError-RootMeanSquareError-Mode04\\ga-000.017-s001-3x5-m004-MG0001-9b7851aa082d1178ee05750f4b5815ce.properties"

file = "G:\My Drive\data\ga\ARC\FitnessError-MovingAverageError-Mode19\ga-062.617-s003-1x1-m019-ARC0375-7b4718a3de3ff677ac24d839feaf0507-consolidated.properties"
timer = Timer()
timer.start()
# hierarchy, score = PCTHierarchy.run_from_file(file, env_props=None, seed=1, render=render, move=None, min=True, plots=plots, history=False,                                               hpct_verbose= False, runs=runs, plots_dir=None, early_termination=False)

prp = PCTRunProperties()
prp.load_db(file)

error_collector_type = prp.db['error_collector_type'].strip()
error_response_type = prp.db['error_response_type']
error_limit = eval(prp.db['error_limit'])
environment_properties = eval(prp.db['environment_properties'])
error_properties = prp.get_error_properties()

if runs==None:
    runs = eval(prp.db['runs'])
config = eval(prp.db['config'])
seed = eval(prp.db['seed'])

if early_termination is None:
    early_termination = eval(prp.db['early_termination'])

hierarchy = PCTHierarchy.from_config_with_environment(config, seed=seed, history=history, suffixes=suffixes, environment_properties=environment_properties)
env = hierarchy.get_preprocessor()[0]
env.set_render(render)
env.early_termination = early_termination
env.reset(full=False, seed=seed)
if error_collector_type is not None:
    error_collector = BaseErrorCollector.collector(error_response_type, error_collector_type, error_limit, min, properties=error_properties)
    hierarchy.set_error_collector(error_collector)
if hpct_verbose:
    hierarchy.summary()
    print(hierarchy.formatted_config())

hierarchy.get_node(0,0).get_function('reference').set_value(3)
print(hierarchy.get_node(0,0).get_function('reference').get_value())

percs = hierarchy.get_node(0,0).get_function('perception')
# print(percs)
counter = 1
for link in percs.get_links():
    print(f"{counter}: {link.get_name()} - {link.get_value()} {percs.weights[counter-1]}")
    counter += 1

# hierarchy.summary()

# hierarchy.run(runs, hpct_verbose)


env.close()
# print(f'Score={score:0.3f}')
timer.stop()
print(f'Mean time: {timer.mean()}')









