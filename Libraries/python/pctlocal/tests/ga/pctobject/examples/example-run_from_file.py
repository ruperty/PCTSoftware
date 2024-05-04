

from os import sep
from pct.hierarchy import PCTHierarchy
from cutils.paths import get_gdrive

print()
filename = 'MountainCarContinuousV0'+sep+'MC08-ReferencedInputsError-RootMeanSquareError-Mode04'+sep+'ga-000.331-s032-2x2-m004-cdf7cc1497ad143c0b04a3d9e72ab783.properties'
filename = 'CartPoleV1'+sep+'Std03-InputsError-RootMeanSquareError-Mode00'+sep+'ga-000.113-s001-1x1-m000-cfe004e44e94d469055bc00d7aac892f.properties'


filename = 'WindTurbine'+sep+'RewardError-SummedError-Mode04'+sep+'ga-4261658.631-s003-2x2-m004-WT0464-98e71af0a1c48f243c97e83d90551af1.properties'
# filename = 'WindTurbine'+sep+'RewardError-SummedError-Mode04'+sep+'ga--1363.872-s001-5x5-m004-WT0495-de0341c6403f67da78fc93acb4a7035c.properties'
# filename = 'WindTurbine'+sep+'RewardError-SummedError-Mode04'+sep+'ga-15454.878-s003-2x2-m004-WT0177-3e7f96f25466be700f1dea62a8caca92.properties'
# filename = 'WindTurbine'+sep+'RewardError-SummedError-Mode04'+sep+'ga--2630.155-s001-3x5-m004-WT0492-70523e6abb04009382b3cc2d58f6f5f5.properties'

root = get_gdrive() 
file = root + 'data'+sep+'ga'+sep+ filename

render=True

try:
    hierarchy, score = PCTHierarchy.run_from_file(file, min=True, render=render)
    print(f'Score={score:0.3f}')

    hierarchy.consolidate()
    hierarchy.run()
    print(f'Score={score:0.3f}')
except FileNotFoundError:
    print(f'File {file} does not exist.')
    