

from os import sep
from pct.hierarchy import PCTHierarchy
from cutils.paths import get_gdrive

filename = 'MountainCarContinuousV0'+sep+'MC08-ReferencedInputsError-RootMeanSquareError-Mode04'+sep+'ga-000.331-s032-2x2-m004-cdf7cc1497ad143c0b04a3d9e72ab783.properties'
filename = 'CartPoleV1'+sep+'Std03-InputsError-RootMeanSquareError-Mode00'+sep+'ga-000.113-s001-1x1-m000-cfe004e44e94d469055bc00d7aac892f.properties'


root = get_gdrive() 
file = root + 'data'+sep+'ga'+sep+ filename

render=True

try:
    score = PCTHierarchy.run_from_file(file, render=render)
    print(f'Score={score:0.3f}')
except FileNotFoundError:
    print(f'File {file} does not exist.')
    