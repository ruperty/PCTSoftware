# https://www.namingcrisis.net/post/2019/03/11/interactive-matplotlib-ipython/
# 

from  os import sep

from utils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual, HPCTEvolveProperties
from pct.architectures import run_from_properties_file
   
# filepath = 'Std-InputsError-RootMeanSquareError-Mode00/test-1level.properties'
# filepath = 'Std-InputsError-RootMeanSquareError-Mode00/ga-000.120-s001-2x3-m0-1690507d808f9d94e8722020c75a1e62.properties'
# filepath = 'Std-TotalError-RootMeanSquareError-Mode00/ga-000.009-s001-2x1-m0-c154bde0a46332caf14754adb39b05ad.properties'

# filename = 'ga-000.019-s001-1x1-m0-1016f98fbd836c361add3860e70bd76d'

# filename = 'ga-000.117-s001-3x3-m0-669248b3e5087c5e888ea90fe2198af4'
# filepath = 'Std-TotalError-RootMeanSquareError-Mode00/'+ filename +'.properties'

test = 10

if test == 0:
    filename = 'ga-000.117-s001-3x3-m0-669248b3e5087c5e888ea90fe2198af4'
    filepath = 'Std-InputsError-RootMeanSquareError-Mode00/'+ filename +'.properties'
    file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath

if test == 1:   
    filename = 'conf-001'
    file = 'output/'+filename+'.config'

if test == 2:
    filename = 'ga-000.113-s001-4x3-m0-669248b3e5087c5e888ea90fe2198af4'
    filepath = 'Std-InputsError-RootMeanSquareError-Mode00/'+ filename +'.properties'
    file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
    move={'CartPoleV1': [-0.4, -0.3],'ICV': [0, 0], 'ICP': [0,  -0.1], 
        'IPV': [-0.0, -0.1],'IPA': [0.0, 0.0], 'Action1ws': [-0.3, -0.3]}
    plots = [ {'plot_items': {'PL1C0ws':'PL1C0ws','PL1C0ws':'ref'}, 'title':'Goal1'},
             {'plot_items': {'IPA':'pa','ICP':'cp'}, 'title':'Inputs'}
            ]




data = [
    [2, 'ga-000.115-s001-2x3-m000-4292b6128e13ac2df54fd2c05a34292e', 'Std00-InputsError-RootMeanSquareError-Mode00', {'CartPoleV1': [-0.4, -0.3],'ICV': [0, 0], 'ICP': [0,  -0.1],         'IPV': [-0.0, -0.1],'IPA': [0.0, 0.0], 'Action1ws': [-0.3, -0.3]}, [ {'plot_items': {'PL1C0ws':'PL1C0ws','PL1C0ws':'ref'}, 'title':'Goal1'},{'plot_items': {'IPA':'pa','ICP':'cp'}, 'title':'Inputs'}], True],
    [3, 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832','Std01-InputsError-RootMeanSquareError-Mode01', {'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0],  'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}, [], True],
    [4,'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832', 'Std01-InputsError-RootMeanSquareError-Mode01',{'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0], 'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}, [], True],
    [5, 'ga-000.130-s001-2x1-m002-9729cd44431b1958b69da786b4ba4f00', 'Std00-InputsError-RootMeanSquareError-Mode02', {'CartPoleV1': [-0.6, -0.1],'ICV': [-0.3, 0.1], 'ICP': [-0.1,  0.2], 'IPV': [0.1, 0.3],'IPA': [0.2, 0.4], 'Action1ws': [-0.65, 0]}, [], True],
    [6, 'ga-000.870-s001-3x6-m001-e8993f3235b484cd5a869600d6d5a374', 'WW01-RewardError-CurrentError-Mode01', {}, [], True]
    ]


if test == 3:
    filename = 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832'
    dir = 'Std01-InputsError-RootMeanSquareError-Mode01'
    filepath = dir + sep + filename +'.properties'
    file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
    move={'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0], 
        'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}
    plots = []

if test == 4:
    filename = 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832'
    dir = 'Std01-InputsError-RootMeanSquareError-Mode01'
    filepath = dir + sep + filename +'.properties'
    file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
    move={'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0], 
        'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}
    plots = []
    
    
def runit(datum):
    filename = datum[1]
    dir = datum[2]
    move = datum[3]
    plots = datum[4]
    min = datum[5]
    filepath = dir + sep + filename +'.properties'
    file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
    
    hep = HPCTEvolveProperties()
    hep.load_db(file)
    render=True

    error_collector_type = hep.db['error_collector_type']
    error_response_type = hep.db['error_response_type']
    error_limit = eval(hep.db['error_limit'])
    runs = eval(hep.db['runs'])
    config = eval(hep.db['config'])
    seed = eval(hep.db['seed'])
    early_termination = eval(hep.db['early_termination'])

    outdir = 'output' + sep + dir
    draw_file = file= outdir + sep  + 'draw-'+ filename + '.png'
    # plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
    # {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
    # plots=[]

    hpct_verbose= False #True
    render=True

    ind, score = HPCTIndividual.run_from_config(config, min, render=render,  error_collector_type=error_collector_type, error_response_type=error_response_type, 
                                                error_properties=None, error_limit=error_limit, steps=runs, hpct_verbose=hpct_verbose, history=True,
                                                seed=seed, early_termination=early_termination, draw_file=draw_file, move=move, plots=plots, suffixes=True, plots_dir=outdir)

    #ind.draw(file='output/' + filename + '.png', node_size=100, font_size=5, with_edge_labels=True)
        
    print("Score: %0.3f" % score)
    #ind.summary()
    print(ind.formatted_config())
    #print(ind.get_config())
    

if test == 5:
    filename = 'ga-000.130-s001-2x1-m002-9729cd44431b1958b69da786b4ba4f00'
    dir = 'Std00-InputsError-RootMeanSquareError-Mode02'
    filepath = dir + sep + filename +'.properties'
    file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
    move={'CartPoleV1': [-0.6, -0.1],'ICV': [-0.3, 0.1], 'ICP': [-0.1,  0.2], 
        'IPV': [0.1, 0.3],'IPA': [0.2, 0.4], 'Action1ws': [-0.65, 0]}
    plots = []




if test == 100:
    for datum in data:
      runit(datum)   
      
if test == 10:
    runit(data[0])


if test ==200:
    hep = HPCTEvolveProperties()
    hep.load_db(file)
    render=True

    error_collector_type = hep.db['error_collector_type']
    error_response_type = hep.db['error_response_type']
    error_limit = eval(hep.db['error_limit'])
    runs = eval(hep.db['runs'])
    config = eval(hep.db['config'])
    seed = eval(hep.db['seed'])
    early_termination = eval(hep.db['early_termination'])

    outdir = 'output' + sep + dir
    draw_file = file= outdir + sep  + 'draw-'+ filename + '.png'
    # plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
    # {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
    # plots=[]


    hpct_verbose= False #True
    render=True

    ind, score = HPCTIndividual.run_from_config(config, render=render,  error_collector_type=error_collector_type, error_response_type=error_response_type, 
                                                error_properties=None, error_limit=error_limit, steps=runs, hpct_verbose=hpct_verbose, history=True,
                                                seed=seed, early_termination=early_termination, draw_file=draw_file, move=move, plots=plots, suffixes=True, plots_dir=outdir)

    #ind.draw(file='output/' + filename + '.png', node_size=100, font_size=5, with_edge_labels=True)
        
    print("Score: %0.3f" % score)
    #ind.summary()
    print(ind.formatted_config())
    #print(ind.get_config())






