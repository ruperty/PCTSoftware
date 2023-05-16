
from pct.hierarchy import PCTHierarchy
from utils.camera import Camera
from utils.image_processing import ImageProcessing as IP

from enum import IntEnum, auto
import logging

logger = logging.getLogger(__name__)


class ROBOTMODE(IntEnum):
    "Modes of robot behaviour."
    FALLEN = auto()
    GENERAL = auto()
    TURNING = auto()
    RESET = auto()
    RISEN = auto()

class RobotAccess(object):
    def __init__(self, robot, mode=1, samplingPeriod=20, config_num=None):
        self.mode=mode
        
        # motors
        self.RShoulderPitchM = robot.getDevice("RShoulderPitch")
        self.LShoulderPitchM = robot.getDevice("LShoulderPitch")
        
        self.LAnklePitchM = robot.getDevice("LAnklePitch")
        self.LKneePitchM = robot.getDevice("LKneePitch")
        self.LHipPitchM = robot.getDevice("LHipPitch")

        self.RAnklePitchM = robot.getDevice("RAnklePitch")
        self.RKneePitchM = robot.getDevice("RKneePitch")
        self.RHipPitchM = robot.getDevice("RHipPitch")
        
        self.LShoulderRollM = robot.getDevice("LShoulderRoll")
        self.LElbowRollM = robot.getDevice("LElbowRoll")
        self.LElbowYawM = robot.getDevice("LElbowYaw")
        
        self.RShoulderRollM = robot.getDevice("RShoulderRoll")
        self.RElbowRollM = robot.getDevice("RElbowRoll")
        self.RElbowYawM = robot.getDevice("RElbowYaw")

        # sensors
        self.RShoulderPitchS = robot.getDevice("RShoulderPitchS")
        self.LShoulderPitchS = robot.getDevice("LShoulderPitchS")

        self.LAnklePitchS = robot.getDevice("LAnklePitchS")
        self.LKneePitchS = robot.getDevice("LKneePitchS")
        self.LHipPitchS = robot.getDevice("LHipPitchS")

        self.RAnklePitchS = robot.getDevice("RAnklePitchS")
        self.RKneePitchS = robot.getDevice("RKneePitchS")
        self.RHipPitchS = robot.getDevice("RHipPitchS")

        #print(f'samplingPeriod={samplingPeriod}')
        self.LAnklePitchS.enable(samplingPeriod)
        self.LKneePitchS.enable(samplingPeriod)
        self.LHipPitchS.enable(samplingPeriod)
        self.RAnklePitchS.enable(samplingPeriod)
        self.RKneePitchS.enable(samplingPeriod)
        self.RHipPitchS.enable(samplingPeriod)


        self.HeadYawM = robot.getDevice("HeadYaw")
        self.HeadYawS = robot.getDevice("HeadYawS")
        self.HeadYawS.enable(samplingPeriod)
        self.camera = Camera(robot)

        robot.step(samplingPeriod)
        
        self.reset_upper_body(config_num)        
        self.create_head_controller(2.0)
        self.create_body_controller(1.0)        # send sensor data
        self.set_initial_sensors()        
        
        

    def apply_actions(self, actions):
        self.set( actions)

        
    def read(self):
        if self.mode == 1:
            return self.readLegs()
        
        if self.mode == 2:
            rsp = self.RShoulderPitchS.getValue()
            lsp = self.LShoulderPitchS.getValue()
            print(f'rsp {rsp} lsp {lsp}')


    def set(self, actions):        
        if self.mode == 1:
            self.setLegs(self.initial_sensors, actions)

    def setShoulders(self):
        cmds = {'lsp': 2, 'rsp': 2}        
        self.setMotorPosition(self.LShoulderPitchM, cmds['lsp'])           
        self.setMotorPosition(self.RShoulderPitchM, cmds['rsp'])           

    # setGuardup(0.33, -1.5, -0.2, -0.33, 1.5, -0.2)
    def setGuardup(self):
        cmds = {'lsr': 0.33, 'ler': -1.5, 'ley': -0.2, 'rsr': -0.33, 'rer': 1.5, 'rey': -0.2}
        self.setMotorPosition(self.LShoulderRollM,cmds['lsr'])    # 0.33
        self.setMotorPosition(self.LElbowRollM,cmds['ler'])    # -1.5
        self.setMotorPosition(self.LElbowYawM,cmds['ley'])    # -0.2
        
        self.setMotorPosition(self.RShoulderRollM,cmds['rsr'])    # -0.33
        self.setMotorPosition(self.RElbowRollM,cmds['rer'])    # 1.5
        self.setMotorPosition(self.RElbowYawM,cmds['rey'])    # -0.2


    def create_body_controller(self, gain):
        self.body_controller = PCTHierarchy(1,1)
        o = self.body_controller.get_function(0, 0, "output")
        o.gain = gain


    def create_head_controller(self, gain):
        self.head_controller = PCTHierarchy(1,1)
        o = self.head_controller.get_function(0, 0, "output")
        o.gain = gain

    def update_body_controller(self, motion_library, mode=None):
        head = self.HeadYawS.getValue()
        # print('mode=',mode)
        if mode == ROBOTMODE.TURNING:
            print('head=',head)
        if abs(head)<0.5:
            head = 0
        p = self.body_controller.get_function(0, 0, "perception")
        p.set_value(head)
        o = self.body_controller.get_function(0, 0, "output")
        self.body_controller()
        out = o.get_value()
        if out < 0:            
            print(f'TurnLeft20 head={head:0.3}')
            motion_library.play('TurnLeft20')
            mode = ROBOTMODE.TURNING
        elif out > 0:            
            print(f'TurnRight20 head={head:0.3}')
            motion_library.play('TurnRight20')
            mode = ROBOTMODE.TURNING
        else:
            if mode == ROBOTMODE.TURNING:
                mode = ROBOTMODE.RESET
            
        return mode


    def update_head_controller(self):
        out = 0.0
        pan = self.get_normalized_opponent_x()
        head = self.HeadYawS.getValue()
        if pan is not None:
            p = self.head_controller.get_function(0, 0, "perception")
            p.set_value(pan)
            o = self.head_controller.get_function(0, 0, "output")
            self.head_controller()
            out = o.get_value()
            str = f'pan={pan:0.3} head={head:0.3} out={out:0.3}'
        else:
            str = f'pan={pan} head={head:0.3} out={out}'
            
        print(str)
        self.set_head_rotation(out)
        # hpct.summary()
        return pan


    def set_head_rotation(self, hy):    
        self.setMotorPosition(self.HeadYawM, hy) 

    def get_normalized_opponent_x(self):
        """Locate the opponent in the image and return its horizontal position in the range [-1, 1]."""
        img = self.camera.get_image()
        _, _, horizontal_coordinate = IP.locate_opponent(img)
        if horizontal_coordinate is None:
            return None
        return horizontal_coordinate * 2 / img.shape[1] - 1

    def reset_upper_body(self, config_num):         
        if config_num == 4:         
            self.setGuardup()
        elif config_num == 10:
            self.setShoulders()   
        elif config_num == 12: 
            self.setShoulders()   
        else:
            self.setGuardup()

        # if self.config_num == 10:

    def setLegs(self, initial_sensors, actions):
        # print(actions)
        self.setMotorPosition(self.LHipPitchM,initial_sensors['LHipPitch'] + actions['LHipPitch'])           
        self.setMotorPosition(self.LKneePitchM,initial_sensors['LKneePitch'] + actions['LKneePitch'])
        self.setMotorPosition(self.LAnklePitchM,initial_sensors['LAnklePitch'] + actions['LAnklePitch'])
        self.setMotorPosition(self.RHipPitchM,initial_sensors['RHipPitch'] + actions['RHipPitch'])        
        self.setMotorPosition(self.RKneePitchM,initial_sensors['RKneePitch'] + actions['RKneePitch'])
        self.setMotorPosition(self.RAnklePitchM,initial_sensors['RAnklePitch'] + actions['RAnklePitch'])

    def setMotorPosition(self, motor, position):
        motor.setPosition(min(max(position, motor.min_position),motor.max_position))

    def set_initial_sensors(self):
        self.initial_sensors =  self.read()       
        logger.info(f'InitialS={self.initial_sensors}')
        #print('InitialS=', self.initial_sensors)
 
       
    def reset_lower_body(self, robot):        
        logger.info(f'Reset lower body')
        actions = {'LHipPitch': 0.0, 'LKneePitch': 0.0, 'LAnklePitch': 0.0, 'RHipPitch': 0.0, 'RKneePitch': 0.0, 'RAnklePitch': 0.0}
        self.apply_actions( actions)
        sensors = self.read()
        sum = self.sum(sensors)
        while not sum==0:
            robot.step(robot.time_step)
            self.apply_actions( actions)
            sensors = self.read()
            sum = self.sum(sensors)
        logger.info(f'Sensors={sensors}')

    def sum(self, msg):
        sum = 0
        for v in msg.values():
            sum += abs(v)
        return sum
    
    def readLegs(self):
        
        lhp = self.LHipPitchS.getValue()        
        lkp = self.LKneePitchS.getValue()
        lap = self.LAnklePitchS.getValue()
        
        rhp = self.RHipPitchS.getValue()        
        rkp = self.RKneePitchS.getValue()
        rap = self.RAnklePitchS.getValue()
        
        legs = {'LHipPitch': round(lhp, 3), 'LKneePitch': round(lkp,3), 'LAnklePitch': round(lap, 3), 'RHipPitch': round(rhp, 3), 'RKneePitch': round(rkp, 3), 'RAnklePitch': round(rap, 3)}
        
        return legs