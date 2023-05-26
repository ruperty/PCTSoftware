
from pct.hierarchy import PCTHierarchy
from pct.putils import smooth
from utils.camera import Camera
from utils.image_processing import ImageProcessing as IP

from enum import IntEnum, auto
import logging, math

logger = logging.getLogger(__name__)


class ROBOTMODE(IntEnum):
    "Modes of robot behaviour."
    FALLEN = auto()
    GENERAL = auto()
    TURNING = auto()
    RESET = auto()
    RISEN = auto()
    PUNCH = auto()
    FORWARDLOOP = auto()
    TURNLEFT60 = auto()

class RobotAccess(object):
    def __init__(self, robot, mode=1, samplingPeriod=20, config_num=None, upper_body=None):
        # print('RobotAccess start')    
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

        ## sensors
        # upper body
        self.RShoulderPitchS = robot.getDevice("RShoulderPitchS")
        self.RShoulderRollS = robot.getDevice("RShoulderRollS")
        self.RElbowRollS = robot.getDevice("RElbowRollS")
        self.RElbowYawS = robot.getDevice("RElbowYawS")

        self.LShoulderPitchS = robot.getDevice("LShoulderPitchS")
        self.LShoulderRollS = robot.getDevice("LShoulderRollS")
        self.LElbowRollS = robot.getDevice("LElbowRollS")
        self.LElbowYawS = robot.getDevice("LElbowYawS")

        # legs
        self.LAnklePitchS = robot.getDevice("LAnklePitchS")
        self.LKneePitchS = robot.getDevice("LKneePitchS")
        self.LHipPitchS = robot.getDevice("LHipPitchS")

        self.RAnklePitchS = robot.getDevice("RAnklePitchS")
        self.RKneePitchS = robot.getDevice("RKneePitchS")
        self.RHipPitchS = robot.getDevice("RHipPitchS")

        # head
        self.HeadYawM = robot.getDevice("HeadYaw")
        self.HeadYawS = robot.getDevice("HeadYawS")

        # sonar
        self.SonarLeftS = robot.getDevice("Sonar/Left")
        self.SonarRightS = robot.getDevice("Sonar/Right")

        # gps
        # self.gps = robot.getDevice("gps")

        self.camera = Camera(robot)

        ## enable sensors
        self.LAnklePitchS.enable(samplingPeriod)
        self.LKneePitchS.enable(samplingPeriod)
        self.LHipPitchS.enable(samplingPeriod)
        self.RAnklePitchS.enable(samplingPeriod)
        self.RKneePitchS.enable(samplingPeriod)
        self.RHipPitchS.enable(samplingPeriod)

        self.HeadYawS.enable(samplingPeriod)

        self.SonarLeftS.enable(samplingPeriod)
        self.SonarRightS.enable(samplingPeriod)

        self.RShoulderPitchS.enable(samplingPeriod)
        self.RShoulderRollS.enable(samplingPeriod)
        self.RElbowRollS.enable(samplingPeriod)
        self.RElbowYawS.enable(samplingPeriod)

        self.LShoulderPitchS.enable(samplingPeriod)
        self.LShoulderRollS.enable(samplingPeriod)
        self.LElbowRollS.enable(samplingPeriod)
        self.LElbowYawS.enable(samplingPeriod)

        robot.step(samplingPeriod)
        
        if upper_body is not None:
            self.set_upper_body(upper_body)        
        
        if config_num is not None:
            self.reset_upper_body(config_num)        
            
        self.create_head_controller(2.0)
        self.create_body_controller(1.0)        # send sensor data
        self.set_initial_sensors()        
        self.sonar_smooth=2.55
        self.smooth_factor=0.1
        
        # print('RobotAccess end')    

        

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
        # logger.info('upper_body')
        cmds = {'lsp': 2, 'rsp': 2}        
        self.setMotorPosition(self.LShoulderPitchM, cmds['lsp'])           
        self.setMotorPosition(self.RShoulderPitchM, cmds['rsp'])           

    # setGuardup(0.33, -1.5, -0.2, -0.33, 1.5, -0.2)
    def setGuardup(self):
        # logger.info('upper_body')
        cmds = {'lsr': 0.33, 'ler': -1.5, 'ley': -0.2, 'rsr': -0.33, 'rer': 1.5, 'rey': -0.2}
        self.setMotorPosition(self.LShoulderRollM,cmds['lsr'])    # 0.33
        self.setMotorPosition(self.LElbowRollM,cmds['ler'])    # -1.5
        self.setMotorPosition(self.LElbowYawM,cmds['ley'])    # -0.2
        
        self.setMotorPosition(self.RShoulderRollM,cmds['rsr'])    # -0.33
        self.setMotorPosition(self.RElbowRollM,cmds['rer'])    # 1.5
        self.setMotorPosition(self.RElbowYawM,cmds['rey'])    # -0.2

    def punch_position(self, mode):
        # logger.info('upper_body')
        if mode == ROBOTMODE.PUNCH:
            # cmds = {'LHipPitch': 0.4, 'LKneePitch': 0.2,  'LAnklePitch': -1.0, 'RHipPitch': -1.6, 'RKneePitch': 1.3, 'RAnklePitch': 0.0, 'RShoulderRoll': 0.3, 'RElbowRoll': 0, 'RElbowYaw': 0, 'RShoulderPitch': -0.5} # stable psition but doesn't connect
            cmds = {'LHipPitch': 0.4, 'LKneePitch': 0.0,  'LAnklePitch': -1.0, 'RHipPitch': -1.6, 'RKneePitch': 1.3, 'RAnklePitch': 0.0, 
                    'RShoulderRoll': 0.3, 'RElbowRoll': 0, 'RElbowYaw': 0, 'RShoulderPitch': 0.25, 
                    'LShoulderRoll': -0.3, 'LElbowRoll': 0, 'LElbowYaw': 0, 'LShoulderPitch': 0.25, }
            self.setMotorPosition(self.LAnklePitchM,cmds['LAnklePitch'])    
            self.setMotorPosition(self.LKneePitchM,cmds['LKneePitch'])    
            self.setMotorPosition(self.LHipPitchM,cmds['LHipPitch'])    
            
            self.setMotorPosition(self.RAnklePitchM,cmds['RAnklePitch'])    
            self.setMotorPosition(self.RKneePitchM,cmds['RKneePitch'])    
            self.setMotorPosition(self.RHipPitchM,cmds['RHipPitch'])    

            self.setMotorPosition(self.RShoulderRollM,cmds['RShoulderRoll'])    
            self.setMotorPosition(self.RElbowRollM,cmds['RElbowRoll'])    
            self.setMotorPosition(self.RElbowYawM,cmds['RElbowYaw'])    
            self.setMotorPosition(self.RShoulderPitchM, cmds['RShoulderPitch'])      

            self.setMotorPosition(self.LShoulderRollM,cmds['LShoulderRoll'])    
            self.setMotorPosition(self.LElbowRollM,cmds['LElbowRoll'])    
            self.setMotorPosition(self.LElbowYawM,cmds['LElbowYaw'])     
            self.setMotorPosition(self.LShoulderPitchM, cmds['LShoulderPitch'])      

            acmds = {'RShoulderRoll': 0.3, 'LShoulderRoll': -0.3}

            if self.check_punch_position(acmds):
                return ROBOTMODE.RESET
            else:
                return ROBOTMODE.PUNCH

        return mode

   
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
        # if mode == ROBOTMODE.TURNING:
        #     print('head=',head)
        if abs(head)<0.5:
            head = 0
        p = self.body_controller.get_function(0, 0, "perception")
        p.set_value(head)
        o = self.body_controller.get_function(0, 0, "output")
        self.body_controller()
        out = o.get_value()
        if out < 0:            
            logger.info(f'TurnLeft20 head={head:0.3}')
            motion_library.play('TurnLeft20')
            mode = ROBOTMODE.TURNING
        elif out > 0:            
            logger.info(f'TurnRight40 head={head:0.3}')
            motion_library.play('TurnRight40')
            mode = ROBOTMODE.TURNING
        else:
            if mode == ROBOTMODE.TURNING:
                mode = ROBOTMODE.RESET
            
        return mode
    
    def run_behaviour(self, motion_library, mode):
        if mode == ROBOTMODE.FORWARDLOOP:
            # print(f'TurnRight20 head={head:0.3}')
            motion_library.play('ForwardLoop')

        if mode == ROBOTMODE.TURNLEFT60:
            # print(f'TurnRight20 head={head:0.3}')
            motion_library.play('TurnLeft60')

            

        return mode


    def distance_control(self, mode):
        if mode != ROBOTMODE.PUNCH:
            sonar_l = self.SonarLeftS.getValue()
            sonar_r = self.SonarRightS.getValue()
            sonar  =  min(sonar_l, sonar_r)
            self.sonar_smooth = smooth(sonar,self.sonar_smooth,self.smooth_factor)
            # if self.sonar_smooth < 1:
            #     print(f'sonar={self.sonar_smooth} ')
            if self.sonar_smooth < 0.35:
                mode = ROBOTMODE.PUNCH
                self.sonar_smooth = 2.55

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
            
        #print(str)
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


    def set_upper_body(self, upper_body):  
        if upper_body == 'guardup':
            self.setGuardup()
        else:
            self.setShoulders()

    def reset_upper_body(self, config_num):       
        self.set_head_rotation(0)  
        if config_num == 4:         
            self.setGuardup()
            # self.setShoulders()   
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
        # logger.info(f'InitialS={self.initial_sensors}')
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
            # print('reset_lower_body', sum)
        logger.info(f'Sensors={sensors}')

    def sum(self, msg):
        sum = 0
        for v in msg.values():
            sum += abs(v)
        return sum
    
    def read_upper_body_right(self):
        rsp = self.RShoulderPitchS.getValue()
        rsr = self.RShoulderRollS.getValue()
        rer = self.RElbowRollS.getValue()
        rey = self.RElbowYawS.getValue()

        rtn = {'RShoulderRoll': round(rsr,3), 'RElbowRoll': round(rer, 3),  'RElbowYaw': round(rey, 3), 'RShoulderPitch': round(rsp, 3)}

        return rtn

    def read_upper_body_left(self):
        lsp = self.LShoulderPitchS.getValue()
        lsr = self.LShoulderRollS.getValue()
        ler = self.LElbowRollS.getValue()
        ley = self.LElbowYawS.getValue()

        rtn = {'LShoulderRoll': round(lsr,3), 'LElbowRoll': round(ler, 3),  'LElbowYaw': round(ley, 3), 'LShoulderPitch': round(lsp, 3)}

        return rtn

    def read_shoulders(self):    
        rsr = self.RShoulderRollS.getValue()
        lsr = self.LShoulderRollS.getValue()

        rtn = {'RShoulderRoll': round(rsr,3), 'LShoulderRoll': round(lsr,3)}

        return rtn

    def read_upper_body(self):
        rsp = self.RShoulderPitchS.getValue()
        rsr = self.RShoulderRollS.getValue()
        rer = self.RElbowRollS.getValue()
        rey = self.RElbowYawS.getValue()
        lsp = self.LShoulderPitchS.getValue()
        lsr = self.LShoulderRollS.getValue()
        ler = self.LElbowRollS.getValue()
        ley = self.LElbowYawS.getValue()

        rtn = {'RShoulderRoll': round(rsr,3), 'RElbowRoll': round(rer, 3),  'RElbowYaw': round(rey, 3), 'RShoulderPitch': round(rsp, 3), 'LShoulderRoll': round(lsr,3), 'LElbowRoll': round(ler, 3),  'LElbowYaw': round(ley, 3), 'LShoulderPitch': round(lsp, 3)}

        return rtn

    def readLegs(self):
        
        lhp = self.LHipPitchS.getValue()        
        lkp = self.LKneePitchS.getValue()
        lap = self.LAnklePitchS.getValue()
        
        rhp = self.RHipPitchS.getValue()        
        rkp = self.RKneePitchS.getValue()
        rap = self.RAnklePitchS.getValue()
        
        legs = {'LHipPitch': round(lhp, 3), 'LKneePitch': round(lkp,3), 'LAnklePitch': round(lap, 3), 'RHipPitch': round(rhp, 3), 'RKneePitch': round(rkp, 3), 'RAnklePitch': round(rap, 3)}
        
        return legs
    
    def check_punch_position(self, d1):
        # d2 = self.readLegs()
        # upper = self.read_upper_body()
        # d2.update(upper)
        
        d2 = self.read_shoulders()

        diff = {key: d1[key] - d2[key] for key in d1}

        # print('diff=', diff)
        sum = self.sum(diff)
        return math.isclose(sum, 0, rel_tol=0.05)        


