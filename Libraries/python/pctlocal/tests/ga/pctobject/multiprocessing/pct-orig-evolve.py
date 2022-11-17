
import time
import os
import sys
import socket
import warnings
import multiprocessing

warnings.simplefilter(action='ignore', category=UserWarning)
from deap import base
from deap import creator

from epct.evolvers import evolve_from_properties_file
from epct.evolvers import CommonToolbox

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)


if hasattr(creator, 'FitnessMin'):
    del creator.FitnessMin
    del creator.Individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


def evolve(processes):
    verbose = {'evolve_verbose':1}
    print_properties=True
    gens=None
    pop_size=None
    output=False
    #gens=1
    #pop_size = 4
    if os.name=='nt':
        out_dir='c:/tmp/'
    else:
        out_dir='/mnt/c/tmp/'
        root_dir = '/mnt/c'
        user='ryoung'
        if socket.gethostname() == 'DESKTOP-5O07H5P':
            user='ruper'

        file_path = 'Users/'+user+'/Versioning/PCTSoftware/Libraries/python/pctlocal/tests/ga/dynamic/CartPoleV1'

    move={'OL0C0ws':[0.25,0], 'CL0C0':[0.25,0]}
    filename = 'InputsError-RootMeanSquareError-Binary-WeightedSum-Std.properties'



    tic = time.perf_counter()
    out,evr,score = evolve_from_properties_file(root_dir=root_dir, path=file_path, file=filename, 
        gens=gens, pop_size=pop_size, out_dir=out_dir, draw=False, verbose=verbose, 
        print_properties=print_properties, move=move, output=output, overwrite=True,
        toolbox=toolbox,processes=processes)
    toc = time.perf_counter()
    elapsed = toc-tic
    print(f'Evolve time: {elapsed:4.2f}')



if __name__ == "__main__":
    processes=4
    argsc=len(sys.argv)
    print(argsc)
    if argsc>1:
        processes = int(sys.argv[1])
    print('processes ', processes)
    evolve(processes)