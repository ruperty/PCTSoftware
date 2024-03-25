

import os 
# import warnings 
# warnings.simplefilter("ignore",category=UserWarning)

import numpy.testing as npt

from epct.po_evolvers import HPCTEvolveProperties, HPCTIndividual
# from cutils.paths import get_root_path, get_gdrive
from deap import base, creator
from epct.evolvers import CommonToolbox
from epct.configs import get_debug_level
from epct.evolve import evolve_setup


toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)


class TestEvolveWindTurbine():

    def __init__(self):
        if hasattr(creator, 'FitnessMin'):
            del creator.FitnessMin
            del creator.Individual

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)        
        if get_debug_level() > 1:
            self.pop_size,  self.gens = 100, 10     
        else:     
            self.pop_size,  self.gens = 4, 1
        debug= 0 #0 #3 # details of population in each gen, inc. mutate and merge
        hpct_verbose= False #True # log of every control system iteration
        evolve_verbose =  1 #2 # output of evolve iterations, 2 for best of each gen
        run_gen_best = True
        self.verbose={ 'debug': debug, 'evolve_verbose': evolve_verbose, 'hpct_verbose':hpct_verbose, 'run_gen_best':run_gen_best}
        self.prefix = 'testfiles' 
        self.suffix = ".properties"
        self.environment_properties={}

   

    def test_WT0538_RewardError_SummedError_Mode05(self):
        filename = 'WT0538-RewardError-SummedError-Mode05'        
        verbosed = {'debug': 0,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': False,
                    'save_arch_gen': False, 'run_gen_best': True, 'display_env': False, 'hpct_verbose': False}

        max = False
        env_name = "WindTurbine"
        drive = 'data' + os.sep
        root_path = self.prefix + os.sep
        configs_dir = ""
        args = {'file': filename, 'env_name': env_name, 'verbosed':verbosed, 'overwrite':True, 'draw_file' :False,
                        'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir, 'seed': 1,    
                        'comparisons' : True, 'comparisons_print_plots': False, 'hierarchy_plots': None,
                        'pop_size': self.pop_size, 'gens' : self.gens }

        score, results = evolve_setup(args)
        print(score)
        print(results)
        if os.name=='nt':

            npt.assert_almost_equal(score, -1329.2441095100335)
            npt.assert_almost_equal(results['energy_gain'], -2.735901797285656)
            npt.assert_almost_equal(results['net_energy_gain'], -2.659648309822038)
        else:
            npt.assert_almost_equal(score, -1329.2441095100335)
            npt.assert_almost_equal(results['energy_gain'], 0)
            npt.assert_almost_equal(results['net_energy_gain'], 0.40101754527281)



test = TestEvolveWindTurbine()
test.test_WT0538_RewardError_SummedError_Mode05()


