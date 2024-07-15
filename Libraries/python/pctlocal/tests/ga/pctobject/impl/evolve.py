
from comet_ml import Experiment

import argparse
from cutils.paths import get_root_path, get_gdrive
from epct.evolve import evolve_setup


# python impl/evolve.py WindTurbine WT0416-RewardError-SummedError-Mode02 -b -o 

# python impl/evolve.py MicroGrid MG0001-RewardError-SummedError-Mode04 -b -o -x -v 
# python impl/evolve.py MicroGrid MG0001-RewardError-SummedError-Mode04 -b -o -x -a -aa -df 
# python impl/evolve.py WindTurbine WT0095-RewardError-RootMeanSquareError-Mode02 -b -a -aa -rp "{'comparisons' : True, 'comparisons_print_plots': False}" -db 4 > out.txt
# python impl/evolve.py ARC ARC0001-FitnessError-MovingSumError-Mode07 -b -v  > out.txt







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
	parser.add_argument("-db", "--debug", type=int, help="details of population in each gen, inc. mutate and merge", default=0)
	parser.add_argument("-pl", "--plots", type=str, help="hierarchy plots definition")
	parser.add_argument("-df", "--draw_file", help="draw image of best individual to file", action="store_true")	
	parser.add_argument("-o", "--overwrite", help="overwrite existing results file", action="store_true")
	# parser.add_argument("-l", "--log", help="log experiment to comet", action="store_true")
	parser.add_argument('-p', '--project', type=str, help="comet project name")#, default="test-evolve")
	parser.add_argument("-rp", "--results_props", type=str, help="properties for the results for an environment")


	args = parser.parse_args()
	env_name = args.env_name 
	filename = args.file
	start=args.start
	iters=args.iters                
	early = args.early 
	hierarchy_plots = args.plots
	max=args.max        
	overwrite = args.overwrite
	draw_file = args.draw_file
	hpct_verbose= args.hpct_verbose
	save_arch_all = args.save_arch_all
	# log_experiment= args.log
	results_props = eval(args.results_props) if args.results_props else None
	plots_dir = 'c:/tmp'
	log_testing_to_experiment = False
	api_key='WVBkFFlU4zqOyfWzk5PRSQbfD'
	project_name=args.project
	display_env=args.display_env

		
	verbosed = {'debug': args.debug,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': save_arch_all,
				'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best, 'display_env': display_env, 'hpct_verbose':hpct_verbose}
	drive = get_gdrive()
	root_path=get_root_path()
	configs_dir = 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/'

	if results_props is not None:
		arg = {'file': filename, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite, 'draw_file' :draw_file,
						'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir, 'hierarchy_plots': hierarchy_plots,
						'api_key':api_key, 'project_name':project_name,  'log_testing_to_experiment':log_testing_to_experiment, 'plots_dir': plots_dir
		} | results_props
	else:
		arg = {'file': filename, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite, 'draw_file' :draw_file,
						'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir, 'hierarchy_plots': hierarchy_plots,
						'api_key':api_key, 'project_name':project_name,  'log_testing_to_experiment':log_testing_to_experiment, 'plots_dir': plots_dir
		} 
	# env_proc = EnvironmentProcessingFactory.createEnvironmentProcessing(f'{env_name}EnvironmentProcessing')	
	# env_proc.set_properties(args=arg)
	# arg['workspace']=env_proc.get_workspace()


	for i in range(start, iters+start, 1):
		arg['seed']=i
		score = evolve_setup(arg)
		pass
	



