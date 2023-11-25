
#import logging
import argparse
from cutils.paths import get_root_path, get_gdrive
from eepct.hpct import evolve_from_properties

#logger = logging.getLogger(__name__)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("file", help="the properties file name")
	parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_false")
	parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_false")
	parser.add_argument("-d", "--display_env", help="display best of each generation", action="store_false")
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
		
	verbosed = {'debug': 0,  'evolve_verbose': 1, 'deap_verbose': False, 'save_arch_all': False,
				'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best, 'display_env': False, 'hpct_verbose':False}
	drive = get_gdrive()
	root_path=get_root_path()
	configs_dir = 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/'
	overwrite=True

	for i in range(start, iters+start, 1):
		arg = {'seed': i, 'file': filename, 'env_name':args.env_name, 'verbosed':verbosed, 'overwrite':overwrite,
						'max':max, 'drive':drive, 'root_path':root_path, 'configs_dir':configs_dir
		}#,'gens':args.gens, 'pop':args.pop }
					
		pf = evolve_from_properties(arg)
		pass
	
	# out_dir= get_gdrive() + f'data{sep}ga{sep}'

	# if max:
	# 		creator.create("FitnessMax", base.Fitness, weights=(1.0,))
	# 		creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMax)
	# 		flip=True
	# 		min=False
	# else:
	# 		creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
	# 		creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)
	# 		flip=False
	# 		min=True

	# toolbox = base.Toolbox()
	# CommonToolbox.getInstance().set_toolbox(toolbox)

	# node_size, font_size=150, 10

	# root = get_root_path()

	# file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/' + env_name +'/'+ filename + ".properties"

	# evolve_verbose =  1 #2 # output of evolve iterations, 2 for best of each gen

	# verbose={ 'debug': args.debug, 'evolve_verbose': evolve_verbose, 'display_env': args.display_env, 'hpct_verbose':hpct_verbose, 
	# 		'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best}

	# hep = HPCTEvolveProperties()
	# output=True
	# overwrite=True

	# for seed in range(start, iters+start, 1):
	# 	hash_num, desc, properties_str = hep.configure_evolver_from_properties_file(file=file, seed=seed, print_properties=True, verbose=verbose, toolbox=toolbox,  min=min)
		
	# 	# logging info
	# 	now = datetime.now() # current date and time
	# 	date_time = now.strftime("%Y%m%d-%H%M%S")
	# 	log_dir=sep.join((out_dir, env_name, desc))
	# 	makedirs(log_dir,exist_ok = True) 
	# 	log_file=sep.join((log_dir, "evolve-" + hash_num+"-"+date_time+".log"))
	# 	logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )
	# 	logger = logging.getLogger(__name__)
	# 	logger.info("Evolving {} ".format(env_name))
	# 	logger.info(properties_str)
	# 	logger.info(f'hash_num={hash_num}')

	# 	# try:
	# 	hep.run_configured_evolver( file=file, print_properties=True, draw_file=True, out_dir=out_dir, hash_num=hash_num,
	# 							output=output, overwrite=overwrite, node_size=node_size, font_size=font_size, log=True)

		





