# https://www.namingcrisis.net/post/2019/03/11/interactive-matplotlib-ipython/
# 

from os import makedirs
from  os import sep

from cutils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual, HPCTEvolveProperties
from pct.architectures import run_from_properties_file
from pct.network import ClientConnectionManager   

test = 30


  
def runit_old(datum):
    env  = datum[1]
    filename = datum[2]
    hash = datum[3]

    dir = datum[4]
    move = datum[5]
    plots = datum[6]
    min = datum[7]
    filepath = dir + sep + hash + sep + filename  
    file = get_gdrive() + 'data'+sep+'ga'+sep+ env +sep + filepath
    
    hep = HPCTEvolveProperties()
    hep.load_db(file)

    error_collector_type = hep.db['error_collector_type']
    error_response_type = hep.db['error_response_type']
    error_limit = eval(hep.db['error_limit'])
    runs = eval(hep.db['runs'])
    config = eval(hep.db['config'])
    seed = eval(hep.db['seed'])
    early_termination = eval(hep.db['early_termination'])
    env_props={'game_duration':10000, 'rmode' : 1, 'sync': 'false'}
    env_props={'game_duration':10000, 'rmode' : 1, 'sync': 'false', 'upper_body':'guardup'}
    outdir = 'output' + sep + dir
    makedirs(outdir, exist_ok=True)
    #draw_file = file= outdir + sep  + 'draw-'+ filename + hash + '.png'
    # plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
    # {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
    # plots=[]

    hpct_verbose= False #True #False #
    render=False

    ind, score = HPCTIndividual.run_from_config(config, min, render=render,  error_collector_type=error_collector_type, error_response_type=error_response_type, 
                                                error_properties=None, error_limit=error_limit, steps=runs, hpct_verbose=hpct_verbose, history=True, environment_properties=env_props,
                                                seed=seed, early_termination=early_termination,  move=move, plots=plots, suffixes=True, plots_dir=outdir)

    # draw_file=draw_file,

    #ind.draw(file='output/' + filename + '.png', node_size=100, font_size=5, with_edge_labels=True)
        
    print("Score: %0.3f" % score)
    #ind.summary()
    #print(ind.formatted_config())
    #print(ind.get_config())


def runit(datum, env_props, render=False, history=False, move=None, plots=None, runs=None):
    filename = datum[1]
    root = get_gdrive() 

    index1 = filename.find(sep)
    env = filename[0:index1]
    index2 = filename.find(sep,index1+1)
    gatest = filename[index1+1:index2]

    file = root + 'data'+sep+'ga'+sep+ filename
    
    hep = HPCTEvolveProperties()
    hep.load_db(file)

    error_collector_type = hep.db['error_collector_type']
    error_response_type = hep.db['error_response_type']
    error_limit = eval(hep.db['error_limit'])
    if runs==None:
        runs = eval(hep.db['runs'])
    config = eval(hep.db['config'])
    seed = eval(hep.db['seed'])
    early_termination = eval(hep.db['early_termination'])

    if history:
        end = filename.find('.properties')
        outdir =  root + 'data'+sep+'ga'+sep + env + sep + gatest+ sep + filename[end-32:end]
        # makedirs(outdir, exist_ok=True)


    hpct_verbose= False #True #False #
    
    
    ind, score = HPCTIndividual.run_from_config(config, min, render=render,  error_collector_type=error_collector_type, error_response_type=error_response_type, 
                                                error_properties=None, error_limit=error_limit, steps=runs, hpct_verbose=hpct_verbose, history=history, 
                                                environment_properties=env_props,
                                                seed=seed, early_termination=early_termination, move=move, plots=plots, suffixes=True, plots_dir=outdir)

        
    


data_old = [
    [0, 'CartPoleV1', 'ga-000.115-s001-2x3-m000-4292b6128e13ac2df54fd2c05a34292e', 'Std00-InputsError-RootMeanSquareError-Mode00', {'CartPoleV1': [-0.4, -0.3],'ICV': [0, 0], 'ICP': [0,  -0.1],         'IPV': [-0.0, -0.1],'IPA': [0.0, 0.0], 'Action1ws': [-0.3, -0.3]}, [ {'plot_items': {'PL1C0ws':'PL1C0ws','PL1C0ws':'ref'}, 'title':'Goal1'},{'plot_items': {'IPA':'pa','ICP':'cp'}, 'title':'Inputs'}], True],
    [1, 'CartPoleV1', 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832','Std01-InputsError-RootMeanSquareError-Mode01', {'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0],  'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}, [], True],
    [2, 'CartPoleV1', 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832', 'Std01-InputsError-RootMeanSquareError-Mode01',{'CartPoleV1': [-0.8, -0.2],'ICV': [-0.3, 0], 'ICP': [-0.1,  0], 'IPV': [-0.1, 0],'IPA': [0.0, -0.2], 'Action1ws': [-0.8, -0.2]}, [], True],
    [3, 'CartPoleV1', 'ga-000.130-s001-2x1-m002-9729cd44431b1958b69da786b4ba4f00', 'Std00-InputsError-RootMeanSquareError-Mode02', {'CartPoleV1': [-0.6, -0.1],'ICV': [-0.3, 0.1], 'ICP': [-0.1,  0.2], 'IPV': [0.1, 0.3],'IPA': [0.2, 0.4], 'Action1ws': [-0.65, 0]}, [], True],
    [4, 'WebotsWrestler', 'ga-000.870-s001-3x6-m001-e8993f3235b484cd5a869600d6d5a374', 'WW01-RewardError-CurrentError-Mode01', {}, [], True], # 0.906 (10) good, stable, 1 ref
    [5, 'WebotsWrestler', 'ga-000.365-s001-7x10-m004-0216b6fa50e383e602a9d3ad2739f69a', 'WW01-11-RewardError-CurrentError-Mode04', {}, [], False], # 0.365 (10) bad, 2 ref
    [6, 'WebotsWrestler', 'ga-000.661-s001-5x7-m003-6dfb7f2bec54a72660f78251bc02b092', 'WW01-09-RewardError-CurrentError-Mode03', {}, [], False], # 0.661 (10) poor, kneeling, 2 ref
    [7, 'WebotsWrestler', 'ga-001.559-s001-3x7-m002-6a329c48b9f246288ff944df11e21a98.properties', '6a329c48b9f246288ff944df11e21a98', 'WW01-07-RewardError-CurrentError-Mode02', {}, [], False], # 1.631 (10) good, dragging right leg but looks stable, 2 ref *
    [8, 'WebotsWrestler', 'ga-000.554-s001-3x5-m001-396442a24782fbf5d945531d302e886c', 'WW01-05-RewardError-CurrentError-Mode01', {}, [], False], # 0.554 (10) jittery, 1 ref
    [9, 'WebotsWrestler', 'ga-001.848-s001-4x8-m001-c589fa85b67d512975680f7265d52149', 'WW01-04-RewardError-CurrentError-Mode01', {}, [], False], # 1.547 (10) good, dragging left leg, 2 ref *
    [10, 'WebotsWrestler', 'ga-001.884-s001-2x4-m001-d63ec5dffda565b2c064458630f1643d', 'WW01-06-RewardError-CurrentError-Mode01', {}, [], False], # 1.620 (10) good weird, kneeling on right leg, though could be stable, 4 ref
    [11, 'WebotsWrestler', 'ga-002.149-s001-2x7-m001-a71b1e63499693a10f3adff35f0bb04d', 'WW01-04-RewardError-CurrentError-Mode01', {}, [], False], # 2.033 (10) jittery, not too stable, 2 ref *
    [12, 'WebotsWrestler', 'ga-002.039-s001-3x9-m002-1557e1adc59a7ef0c50cc2b8080f4265.properties', '1557e1adc59a7ef0c50cc2b8080f4265','WW01-08-RewardError-CurrentError-Mode02', {}, [], False], # 1.908 (10) good, hopping on two feet, 2 ref *
    [13, 'WebotsWrestler', 'ga-001.237-s001-2x10-m002-4cc6f7a44200996b66974152c48749ad.properties', '4cc6f7a44200996b66974152c48749ad', 'WW01-07-RewardError-CurrentError-Mode02', {}, [], False], # 0.322 (30) moves very slowly
    [14, 'WebotsWrestler', 'output\conf-018.config', '8310ba064d95eee8c3347389c6f74628', 'WW01-03-RewardError-CurrentError-Mode01', {}, [], False], # 0.024 (10) dud, does nothing
    [15, 'WebotsWrestler', 'output\conf-020.config', '6fca917053fd90d970824b5d63021dbc', 'WW01-10-RewardError-CurrentError-Mode03', {}, [], False], # 0.073 (10) dud, does nothing
    [16, 'WebotsWrestler', 'ga-001.864-s001-6x6-m001-198353167ff8dc603079da89b6bbd041.properties', '198353167ff8dc603079da89b6bbd041', 'WW01-02-RewardError-CurrentError-Mode01', {}, [], False], # 0.322 (30) moves very slowly
    [17, 'WebotsWrestler', 'ga-001.938-s001-3x5-m003-9d4d2585c69a1678f06d75f9767678aa.properties', '9d4d2585c69a1678f06d75f9767678aa', 'WW01-10-RewardError-CurrentError-Mode03', {}, [], False], # 0.022 (10) dud, does nothing 
   
    ]

data = [
    [0, 'CartPoleV1'+sep+'Std03-InputsError-RootMeanSquareError-Mode00'+sep+'ga-000.113-s001-1x1-m000-cfe004e44e94d469055bc00d7aac892f.properties'],
    
    [1],[2],[3],
    # 0.906 (10) good, stable, moves slowly, 1 ref
    [4, 'WebotsWrestler\\WW01-RewardError-CurrentError-Mode01\ga-000.870-s001-3x6-m001-e8993f3235b484cd5a869600d6d5a374.properties'],
    # deleted
    [5, 'WebotsWrestler\\deleted'],    
     # 0.061 (10) poor, kneeling, 2 ref
    [6, 'WebotsWrestler\\WW01-09-RewardError-CurrentError-Mode03\\ga-000.661-s001-5x7-m003-6dfb7f2bec54a72660f78251bc02b092.properties'],
    # 1.631 (10) good, dragging right leg but looks stable, 2 ref *
    [7, 'WebotsWrestler\WW01-07-RewardError-CurrentError-Mode02\\6a329c48b9f246288ff944df11e21a98\ga-001.559-s001-3x7-m002-6a329c48b9f246288ff944df11e21a98.properties'],
    # 0.554 (10) jittery, 1 ref
    [8, 'WebotsWrestler\\WW01-05-RewardError-CurrentError-Mode01\ga-000.554-s001-3x5-m001-396442a24782fbf5d945531d302e886c.properties'],
     # 1.547 (10) good, dragging left leg, 2 ref *
    [9, 'WebotsWrestler\\WW01-04-RewardError-CurrentError-Mode01\\ga-001.848-s001-4x8-m001-c589fa85b67d512975680f7265d52149.properties'],
    # 1.620 (10) good weird, kneeling on right leg, though could be stable, 4 ref
    [10, 'WebotsWrestler\\WW01-06-RewardError-CurrentError-Mode01\\ga-001.884-s001-2x4-m001-d63ec5dffda565b2c064458630f1643d.properties'],
    # 0.088 (10) jittery, not too stable, 2 ref 
    [11, 'WebotsWrestler\\WW01-04-RewardError-CurrentError-Mode01\ga-002.149-s001-2x7-m001-a71b1e63499693a10f3adff35f0bb04d.properties'],
    # 1.908 (10) good, hopping on two feet, 2 ref *    
    [12, 'WebotsWrestler\\WW01-08-RewardError-CurrentError-Mode02\\1557e1adc59a7ef0c50cc2b8080f4265\ga-002.039-s001-3x9-m002-1557e1adc59a7ef0c50cc2b8080f4265.properties'],     
    # 0.048 (10) rubbish, 2 ref 
    [13, 'WebotsWrestler\WW01-07-RewardError-CurrentError-Mode02\\4cc6f7a44200996b66974152c48749ad\ga-001.237-s001-2x10-m002-4cc6f7a44200996b66974152c48749ad.properties'],[14],[15],
    # 0.002 (10) rubbish, 1 ref
    [16, 'WebotsWrestler\WW01-02-RewardError-CurrentError-Mode01\\198353167ff8dc603079da89b6bbd041\ga-001.864-s001-6x6-m001-198353167ff8dc603079da89b6bbd041.properties'],
    # 0.022 (10) dud, does nothing, 2 ref
    [17, 'WebotsWrestler\WW01-10-RewardError-CurrentError-Mode03\\9d4d2585c69a1678f06d75f9767678aa\ga-001.938-s001-3x5-m003-9d4d2585c69a1678f06d75f9767678aa.properties'],
    # 1.250 (5) looks good, fast but a bit unstable, 2 ref *
    [18, 'WebotsWrestler\WW01-07-RewardError-CurrentError-Mode02\\108925b64cd5a2b96bde2bfc108fd4f8\output\conf-011-2.015.config'], 
    # 0.028 (10) dud, does nothing, 2 ref
    [19, 'WebotsWrestler\WW01-10-RewardError-CurrentError-Mode03\\9d4d2585c69a1678f06d75f9767678aa\ga-001.952-s001-5x5-m003-9d4d2585c69a1678f06d75f9767678aa.properties'], 
    # 1.254 (10) good, wobbles forwards ands turns randomly, 2 ref *
    [20, 'WebotsWrestler\WW01-12-RewardError-CurrentError-Mode04\\07510d709b16c265c7868c20a5fea471\ga-002.026-s001-3x7-m004-07510d709b16c265c7868c20a5fea471.properties'], 
    # 0.018 (10) dud, does nothing, 2 ref 
    [21, 'WebotsWrestler\WW01-12-RewardError-CurrentError-Mode04\\bbde6e0496da05e6d740ed4fd0d49654\ga-001.402-s001-2x9-m004-bbde6e0496da05e6d740ed4fd0d49654.properties'], 
    # 0.139 (10) not good, 2 ref
    [22, 'WebotsWrestler\\WW01-10-RewardError-CurrentError-Mode03\\ga-000.880-s001-5x9-m003-ab82d3befe36e9f4483baa8ecc1a1947.properties'], 
    # 0.016 (10) dud, does nothing, 2 ref 
    [23, 'WebotsWrestler\WW01-11-RewardError-CurrentError-Mode04\\9ede79c2b618009ba8d8be2cdded4895\\output\\conf-012-1.096.config'], 
    # 0.071 (10) dud, does nothing, 2 ref 
    [24, 'WebotsWrestler\WW01-10-RewardError-CurrentError-Mode03\\6fca917053fd90d970824b5d63021dbc\output\\conf-020-0.908.config'], 
    # 0.053 (10) dud, does nothing, 2 ref *
    [25, 'WebotsWrestler\WW01-03-RewardError-CurrentError-Mode01\\8310ba064d95eee8c3347389c6f74628\output\conf-016-1.784.config'], 
    # 1.275 good, fast shuffling, 2 ref * 
    [26, 'WebotsWrestler\WW01-09-RewardError-CurrentError-Mode03\\ga-001.614-s001-6x6-m003-f37757991a462f567c03e613acc09c2e.properties'], 
    # 
    [27, 'WebotsWrestler\WW01-08-RewardError-CurrentError-Mode02\\ga-001.837-s001-2x5-m002-6a468a669e5944c2d8792af248741dd0.properties'], 

]

# todo
# WW01-10-RewardError-CurrentError-Mode03\d6d662f2b5a398c83d82cf82adf7a44c\output
# WW01-06-RewardError-CurrentError-Mode01/21db068466666c5352cceef7c8c496d9/output/
# WW01-07-RewardError-CurrentError-Mode02/108925b64cd5a2b96bde2bfc108fd4f8/output/
# WW01-02-RewardError-CurrentError-Mode01/b99610e60d6105e758a25236980b0171/output/
# WW01-05-RewardError-CurrentError-Mode01/757a5d1b4a1dea1eb118d18c8f22d7d5/output/
# 

index=0

# C:\Users\ryoung\Google Drive\data\ga\WebotsWrestler\WW01-07-RewardError-CurrentError-Mode02\108925b64cd5a2b96bde2bfc108fd4f8\output


if test == 100:
    for datum in data_old:
      runit_old(datum)   
      
if test == 10:
    # good ones 4, 9, 11, weird 10
    runit_old(data_old[7])

if test == 20:
    
    cm = ClientConnectionManager.getInstance()
    cm.set_port(6666)
    env_props={'game_duration':10000, 'rmode' : 1, 'sync': 'false'}
    env_props={'game_duration':10000, 'rmode' : 1, 'sync': 'false', 'upper_body':'guardup'}

    
    runit(data[index], env_props)
    

if test == 30:
    env_props={}
    history=True
    plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0v':'ref','IPA':'pa'}, 'title':'Goal'},
             {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
    runit(data[index], env_props, render=True, history=history, plots=plots, runs=100)
    




