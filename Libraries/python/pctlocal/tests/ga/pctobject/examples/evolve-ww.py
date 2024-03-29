
import logging
import platform
    
    
import argparse
from os import sep, makedirs, getenv
from datetime import datetime
from eepct.hpct import HPCTEvolveProperties
from cutils.paths import get_root_path, get_gdrive
from deap import base, creator
from epct.evolvers import CommonToolbox
from eepct.hpct import HPCTIndividual
from time import sleep

from pct.network import ClientConnectionManager



if __name__ == '__main__':
    
	parser = argparse.ArgumentParser()
	parser.add_argument("env_name", help="the environment name")
	parser.add_argument("file", help="the properties file name")
	parser.add_argument('-p', '--port', type=int, help="port number")
	args = parser.parse_args()
	env_name = args.env_name 
	filename = args.file
	port = args.port 

	# if port == None:
	#         port = 9999
	#         env_name = 'WebotsWrestler' 
	#         filename = 'XXX-Dummy-Mode04'

	cm = ClientConnectionManager.getInstance()
	cm.set_port(port)

	out_dir= get_gdrive() + f'data{sep}ga{sep}'

	creator.create("FitnessMax", base.Fitness, weights=(1.0,))
	creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMax)

	min=False

	toolbox = base.Toolbox()
	CommonToolbox.getInstance().set_toolbox(toolbox)

	node_size, font_size=150, 10

	root = get_root_path()



	file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/pctobject/configs/' + env_name +'/'+ filename + ".properties"

	local_out_dir = 'output/'  + filename 
	draw_file= local_out_dir + '/' + filename + '-evolve-best' + '.png'

	debug= 0 #0 #3 # details of population in each gen, inc. mutate and merge
	hpct_verbose= False #True # log of every control system iteration
	evolve_verbose =  1 #2 # output of evolve iterations, 2 for best of each gen

	# debug= 2 #3 #0 #3 # details of population in each gen, inc. mutate and merge
	#hpct_verbose= 1 #True # log of every control system iteration
	#evolve_verbose = 3 #2# 1 #2 # output of evolve iterations, 2 for best of each gen

	save_arch_gen = True #False #True
	display_env = True #True #False#
	run_gen_best = True # #False #True

	#save_arch_gen = False #True
	#display_env = False #False#
	#run_gen_best = False # #False #True

	verbose={ 'debug': debug, 'evolve_verbose': evolve_verbose, 'display_env': display_env, 'hpct_verbose':hpct_verbose, 
			'save_arch_gen': save_arch_gen, 'run_gen_best':run_gen_best}

	hep = HPCTEvolveProperties()
	output=True
	overwrite=True

	# for i in range(20):
	#         print(f'Sleeping for {10-i} seconds')
	#         sleep(1)

	hash_num, desc = hep.configure_evolver_from_properties_file(file=file, print_properties=True, verbose=verbose, toolbox=toolbox,  min=min)

	# logging info
	now = datetime.now() # current date and time
	date_time = now.strftime("%Y%m%d-%H%M%S")
	log_dir=sep.join((out_dir, env_name, desc, hash_num, "output"))
	makedirs(log_dir,exist_ok = True) 
	log_file=sep.join((log_dir, "evolve-client-"+platform.node()+"-"+date_time+".log"))
	logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )
	logger = logging.getLogger(__name__)
	logger.info("Evolving {} ".format(env_name))

	try:
			hep.run_configured_evolver( file=file, print_properties=True, draw_file=True, out_dir=out_dir, hash_num=hash_num,
							output=output, overwrite=overwrite, node_size=node_size, font_size=font_size, log=True)

	except Exception as e:
			if hasattr(e, 'message'):
					print(e.message)
					logger.info(e.message)
			else:
					print(e)
					logger.info(e)




	# logger.info('Start evolve_ww')
	# hep.configure_evolver_from_properties_file(file=file, print_properties=True, verbose=verbose, toolbox=toolbox, draw_file=draw_file, 
	#                                         out_dir=out_dir, local_out_dir=local_out_dir, output=output, overwrite=overwrite, 
	#                                         node_size=node_size, font_size=font_size, min=min)
        


