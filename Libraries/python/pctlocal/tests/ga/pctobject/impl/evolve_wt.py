
#import logging
import argparse
from cutils.paths import get_root_path, get_gdrive
from eepct.wind_turbine import evolve_wt_from_properties

#logger = logging.getLogger(__name__)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("file", help="the properties file name")
	parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_true")
	parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_true")
	parser.add_argument("-d", "--display_env", help="display best of each generation", action="store_true")
	parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
	parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
	parser.add_argument('-e', '--early', help="early termination", action="store_true")
	parser.add_argument("-x", "--max", help="maximise fitness function", action="store_true")
	parser.add_argument("-v", "--hpct_verbose", help="hierarchy output", action="store_true")
	parser.add_argument("-db", "--debug", type=int, help="details of population in each gen, inc. mutate and merge", default=0)
	# parser.add_argument('-p', '--pop', type=int, help="population size", default=100)
	# parser.add_argument('-g', '--gens', type=int, help="number of generations")


	args = parser.parse_args()
	env_name = args.env_name 
	filename = args.file
	start=args.start
	iters=args.iters                
	early = args.early 
	max=args.max        
	hpct_verbose= args.hpct_verbose

	comparisons = False 
	comparisons_print_plots = True
	log_experiment= True #False #True
	log_testing_to_experiment = False
	api_key='WVBkFFlU4zqOyfWzk5PRSQbfD'
	project_name='test-evolve'
	workspace='wind-turbine'
	experiment_name = 'steady'
			
	verbosed = {'debug': 0,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': False,
				'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best, 'display_env': False, 'hpct_verbose':hpct_verbose}
	drive = get_gdrive()
	root_path=get_root_path()
	configs_dir = 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/'
	overwrite=True

	for i in range(start, iters+start, 1):
		arg = {'seed': i, 'file': filename, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite,
						'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir, 'comparisons': comparisons, 
					'comparisons_print_plots':comparisons_print_plots, 'log_experiment':log_experiment, 'api_key':api_key,
					'project_name':project_name, 'workspace':workspace, 'experiment_name':experiment_name, 'log_testing_to_experiment':log_testing_to_experiment
		}#,'gens':args.gens, 'pop':args.pop }
					
		pf = evolve_wt_from_properties(arg)
		pass
	

		





