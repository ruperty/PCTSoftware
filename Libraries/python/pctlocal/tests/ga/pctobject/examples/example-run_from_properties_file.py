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

test = 3

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
#ind.pretty_print()





