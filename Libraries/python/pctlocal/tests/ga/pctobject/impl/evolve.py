
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


logger = logging.getLogger(__name__)

# set EA_ENVNAME=CartPoleV1

if __name__ == '__main__':
        
        env_name = getenv('EA_ENVNAME')
        filename = getenv('EA_FILENAME')
        
        if env_name is None:    
                parser = argparse.ArgumentParser()
                parser.add_argument("env_name", help="the environment name")
                parser.add_argument("file", help="the properties file name")
                parser.add_argument("-a", "--save_arch_gen", help="save architecture of each generation", action="store_false")
                parser.add_argument("-b", "--run_gen_best", help="run best of each generation", action="store_false")
                parser.add_argument("-d", "--display_env", help="display best of each generation", action="store_true")
                parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
                parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)

                args = parser.parse_args()
                env_name = args.env_name 
                filename = args.file
                start=args.start
                iters=args.iters
                

        out_dir= get_gdrive() + f'data{sep}ga{sep}'

        max = False
        if max:
                creator.create("FitnessMax", base.Fitness, weights=(1.0,))
                creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMax)
                flip=True
                min=False
        else:
                creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
                creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)
                flip=False
                min=True


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

       

        verbose={ 'debug': debug, 'evolve_verbose': evolve_verbose, 'display_env': args.display_env, 'hpct_verbose':hpct_verbose, 
                'save_arch_gen': args.save_arch_gen, 'run_gen_best':args.run_gen_best}
        
        # print(verbose)

        hep = HPCTEvolveProperties()
        output=True
        overwrite=True

         # logging info
        now = datetime.now() # current date and time
        date_time = now.strftime("%Y%m%d-%H%M%S")
        log_dir=sep.join((out_dir, env_name, filename))
        makedirs(log_dir,exist_ok = True) 
        log_file=sep.join((log_dir, "evolve-"+platform.node()+"-"+date_time+".log"))
        logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )
        logger = logging.getLogger(__name__)

        for seed in range(start, iters+start, 1):
                hash_num, desc, properties_str = hep.configure_evolver_from_properties_file(file=file, seed=seed, print_properties=True, verbose=verbose, toolbox=toolbox,  min=min)
                
                logger.info("Evolving {} ".format(env_name))
                logger.info(properties_str)

                # try:
                hep.run_configured_evolver( file=file, print_properties=True, draw_file=True, out_dir=out_dir, hash_num=hash_num,
                                        output=output, overwrite=overwrite, node_size=node_size, font_size=font_size, log=True)

                # except Exception as e:
                #         if hasattr(e, 'message'):
                #                 print(e.message)
                #                 logger.info(e.message)
                #         else:
                #                 print(e)
                #                 logger.info(e)


        


