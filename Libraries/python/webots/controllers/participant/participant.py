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



import numpy as np
from os import sep
from time import sleep
import math, time
from controller import Robot
import sys
import platform
import argparse

# We provide a set of utilities to help you with the development of your controller. You can find them in the utils folder.
# If you want to see a list of examples that use them, you can go to https://github.com/cyberbotics/wrestling#demo-robot-controllers
sys.path.append('..')
from utils.motion_library import MotionLibrary

from utils.image_processing import ImageProcessing as IP
from utils.fall_detection import FallDetection
# from utils.gait_manager import GaitManager
# from utils.camera import Camera

from utilities.robot import RobotAccess
from pct.network import Server
from controller import Supervisor
from pct.network import ServerConnectionManager

from datetime import datetime


def get_gdrive():
    import socket
    import os
    if socket.gethostname() == 'DESKTOP-5O07H5P':
        root_dir='/mnt/c/Users/ruper/My Drive/'
        if os.name == 'nt' :
            root_dir='C:\\Users\\ruper\\My Drive\\'
    elif socket.gethostname() == 'UKM5570RYOUNG2':
        if os.name == 'nt' :
            root_dir='G:\\My Drive\\'
    else:
        root_dir='/mnt/c/Users/ryoung/My Drive/'        
        if os.name == 'nt' :
            root_dir='C:\\Users\\ryoung\\Google Drive\\'
    return root_dir

test = 3

out_dir= get_gdrive() + f'data{sep}ga'
env_name = 'WebotsWrestler'

import logging
now = datetime.now() # current date and time
date_time = now.strftime("%Y%m%d-%H%M%S")
log_file=sep.join((out_dir, env_name, "ww-evolve-server-"+platform.node()+"-"+date_time+".log"))
print('log_file=',log_file)
logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )
logger = logging.getLogger(__name__)

class WrestlerSupervisorServer(Supervisor):
    def initSupervisor(self):
        #print('******************************************')
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
        self.robot_down= [0] * 2
        self.outside_ring = False 
        #self.robot_backwards = False


    def initServer(self):     
        self.done = False   
        # self.server = Server(port=port)
        recv = self.receive()
        if 'msg' in recv and recv['msg']=='init':
            # print(f'Initialisation recevied from client. {recv}')
            #logger.info(f'Initialisation recevied from client. {recv}')
            if 'rmode' in recv:
                rmode =  recv['rmode']
            else:                
                # self.close()    
                raise Exception('Mode not received in initialisation.')
            
            if 'game_duration' in recv:
                self.game_duration =  recv['game_duration']
            else:                
                # self.close()    
                raise Exception('Game duration not received in initialisation.')

            if 'sync' in recv:
                sync =  recv['sync']
                if sync == 'true':
                    sync = True
                if sync == 'false':
                    sync = False

                if sync != self.synchronization:
                    # self.close()    
                    raise Exception('Sync is not the same as world file.')
                    
                
            else:                
                # self.close()    
                raise Exception('Sync not received in initialisation.')
        else:
            # self.close()    
            raise Exception('Initialisation not recevied from client.')

        # self.simulationReset()
        # self.game_duration = 10000 # 60000 #3 * 60 * 1000  # a game lasts 3 minutes

        return rmode
    
    def initMotors(self, rmode, samplingperiod):
        self.rr = RobotAccess(self, rmode, samplingperiod)
        self.rr.setShoulders(2,2)
        # send sensor data
        self.initial_sensors = self.send_sensors(performance=0)

    def send(self, data):
        ServerConnectionManager.getInstance().send(data)
        # self.server.put_dict(data)

    def receive(self):
        recv = ServerConnectionManager.getInstance().receive()
        # recv = self.server.get_dict()
        #print(recv)
        return recv
        
    def send_sensors(self, performance):        
        sensors = self.rr.read()
        if self.done:
            msg = {'msg':'done', 'performance':round(performance, 3), 'sensors': sensors}
        else:
            msg = {'msg':'values', 'performance':round(performance, 3), 'sensors': sensors}
            
        self.send(msg)
        
        return sensors

    def get_actions(self):
        recv = self.receive()
        self.actions = recv['actions']
        if recv['msg'] == 'close':
            self.server.finish()
            return False
        return True
        
    def apply_actions(self):
        #actions= {'LHipPitch': 0, 'LKneePitch': 0, 'LAnklePitch': 0, 'RHipPitch': 0, 'RKneePitch': 0, 'RAnklePitch': 0}
        #self.rr.set( self.initial_sensors,actions)
        #print('actions',self.actions)
        #logging.info(f'actions {self.actions}')

        self.rr.set( self.initial_sensors,self.actions)


    # def close(self):
    #     self.server.close()
        
    def run(self, port=None):
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        time_step = int(self.getBasicTimeStep())
        self.step(time_step)
        self.initSupervisor()
        self.motion_library = MotionLibrary()
        #self.motion_library.play('Forwards')
        ko_labels = ['', '']
        coverage_labels = ['', '']

        # print(time_step)
        ttime,loops=0,0
        seconds = -1
        ko = -1
        rmode = self.initServer()
        self.initMotors(rmode=rmode, samplingperiod=time_step)
        tic = time.perf_counter()
        while  self.step(time_step) != -1: 
            # if time > 22000:
            #     self.motion_library.play('Backwards')
            # else:
            #     self.motion_library.play('Forwards')
                
            # receive action data from client
            if not self.get_actions():
                break

            # apply action data
            self.apply_actions()
            ko, performance = self.evaluation(ttime, seconds, ko_labels, coverage_labels, ko)            

            if ttime > self.game_duration or ko != -1 or self.robot_down[0]:
                self.done = 1
                self.send_sensors(performance)
                break
            
            # send sensor data
            self.send_sensors(performance)

            ttime += time_step            
            loops+=1

        toc = time.perf_counter()
        elapsed = 1000 * (toc-tic)
        loop_time = elapsed/loops
        logger.info(f'Time={ttime} Elapsed time: {elapsed:4.0f} loops={loops} loop_time={loop_time}')   
                        
        # self.close()

        if ko == 0:
            # print('Red is KO. Blue wins!')
            performance = 0
        elif ko == 1:
            # print('Blue is KO. Red wins!')
            performance = 10
        # in case of coverage equality, blue wins
        
        # elif self.coverage[0] > self.coverage[1]:
        #     print('Red wins coverage: %s > %s' % (self.coverage[0], self.coverage[1]))
        #     #performance = 1
        # else:
        #     print('Blue wins coverage: %s >= %s' % (self.coverage[1], self.coverage[0]))
        #     #performance = 0
        logger.info(f'Final performance: {performance}')    
        #del self.motion_library
        #del self.motion_library
        #in my own timedel self.motion_library

    def evaluation(self, time, seconds, ko_labels, coverage_labels, ko):
        if time % 200 == 0:
            s = int(time / 1000) % 60
            if seconds != s:
                seconds = s
                minutes = int(time / 60000)
                # print(f'{time} {minutes:02}:{seconds:02}')
            box = [0] * 3
            for i in range(2):
                position = self.robot[i].getPosition()
                #color = 0xff0000 if i == 0 else 0x0000ff
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
                else:
                    if i==0:
                        self.outside_ring = True

                if position[2] < 0.9 or self.outside_ring:  # low position threshold
                    #print(i, position)
                    self.robot_down[i] = True
                    # if position[0] < -0.1:
                    #     self.robot_backwards = True
                    self.ko_count[i] = self.ko_count[i] + 200
                    if self.ko_count[i] > 10000:  # 10 seconds
                        ko = i
                else:
                    self.ko_count[i] = 0
                counter = 10 - self.ko_count[i] // 1000
                string = '' if self.ko_count[i] == 0 else str(counter) if counter > 0 else 'KO'
                # if string != ko_labels[i] and string:
                #     print(f'robot {i}: {string}')
                ko_labels[i] = string

        if self.robot_down[0]:
            performance = self.coverage[0]/10
            if self.outside_ring:
                performance = -performance 
        else:
            performance = self.coverage[0]
            
        return ko, performance




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

    def run(self, CI, time_step=None, max_loops=None):
        self.rr = RobotAccess(self)
        self.initSupervisor()
        self.motion_library = MotionLibrary()
        self.time_step = int(self.getBasicTimeStep())
        ko_labels = ['', '']
        coverage_labels = ['', '']
        # Performance output used by automated CI script
        game_duration = 1000 # 5000 # 3 * 60 * 1000  # a game lasts 3 minutes
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        fileTimeStep=int(self.getBasicTimeStep())
        if time_step==None:
            time_step = fileTimeStep
        #print(time_step)
        
        if max_loops==None:
            max_loops = game_duration/time_step
        
        time = 0
        seconds = -1
        ko = -1
        loops=0
        
        while self.step(self.time_step) != -1:  # mandatory function to make the simulation run
            if time > 22000:
                self.motion_library.play('Backwards')
            else:
                self.motion_library.play('Forwards')
                
            legs = self.rr.readLegs()
            print(legs)            

            ko = self.evaluation(time, seconds, ko_labels, coverage_labels, ko)            

            # if self.step(time_step) == -1 or time > game_duration or ko != -1 or loops==max_loops:
            if ko != -1 or loops==max_loops:
                break
            time += time_step
            loops = loops+1
            
        print(f'Time={time} loops={loops} time_step={time_step} ftime_step={fileTimeStep}')
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



        
class WrestlerServer (Robot):
    
    def __init__(self):
        Robot.__init__(self)
        self.rr = RobotAccess(self)
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



 

from utilities.hpct import HPCTHelper

class Wrestler (Robot):
    
    def __init__(self, config_num=None):
        Robot.__init__(self)
        self.rr = RobotAccess(self)
        self.fileTimeStep = int(self.getBasicTimeStep())
        self.rmode=1
        self.hpcthelper = HPCTHelper(config_num=config_num, mode=self.rmode)
        self.fall_detector = FallDetection(self.fileTimeStep, self)
    
    def change_action(self, type):
        config_num = self.hpcthelper.getConfigNum()
        if type == 0:
            if config_num == 10:         
               self.hpcthelper.set_new_references()
            elif config_num == 4:         
               self.hpcthelper.set_new_references()
            elif config_num == 12:         
               self.hpcthelper.set_new_references()
        
        if type == 1:
            if config_num == 10:         
               self.hpcthelper.reset_reference_values()
            elif config_num == 4:         
               self.hpcthelper.reset_reference_values()


    def run(self, time_step=None, max_loops=None):
        # to load all the motions from the motions folder, we use the MotionLibrary class:
        motion_library = MotionLibrary()
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        self.fileTimeStep=int(self.getBasicTimeStep())
        if time_step==None:
            time_step = self.fileTimeStep
        #print(time_step)
        game_duration = 120000
        ttime=0
        loops=0
        # hpct = self.hpcthelper.get_controller()
        # environment = hpct.get_environment()
        self.initMotors(mode=self.rmode, samplingperiod=time_step)
        sensors = self.rr.read()    
        self.hpcthelper.set_obs(sensors)
        tic = time.perf_counter()
        while self.step(time_step) != -1 and ttime < game_duration:  # mandatory function to make the simulation run
            self.check_fallen()
            if ttime % 10000 == 0:
                self.change_action(1)
            elif ttime % 5000 == 0:
                self.change_action(0)

            #motion_library.play('Forwards')
            self.actions = self.hpcthelper.get_actions()
            self.apply_actions()
            out = self.hpcthelper.step()
            #sleep(.005)
            sensors = self.rr.read()    
            self.hpcthelper.set_obs(sensors)
            ttime += time_step
            if loops==max_loops:
                break
            loops+=1
        
        toc = time.perf_counter()
        elapsed = 1000 * (toc-tic)
        loop_time = elapsed/loops
        print(f'Time={ttime} Elapsed time: {elapsed:4.0f} loops={loops} loop_time={loop_time}')   
        
    def check_fallen(self):
        if self.fall_detector.detect_fall():
            self.fall_detector.check()    
            #self.hpcthelper.reset_hierarchy()
            self.hpcthelper.reset_reference_values()
            self.reset_upper_body(self.hpcthelper.getConfigNum())

    def apply_actions(self):
        self.rr.set( self.initial_sensors,self.actions)
        
    def reset_upper_body(self, config_num):         
        if config_num == 4:         
            self.rr.setGuardup(0.33, -1.5, -0.2, -0.33, 1.5, -0.2)
        elif config_num == 10:         
            self.rr.setShoulders(2,2)   
        elif config_num == 12:         
            self.rr.setShoulders(2,2)   
        else:
            self.rr.setGuardup(0.33, -1.5, -0.2, -0.33, 1.5, -0.2)

        # if self.config_num == 10:


    def initMotors(self, mode, samplingperiod):
        self.rr = RobotAccess(self, mode, samplingperiod)
        self.reset_upper_body(self.hpcthelper.getConfigNum())
        
        # send sensor data
        self.initial_sensors =  self.rr.read()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help="controller port number")
    parser.add_argument('-wp', '--wport', type=int, help="webots port number")
    parser.add_argument('-s', '--sync', help="webots port number", action="store_true")

    args = parser.parse_args()
    port = args.port 
    wport = args.wport
    sync = args.sync
    
    # print(sync)


    if test == 1:
        # create the referee instance and run main loop
        CI = os.environ.get("CI")
        wrestler = WrestlerSupervisor()    
        time_step=None
        max_loops=10
        
        wrestler.simulationReset()
        #wrestler.simulationSetMode(wrestler.SIMULATION_MODE_FAST)
        tic = time.perf_counter()
        wrestler.run(CI, time_step=time_step, max_loops=max_loops)
        toc = time.perf_counter()
        elapsed = 1000 * (toc-tic)
        print(f'Elapsed time: {elapsed:4.0f}')   
        
        # wrestler.simulationReset()        
        # wrestler.simulationSetMode(wrestler.SIMULATION_MODE_FAST)
        # tic = time.perf_counter()
        # wrestler.run(CI)
        # toc = time.perf_counter()
        # elapsed = toc-tic
        # print(f'Elapsed time: {elapsed:4.4f}')



    if test == 2:
        wrestler = WrestlerServer()
        wrestler.run()
        
    if test == 3:
        # on nosync
        # 4 - ok with guard position 
        # 9 - ok with guard position
        # 10 - right leg behind, good with reversing 5 secs, not good with guard position 
        # 12 - not good with guard position
        wrestler = Wrestler(config_num=9)    
        tic = time.perf_counter()
        # wrestler.run(time_step=20, max_loops=1000)    
        
        wrestler.run(time_step=20)    
        toc = time.perf_counter()
        elapsed = toc-tic
        print(f'Elapsed time: {elapsed:4.4f}')   
    
    if test == 4:
        # create the referee instance and run main loop
        #start_webots()
        if port==None:
            port = 6666
        if wport==None:
            wport = 1234
        if sync==None:
            sync=False

        ram_limit=20 * 1000 * 1000 * 1000
        from utilities.processes import Executor
        ex = Executor(port=port, wport=wport, sync=sync)
            
        ServerConnectionManager.getInstance().set_port(port=port)
        ex.start_evolver()
        
        while True:
            ex.start_webots()
            wrestler = WrestlerSupervisorServer()
            logger.info(f'Basic time step={wrestler.getBasicTimeStep()}')
            while True:
                wrestler.simulationReset()
                wrestler.run(port=port)
                ram = ex.webots_ram()
                if ram > ram_limit:
                    logger.info(f'Ram={ram} exceeds limit {ram_limit}, restarting webots')
                    status = 1 #EXIT_SUCCESS
                    wrestler.simulationQuit(status) 
                    del wrestler
                    break
                
                

