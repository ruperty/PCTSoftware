


import time
import argparse
from deap import base, creator
from epct.evolvers import CommonToolbox
from  multiprocessing import Pool
from os import sep
from cutils.paths import get_root_path, get_gdrive
from eepct.hpct import HPCTEvolveProperties
from eepct.hpct import HPCTIndividual

def evolve(args):
        seed=args['seed']
        filename=args['file']
        verbosed=args['verbosed']
        gens=args['gens']
        pop=args['pop']
        verbose=args['verbose']
        overwrite=args['overwrite']
        #{'seed': i, 'file': args.file, 'verbosed':args.verbosed, 'gens':args.gens, 'pop':args.pop, 
        #           'test':args.test, 'overwrite':args.overwrite, 'move':move, 'verbose': args.verbose}
        
        print(f'Start seed {seed}')
        tic = time.perf_counter()
        

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
        


        hep = HPCTEvolveProperties()
        output=True
        overwrite=True

        hash_num, desc, properties_str = hep.configure_evolver_from_properties_file(file=file, seed=seed, print_properties=True, verbose=verbose, toolbox=toolbox,  min=min)

        out, evr, score = hep.run_configured_evolver( file=file, print_properties=True, draw_file=True, out_dir=out_dir, hash_num=hash_num,
                                                output=output, overwrite=overwrite, node_size=node_size, font_size=font_size, log=True)


        if out != None:
                toc = time.perf_counter()
                elapsed = toc-tic        
                print(f'Seed {seed} Evolve time: {elapsed:4.2f}')



if __name__ == '__main__':
    
        parser = argparse.ArgumentParser()
        parser.add_argument("file", help="the properties file name")
        parser.add_argument("env_name", help="the environment name")
        parser.add_argument("-v", "--verbose", help="print output ", action="store_true")
        parser.add_argument("-hi","--history", help="plot stats history", action="store_true")
        parser.add_argument("-o", "--overwrite", help="overwrite existing file", action="store_true")
        parser.add_argument("-r", "--render", help="display environment run after each generation", action="store_true")
        #parser.add_argument("-t", "--test", help="test run", action="store_true")
        
        parser.add_argument('-i', '--iters', type=int, help="number of times to run, with different seeds", default=1)
        parser.add_argument('-p', '--pop', type=int, help="population size", default=100)
        parser.add_argument('-g', '--gens', type=int, help="number of generations")
        parser.add_argument('-s', '--start', type=int, help="initial seed value", default=1)
        parser.add_argument('-d', '--debug', type=int, help="debug level, 0 - 3", default=0)
        
        args = parser.parse_args()
        start=args.start
        iters=args.iters
                
        verbosed = {'debug':args.debug,  'evolve_verbose':args.verbose, 'deap_verbose': False, 'save_arch_all': False,
                'save_arch_gen':  False, 'display_env':args.render, 'deap_verbose':False, 'hpct_verbose':False}
        
        print(verbosed)


        list=[]
        for i in range(start, iters+start, 1):
                arg = {'seed': i, 'file': args.file, 'env_name':args.env_name, 'verbosed':verbosed, 'gens':args.gens, 
                'pop':args.pop, 'overwrite':args.overwrite, 'verbose': args.verbose}
                list.append(arg) 
    
        p = Pool()
        p.map(evolve, list)
        
        p.close()
        p.join()
