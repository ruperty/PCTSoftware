# python testing/test-hpct-model-steady.py

from os import sep, listdir
from os.path import isfile
from cutils.paths import get_gdrive

from eepct.wind_turbine import wind_turbine_results, get_environment_properties

log_experiment = False
comparisons = False #True #False
comparisons_print_plots = True
WT='WindTurbine'
environment_properties=None
# environment_properties={'series': 'steady', 'zero_threshold': 1.25, 'keep_history': True, 'range': 'test'}
# environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True, 'range': 'test'}
# environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True, 'range': 'test', 'reward_type': 'surface2'}
# environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True}

root = get_gdrive() 
wtdir = root + sep + 'data'+sep+'ga'+sep + WT
plots=None
history=False
verbose=False
early=None

test=2

if test==1:

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
                wind_turbine_results(environment_properties=environment_properties, log_experiment=log_experiment, root=root, verbose=verbose, early=early, comparisons=comparisons, comparisons_print_plots=comparisons_print_plots, property_dir=property_dir, property_file=file)

if test ==2:

    # property_dir = 'RewardError-RootMeanSquareError-Mode04'
    # file = 'ga-19073.531-s001-2x4-m004-WT20-eda030b5312bf8c0b89e50a4a75a22f7.properties'

    # property_dir = 'RewardError-SummedError-Mode00'
    # file = 'ga-28251.409-s001-2x2-m000-WT21-be71d6baeeb226c7e272315e736ecb42.properties'

    property_dir = 'ReferencedInputsError-RootMeanSquareError-Mode04-old'
    # file = 'ga-006.223-s001-2x3-m004-WT181-404dfa64508ea87ebf6941a9f9332ac7.properties'
    file = 'ga-005.701-s001-2x3-m004-WT182-541d9dd89dbd748f186d68b0ad296597.properties'


    if environment_properties is None:
        environment_properties = get_environment_properties(root=root, property_dir=property_dir, property_file=file)
        environment_properties['keep_history'] = True
        environment_properties['range'] = 'test'
        # environment_properties['reward_type']= 'power'
        print(environment_properties)
    wind_turbine_results(environment_properties=environment_properties, log_experiment=log_experiment, root=root, verbose=verbose, early=early, comparisons=comparisons, comparisons_print_plots=comparisons_print_plots, property_dir=property_dir, property_file=file)







