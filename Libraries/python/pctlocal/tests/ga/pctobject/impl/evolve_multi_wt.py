


import argparse

from os import cpu_count, sep, path
from multiprocessing import Pool
from cutils.paths import get_root_path, get_gdrive
from eepct.wind_turbine import evolve_wt_from_properties


if __name__ == '__main__':
    
	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("files", help="the properties file name list")

	parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
	# parser.add_argument('-p', '--pop', type=int, help="population size", default=100)
	# parser.add_argument('-g', '--gens', type=int, help="number of generations")
	parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
	parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_true")
	parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_true")
	parser.add_argument("-x", "--max", help="maximise fitness function", action="store_true")
	parser.add_argument('-c', '--cpu', type=int, help="number of processes", default=8)
	
	args = parser.parse_args()
	start=args.start
	iters=args.iters

	verbose=False

	comparisons = False 
	comparisons_print_plots = True
	log_experiment=True
	api_key='WVBkFFlU4zqOyfWzk5PRSQbfD'
	project_name='test-evolve'
	workspace='wind-turbine'
	experiment_name = 'steady'

	verbosed = {'debug': 0,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': False,
				'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best, 'display_env': False, 'hpct_verbose':False}
	drive = get_gdrive()
	root_path=get_root_path()
	configs_dir = 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/'
	overwrite=True

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
					arg = {'seed': i, 'file': filen, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite,
                    'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir, 'comparisons': comparisons, 
					'comparisons_print_plots':comparisons_print_plots, 'log_experiment':log_experiment, 'api_key':api_key,
					'project_name':project_name, 'workspace':workspace, 'experiment_name':experiment_name
					}#,'gens':args.gens, 'pop':args.pop }
					list.append(arg) 

	# print(list)

	mprocesses = cpu_count()
	print(f'Machine processes={mprocesses}')
	processes = args.cpu
	if processes > len(list):
			processes = len(list)
	print(f'Application processes={processes}')
	p = Pool(processes=processes)

	p.map(evolve_wt_from_properties, list)
	
	p.close()
	p.join()
