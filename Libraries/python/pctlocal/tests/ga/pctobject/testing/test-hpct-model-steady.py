

from os import sep, path, makedirs, listdir
from cutils.paths import get_gdrive

from eepct.wind_turbine import wind_turbine_results

log_experiment = False
comparisons = False #True #False
comparisons_print_plots = True
wt='WindTurbine'
environment_properties={'series': 'steady', 'zero_threshold': 1.25, 'keep_history': True, 'range': 'test'}
environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True, 'range': 'test'}
environment_properties={'series': 'steady', 'zero_threshold': 1, 'keep_history': True}

root = get_gdrive() 
wtdir = root + sep + 'data'+sep+'ga'+sep + wt
plots=None
history=False
verbose=False
early=None

for property_dir in sorted(listdir(wtdir)):
    print(property_dir)
    tmp_dir = wtdir + sep + property_dir
    for file in sorted(listdir(tmp_dir)):
        if file.endswith(".properties"):
            print(file)
            wind_turbine_results(environment_properties=environment_properties, log_experiment=log_experiment, root=root, verbose=verbose, early=early, comparisons=comparisons, comparisons_print_plots=comparisons_print_plots, property_dir=property_dir, property_file=file)








