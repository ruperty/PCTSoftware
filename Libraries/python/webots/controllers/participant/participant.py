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
import os
import time
import math
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


from  pct.network import Server
from controller import Supervisor


class WrestlerSupervisorServer(Supervisor):
    def initSupervisor(self):
        self.robot = [0] * 2
        self.robot[1] = self.getFromDef('WRESTLER_BLUE').getFromProtoDef('HEAD_SLOT')
        self.robot[0] = self.getFromDef('WRESTLER_RED').getFromProtoDef('HEAD_SLOT')
        self.min = [[0] * 3 for i in range(2)]
        self.max = [[0] * 3 for i in range(2)]
        for i in range(2):
            self.min[i] = self.robot[i].getPosition()
            self.max[i] = self.robot[i].getPosition()
        self.coverage = [0] * 2
        self.ko_count = [0] * 2

    def initServer(self):        
        self.server = Server()
        rec = self.server.get_dict()
        print(rec)
        dict = {'msg': 'initial', 'leg': 0.1}
        self.server.put_dict(dict)
        print("finished init")

    def run(self, CI):
        self.initSupervisor()
        self.initServer()
        self.rr = RobotReadings(self)
        self.motion_library = MotionLibrary()
        self.time_step = int(self.getBasicTimeStep())
        ko_labels = ['', '']
        coverage_labels = ['', '']
        # Performance output used by automated CI script
        game_duration = 3 * 60 * 1000  # a game lasts 3 minutes
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        time_step = int(self.getBasicTimeStep())
        print(time_step)
        time = 0
        seconds = -1
        ko = -1
        
        while self.step(self.time_step) != -1:  # mandatory function to make the simulation run
            if time > 22000:
                self.motion_library.play('Backwards')
            else:
                self.motion_library.play('Forwards')
                
            legs = self.rr.readLegs()
            print(legs)            
            rec = self.server.get_dict()
            print(rec)
            if rec['msg'] == 'close':
                self.server.finish()
                break

            ko = self.evaluation(time, seconds, ko_labels, coverage_labels, ko)            


            if self.step(time_step) == -1 or time > game_duration or ko != -1:
                done = {'msg':'done'}
                self.server.put_dict(done)
                break
            
            self.server.put_dict(legs)

            time += time_step
            
            
        self.server.close()

        if ko == 0:
            print('Red is KO. Blue wins!')
            performance = 0
        elif ko == 1:
            print('Blue is KO. Red wins!')
            performance = 1
        # in case of coverage equality, blue wins
        elif self.coverage[0] > self.coverage[1]:
            print('Red wins coverage: %s > %s' % (self.coverage[0], self.coverage[1]))
            performance = 1
        else:
            print('Blue wins coverage: %s >= %s' % (self.coverage[1], self.coverage[0]))
            performance = 0

    def evaluation(self, time, seconds, ko_labels, coverage_labels, ko):
        if time % 200 == 0:
            s = int(time / 1000) % 60
            if seconds != s:
                seconds = s
                minutes = int(time / 60000)
                print(f'{time} {minutes:02}:{seconds:02}')
            box = [0] * 3
            for i in range(2):
                position = self.robot[i].getPosition()
                color = 0xff0000 if i == 0 else 0x0000ff
                if abs(position[0]) < 1 and abs(position[1]) < 1:  # inside the ring
                    coverage = 0
                    for j in range(2):
                        if position[j] < self.min[i][j]:
                            self.min[i][j] = position[j]
                        elif position[j] > self.max[i][j]:
                            self.max[i][j] = position[j]
                        box[j] = self.max[i][j] - self.min[i][j]
                        coverage += box[j] * box[j]
                    coverage = math.sqrt(coverage)
                    self.coverage[i] = coverage
                    string = '{:.3f}'.format(coverage)
                    if string != coverage_labels[i]:
                        print(f'coverage for robot {i}: {string}')
                    coverage_labels[i] = string
                if position[2] < 0.9:  # low position threshold
                    self.ko_count[i] = self.ko_count[i] + 200
                    if self.ko_count[i] > 10000:  # 10 seconds
                        ko = i
                else:
                    self.ko_count[i] = 0
                counter = 10 - self.ko_count[i] // 1000
                string = '' if self.ko_count[i] == 0 else str(counter) if counter > 0 else 'KO'
                if string != ko_labels[i] and string:
                    print(f'robot {i}: {string}')
                ko_labels[i] = string

        return ko




class WrestlerSupervisor(Supervisor):
    def initSupervisor(self):
        self.robot = [0] * 2
        self.robot[1] = self.getFromDef('WRESTLER_BLUE').getFromProtoDef('HEAD_SLOT')
        self.robot[0] = self.getFromDef('WRESTLER_RED').getFromProtoDef('HEAD_SLOT')
        self.min = [[0] * 3 for i in range(2)]
        self.max = [[0] * 3 for i in range(2)]
        for i in range(2):
            self.min[i] = self.robot[i].getPosition()
            self.max[i] = self.robot[i].getPosition()
        self.coverage = [0] * 2
        self.ko_count = [0] * 2

    def run(self, CI):
        self.initSupervisor()
        self.motion_library = MotionLibrary()
        self.time_step = int(self.getBasicTimeStep())
        ko_labels = ['', '']
        coverage_labels = ['', '']
        # Performance output used by automated CI script
        game_duration = 5000 # 3 * 60 * 1000  # a game lasts 3 minutes
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        time_step = int(self.getBasicTimeStep())
        #print(time_step)
        time = 0
        seconds = -1
        ko = -1
        
        while True: # self.step(self.time_step) != -1:  # mandatory function to make the simulation run
            if time > 22000:
                self.motion_library.play('Backwards')
            else:
                self.motion_library.play('Forwards')
                
            ko = self.evaluation(time, seconds, ko_labels, coverage_labels, ko)            

            if self.step(time_step) == -1 or time > game_duration or ko != -1:
                break
            time += time_step
        if ko == 0:
            print('Red is KO. Blue wins!')
            performance = 0
        elif ko == 1:
            print('Blue is KO. Red wins!')
            performance = 1
        # in case of coverage equality, blue wins
        elif self.coverage[0] > self.coverage[1]:
            print('Red wins coverage: %s > %s' % (self.coverage[0], self.coverage[1]))
            performance = 1
        else:
            print('Blue wins coverage: %s >= %s' % (self.coverage[1], self.coverage[0]))
            performance = 0

    def evaluation(self, time, seconds, ko_labels, coverage_labels, ko):
        if time % 200 == 0:
            s = int(time / 1000) % 60
            if seconds != s:
                seconds = s
                minutes = int(time / 60000)
                #print(f'{time} {minutes:02}:{seconds:02}')
            box = [0] * 3
            for i in range(2):
                position = self.robot[i].getPosition()
                color = 0xff0000 if i == 0 else 0x0000ff
                if abs(position[0]) < 1 and abs(position[1]) < 1:  # inside the ring
                    coverage = 0
                    for j in range(2):
                        if position[j] < self.min[i][j]:
                            self.min[i][j] = position[j]
                        elif position[j] > self.max[i][j]:
                            self.max[i][j] = position[j]
                        box[j] = self.max[i][j] - self.min[i][j]
                        coverage += box[j] * box[j]
                    coverage = math.sqrt(coverage)
                    self.coverage[i] = coverage
                    string = '{:.3f}'.format(coverage)
                    # if string != coverage_labels[i]:
                    #     print(f'coverage for robot {i}: {string}')
                    coverage_labels[i] = string
                if position[2] < 0.9:  # low position threshold
                    self.ko_count[i] = self.ko_count[i] + 200
                    if self.ko_count[i] > 10000:  # 10 seconds
                        ko = i
                else:
                    self.ko_count[i] = 0
                counter = 10 - self.ko_count[i] // 1000
                string = '' if self.ko_count[i] == 0 else str(counter) if counter > 0 else 'KO'
                if string != ko_labels[i] and string:
                    print(f'robot {i}: {string}')
                ko_labels[i] = string

        return ko


class Wrestler (Robot):
    
    def __init__(self):
        Robot.__init__(self)
        self.rr = RobotReadings(self)
        # to load all the motions from the motions folder, we use the MotionLibrary class:
        self.motion_library = MotionLibrary()
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        self.time_step = int(self.getBasicTimeStep())
        print(f'time_step={self.time_step}')
        self.coverage = 0
        
        self.server = Server()
        rec = self.server.get_dict()
        print(rec)
        dict = {'msg': 'initial', 'leg': 0.1}
        self.server.put_dict(dict)
        print("finished init")


    
    def set_coverage(self, coverage):
        self.coverage = coverage

    def get_coverage(self):
        return self.coverage 

    def run(self):
        while self.step(self.time_step) != -1:  # mandatory function to make the simulation run
            #print("b4")
            self.motion_library.play('Forwards')
            legs = self.rr.readLegs()
            print(legs)            
            rec = self.server.get_dict()
            print(rec)
            if rec['msg'] == 'close':
                self.server.finish()
                break
            self.server.put_dict(legs)
            
        self.server.close()


test = 1

if test == 1:
    # create the referee instance and run main loop
    CI = os.environ.get("CI")
    
    wrestler = WrestlerSupervisor()    
    tic = time.perf_counter()
    wrestler.run(CI)
    toc = time.perf_counter()
    elapsed = toc-tic
    print(f'Elapsed time: {elapsed:4.4f}')
    
    # if CI:
    wrestler.simulationSetMode(wrestler.SIMULATION_MODE_PAUSE)
    #wrestler.worldReload()
    wrestler.simulationReset()
    
    print("reset")
    # wrestler.simulationSetMode(wrestler.SIMULATION_MODE_FAST)
    
    wrestler.simulationSetMode(wrestler.WB_SUPERVISOR_SIMULATION_MODE_FAST)

    #wrestler = WrestlerSupervisor()    
    wrestler.run(CI)
    toc = time.perf_counter()
    elapsed = toc-tic
    print(f'Elapsed time: {elapsed:4.4f}')


if test == 2:
    wrestler = Wrestler()
    wrestler.run()
    
    
if test == 3:
    # create the referee instance and run main loop
    CI = os.environ.get("CI")
    wrestler = WrestlerSupervisorServer()
    wrestler.run(CI)
    if CI:
        wrestler.simulationSetMode(wrestler.SIMULATION_MODE_PAUSE)
