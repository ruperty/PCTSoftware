

class RobotAccess(object):
    def __init__(self, robot, mode=1):
        self.mode=mode
        self.RShoulderPitch = robot.getDevice("RShoulderPitch")
        self.LShoulderPitch = robot.getDevice("LShoulderPitch")
        
        self.LAnklePitch = robot.getDevice("LAnklePitch")
        self.LAnkleRoll = robot.getDevice("LAnkleRoll")
        self.LKneePitch = robot.getDevice("LKneePitch")
        self.LHipPitch = robot.getDevice("LHipPitch")
        self.LHipRoll = robot.getDevice("LHipRoll")
        self.LHipYawPitch = robot.getDevice("LHipYawPitch")

        self.RAnklePitch = robot.getDevice("RAnklePitch")
        self.RAnkleRoll = robot.getDevice("RAnkleRoll")
        self.RKneePitch = robot.getDevice("RKneePitch")
        self.RHipPitch = robot.getDevice("RHipPitch")
        self.RHipRoll = robot.getDevice("RHipRoll")
        self.RHipYawPitch = robot.getDevice("LHipYawPitch")
        
        
    def read(self):
        if self.mode == 1:
            return self.readLegs()
        
        if self.mode == 2:
            rsp = self.RShoulderPitch.getTargetPosition()
            lsp = self.LShoulderPitch.getTargetPosition()
            print(f'rsp {rsp} lsp {lsp}')


    def set(self, initial_sensors, actions):        
        if self.mode == 1:
            self.setLegs(initial_sensors, actions)

    def setLegs(self, initial_sensors, actions):
        print(actions)
        position = initial_sensors['LHipPitch'] + actions['LHipPitch']
        self.LHipPitch.setPosition(position)           
        self.LKneePitch.setPosition(initial_sensors['LKneePitch'] + actions['LKneePitch'])
        self.LAnklePitch.setPosition(initial_sensors['LAnklePitch'] + actions['LAnklePitch'])
        self.RHipPitch.setPosition(initial_sensors['RHipPitch'] + actions['RHipPitch'])        
        self.RKneePitch.setPosition(initial_sensors['RKneePitch'] + actions['RKneePitch'])
        self.RAnklePitch.setPosition(initial_sensors['RAnklePitch'] + actions['RAnklePitch'])

    def readLegs(self):
        
        lhp = self.LHipPitch.getTargetPosition()        
        lkp = self.LKneePitch.getTargetPosition()
        lap = self.LAnklePitch.getTargetPosition()
        
        rhp = self.RHipPitch.getTargetPosition()        
        rkp = self.RKneePitch.getTargetPosition()
        rap = self.RAnklePitch.getTargetPosition()
        
        legs = {'LHipPitch': round(lhp, 3), 'LKneePitch': round(lkp,3), 'LAnklePitch': round(lap, 3), 'RHipPitch': round(rhp, 3), 'RKneePitch': round(rkp, 3), 'RAnklePitch': round(rap, 3)}
        
        return legs