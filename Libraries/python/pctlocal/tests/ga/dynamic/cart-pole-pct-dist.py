#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 12:55:43 2021

@author: ruperty
"""

from pct.architectures import run_from_properties_file


runs=800
#runs=10
render=True
draw=True
    
filename = 'testfiles/ga-000.110-s029-1x1-6655--1760182505815353182-dist.properties'

"""
filename = 'testfiles/ga-001.444-3344-397818342161201780-dist.properties'

nevals = 1
move={'OL0C0ws':[0.25,0], 'CL0C0':[0.25,0]}
plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
        {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
hpct = run_from_properties_file(file=filename,  nevals=nevals, move=move, draw=draw,
                          plots_figsize=(12,5), figsize=(10,10), render=render, runs=runs, plots=plots, print_properties=True)
"""



nevals = 1
plots_figsize=(12,5)
move={'OL0C0sm':[0.25,0], 'CL0C0':[0.25,0]}
plots = [ 
        {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
        {'plot_items': {'ICV':'cv', 'IPV':'pv','IPA':'pa','ICP':'cp'}, 'title':'Inputs'},
        {'plot_items': {'CL0C0':'err'}, 'title':'Error'},          
        {'plot_items': {'Action1ws':'out'}, 'title':'Output'}
        ]   
hpct = run_from_properties_file(file=filename, nevals=nevals, move=move, draw=draw, hpct_verbose=True,
                          plots_figsize=plots_figsize, figsize=(10,10), render=render, runs=runs, plots=plots, print_properties=True)



import numpy as np
import matplotlib.pyplot as plt

plots_figsize=(40,5)

num_items=runs
x = np.linspace(0, num_items-1, num_items)
#style.use('fivethirtyeight')

fig = plt.figure(figsize=plots_figsize)
ax1 = fig.add_subplot(1,1,1)

acty = np.clip(hpct[0].get_history_data()['Action1ws'], -1, 1)
ax1.plot(x, acty, label='Act')

freqy = []
sum=0
for y in acty:
    sum+=y
    freqy.append(sum)

ax1.plot(x, freqy, label='Freq')


plt.title('Action')
plt.legend()
plt.show()
