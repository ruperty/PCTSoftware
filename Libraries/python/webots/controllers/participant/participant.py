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
from os import sep, environ, getpid, getenv
from time import sleep
import math, time, logging
from controller import Robot
import sys
import platform
import argparse

# We provide a set of utilities to help you with the development of your controller. You can find them in the utils folder.
# If you want to see a list of examples that use them, you can go to https://github.com/cyberbotics/wrestling#demo-robot-controllers
sys.path.append('..')
from utils.motion_library import MotionLibrary
from utils.fall_detection import FallDetection
# from utils.gait_manager import GaitManager
# from utils.camera import Camera

from utilities.robot import RobotAccess, ROBOTMODE
from pct.network import Server, ServerConnectionManager
from controller import Supervisor
from pct.putils import SingletonObjects
from utilities.processes import Executor

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
                raise Exception('Mode not received in initialisation.')
            
            if 'game_duration' in recv:
                self.game_duration =  recv['game_duration']
            else:                
                raise Exception('Game duration not received in initialisation.')

            self.upper_body='shoulders'
            if 'upper_body' in recv:
                self.upper_body =  recv['upper_body']
            # else:                
            #     raise Exception('Upper body not received in initialisation.')

            if 'sync' in recv:
                sync =  recv['sync']
                if sync == 'true':
                    sync = True
                if sync == 'false':
                    sync = False

                if sync != self.synchronization:
                    print(f'Sync {sync} is not the same as world file {self.synchronization}.')
                    raise Exception(f'Sync {sync} is not the same as world file {self.synchronization}.')
            else:                
                raise Exception('Sync not received in initialisation.')
        else:
            raise Exception('Initialisation not recevied from client.')

        return rmode
    
    def initMotors(self, rmode, samplingperiod):
        self.rr = RobotAccess(self, rmode, samplingperiod)
        if self.upper_body == 'guardup':
            self.rr.setGuardup()
        else:
            self.rr.setShoulders()
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

        self.rr.set( self.actions)


    # def close(self):
    #     self.server.close()
        
    def run(self, port=None, extern=False):
        self.time_step = int(self.getBasicTimeStep())
        self.step(self.time_step)
        self.initSupervisor()
        self.motion_library = MotionLibrary(extern=extern)
        #self.motion_library.play('Forwards')
        ko_labels = ['', '']
        coverage_labels = ['', '']

        # print(time_step)
        ttime,loops=0,0
        seconds = -1
        ko = -1
        rmode = self.initServer()
        self.initMotors(rmode=rmode, samplingperiod=self.time_step)
        tic = time.perf_counter()
        while  self.step(self.time_step) != -1: 
            # pan = self.rr.get_normalized_opponent_x()
            # print(pan)

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

            if ttime > self.game_duration or ko != -1 or self.robot_down[0] :# or self.outside_ring:
                self.done = 1
                self.send_sensors(performance)
                break
            
            # send sensor data
            self.send_sensors(performance)

            ttime += self.time_step            
            loops+=1

        toc = time.perf_counter()
        elapsed = 1000 * (toc-tic)
        loop_time = elapsed/loops
        if ttime >= self.game_duration:
            logger.info(f'Time={ttime} Performance={performance} Elapsed time={elapsed:4.0f} loops={loops} loop_time={loop_time}')   
                        
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
        
        # logger.info(f'Final performance: {performance}')    

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
                        #print(f'outside_ring')
                        # print(f'outside_ring')

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
            #print(f'robot_down')
            # print(f'robot_down')
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
        # print(self.coverage)
        # print(self.min)
        # print(self.max)
        self.ko_count = [0] * 2
        self.robot_down= [0] * 2
        self.outside_ring = False 


    def initialise(self, properties):    
        self.simulationReset()
        self.time_step = int(self.getBasicTimeStep())
        upper_body=properties['upper_body']
        self.initMotors(mode=properties['rmode'], samplingperiod=self.time_step, upper_body=upper_body)
        self.initSupervisor()

        self.ko_labels = ['', '']
        self.coverage_labels = ['', '']
        self.game_duration = properties['game_duration']
        self.ttime,self.loops,self.seconds,self.ko,self.done= 0, 0, -1, -1, False
        self.observations={}

    def initMotors(self, mode=None, samplingperiod=None, config_num=None, upper_body=None):
        self.rr = RobotAccess(self, mode=mode, samplingPeriod=samplingperiod, config_num=config_num, upper_body=upper_body)


    def rstep(self, actions):
        self.rr.apply_actions(actions)
        self.ko, self.performance = self.evaluation(self.ttime, self.ko)            
        sensors = self.rr.read()

        if self.step(self.time_step) == -1 or self.ttime > self.game_duration or self.ko != -1 or self.robot_down[0]:
            self.done = True

        self.ttime += self.time_step            
        self.loops+=1
        
        self.observations['performance']=self.performance
        self.observations['done']=self.done
        self.observations['sensors']=sensors
        return self.observations      


    def evaluation(self, time, ko):
        if time % 200 == 0:
            s = int(time / 1000) % 60
            if self.seconds != s:
                self.seconds = s
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

                    # if i == 0:
                    #     print('coverage=', coverage)

                    string = '{:.3f}'.format(coverage)
                    # if string != coverage_labels[i]:
                    #     print(f'coverage for robot {i}: {string}')
                    self.coverage_labels[i] = string
                else:
                    if i==0:
                        self.outside_ring = True
                        #print(f'outside_ring')
                        # print(f'outside_ring')

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
                self.ko_labels[i] = string

        if self.robot_down[0]:
            #print(f'robot_down')
            # print(f'robot_down')
            performance = self.coverage[0]/10
            if self.outside_ring:
                performance = -performance 
        else:
            performance = self.coverage[0]
            
        if ko == 0:
            # print('Red is KO. Blue wins!')
            performance = 0
        elif ko == 1:
            # print('Blue is KO. Red wins!')
            performance = 10
                             
        return ko, performance


        
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

class PCTWrestler (Robot):
    
    def __init__(self, config_num=None, time_step=None, game_duration = 180000):
        logger.info('Initialising PCTWrestler')
        Robot.__init__(self)
        ftime_step = int(self.getBasicTimeStep())
        if time_step==None:
            self.time_step=ftime_step
        else:
            self.time_step=time_step 

        print(f'File time step={ftime_step}, used time step={self.time_step}')
        self.rmode=1
        self.hpcthelper = HPCTHelper(config_num=config_num, mode=self.rmode)
        self.fall_detector = FallDetection(self.time_step, self)
        self.game_duration = game_duration

    
    def run(self, max_loops=None):
        self.motion_library = MotionLibrary()
        ttime=0
        loops=0
        hpct_verbose=False
        mode = ROBOTMODE.GENERAL
        self.initMotors(mode=self.rmode, samplingperiod=self.time_step, config_num=self.hpcthelper.get_config_num())
        sensors = self.rr.read()    
        self.hpcthelper.set_obs(sensors)
        tic = time.perf_counter()
        centretime=7500
        while self.step(self.time_step) != -1 :  # mandatory function to make the simulation run
            if mode != ROBOTMODE.PUNCH:
                mode = self.check_fallen(mode=mode)            

            # if ttime<centretime:
            mode = self.resetting(mode=mode)
            # else:
            #     mode = self.resetting_upper_body(mode=mode)

            self.rr.update_head_controller()
            # if ttime>=6000:
            mode = self.rr.update_body_controller(self.motion_library, mode=mode)  
            
            mode = self.rr.distance_control(mode)
            mode = self.rr.punch_position(mode)

            # if ttime>=centretime and mode == ROBOTMODE.GENERAL:
            #     mode = ROBOTMODE.TURNLEFT60

            # mode = self.rr.run_behaviour(self.motion_library, mode=mode)  

            if mode == ROBOTMODE.GENERAL:
                self.actions = self.hpcthelper.get_actions()
                self.rr.apply_actions(self.actions)
                out = self.hpcthelper.step(verbose=hpct_verbose)
                sensors = self.rr.read()    
                self.hpcthelper.set_obs(sensors)

            ttime += self.time_step
            if loops==max_loops:
                break
            if ttime > self.game_duration:
                break
            loops+=1
        
        toc = time.perf_counter()
        elapsed = 1000 * (toc-tic)
        loop_time = elapsed/loops
        print(f'Time={ttime} Elapsed time: {elapsed:4.0f} loops={loops} loop_time={loop_time}')   
        
    def check_fallen(self, mode):
        
        # print('check_fallen',mode)
        if self.fall_detector.detect_fall():
            mode = ROBOTMODE.FALLEN
            logger.info('Fallen')
            self.fall_detector.check()    
            logger.info('Back up')
        
        if mode == ROBOTMODE.FALLEN:
            mode = ROBOTMODE.RESET
        return mode
    
    def resetting(self, mode):
        if mode == ROBOTMODE.RESET:
            logger.info('resetting hierarchy')
            self.hpcthelper.reset_hierarchy()
            self.hpcthelper.reset_reference_values()
            self.rr.reset_upper_body(self.hpcthelper.get_config_num())
            # self.motion_library.play("TurnLeft60")
            # self.motion_library.play("Stand")
            self.rr.reset_lower_body(self)
            mode = ROBOTMODE.GENERAL
            
            print('resetting',mode)
            
        return mode

    def resetting_upper_body(self, mode):
        if mode == ROBOTMODE.RESET:
            logger.info('resetting upper_body')
            self.rr.reset_upper_body(self.hpcthelper.get_config_num())
            mode = ROBOTMODE.GENERAL            
        return mode


    def initMotors(self, mode=None, samplingperiod=None, config_num=None):
        self.rr = RobotAccess(self, mode, samplingperiod, config_num=config_num)


    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help="controller port number")
    parser.add_argument('-wp', '--wport', type=int, help="webots port number")
    parser.add_argument('-t', '--test', type=int, help="test scenario")
    parser.add_argument('-s', '--sync', help="webots port number", action="store_true")
    parser.add_argument('-l', '--log', help="logging", action="store_true")
    parser.add_argument('-e', '--extern', help="extern", action="store_true")

    args = parser.parse_args()
    port = args.port 
    wport = args.wport
    test = args.test
    sync = args.sync
    log = args.log
    extern = args.extern

    # if port==None:
    #     port = 6666
    # if wport==None:
    #     wport = 1234
    # if test is None:
    #     test = 7
    log=True

    test = eval(getenv('WW_TEST'))
    print('test is ',test)
    if test is None:
        test = 7
    print('test is ',test)


    # print(f'Sync={sync} test={test} port={port} wport={wport}')

    if test == 3:
        if log:
            out_dir= f'c:{sep}tmp'
            now = datetime.now() # current date and time
            # date_time = now.strftime("%Y%m%d-%H%M%S")
            # log_file=sep.join((out_dir, "participant-"+date_time+".log"))
            log_file=sep.join((out_dir, "participant.log"))
            print('log_file=',log_file)
            logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )

    if test == 5 :
        if log:
            out_dir= get_gdrive() + f'data{sep}ga'
            if test == 5:
                env_name = 'WebotsWrestler'
            if test == 6:
                env_name = "WebotsWrestlerSupervisor"

            now = datetime.now() # current date and time
            date_time = now.strftime("%Y%m%d-%H%M%S")
            log_file=sep.join((out_dir, env_name, "ww-evolve-server-"+platform.node()+"-"+date_time+".log"))
            print('log_file=',log_file)
            logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )


    if test == 1:
        # create the referee instance and run main loop
        CI = environ.get("CI")
        wrestler = WrestlerSupervisor()    
        self.time_step=None
        max_loops=10
        
        wrestler.simulationReset()
        #wrestler.simulationSetMode(wrestler.SIMULATION_MODE_FAST)
        tic = time.perf_counter()
        wrestler.run(CI, time_step=self.time_step, max_loops=max_loops)
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
        # 4 - ok with guard position, slow 
        # 9 - ok with guard position, not very stable but does standup again
        # 10 - right leg behind, good with reversing 5 secs, not good with guard position 
        # 12 - not good with guard position, falls over after reset, why???
        # 17 - doesn't do anything
        # 18 - fast but a bit unstable, keeps falling over,  2 ref
        # 20 - wobbles alot and falls over, 2 ref 
        # 25 - doesn't do much
        # 26 - good, but falls over after 2 secs, debug?
        # 27 - fast shuffling, though unstable
        # 28 - dud falls over
        # 29 - dud falls over
        # 30 - dud falls over
        # 31 - fairly fast, but unstable
        wrestler = PCTWrestler(config_num=33,  game_duration=180000)    
        tic = time.perf_counter()
        # wrestler.run(time_step=20, max_loops=1000)    
        
        wrestler.run()    
        toc = time.perf_counter()
        elapsed = toc-tic
        print(f'Elapsed time: {elapsed:4.4f}')   
    
    if test == 4:
        # create the referee instance and run main loop
      
        # ram_limit= 500 * 1000 * 1000 # 20 * 1000 * 1000 * 1000
        ram_limit= 10 * 1000 * 1000 * 1000
        ex = Executor(port=port, wport=wport, sync=sync)
            
        ServerConnectionManager.getInstance().set_port(port=port)
        ex.start_evolver()
        ctr=1
    
        while True:
            try:
                ex.start_webots()
            except Exception as e:
                print(e.message)
                logger.info(e.message)
                break

            logger.info(ex.get_process_info_by_name('python.exe', 'evolve', '9999'))
            logger.info(ex.get_process_info_by_pid(getpid()))
            logger.info(ex.get_process_info_webots())

            wrestler = WrestlerSupervisorServer()
            logger.info(f'Basic time step={wrestler.getBasicTimeStep()}')
            logger.info(f'Memory={ex.webots_ram()}')
            
            while True:
                wrestler.simulationReset()
                wrestler.run(port=port)
                if ctr % 10:
                    logger.info(ex.get_process_info_by_name('python.exe', 'evolve.py', '9999'))
                    logger.info(ex.get_process_info_by_pid(getpid()))
                    logger.info(ex.get_process_info_webots())
                    ram = ex.webots_ram()
                    if ram > ram_limit :
                        logger.info(f'Ctr={ctr}')             
                        logger.info(f'Ram={ram} exceeds limit {ram_limit}, restarting webots')
                        status = 1 #EXIT_SUCCESS
                        wrestler.simulationQuit(status) 
                        del wrestler
                        break
                ctr+=1
                
    if test == 5:
        # create the referee instance and run main loop
            
        ServerConnectionManager.getInstance().set_port(port=port)            
        ctr=1
        ex = Executor(port=port, wport=wport, sync=sync)
        # extern = not notextern
        wrestler = WrestlerSupervisorServer()
        print(f'Basic time step={wrestler.getBasicTimeStep()}')
        print(f'Memory={ex.webots_ram()}')

        while True:
            wrestler.simulationReset()
            wrestler.run(port=port, extern=extern)
            if ctr % 100 == 0:
                estr=ex.get_process_info_by_name('python.exe', 'evolve.py', f'{port}')
                pstr=ex.get_process_info_by_pid(getpid())
                wstr=ex.get_process_info_webots()
                now = datetime.now()
                date_time = now.strftime("%Y%m%d-%H%M%S")
                memory = '\n'.join((f'Memory: {ctr} PID: {ex.pid} Time: {date_time}', estr, pstr, wstr))
                logger.info(memory)
                print(memory)
                # print(ex.get_process_info_by_name('python.exe', 'evolve.py', f'{port}'))
                # print(ex.get_process_info_by_pid(getpid()))
                # print(ex.get_process_info_webots())
            ctr+=1


    if test == 6:
        from deap import base, creator
        from eepct.hpct import HPCTIndividual
        from epct.evolvers import CommonToolbox
        from cutils.paths import get_root_path, get_gdrive
        from eepct.hpct import HPCTEvolveProperties
        from os import sep, makedirs


        wrestler = WrestlerSupervisor()
        SingletonObjects.getInstance().add_object('wrestler', wrestler)

        env_name = "WebotsWrestlerSupervisor"
        # fname=10
        # if fname ==1 :
        #     filename = "WW01-01-RewardError-CurrentError-Mode01"
        # if fname ==2 :
        #     filename = "WW01-02-RewardError-CurrentError-Mode01"
        # if fname ==3 :
        #     filename = "WW01-03-RewardError-CurrentError-Mode01"
        # if fname ==4 :
        #     filename = "WW01-04-RewardError-CurrentError-Mode01"
        # if fname ==5 :
        #     filename = "WW01-05-RewardError-CurrentError-Mode01"
        # if fname ==6 :
        #     filename = "WW01-06-RewardError-CurrentError-Mode01"
        # if fname ==7 :
        #     filename = "WW01-07-RewardError-CurrentError-Mode02"
        # if fname ==8 :
        #     filename = "WW01-08-RewardError-CurrentError-Mode02"
        # if fname ==9 :
        #     filename = "WW01-09-RewardError-CurrentError-Mode03"
        # if fname ==10 :
        #     filename = "WW01-10-RewardError-CurrentError-Mode03"
        # if fname ==11 :
        #     filename = "WW01-11-RewardError-CurrentError-Mode04"
        # if fname ==12 :
        #     filename = "WW01-12-RewardError-CurrentError-Mode04"

        filename = getenv('WW_CONFIG')
        print(filename, filename)
        out_dir= get_gdrive() + f'data{sep}ga{sep}'

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMax)

        min=False

        toolbox = base.Toolbox()
        CommonToolbox.getInstance().set_toolbox(toolbox)

        node_size, font_size=150, 10

        root = get_root_path()

        file = root + 'Versioning/PCTSoftware/Libraries/python/pctlocal/tests\\ga/pctobject/configs/' + env_name +'/'+ filename + ".properties"

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

        hash_num, desc, properties_str = hep.configure_evolver_from_properties_file(file=file, print_properties=True, verbose=verbose, toolbox=toolbox,  min=min)

        # logging info
        now = datetime.now() # current date and time
        date_time = now.strftime("%Y%m%d-%H%M%S")
        log_dir=sep.join((out_dir, env_name, desc, hash_num, "output"))
        makedirs(log_dir,exist_ok = True) 
        log_file=sep.join((log_dir, "evolve-client-"+platform.node()+"-"+date_time+".log"))
        logging.basicConfig(filename=log_file, level=logging.INFO,    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s.%(lineno)d %(message)s",datefmt= '%H:%M:%S'    )
        logger = logging.getLogger(__name__)
        logger.info("Evolving {} ".format(env_name))
        logger.info(properties_str)


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

        status = 1 #EXIT_SUCCESS
        wrestler.simulationQuit(status) 


    if test == 7:
        from eepct.hpct import HPCTIndividual
        
        wrestler = WrestlerSupervisor()
        SingletonObjects.getInstance().add_object('wrestler', wrestler)


        root = get_gdrive()
        env_props={'game_duration':10000, 'rmode' : 1, 'sync': 'false', 'upper_body':'guardup'}

        files = ['WebotsWrestlerSupervisor\\WW01-06-RewardError-CurrentError-Mode01\\ga-001.276-s001-3x4-m001-21db068466666c5352cceef7c8c496d9.properties',
                    'WebotsWrestlerSupervisor\\WW01-07-RewardError-CurrentError-Mode02\\ga-001.903-s001-5x8-m002-108925b64cd5a2b96bde2bfc108fd4f8.properties',
                    'WebotsWrestlerSupervisor\\WW01-08-RewardError-CurrentError-Mode02\\ga-001.443-s001-4x10-m002-8dcd95a5aea2589f13c7f6bc603ca2e0.properties',
                    'WebotsWrestlerSupervisor\\WW01-09-RewardError-CurrentError-Mode03\\ga-000.111-s001-9x9-m003-f37757991a462f567c03e613acc09c2e.properties',
                    'WebotsWrestlerSupervisor\\WW01-10-RewardError-CurrentError-Mode03\\ga-001.732-s001-3x8-m003-d6d662f2b5a398c83d82cf82adf7a44c.properties',
                    'WebotsWrestlerSupervisor\\WW01-11-RewardError-CurrentError-Mode04\\ga-000.753-s001-2x2-m004-32a6774decb5c3f7cc89a67a47530398.properties',
                    'WebotsWrestlerSupervisor\\WW01-12-RewardError-CurrentError-Mode04\\ga-000.818-s001-3x7-m004-344d674e5423a22c0aa0c12f91d74a84.properties']

        files = [
            # 'WebotsWrestlerSupervisor\\WW01-06-RewardError-CurrentError-Mode01\\ga-000.064-s001-3x6-m001-1c4088fe6bdd2464080de0c4261d43f5.properties',
            # 'WebotsWrestlerSupervisor\\WW01-01-RewardError-CurrentError-Mode01\\ga-000.152-s001-8x10-m001-4a71894fbdf43463f02f3e84bc0d7e94.properties',

            'WebotsWrestlerSupervisor\\WW01-07-RewardError-CurrentError-Mode02\\ga-001.776-s001-3x5-m002-27f4085024c2f7879344ae55bb28904c.properties',
            'WebotsWrestlerSupervisor\\WW01-02-RewardError-CurrentError-Mode01\\ga-001.536-s001-5x6-m001-612442651880a50388df8860cfa72209.properties',
            'WebotsWrestlerSupervisor\\WW01-08-RewardError-CurrentError-Mode02\\ga-002.230-s001-2x6-m002-baff0450b076d566ae3d620dacbc31eb.properties',
            'WebotsWrestlerSupervisor\\WW01-09-RewardError-CurrentError-Mode03\\ga-002.481-s001-2x2-m003-9a64fd541da0b63ef26d6c9fa9f7fdfd.properties',

            # 'WebotsWrestlerSupervisor\\WW01-03-RewardError-CurrentError-Mode01\\ga-001.915-s001-2x2-m001-028fd92550db5c336676a9bd34189279.properties'
            # 'WebotsWrestlerSupervisor\\WW01-10-RewardError-CurrentError-Mode03\\ga-001.085-s001-4x10-m003-19b2d6dad801b22bc5d20f04d13efd07.properties'            
            # 'WebotsWrestlerSupervisor\\WW01-11-RewardError-CurrentError-Mode04\ga-001.923-s001-4x3-m004-bed1bb89b056f966c528b4c8296df4c5.properties'
            
            # 'WebotsWrestlerSupervisor\\WW01-04-RewardError-CurrentError-Mode01\ga-001.915-s001-2x2-m001-79925912a1d3e3e09e8d6efeeb67eba1.properties'
            
            ]

        for file in files:
            print(file)
            score = HPCTIndividual.run_from_file(root, file, env_props, hpct_verbose= False)
            print("Score: %0.3f" % score)


            
            
        # status = 1 #EXIT_SUCCESS
        # wrestler.simulationQuit(status) 

    
    