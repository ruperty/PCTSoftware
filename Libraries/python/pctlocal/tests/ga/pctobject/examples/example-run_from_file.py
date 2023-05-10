# https://www.namingcrisis.net/post/2019/03/11/interactive-matplotlib-ipython/
# 

from os import makedirs
from  os import sep

from cutils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual, HPCTEvolveProperties
from pct.architectures import run_from_properties_file
from pct.network import ClientConnectionManager   

test = 10


cm = ClientConnectionManager.getInstance()
cm.set_port(6667)
  
def runit(datum):
    env  = datum[1]
    filename = datum[2]
    hash = datum[3]

    dir = datum[4]
    move = datum[5]
    plots = datum[6]
    min = datum[7]
    filepath = dir + sep + hash + sep + filename  
    file = get_gdrive() + 'data/ga/'+ env +'/' + filepath
    
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
    env_props={'game_duration':10000, 'rmode' : 1, 'sync': 'true', 'upper_body':'guardup'}
    outdir = 'output' + sep + dir
    makedirs(outdir, exist_ok=True)
    #draw_file = file= outdir + sep  + 'draw-'+ filename + hash + '.png'
    # plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
    # {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
    # plots=[]

    hpct_verbose= True #False #
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
    [10, 'WebotsWrestler', 'ga-001.884-s001-2x4-m001-d63ec5dffda565b2c064458630f1643d', 'WW01-06-RewardError-CurrentError-Mode01', {}, [], False], # 1.620 (10) good weird, kneeling on right leg, though could be stable, 4 ref
    [11, 'WebotsWrestler', 'ga-002.149-s001-2x7-m001-a71b1e63499693a10f3adff35f0bb04d', 'WW01-04-RewardError-CurrentError-Mode01', {}, [], False], # 2.033 (10) jittery, not too stable, 2 ref *
    [12, 'WebotsWrestler', 'ga-002.039-s001-3x9-m002-1557e1adc59a7ef0c50cc2b8080f4265.properties', '1557e1adc59a7ef0c50cc2b8080f4265','WW01-08-RewardError-CurrentError-Mode02', {}, [], False], # 1.908 (10) good, hopping on two feet, 2 ref *
    [13, 'WebotsWrestler', 'ga-001.237-s001-2x10-m002-4cc6f7a44200996b66974152c48749ad.properties', '4cc6f7a44200996b66974152c48749ad', 'WW01-07-RewardError-CurrentError-Mode02', {}, [], False], # 0.322 (30) moves very slowly
    [14, 'WebotsWrestler', 'output\conf-018.config', '8310ba064d95eee8c3347389c6f74628', 'WW01-03-RewardError-CurrentError-Mode01', {}, [], False], # 0.024 (10) dud, does nothing
    [15, 'WebotsWrestler', 'output\conf-020.config', '6fca917053fd90d970824b5d63021dbc', 'WW01-10-RewardError-CurrentError-Mode03', {}, [], False], # 0.073 (10) dud, does nothing
    [16, 'WebotsWrestler', 'ga-001.864-s001-6x6-m001-198353167ff8dc603079da89b6bbd041.properties', '198353167ff8dc603079da89b6bbd041', 'WW01-02-RewardError-CurrentError-Mode01', {}, [], False], # 0.322 (30) moves very slowly
    [17, 'WebotsWrestler', 'ga-001.938-s001-3x5-m003-9d4d2585c69a1678f06d75f9767678aa.properties', '9d4d2585c69a1678f06d75f9767678aa', 'WW01-10-RewardError-CurrentError-Mode03', {}, [], False] # ??? (10) 
   
    ]


# C:\Users\ryoung\Google Drive\data\ga\WebotsWrestler\WW01-03-RewardError-CurrentError-Mode01\8310ba064d95eee8c3347389c6f74628\output
# conf-018.config
# config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'WebotsWrestler', 'name': 'WebotsWrestler', 'value': [-0.0, -0.0, 0.0, -0.0, -0.0, 0.0], 'links': {0: 'Action1', 1: 'Action2', 2: 'Action3', 3: 'Action4', 4: 'Action5', 5: 'Action6'}, 'env_name': 'WebotsWrestler', 'performance': 1.958, 'done': True}, 'pre1': {'type': 'IndexedParameter', 'name': 'LHipPitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'LKneePitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 1}, 'pre3': {'type': 'IndexedParameter', 'name': 'LAnklePitch', 'value': 0.0, 'links': {0: 'WebotsWrestler'}, 'index': 2}, 'pre4': {'type': 'IndexedParameter', 'name': 'RHipPitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 3}, 'pre5': {'type': 'IndexedParameter', 'name': 'RKneePitch', 'value': -0.0, 'links': {0: 'WebotsWrestler'}, 'index': 4}, 'pre6': {'type': 'IndexedParameter', 'name': 'RAnklePitch', 'value': 0.0, 'links': {0: 'WebotsWrestler'}, 'index': 5}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': -0.0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4', 5: 'OL1C5', 6: 'OL1C6', 7: 'OL1C7', 8: 'OL1C8'}, 'weights': [0.386276350173114, -0.7658387392014291, 0.7071393465081743, -0.00482854601790117, 0.9325635657468081, 0.9381316391460739, 0.20686866074513643, 0.5052793259963679, -0.4119851664840578]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': -0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [0, 1, 0, 0, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0.0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': -0.0, 'links': {0: 'CL0C0'}, 'gain': -1.0268980382502524}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': -0.0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4', 5: 'OL1C5', 6: 'OL1C6', 7: 'OL1C7', 8: 'OL1C8'}, 'weights': [-0.6466018227080479, -0.8779493905743879, 0.5894521729815243, 0.1333079522034949, 1.1600199491792604, -0.3836825324721681, -0.4274868314771466, -0.5387608201529059, -0.03278918684371801]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0.0, 'links': {0: 'LHipPitch', 1: 'LKneePitch', 2: 'LAnklePitch', 3: 'RHipPitch', 4: 'RKneePitch', 5: 'RAnklePitch'}, 'weights': [0, 1, 0, 0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': -0.0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0.0, 'links': {0: 'CL0C1'}, 'gain': -0.26752044904086275}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C0', 'value': 0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [0.8544097011929193, -0.5244235277308322]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': -0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0.0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': -0.0, 'links': {0: 'CL1C0'}, 'gain': -0.32812384278134066}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C1', 'value': 0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [0.7486485128502911, -0.7681300884981448]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': -0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0.0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0.0, 'links': {0: 'CL1C1'}, 'gain': 0.028224796922422718}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L1C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C2', 'value': 0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [0.11292697063567028, 0.6594142277511428]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C2', 'value': 0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C2', 'value': 0.0, 'links': {0: 'RL1C2', 1: 'PL1C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C2', 'value': 0.0, 'links': {0: 'CL1C2'}, 'gain': 0.9227119708402556}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L1C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C3', 'value': -0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [-0.6424085832726614, 0.43819776075029554]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C3', 'value': -0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C3', 'value': -0.0, 'links': {0: 'RL1C3', 1: 'PL1C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C3', 'value': -0.0, 'links': {0: 'CL1C3'}, 'gain': 0.6768323340724312}}}}, 'col4': {'col': 4, 'node': {'type': 'PCTNode', 'name': 'L1C4', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C4', 'value': 0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [0.3089645032665478, -0.03705225598147788]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C4', 'value': 0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C4', 'value': 0.0, 'links': {0: 'RL1C4', 1: 'PL1C4'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C4', 'value': -0.0, 'links': {0: 'CL1C4'}, 'gain': -1.262603262623514}}}}, 'col5': {'col': 5, 'node': {'type': 'PCTNode', 'name': 'L1C5', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C5', 'value': 0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [0.6284986152245793, 0.7112148533234558]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C5', 'value': 0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C5', 'value': 0.0, 'links': {0: 'RL1C5', 1: 'PL1C5'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C5', 'value': 0.0, 'links': {0: 'CL1C5'}, 'gain': 0.5622757040572045}}}}, 'col6': {'col': 6, 'node': {'type': 'PCTNode', 'name': 'L1C6', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C6', 'value': -0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [-0.5934480063604864, -0.43955364580126544]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C6', 'value': -0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C6', 'value': -0.0, 'links': {0: 'RL1C6', 1: 'PL1C6'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C6', 'value': 0.0, 'links': {0: 'CL1C6'}, 'gain': -0.9464946473301505}}}}, 'col7': {'col': 7, 'node': {'type': 'PCTNode', 'name': 'L1C7', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C7', 'value': -0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [-0.5139577667358646, 0.696721811128133]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C7', 'value': 0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C7', 'value': -0.0, 'links': {0: 'RL1C7', 1: 'PL1C7'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C7', 'value': -0.0, 'links': {0: 'CL1C7'}, 'gain': 0.27863887584941316}}}}, 'col8': {'col': 8, 'node': {'type': 'PCTNode', 'name': 'L1C8', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C8', 'value': 0.0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [1.1746560522159695, 1.2712970476024377]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C8', 'value': 0.0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C8', 'value': 0.0, 'links': {0: 'RL1C8', 1: 'PL1C8'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C8', 'value': -0.0, 'links': {0: 'CL1C8'}, 'gain': -0.5240130334672518}}}}}}, 'level2': {'level': 2, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L2C0', 'refcoll': {'0': {'type': 'EAVariable', 'name': 'RL2C0', 'value': -0.19831660702961182, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C0', 'value': 0.0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4', 5: 'PL1C5', 6: 'PL1C6', 7: 'PL1C7', 8: 'PL1C8'}, 'weights': [0, 0, 1, 0, 1, 1, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C0', 'value': -0.0, 'links': {0: 'RL2C0', 1: 'PL2C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C0', 'value': 0.0, 'links': {0: 'CL2C0'}, 'gain': -1.40615191063179}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L2C1', 'refcoll': {'0': {'type': 'EAVariable', 'name': 'RL2C1', 'value': 0.284363270827233, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C1', 'value': 0.0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4', 5: 'PL1C5', 6: 'PL1C6', 7: 'PL1C7', 8: 'PL1C8'}, 'weights': [0, 0, 1, 0, 1, 1, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C1', 'value': 0.0, 'links': {0: 'RL2C1', 1: 'PL2C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C1', 'value': 0.0, 'links': {0: 'CL2C1'}, 'gain': 1.0652531273986903}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [0.9809639262152116, -0.7592159039981807]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-0.4676151045947297, -0.39747468263773167]}, 'post2': {'type': 'EAWeightedSum', 'name': 'Action3', 'value': 0.0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-0.1976944077319437, 0.4584141490547293]}, 'post3': {'type': 'EAWeightedSum', 'name': 'Action4', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-0.21537741048482328, -0.5953504922862894]}, 'post4': {'type': 'EAWeightedSum', 'name': 'Action5', 'value': -0.0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-0.004606701867770874, -0.056857700756761664]}, 'post5': {'type': 'EAWeightedSum', 'name': 'Action6', 'value': 0.0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [0.2549695951883113, 0.6683858438249849]}}}


if test == 100:
    for datum in data:
      runit(datum)   
      
if test == 10:
    # good ones 4, 9, 11, weird 10
    runit(data[17])







