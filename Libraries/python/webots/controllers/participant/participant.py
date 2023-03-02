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
#from pct.putils import FunctionsList
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


class Wrestler (Robot):
    def run(self):
        print("hello")
        # to load all the motions from the motions folder, we use the MotionLibrary class:
        motion_library = MotionLibrary()
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        time_step = int(self.getBasicTimeStep())
        while self.step(time_step) != -1:  # mandatory function to make the simulation run
            #print("b4")
            motion_library.play('Forwards')
            #print("b5")


# create the Robot instance and run main loop
wrestler = Wrestler()
wrestler.run()


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