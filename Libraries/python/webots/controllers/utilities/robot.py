

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
        robot.step(samplingPeriod)


        
        
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



    def reset_lower_body(self):
        self.actions = {'LHipPitch': 0.0, 'LKneePitch': 0.0, 'LAnklePitch': 0.0, 'RHipPitch': 0.0, 'RKneePitch': 0.0, 'RAnklePitch': 0.0}
        self.apply_actions()
        sensors = self.rr.read()
        sum = self.hpcthelper.sum(sensors)
        while not sum==0:
            self.apply_actions()
            sensors = self.rr.read()
            print('Sensors=', sensors)
            sum = self.hpcthelper.sum(sensors)

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