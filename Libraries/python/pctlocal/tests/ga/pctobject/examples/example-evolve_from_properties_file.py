
import os

from eepct.hpct import HPCTEvolveProperties
from utils.paths import get_root_path, get_gdrive

from deap import base, creator

from epct.evolvers import CommonToolbox

from eepct.hpct import HPCTIndividual

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

node_size, font_size=150, 10

root = get_root_path()

test = 8

# InputsError
if test == 1:
    filename = 'Std00-InputsError-RootMeanSquareError-Mode00'
if test == 2:
    filename = 'Std01-InputsError-RootMeanSquareError-Mode00'
if test == 3:
    filename = 'Std00-InputsError-RootMeanSquareError-Mode01'
if test == 4:
    filename = 'Std01-InputsError-RootMeanSquareError-Mode01'
    
# TotalError
if test == 5:
    filename = 'Std00-TotalError-RootMeanSquareError-Mode00'
if test == 6:
    filename = 'Std01-TotalError-RootMeanSquareError-Mode00'
if test == 7:
    filename = 'Std00-TotalError-RootMeanSquareError-Mode01'
if test == 8:
    filename = 'Std01-TotalError-RootMeanSquareError-Mode01'
        
#mode 01

file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/CartPoleV1/'+ filename + ".properties"
out_dir= get_gdrive() + 'data/ga/'
#print(out_dir)

output=True
overwrite=True

#draw_file= 'output' + os.sep + filename + os.sep + filename + '-evolve-best' + '.png'
#draw_file= 'output'  + os.sep + filename + '-evolve-best' + '.png'

local_out_dir = 'output/'  + filename 

draw_file= local_out_dir + '/' + filename + '-evolve-best' + '.png'

debug= 0 #0 #3 # details of population in each gen, inc. mutate and merge
hpct_verbose= False #True # log of every control system iteration
evolve_verbose =  1 #2 # output of evolve iterations, 2 for best of each gen

#debug= 4 #0 #3 # details of population in each gen, inc. mutate and merge
#hpct_verbose= 1 #True # log of every control system iteration
#evolve_verbose = 2# 1 #2 # output of evolve iterations, 2 for best of each gen

save_arch_gen = True #False #True
display_env = True #True #False#
run_gen_best = True # #False #True

save_arch_gen = False #True
display_env = False #False#
run_gen_best = False # #False #True

verbose={ 'debug': debug, 'evolve_verbose': evolve_verbose, 'display_env': display_env, 'hpct_verbose':hpct_verbose, 
         'save_arch_gen': save_arch_gen, 'run_gen_best':run_gen_best}

hep = HPCTEvolveProperties()
output=True


#if __name__ == "__main__":

hep.evolve_from_properties_file(file=file, print_properties=True, verbose=verbose, toolbox=toolbox, draw_file=draw_file, 
                                    out_dir=out_dir, local_out_dir=local_out_dir, output=output, overwrite=overwrite, node_size=node_size, font_size=font_size)
# hep.load_properties(file=file, evolve=True, print_properties=True)



