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

from abc import ABC

import numpy as np
from pct.functions import BaseFunction
from pct.putils import FunctionsList
from epct.functions import EAConstant

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
        def create(self, seed=None): return Wrestler(seed=seed)
    class FactoryWithNamespace:
        def create(self, namespace=None, seed=None): return Wrestler(namespace=namespace, seed=seed)          

import os
CI = os.environ.get("CI")
print(CI)

wrestler = WebotsWrestler()
for _ in range(100):
    wrestler()






# create the Robot instance and run main loop

# print("hello")
# wrestler = Wrestler()
# wrestler.run()


# class Fatima (Robot):
#     SMALLEST_TURNING_RADIUS = 0.1
#     SAFE_ZONE = 0.75
#     TIME_BEFORE_DIRECTION_CHANGE = 200  # 8000 ms / 40 ms

#     def __init__(self):
#         Robot.__init__(self)
#         self.time_step = int(self.getBasicTimeStep())

#         self.camera = Camera(self)
#         self.fall_detector = FallDetection(self.time_step, self)
#         self.gait_manager = GaitManager(self, self.time_step)
#         self.heading_angle = 3.14 / 2
#         # Time before changing direction to stop the robot from falling off the ring
#         self.counter = 0

#     def run(self):
#         while self.step(self.time_step) != -1:
#             # We need to update the internal theta value of the gait manager at every step:
#             t = self.getTime()
#             self.gait_manager.update_theta()
#             if 0.3 < t < 2:
#                 self.start_sequence()
#             elif t > 2:
#                 self.fall_detector.check()
#                 self.walk()

#     def start_sequence(self):
#         """At the beginning of the match, the robot walks forwards to move away from the edges."""
#         self.gait_manager.command_to_motors(heading_angle=0)

#     def walk(self):
#         """Dodge the opponent robot by taking side steps."""
#         normalized_x = self._get_normalized_opponent_x()
#         # We set the desired radius such that the robot walks towards the opponent.
#         # If the opponent is close to the middle, the robot walks straight.
#         desired_radius = (self.SMALLEST_TURNING_RADIUS / normalized_x) if abs(normalized_x) > 1e-3 else None
#         # TODO: position estimation so that if the robot is close to the edge, it switches dodging direction
#         if self.counter > self.TIME_BEFORE_DIRECTION_CHANGE:
#             self.heading_angle = - self.heading_angle
#             self.counter = 0
#         self.counter += 1
#         self.gait_manager.command_to_motors(desired_radius=desired_radius, heading_angle=self.heading_angle)

#     def _get_normalized_opponent_x(self):
#         """Locate the opponent in the image and return its horizontal position in the range [-1, 1]."""
#         img = self.camera.get_image()
#         _, _, horizontal_coordinate = IP.locate_opponent(img)
#         if horizontal_coordinate is None:
#             return 0
#         return horizontal_coordinate * 2 / img.shape[1] - 1


# # create the Robot instance and run main loop
# wrestler = Fatima()
# wrestler.run()