#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:08:59 2021

@author: ruperty
"""



from pct.architectures import run_from_properties_file

from pct.putils import get_gdrive


import os

seed=None
plots = []
nevals = None
runs=500

root_dir=get_gdrive()
prefix = 'data/ga/'
env = 'PendulumV0/'
type = 'Default/'
move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}

test=43

if test==10:
    # NG
    # Just controls velocity
    file = 'ga-004.694-s027-1x2-3344--6233767676388718113.properties'
    plots = [ {'plot_items': {'IV':'iv','IT':'it'}, 'title':'Input'}]  
    #nevals=1

if test>=20:
    type = 'InErr-Rms/'
    if test==20:
        # only works with plenty of momentum
        file = 'ga-000.793-s057-1x2-3344--1603152508696519723.properties'
        plots = [ {'plot_items': {'IV':'iv','IT':'it'}, 'title':'Input'}]  
        nevals=1
        seed = 58
    
if test>=30:
    type = 'InErr-Rms-AllFlts/'
    if test==30:
        # 19, 20, 21 work well
        file = 'ga-000.270-s009-1x2-3344--6832704055390970200.properties'
        nevals = 3
        seed=19
        #plots = [ {'plot_items': {'IV':'iv','IT':'it','PL0C1ws':'per'}, 'title':'Input'}]
        plots = [ {'plot_items': {'IV':'iv','IT':'it'}, 'title':'Input'}]  

if test>=40:
    type = 'InErr-Rms-AllFlts-Sm/'
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0sm':[-0.65,0],'OL0C1sm':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}

    if test==40:
        # NG
        file = 'ga-000.264-s057-1x2-6655--7181215812947504735.properties'
        nevals = 3
        seed = 12
        
    if test==41:
        # Interesting, whatever position it increases oscillation to above horizontal 
        file =     'ga-000.037-s005-1x2-6655--4525019535786952685.properties'
        nevals = 1
        plots = [ {'plot_items': {'OL0C0sm':'out','CL0C0':'com'}, 'title':'Output0'},
                 {'plot_items': {'OL0C1sm':'out','CL0C1':'com'}, 'title':'Output1'},
                 {'plot_items': {'PL0C0ws':'per0','PL0C1ws':'per1'}, 'title':'Percs'},
             {'plot_items': {'IT':'it','IV':'iv'}, 'title':'Inputs'},
             {'plot_items': {'Action1ws':'act'}, 'title':'Action'}]
    
    
    if test==42:
        # ok for 58
        file = 'ga-000.589-s056-1x2-6655-7368186912913101896.properties'
        #nevals = 1
        print(nevals)
    
    if test==43:
        # good 8, 12
        type = os.sep + 'old' + os.sep + 'older' + os.sep + type 
        file = 'ga-000.825-s008-1x2-6655-5991537330581304229.properties'
        #
        #seed=13
        nevals = 1
        #runs=1000

    
    if test==44:
        # good 12
        file = 'ga-000.958-s009-1x2-6655-431502643459550332.properties'
        #nevals = 1
    
    if test==45:
        # keeps circling in alternate directions
        file = 'ga-001.006-s023-1x2-6655--884094589413920980.properties'
        #nevals = 1
        seed=26

 


if test>=50:
    type = 'InErr-Rms-AllFlts-Sm-Theta/'
    if test==50:
        # NG
        file = 'ga-000.523-s057-1x1-6655--7487932617301201865.properties'
        plots = [ {'plot_items': {'OL0C0sm':'out'}, 'title':'Output'}]  
        move={}

    if test==51:
        # 19, 20, 21 work well
        file = 'ga-000.608-s019-2x1-6655-1143066670096887294.properties'
        plots = [ {'plot_items': {'OL0C0sm':'out'}, 'title':'Output'}]  
        move={}
        #seed=25


if test>=60:
    type = 'InErr-Rms-Alo/'
    move={'IV':[-0.5,0.5],'IT':[0.65,0.3],'OL0C0ws':[-0.65,0],'OL0C1ws':[0.65,0],
          'PendulumV0':[-.5,-0.25], 'Action1ws':[-0.4,0]}
    if test==60:
        # 58 is good
        file = 'ga-000.793-s057-1x2-3344-2972144816251611205.properties'
        #nevals = 1
        
    if test==61:
        # 12 is good
        file = 'ga-000.809-s009-1x2-3344-5581745663976037338.properties'
        #nevals = 1
        seed=12
    
if test>=70:
    type = 'InErr-Rms-Flts/'
    if test==70:
        # 19 is a good one
        file='ga-000.809-s009-1x2-3344-7111951246514006343.properties'
        #plots = [ {'plot_items': {'OL0C0sm':'out0','OL0C1sm':'out1','OL0C2sm':'out2'}, 'title':'Output'}]
        nevals=1
        seed=19   
    if test==71:
        # NI
        file = 'ga-000.068-s031-3344--8521882817245232211.properties'
    if test==72:
        # NI
        file = 'ga-000.147-s009-3344-3164731553821658998.properties'
        nevals=5
    if test==73:
        # works for 9, 10, 11
        file = 'ga-000.270-s009-1x2-3344-859779289552369250.properties'


if test>=80:
    type = 'Rms-AllFlts-Sm-Three/'
    if test==80:
        # NG
        file='ga-000.186-s095-1x3-6655--8148415450089367205.properties'
        plots = [ {'plot_items': {'OL0C0sm':'out0','OL0C1sm':'out1','OL0C2sm':'out2'}, 'title':'Output'},
                 {'plot_items': {'ICT':'ict','IST':'ist','IV':'iv'}, 'title':'Inputs'},
                 {'plot_items': {'Action1ws':'act'}, 'title':'Action'}]
        move={}
        move={'ICT':[-1,0.4],'IST':[-0.6,0.2],'IV':[-0.1, 0],
              'OL0C0sm':[-0.75,0],'OL0C1sm':[0.0,0],'OL0C2sm':[0.75,0],
              'PendulumV0':[-.5,0], 'Action1ws':[-0.4,0]}
        nevals = 1
    
    
print(file)

file_path=os.sep.join((prefix, env, type))
    
#hpct, env = 
run_from_properties_file(root_dir=root_dir, path=file_path, file=file, nevals=nevals, move=move, 
                          runs=runs, draw=True,   plots=plots, seed=seed, print_properties=True)








