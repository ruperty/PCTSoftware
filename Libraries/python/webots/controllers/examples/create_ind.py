

#from controller import Robot


# from utilities.robot import RobotReadings
# from participant.participant import Wrestler

from webots.environments import WebotsWrestler


# from eepct.hpct import HPCTIndividual, HPCTEvolver, HPCTArchitecture, HPCTEvolverWrapper
# from eepct.hpct import HPCTFUNCTION, HPCTLEVEL, HPCTVARIABLE

from epct.evolvers import CommonToolbox
from deap import base, creator



creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)

print("hi")


if __name__ == "__main__":

    lower, upper = -1, 1 
    arch = HPCTArchitecture(lower_float=lower, upper_float=upper)
    arch.configure()
    arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
    arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
    print(arch)


