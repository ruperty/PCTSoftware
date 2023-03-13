

class RobotReadings(object):
    def __init__(self, robot):
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
        rsp = self.RShoulderPitch.getTargetPosition()
        lsp = self.LShoulderPitch.getTargetPosition()
        print(f'rsp {rsp} lsp {lsp}')

    def readLegs(self):
        lkp = self.LKneePitch.getTargetPosition()
        rkp = self.RKneePitch.getTargetPosition()
        
        legs = {'LKneePitch': round(lkp,3), 'RKneePitch': round(rkp, 3)}
        
        #print(f'rkp {rkp} lkp {lkp}')
        
        return legs