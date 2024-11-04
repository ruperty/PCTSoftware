#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""


from os import sep

from pct.putils import Timer, PCTRunProperties
from pct.hierarchy import PCTHierarchy
from pct.errors import BaseErrorCollector
import os
import random

# plots = "scEdges,scFitness"
plots = False
render=True
runs=250
early_termination = True
hpct_verbose = False
history = True
suffixes=False
plots_dir = "c:/tmp/ARC"
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
plots_figsize=(15,4)
run = True #False


# file = "G:\My Drive\data\ga\ARC\FitnessError-MovingAverageError-Mode19\ga-062.617-s003-1x1-m019-ARC0375-7b4718a3de3ff677ac24d839feaf0507-consolidated.properties"

file = "G:\My Drive\data\ga\ARC\FitnessError-MovingAverageError-Mode19\ga-000.386-s002-1x1-m019-ARC0427-e6024b9e73a754e3dc8d56773c55056f.properties"
timer = Timer()
timer.start()
# hierarchy, score = PCTHierarchy.run_from_file(file, env_props=None, seed=1, render=render, move=None, min=True, plots=plots, history=False,                                               hpct_verbose= False, runs=runs, plots_dir=None, early_termination=False)

prp = PCTRunProperties()
prp.load_db(file)

error_collector_type = prp.db['error_collector_type'].strip()
error_response_type = prp.db['error_response_type']
error_limit = eval(prp.db['error_limit'])
environment_properties = eval(prp.db['environment_properties'])
# environment_properties['index'] = 0

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

# overidding values from G:\My Drive\data\ga\ARC\FitnessError-MovingAverageError-Mode19\ga-000.500-s001-1x1-m019-ARC0328-9799d017b565995c04c518b7e15c0e1c-consolidated.properties

hierarchy.get_node(0,0).get_function('reference').set_value(3)
print(hierarchy.get_node(0,0).get_function('reference').get_value())

percs = hierarchy.get_node(0,0).get_function('perception')
# print(percs)
counter = 1
for link in percs.get_links():
    percs.weights[counter-1] = 0
    if link.get_name() == 'IE' :
        percs.weights[counter-1] = -1
    if link.get_name() == 'II':
        percs.weights[counter-1] = 1
    # print(f"{counter}: {link.get_name()} - {percs.weights[counter-1]}")
    counter += 1

output = hierarchy.get_node(0,0).get_function('output')
output.gain = 0.147
print(output.get_config())

actions = hierarchy.get_postprocessor()
for action in actions:
    for action in actions:
        action.smooth_factor = random.uniform(0.05, 0.95)
    # print(action.get_config())

# hierarchy.summary()
# run = False

if run:
    hierarchy.run(runs, hpct_verbose)

    if history:
        if plots:
            plots = hierarchy.get_plots_config(plots, "xx")
            
            for plot in plots:
                plotfile=None
                if plots_dir:
                    plotfile = plots_dir + sep + plot['title'] + '-' + str(hierarchy.get_namespace()) + '.png'
                fig = hierarchy.hierarchy_plots(title=plot['title'], plot_items=plot['plot_items'], figsize=plots_figsize, file=plotfile)
                import matplotlib.pyplot as plt
                plt.close(fig)  # Close the figure here

env.close()
# print(f'Score={score:0.3f}')
timer.stop()
print(f'Mean time: {timer.mean()}')









