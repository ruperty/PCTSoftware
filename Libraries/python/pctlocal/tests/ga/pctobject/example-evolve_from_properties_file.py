

from eepct.hpct import HPCTEvolveProperties
from utils.paths import get_root_path, get_gdrive

from deap import base, creator

from epct.evolvers import CommonToolbox

from eepct.hpct import HPCTIndividual

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)


root = get_root_path()

file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/CartPoleV1/Std-InputsError-RootMeanSquareError-Mode00.properties'
out_dir= get_gdrive() + 'data/ga/'
print(out_dir)
#file = root + 'tmp/CartPoleV1/InputsError-RootMeanSquareError-Binary-WeightedSum-Topp1/ga-000.160-s001-5x5-m0-fed09c2940d19fc9624a4c166c7e9dcb.properties'
#out_dir=  '/mnt/c/tmp/ga/'


output=True
overwrite=True
# draw_file='evolve-best.png'
draw_file='efpf.png'
verbose={ 'debug': 0, 'evolve_verbose':2, 'display_env': True, 'hpct_verbose':False}

hep = HPCTEvolveProperties()
output=True

hep.evolve_from_properties_file(file=file, print_properties=True, verbose=verbose, toolbox=toolbox, draw_file=draw_file, out_dir=out_dir, output=output, overwrite=overwrite)
# hep.load_properties(file=file, evolve=True, print_properties=True)



