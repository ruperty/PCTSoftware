# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Minimalist controller example for the Robot Wrestling Tournament.
   Demonstrates how to play a simple motion file."""


import numpy as np

from controller import Robot
import sys

# We provide a set of utilities to help you with the development of your controller. You can find them in the utils folder.
# If you want to see a list of examples that use them, you can go to https://github.com/cyberbotics/wrestling#demo-robot-controllers
sys.path.append('..')
from utils.motion_library import MotionLibrary

from utils.image_processing import ImageProcessing as IP
from utils.fall_detection import FallDetection
from utils.gait_manager import GaitManager
from utils.camera import Camera

from utilities.robot import RobotReadings


class Wrestler (Robot):
    
    def __init__(self):
        Robot.__init__(self)
        self.rr = RobotReadings(self)
        # to load all the motions from the motions folder, we use the MotionLibrary class:
        self.motion_library = MotionLibrary()
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        self.time_step = int(self.getBasicTimeStep())
        self.coverage = 0
        
    def __call__(self, verbose=False):
        out = self.step(self.time_step)
        print(out)
        self.motion_library.play('Forwards')
        self.rr.readLegs()
        print("coverage=",self.get_coverage())
    
    def set_coverage(self, coverage):
        self.coverage = coverage

    def get_coverage(self):
        return self.coverage 

    def run(self):
        while self.step(self.time_step) != -1:  # mandatory function to make the simulation run
            #print("b4")
            self.motion_library.play('Forwards')
            self.rr.readLegs()
            #print("b5")


from pct.functions import BaseFunction
from pct.putils import FunctionsList


class WebotsWrestler(BaseFunction):
    "A function that creates and runs a Webots Wrestler robot."
    
    def __init__(self, render=False, value=0, name="Wrestler", seed=None, links=None, new_name=True, 
                 early_termination=True, namespace=None):    
        super().__init__(name=name, value=value, links=links, new_name=new_name, namespace=namespace)
        self.robot = Wrestler()
        self.early_termination=early_termination
        
        
    def __call__(self, verbose=False):        
        super().__call__(verbose)

        self.robot()
                
        return self.value

    def early_terminate(self):
        if self.early_termination:
            if self.really_done:
                raise Exception(f'1000: OpenAIGym Env: {self.env_name} has terminated.')
            if self.done:
                self.reward = 0
                self.really_done = True
                
    def process_input(self):
        force = min(max(self.input, self.min_action), self.max_action)
        self.input=[force]
        
    def process_values(self):
        reward = self.obs[1]
        if reward > 90:
            reward = 0
        self.reward = - reward
        pos = self.value[0] + 1.2
        self.value = np.append(self.value, pos)

    def summary(self, extra=False):
        super().summary("", extra=extra)
        
    def get_graph_name(self):
        return super().get_graph_name() 

    def get_config(self, zero=1):
        "Return the JSON  configuration of the function."
        config = {"type": type(self).__name__,
                    "name": self.name}
        
        if isinstance(self.value, np.ndarray):
            config["value"] = self.value.tolist() * zero
        else:
            config["value"] = self.value * zero
        
        ctr=0
        links={}
        for link in self.links:
            func = FunctionsList.getInstance().get_function(self.namespace, link)
            try:
                links[ctr]=func.get_name()
            except AttributeError:
                #raise Exception(f' there is no function called {link}, ensure it exists first.')            
                print(f'WARN: there is no function called {link}, ensure it exists first.')            
                links[ctr]=func
                
            ctr+=1
        
        config['links']=links

        config["env_name"] = self.env_name
        #config["values"] = self.value
        config["reward"] = self.reward
        config["done"] = self.done
        config["info"] = self.info
    
    
    class Factory:
        def create(self, seed=None): return WebotsWrestler(seed=seed)
    class FactoryWithNamespace:
        def create(self, namespace=None, seed=None): return WebotsWrestler(namespace=namespace, seed=seed)          


from pct.environments import EnvironmentFactory

env = EnvironmentFactory.createEnvironment("WebotsWrestler")

print("hello")

#from webots.environments import WebotsWrestler


import random
from eepct.hpct import HPCTIndividual, HPCTEvolver, HPCTArchitecture, HPCTEvolverWrapper
from eepct.hpct import HPCTFUNCTION, HPCTLEVEL, HPCTVARIABLE


from epct.evolvers import CommonToolbox
from deap import base, creator



creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

lower, upper = -1, 1 
arch = HPCTArchitecture(lower_float=lower, upper_float=upper)
arch.configure()
arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
print(arch)

env_name = 'WebotsWrestler'
env_inputs_indexes=[1, 0, 3, 2]
env_inputs_names=['ICV', 'ICP', 'IPV', 'IPA']
references=[0]

error_collector_type , error_response_type = 'InputsError', 'RootMeanSquareError'
seed, debug, pop_size, processes, runs, nevals, num_actions=1, 0, 10, 1, 500, 1, 1
min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 5, 1, 5, 100
zerolevel_inputs_indexes=None
toplevel_inputs_indexes=None

environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes, 'render':False, 'early_termination': False,
    'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env_name, 'num_actions':num_actions, 'references':references}
hpct_run_properties ={ 'hpct_verbose':False, 'debug':debug , 'runs':runs, 'nevals':nevals, 'seed':seed,  'error_collector_type' :  'InputsError', 'error_response_type' : 'RootMeanSquareError'}   
evolve_properties = {'attr_mut_pb':0.8,'structurepb':1} #, 'attr_cx_uniform_pb':0.5, 'alpha':0.5} 
hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit, 'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit }    


evolver_properties = {'environment_properties':environment_properties, 
    'evolve_properties':evolve_properties,  
    'hpct_structure_properties':hpct_structure_properties,
    'hpct_run_properties':hpct_run_properties,
    'arch': arch}


random.seed(seed)
evolver = HPCTEvolver(**evolver_properties)
#print(evolver_properties)
evr = HPCTEvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes, p_crossover=0.8, p_mutation=0.5, display_env=True)

test=1
if test==1:
    
    loops = 10
    for _ in range(loops):
        ind1 = evr.toolbox.individual()        
        print()
        print(ind1.get_parameters_list())


