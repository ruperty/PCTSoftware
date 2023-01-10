

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

test = 0

if test == 0:
    filename = 'Std-InputsError-RootMeanSquareError-Mode00'
if test == 1:
    filename = 'Std-InputsError-RootMeanSquareError-Mode01'

file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/CartPoleV1/'+ filename + ".properties"
out_dir= get_gdrive() + 'data/ga/'
print(out_dir)

output=True
overwrite=True

draw_file= filename + '-evolve-best' + '.png'

debug= 0 #0 #3 # details of population in each gen, inc. mutate and merge
hpct_verbose= False #True # log of every control system iteration
evolve_verbose =  1 #2 # output of evolve iterations, 2 for best of each gen

# debug= 3 #0 #3 # details of population in each gen, inc. mutate and merge
# hpct_verbose= True # log of every control system iteration
# evolve_verbose = 2# 1 #2 # output of evolve iterations, 2 for best of each gen

save_arch_gen = True #False #True
display_env = False #True #False
run_gen_best = True #False #True

verbose={ 'debug': debug, 'evolve_verbose': evolve_verbose, 'display_env': display_env, 'hpct_verbose':hpct_verbose, 'save_arch_gen': save_arch_gen, 'run_gen_best':run_gen_best}

hep = HPCTEvolveProperties()
output=True

hep.evolve_from_properties_file(file=file, print_properties=True, verbose=verbose, toolbox=toolbox, draw_file=draw_file, 
                                out_dir=out_dir, output=output, overwrite=overwrite, node_size=100, font_size=6)
# hep.load_properties(file=file, evolve=True, print_properties=True)



