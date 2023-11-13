


import logging
import time
import argparse

from os import sep, makedirs, getenv, cpu_count
from datetime import datetime
from deap import base, creator
from epct.evolvers import CommonToolbox
from multiprocessing import Pool
from cutils.paths import get_root_path, get_gdrive
from eepct.hpct import HPCTEvolveProperties
from eepct.hpct import HPCTIndividual

def evolve(args):
	seed=args['seed']
	filename=args['file']

	env_name=args['env_name']
	verbose= args['verbosed']
	min=True
	max= args['max']

	tic = time.perf_counter()
	out_dir= get_gdrive() + f'data{sep}ga{sep}'
	node_size, font_size=150, 10
	root = get_root_path()

	file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/' + env_name +'/'+ filename + ".properties"

	# local_out_dir = 'output/'  + filename 
	# draw_file= local_out_dir + '/' + filename + '-evolve-best' + '.png'

	if max:
			# flip=True
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

	print(f'Start seed={seed} min={min} file={filename}')

	hep = HPCTEvolveProperties()
	output=True
	overwrite=True


	# print(verbose)
	hash_num, desc, properties_str = hep.configure_evolver_from_properties_file(file=file, seed=seed, verbose=verbose, toolbox=toolbox,  min=min, print_properties=False)        

		# logging info
	now = datetime.now() # current date and time
	date_time = now.strftime("%Y%m%d-%H%M%S")
	log_dir=sep.join((out_dir, env_name, desc))
	makedirs(log_dir,exist_ok = True) 
	log_file=sep.join((log_dir, "evolve-"+  hash_num +"-"+ date_time+".log"))
	logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )
	logger = logging.getLogger(__name__)
	logger.info("Evolving {} ".format(env_name))
	logger.info(properties_str)
	logger.info(f'hash_num={hash_num}')
	
	out, evr, score = hep.run_configured_evolver( file=file, print_properties=True, draw_file=True, out_dir=out_dir, hash_num=hash_num, output=output, overwrite=overwrite, node_size=node_size, font_size=font_size, log=True)
	# out = True

	if out != None:
			toc = time.perf_counter()
			elapsed = toc-tic        
			print(f'Seed {seed} Evolve time: {elapsed:4.2f}')



if __name__ == '__main__':
    
	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("files", help="the properties file name list")

	parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
	parser.add_argument('-p', '--pop', type=int, help="population size", default=100)
	parser.add_argument('-g', '--gens', type=int, help="number of generations")
	parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
	parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_false")
	parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_false")
	parser.add_argument("-x", "--max", help="maximise fitness function", action="store_true")
	parser.add_argument('-c', '--cpu', type=int, help="number of processes", default=8)
	
	args = parser.parse_args()
	start=args.start
	iters=args.iters
			
	verbosed = {'debug': 0,  'evolve_verbose': 0, 'deap_verbose': False, 'save_arch_all': False,
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
					arg = {'seed': i, 'file': filen, 'env_name':args.env_name, 'verbosed':verbosed, 'gens':args.gens, 'pop':args.pop, 'max':max}
					list.append(arg) 

	# print(list)

	mprocesses = cpu_count()
	print(f'Machine processes={mprocesses}')
	processes = args.cpu
	if processes > len(list):
			processes = len(list)
	print(f'Application processes={processes}')
	p = Pool(processes=processes)

	p.map(evolve, list)
	
	p.close()
	p.join()
