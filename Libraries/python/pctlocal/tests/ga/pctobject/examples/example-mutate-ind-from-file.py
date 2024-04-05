

import time, random

from deap import base, creator
from epct.evolvers import CommonToolbox
from epct.po_evolvers import HPCTIndividual, HPCTEvolver, HPCTArchitecture, HPCTEvolverWrapper, HPCTEvolveProperties
from epct.po_architecture import HPCTLEVEL, HPCTFUNCTION, HPCTVARIABLE

from cutils.paths import get_root_path


# creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

# toolbox = base.Toolbox()
# CommonToolbox.getInstance().set_toolbox(toolbox)



root = get_root_path()


filename = 'WT0095-RewardError-RootMeanSquareError-Mode02'

file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/WindTurbine/'+ filename + ".properties"

max = False
if max:
    pass
    min=False
    if hasattr(creator, 'FitnessMax'):
            pass
    else:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMax)
else:
    # flip=False
    min=True
    if hasattr(creator, 'FitnessMin'):
            pass
    else:
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
            creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

verbose = {'debug': 2,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': False,
				'save_arch_gen': False, 'run_gen_best':False, 'display_env': False, 'hpct_verbose':False}


seed = 4
hep = HPCTEvolveProperties()
hash_num, desc, properties_str = hep.configure_evolver_from_properties_file(file=file, seed=seed, verbose=verbose, toolbox=toolbox,  min=min, 
                                                                                print_properties=False)        
evr = HPCTEvolverWrapper(**hep.wrapper_properties)

# cfilename = 'G:\My Drive\data\ga\WindTurbine\RewardError-RootMeanSquareError-Mode02\c0e106ffc5cde4b3454cf9e6d5845e3e\conf-test.config'
# hpct, hep = HPCTIndividual.from_properties_file(cfilename)

# ind.hierarchy = hpct.hierarchy 

for seed in range(6, 7, 1):
	print(f'seed={seed}')
	random.seed(seed)
	ind = evr.toolbox.individual()
	print(ind.get_grid())	
	for i in range(2):
		print(i, end=" ")
		ind()
		ind, = evr.toolbox.mutate(ind, choice=2, add_nodes=4)
		print(ind.get_grid())			
              
		link=ind.get_node(1,0).get_function_from_collection(HPCTFUNCTION.REFERENCE).get_links()[0]
		if isinstance(link, str):
			print('LNAME:',link)      
		else:    
			print(link.get_name())      
		pass


