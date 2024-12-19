

from comet_ml import Experiment
import argparse
import os
from multiprocessing import Pool
# from cutils.paths import get_root_path, get_gdrive
from epct.evolve import evolve_setup
from pct.putils import set_dirs


def remove_files_in_plots_dir(plots_dir):
	
	files = os.listdir(plots_dir)
	for file in files:
		file_path = os.path.join(plots_dir, file)
		if os.path.isfile(file_path):
			os.remove(file_path)


if __name__ == '__main__':
    
	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("files", help="the properties file name list")
	parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
	parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
	parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_true")
	parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_true")
	parser.add_argument("-x", "--max", help="maximise fitness function", action="store_true")
	parser.add_argument('-c', '--cpu', type=int, help="number of processes", default=8)
	parser.add_argument('-p', '--project', type=str, help="comet project name")#, default="test-evolve")
	parser.add_argument("-rp", "--results_props", type=str, help="properties for the results for an environment")
	parser.add_argument("-pl", "--plots", type=str, help="hierarchy plots definition")
	parser.add_argument("-df", "--draw_file", help="draw image of best individual to file", action="store_true")
	parser.add_argument("-o", "--overwrite", help="overwrite existing results file", action="store_true")
	parser.add_argument("-ds", "--dirs", type=str, help="directories for root and gdrive", default=None)

	args = parser.parse_args()
	start=args.start
	iters=args.iters

	overwrite = args.overwrite
	draw_file = args.draw_file
	hierarchy_plots = args.plots
	results_props = eval(args.results_props) if args.results_props else None
	log_testing_to_experiment = False
	project_name=args.project
	dirs = set_dirs(args.dirs)


	remove_files_in_plots_dir(dirs['plots_dir'])

	verbosed = {'debug': 0,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': False,
				'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best, 'display_env': False, 'hpct_verbose':False}


	list=[]
	for file in eval(args.files):    
			index = file.find(' ')
			if index < 0:
				filen=file
				max = args.max
			else:
				filen = file[0:index]
				arg = file[index+1:]
				if arg == '-x' or arg == '-max':
					max = True


			print(filen)    
			for i in range(start, iters+start, 1):
				if results_props:
					arg = {'seed': i, 'file': filen, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite, 'draw_file' :draw_file,
                    'max':max, 'drive':dirs['drive'], 'root_path':dirs['root_path'], 'configs_dir':dirs['configs_dir'], 'hierarchy_plots': hierarchy_plots,
					'project_name':project_name,  'log_testing_to_experiment':log_testing_to_experiment, 'plots_dir': dirs['plots_dir']
					} | results_props
				else:
					arg = {'seed': i, 'file': filen, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite, 'draw_file' :draw_file,
                    'max':max, 'drive':dirs['drive'], 'root_path':dirs['root_path'], 'configs_dir':dirs['configs_dir'], 'hierarchy_plots': hierarchy_plots,
					'project_name':project_name,  'log_testing_to_experiment':log_testing_to_experiment, 'plots_dir': dirs['plots_dir']
					} 

				list.append(arg) 

	# print(list)

	mprocesses = os.cpu_count()
	print(f'Machine processes={mprocesses}')
	processes = args.cpu
	if processes > len(list):
			processes = len(list)
	print(f'Application processes={processes}')
	p = Pool(processes=processes)

	p.map(evolve_setup, list)
	
	p.close()
	p.join()
