# python testing/test-hpct-model-steady.py

from os import sep, listdir
from os.path import isfile
from cutils.paths import get_gdrive
# from statistics import sum
from eepct.wind_turbine import wind_turbine_results, get_environment_properties

log_experiment = None
comparisons = True # False #True #False
comparisons_print_plots = True
WT='WindTurbine'
environment_properties=None
# environment_properties={'series': 'steady', 'zero_threshold': 1.25, 'keep_history': True, 'range': 'test'}
# environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True, 'range': 'test'}
# environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True, 'range': 'test', 'reward_type': 'surface2'}
# environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True}

root = get_gdrive() 
plots=None
history=False
verbose=False
early=None
plots=[]

test=2

if test==1:
    wtdir = root + sep + 'data'+sep+'ga'+sep + WT

    for property_dir in sorted(listdir(wtdir)):
        #print(property_dir)
        tmp_dir = wtdir + sep + property_dir
        if isfile(tmp_dir):
            continue
        for file in sorted(listdir(tmp_dir)):
            if file.endswith(".properties"):
                if environment_properties is None:
                    environment_properties = get_environment_properties(root=root, property_dir=property_dir, property_file=file)
                    environment_properties['range'] = 'test'
                    environment_properties['keep_history'] = True
                #print(file)
                wind_turbine_results(environment_properties=environment_properties, log_experiment=log_experiment, root=root, verbose=verbose, early=early, comparisons=comparisons, comparisons_print_plots=comparisons_print_plots, property_dir=property_dir, property_file=file, plots=plots)

if test ==2:

         
    # plots = [  {'plot_items': {'IYE':'ye'}, 'title':'YawError'}, 
    #          {'plot_items': {'IWD':'wd'}, 'title':'Wind'}, 
    #          {'plot_items': {'CL1C1':'eLM', 'ILM':'ilm'},'title':'LMErrors'}, 
    #          {'plot_items': {'CL1C0':'eYE'},'title':'YEErrors'}, 
    #         #  {'plot_items': {'CL1C1':'eLM', 'CL1C0':'eYE'},'title':'RefErrors'}, 
    #          {'plot_items': {'Action1ws':'Action1ws'}, 'title':'Output'}]   
    
    plots=[]

    property_dir = 'RewardError-SummedError-Mode03'
    file = 'ga-3692779.547-s001-2x3-m003-WT0430-8d7129ec82d81370fb660b36a069003d.properties'

    # property_dir = 'RewardError-RootMeanSquareError-Mode04'
    # file = 'ga-001.537-s001-3x3-m004-WT0208-cb9e85fe4c8b9fa355086b0a6a8cc911.properties'


    
    if environment_properties is None:
        environment_properties = get_environment_properties(root=root, property_dir=property_dir, property_file=file)
        environment_properties['keep_history'] = True
        environment_properties['range'] = 'test'
        # environment_properties['reward_type']= 'power'
        print(environment_properties)
    
    print(file)
    energy_gain, power_improvement, rel_net_prod_change, net_prod_change = wind_turbine_results(environment_properties=environment_properties, experiment=log_experiment, root=root, verbose=verbose, early=early, comparisons=comparisons, comparisons_print_plots=comparisons_print_plots, property_dir=property_dir, property_file=file, plots=plots)

    print(f'energy_gain = {energy_gain:4.2f}')
    print(f'power_improvement = {power_improvement.sum():4.2f}')
    print(f'rel_net_prod_change = {sum(rel_net_prod_change):4.2f}')
    print(f'net_prod_change = {sum(net_prod_change):4.2f}')


    






