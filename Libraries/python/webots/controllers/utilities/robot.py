

class RobotAccess(object):
    def __init__(self, robot, mode=1, samplingPeriod=20):
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

        # sensors
        self.RShoulderPitchS = robot.getDevice("RShoulderPitchS")
        self.LShoulderPitchS = robot.getDevice("LShoulderPitchS")

        self.LAnklePitchS = robot.getDevice("LAnklePitchS")
        self.LKneePitchS = robot.getDevice("LKneePitchS")
        self.LHipPitchS = robot.getDevice("LHipPitchS")

        self.RAnklePitchS = robot.getDevice("RAnklePitchS")
        self.RKneePitchS = robot.getDevice("RKneePitchS")
        self.RHipPitchS = robot.getDevice("RHipPitchS")

        print('getSamplingPeriod=',self.LAnklePitchS.getSamplingPeriod())
        robot.step(samplingPeriod)
        self.LAnklePitchS.enable(samplingPeriod)
        self.LKneePitchS.enable(samplingPeriod)
        self.LHipPitchS.enable(samplingPeriod)
        self.RAnklePitchS.enable(samplingPeriod)
        self.RKneePitchS.enable(samplingPeriod)
        self.RHipPitchS.enable(samplingPeriod)


        
        
    def read(self):
        if self.mode == 1:
            return self.readLegs()
        
        if self.mode == 2:
            rsp = self.RShoulderPitchS.getValue()
            lsp = self.LShoulderPitchS.getValue()
            print(f'rsp {rsp} lsp {lsp}')


    def set(self, initial_sensors, actions):        
        if self.mode == 1:
            self.setLegs(initial_sensors, actions)

    def setShoulders(self, left, right):
        self.setMotorPosition(self.LShoulderPitchM,left)           
        self.setMotorPosition(self.RShoulderPitchM,right)           

    def setLegs(self, initial_sensors, actions):
        self.setMotorPosition(self.LHipPitchM,initial_sensors['LHipPitch'] + actions['LHipPitch'])           
        self.setMotorPosition(self.LKneePitchM,initial_sensors['LKneePitch'] + actions['LKneePitch'])
        self.setMotorPosition(self.LAnklePitchM,initial_sensors['LAnklePitch'] + actions['LAnklePitch'])
        self.setMotorPosition(self.RHipPitchM,initial_sensors['RHipPitch'] + actions['RHipPitch'])        
        self.setMotorPosition(self.RKneePitchM,initial_sensors['RKneePitch'] + actions['RKneePitch'])
        self.setMotorPosition(self.RAnklePitchM,initial_sensors['RAnklePitch'] + actions['RAnklePitch'])

    def setMotorPosition(self, motor, position):
        motor.setPosition(min(max(position, motor.min_position),motor.max_position))

    def readLegs(self):
        
        lhp = self.LHipPitchS.getValue()        
        lkp = self.LKneePitchS.getValue()
        lap = self.LAnklePitchS.getValue()
        
        rhp = self.RHipPitchS.getValue()        
        rkp = self.RKneePitchS.getValue()
        rap = self.RAnklePitchS.getValue()
        
        legs = {'LHipPitch': round(lhp, 3), 'LKneePitch': round(lkp,3), 'LAnklePitch': round(lap, 3), 'RHipPitch': round(rhp, 3), 'RKneePitch': round(rkp, 3), 'RAnklePitch': round(rap, 3)}
        
        return legs