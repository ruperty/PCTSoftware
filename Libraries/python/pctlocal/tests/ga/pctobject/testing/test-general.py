import json, socket, psutil, random
import numpy as np

from pct.putils import FunctionsList
from pct.putils import floatListsToString
from pct.functions import Constant, Proportional
from pct.hierarchy import PCTHierarchy
#from pct.network import ConnectionManager

from epct.structure import ParameterFactory

test = 14


if test == 14:

    random.seed(1)
    smooth_factor_parameter = ParameterFactory.createParameter('Float')
    smooth_factor_parameter.set_properties({'lower_float':0, 'upper_float':1})

    # evolve_properties1 = {'alpha':0.5}
    ep = {'mu':0.25, 'sigma':0.5, 'attr_mut_pb':1}
    smooth_factor = smooth_factor_parameter.get_list(1)[0]
    print(smooth_factor)

    for i in range(100):
        smooth_factor, mut = smooth_factor_parameter.mutate_single(smooth_factor, ep)
        if smooth_factor > 1:
            print(i, smooth_factor)

if test == 13:

    for i in range(700,711):
        
        print(i)
        v = np.exp(i)

    # value = -0.0468
    # print(f'{value:4.2f}')

    # wtss = [0]
    # weights = [float(f'{wt:4.3}') for wt in wtss]


if test == 12:
    const = Constant(1, name='const')
    ns = const.namespace
    print(const())
    pr = Proportional(name='pr', links=const, namespace=ns)
    pr.summary()
    assert pr() == 1



    

if test == 11:
    hpct = PCTHierarchy(1,1)
    o = hpct.get_function(0, 0, "output")
    o.gain = .5
    hpct.summary()
    p = hpct.get_function(0, 0, "perception")
    p.set_value(1)
    p.summary()
    out = o.get_value()
    print(out)
    o.summary()

    
if test == 10:
    fl = [[[-0.125555], 0.543666]]
    fl = [2,2]
    print(floatListsToString(fl, 3))
    
if test == 9:

    for p in psutil.process_iter():
        #    if 'webots-bin' in p.name() and port_text in p.cmdline() :
        # print(p.memory_info().rss, p.cmdline(), p.name())   
        print(p.memory_info().rss,  p.name())   
                # return p.memory_info().rss
        
        

if test == 8:
    print(socket.getdefaulttimeout())

if test == 7:
    dateTimeObj=1
    results = f'# Date {dateTimeObj}\n' + '# Result'+'\n'
    print(results)
    
    logs = '###  gen  pop      min       mean        max   mut muts  timing'
    print(logs)
    print('###    1    4   -0.006      0.004      0.023   75%  75%   1.345')

if test == 6:
    dict = {'sync': 'true'}
    json_object = json.dumps(dict) 
    print(json_object)
    init = {'a':1}
    init.update(dict)
    print(init)

if test == 5:
    cm = ConnectionManager.getInstance()
    cm.set_port(6667)
    cm.connect()



if test == 4:
    import platform
    print(platform.node())

if test == 3:
    import os    
    home_dir = os.path.expanduser( '~' )
    print(home_dir)
    
    from datetime import datetime
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d-%H%M%S")
    print("date and time:",date_time)
    
if test == 0:
    str_list = ['a', 'b']
    formatted = ' '.join(str_list)
    print(formatted)
        
if test == 1:
    # simple delete
    c = Constant(11)
    FunctionsList.getInstance().report()
    FunctionsList.getInstance().delete_function(c.namespace, c.name)
    FunctionsList.getInstance().report()


def format_list(alist, formatted):
    if isinstance(alist[0], float):
        # str_list = ['[']
        # str_list.append([f'{num:0.3f}' for num in alist])
        # str_list.append(']')
        return [round(num,3) for num in alist]
    else:
        for item in alist:    
            formatted.append(format_list(item, formatted))
            
    
            
                            
if test == 2:
    lists =  [[-0.20280445403006664, -0.30561588932079725], [-1.109996740904304, -0.31602389805294073, -0.5475055584320996]]
    formatted=[]
    format_list(lists,formatted)
    print(formatted)