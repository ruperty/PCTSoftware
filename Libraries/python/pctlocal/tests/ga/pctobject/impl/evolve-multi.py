


import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the properties file name")
    
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
        
    verbosed = {'debug':args.debug, 'evolve_verbose':args.verbose, 'deap_verbose': False, 'save_arch_all': False,
               'save_arch_gen':  False, 'display_env':args.render, 'deap_verbose':False, 'hpct_verbose':False}
    
    print(verbosed)