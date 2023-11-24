


import argparse

from os import cpu_count, sep
from multiprocessing import Pool
from cutils.paths import get_root_path, get_gdrive
from eepct.hpct import evolve_from_properties
from eepct.wind_turbine import wind_turbine_results, get_environment_properties

def evolve_wt_from_properties(args):
	filepath = evolve_from_properties(args)
	environment_properties=None
	root = get_gdrive() 
	comparisons = False #True #False
	comparisons_print_plots = True
	log_experiment=False
	plots=None
	verbose=False
	early=None
	plots=[]

	index1=filepath.rindex(sep)
	file = filepath[index1+1:]
	print(file)
	index2=filepath.rindex(sep, 0, index1)
	property_dir=filepath[index2+1:index1]
	print(property_dir)

	if environment_properties is None:
		environment_properties = get_environment_properties(root=root, property_dir=property_dir, property_file=file)
		environment_properties['keep_history'] = True
		environment_properties['range'] = 'test'
        # environment_properties['reward_type']= 'power'
		print(environment_properties)

	wind_turbine_results(environment_properties=environment_properties, log_experiment=log_experiment, root=root, verbose=verbose, 
					  early=early, comparisons=comparisons, comparisons_print_plots=comparisons_print_plots, property_dir=property_dir, property_file=file, plots=plots)





if __name__ == '__main__':
    
	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("files", help="the properties file name list")

	parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
	# parser.add_argument('-p', '--pop', type=int, help="population size", default=100)
	# parser.add_argument('-g', '--gens', type=int, help="number of generations")
	parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
	parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_false")
	parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_false")
	parser.add_argument("-x", "--max", help="maximise fitness function", action="store_true")
	parser.add_argument('-c', '--cpu', type=int, help="number of processes", default=8)
	
	args = parser.parse_args()
	start=args.start
	iters=args.iters
			
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
                    'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir
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
