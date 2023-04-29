# https://www.namingcrisis.net/post/2019/03/11/interactive-matplotlib-ipython/
# 

from os import makedirs
from  os import sep

from utils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual, HPCTEvolveProperties
from pct.architectures import run_from_properties_file
   

test = 10


  
def runit(datum):
    env  = datum[1]
    filename = datum[2]
    dir = datum[3]
    move = datum[4]
    plots = datum[5]
    min = datum[6]
    filepath = dir + sep + filename +'.properties'
    file = get_gdrive() + 'data/ga/'+ env +'/' + filepath
    
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
    makedirs(outdir, exist_ok=True)
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
    #print(ind.formatted_config())
    #print(ind.get_config())



data = [
    [0, 'CartPoleV1', 'ga-000.115-s001-2x3-m000-4292b6128e13ac2df54fd2c05a34292e', 'Std00-InputsError-RootMeanSquareError-Mode00', {'CartPoleV1': [-0.4, -0.3],'ICV': [0, 0], 'ICP': [0,  -0.1],         'IPV': [-0.0, -0.1],'IPA': [0.0, 0.0], 'Action1ws': [-0.3, -0.3]}, [ {'plot_items': {'PL1C0ws':'PL1C0ws','PL1C0ws':'ref'}, 'title':'Goal1'},{'plot_items': {'IPA':'pa','ICP':'cp'}, 'title':'Inputs'}], True],
    [1, 'CartPoleV1', 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832','Std01-InputsError-RootMeanSquareError-Mode01', {'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0],  'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}, [], True],
    [2, 'CartPoleV1', 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832', 'Std01-InputsError-RootMeanSquareError-Mode01',{'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0], 'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}, [], True],
    [3, 'CartPoleV1', 'ga-000.130-s001-2x1-m002-9729cd44431b1958b69da786b4ba4f00', 'Std00-InputsError-RootMeanSquareError-Mode02', {'CartPoleV1': [-0.6, -0.1],'ICV': [-0.3, 0.1], 'ICP': [-0.1,  0.2], 'IPV': [0.1, 0.3],'IPA': [0.2, 0.4], 'Action1ws': [-0.65, 0]}, [], True],
    [4, 'WebotsWrestler', 'ga-000.870-s001-3x6-m001-e8993f3235b484cd5a869600d6d5a374', 'WW01-RewardError-CurrentError-Mode01', {}, [], True], # 0.906 (10) good, stable, 1 ref
    [5, 'WebotsWrestler', 'ga-000.365-s001-7x10-m004-0216b6fa50e383e602a9d3ad2739f69a', 'WW01-11-RewardError-CurrentError-Mode04', {}, [], False], # 0.365 (10) bad, 2 ref
    [6, 'WebotsWrestler', 'ga-000.661-s001-5x7-m003-6dfb7f2bec54a72660f78251bc02b092', 'WW01-09-RewardError-CurrentError-Mode03', {}, [], False], # 0.661 (10) poor, kneeling, 2 ref
    [7, 'WebotsWrestler', 'ga-001.559-s001-3x7-m002-6a329c48b9f246288ff944df11e21a98', 'WW01-07-RewardError-CurrentError-Mode02', {}, [], False], # 1.631 (10) good, dragging right leg but looks stable, 2 ref *
    [8, 'WebotsWrestler', 'ga-000.554-s001-3x5-m001-396442a24782fbf5d945531d302e886c', 'WW01-05-RewardError-CurrentError-Mode01', {}, [], False], # 0.554 (10) jittery, 1 ref
    [9, 'WebotsWrestler', 'ga-001.848-s001-4x8-m001-c589fa85b67d512975680f7265d52149', 'WW01-04-RewardError-CurrentError-Mode01', {}, [], False], # 1.547 (10) good, dragging left leg, 2 ref *
    [10, 'WebotsWrestler', 'ga-001.884-s001-2x4-m001-d63ec5dffda565b2c064458630f1643d', 'WW01-06-RewardError-CurrentError-Mode01', {}, [], False], # 1.620 (10) weird, kneeling on right leg, though could be stable, 4 ref
    [11, 'WebotsWrestler', 'ga-002.149-s001-2x7-m001-a71b1e63499693a10f3adff35f0bb04d', 'WW01-04-RewardError-CurrentError-Mode01', {}, [], False] # 2.033 (10) jittery, not too stable, 2 ref *


    ]


if test == 100:
    for datum in data:
      runit(datum)   
      
if test == 10:
    # good ones 4, 9, 11, weird 10
    runit(data[5])







