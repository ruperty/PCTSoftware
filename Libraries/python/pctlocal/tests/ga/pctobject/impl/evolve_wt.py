
#import logging
import argparse, os
from datetime import datetime
from cutils.paths import get_root_path, get_gdrive
from eepct.wind_turbine import evolve_wt_from_properties
#logger = logging.getLogger(__name__)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("file", help="the properties file name")
	parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_true")
	parser.add_argument("-aa", "--save_arch_all", help="save architecture of entire population of each generation", action="store_true")
	parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_true")
	parser.add_argument("-d", "--display_env", help="display best of each generation", action="store_true")
	parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
	parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
	parser.add_argument('-e', '--early', help="early termination", action="store_true")
	parser.add_argument("-x", "--max", help="maximise fitness function", action="store_true")
	parser.add_argument("-v", "--hpct_verbose", help="hierarchy output", action="store_true")
	parser.add_argument("-o", "--overwrite", help="overwrite existing results file", action="store_true")
	parser.add_argument("-l", "--log", help="log experiment to comet", action="store_true")
	parser.add_argument("-df", "--draw_file", help="draw image of best individual to file", action="store_true")
	parser.add_argument("-db", "--debug", type=int, help="details of population in each gen, inc. mutate and merge", default=0)
	parser.add_argument('-p', '--project', type=str, help="comet project name", default="test-evolve")
	parser.add_argument("-pl", "--plots", type=str, help="hierarchy plots definition")

	args = parser.parse_args()
	env_name = args.env_name 
	filename = args.file
	start=args.start
	iters=args.iters                
	early = args.early 
	max=args.max        
	hpct_verbose= args.hpct_verbose
	log_experiment= args.log
	overwrite = args.overwrite
	draw_file = args.draw_file
	hierarchy_plots = args.plots
	save_arch_all = args.save_arch_all

	comparisons = True 
	comparisons_print_plots = True
	plots_dir = 'c:/tmp'
	log_testing_to_experiment = False
	api_key='WVBkFFlU4zqOyfWzk5PRSQbfD'
	project_name=args.project
	workspace='wind-turbine'
	# experiment_name = 'steady'
			
	verbosed = {'debug': 0,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': save_arch_all,
				'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best, 'display_env': False, 'hpct_verbose':hpct_verbose}
	drive = get_gdrive()
	root_path=get_root_path()
	configs_dir = 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/'
	# overwrite=False

	for i in range(start, iters+start, 1):
		arg = {'seed': i, 'file': filename, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite, 'draw_file' :draw_file,
						'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir, 'comparisons': comparisons, 
					'comparisons_print_plots':comparisons_print_plots, 'log_experiment':log_experiment, 'api_key':api_key, 'hierarchy_plots': hierarchy_plots,
					'project_name':project_name, 'workspace':workspace, 'log_testing_to_experiment':log_testing_to_experiment, 'plots_dir': plots_dir
		}#,'gens':args.gens, 'pop':args.pop }
					
		pf = evolve_wt_from_properties(arg)
		pass



		





