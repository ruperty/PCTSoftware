
import os
import logging
import platform
    
    
from datetime import datetime
from eepct.hpct import HPCTEvolveProperties
from utils.paths import get_root_path, get_gdrive
from deap import base, creator
from epct.evolvers import CommonToolbox
from eepct.hpct import HPCTIndividual


from pct.network import ConnectionManager


out_dir= get_gdrive() + 'data/ga/'
env_name = 'WebotsWrestler'

# logging info
now = datetime.now() # current date and time
date_time = now.strftime("%Y%m%d-%H%M%S")
log_file=os.sep.join((out_dir, env_name, "ww-evolve-client-"+platform.node()+"-"+date_time+".log"))
logging.basicConfig(filename=log_file, level=logging.DEBUG,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )

logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.DEBUG)
# fh = logging.FileHandler(log_file)
# fh_formatter = logging.Formatter("%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s-%(lineno)d %(message)s",datefmt= '%H:%M:%S')
# fh.setFormatter(fh_formatter)
# logger.addHandler(fh)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMax)

min=False

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

node_size, font_size=150, 10

root = get_root_path()

test = 2

cm = ConnectionManager.getInstance()
cm.set_port(6668)

# WW01
if test == 1:
    filename = 'WW01-RewardError-SmoothError-Mode00'
if test == 2:
    filename = 'WW01-01-RewardError-CurrentError-Mode01'

if test == 3:
    filename = 'WW01-02-RewardError-CurrentError-Mode01'

if test == 4:
    filename = 'WW01-03-RewardError-CurrentError-Mode01'

if test == 5:
    filename = 'WW01-04-RewardError-CurrentError-Mode01'

if test == 6:
    filename = 'WW01-05-RewardError-CurrentError-Mode01'

if test == 7:
    filename = 'WW01-11-RewardError-CurrentError-Mode04'

logger.info("Evolving {} ".format(env_name))

file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/WebotsWrestler/'+ filename + ".properties"

local_out_dir = 'output/'  + filename 
draw_file= local_out_dir + '/' + filename + '-evolve-best' + '.png'

debug= 0 #0 #3 # details of population in each gen, inc. mutate and merge
hpct_verbose= False #True # log of every control system iteration
evolve_verbose =  1 #2 # output of evolve iterations, 2 for best of each gen

# debug= 2 #3 #0 #3 # details of population in each gen, inc. mutate and merge
#hpct_verbose= 1 #True # log of every control system iteration
#evolve_verbose = 3 #2# 1 #2 # output of evolve iterations, 2 for best of each gen

save_arch_gen = True #False #True
display_env = True #True #False#
run_gen_best = True # #False #True

#save_arch_gen = False #True
#display_env = False #False#
#run_gen_best = False # #False #True

verbose={ 'debug': debug, 'evolve_verbose': evolve_verbose, 'display_env': display_env, 'hpct_verbose':hpct_verbose, 
         'save_arch_gen': save_arch_gen, 'run_gen_best':run_gen_best}

hep = HPCTEvolveProperties()
output=True
overwrite=True

#if __name__ == "__main__":
logger.info('Start evolve_ww')
hep.evolve_from_properties_file(file=file, print_properties=True, verbose=verbose, toolbox=toolbox, draw_file=draw_file, 
                                    out_dir=out_dir, local_out_dir=local_out_dir, output=output, overwrite=overwrite, 
                                    node_size=node_size, font_size=font_size, min=min)
# hep.load_properties(file=file, evolve=True, print_properties=True)



