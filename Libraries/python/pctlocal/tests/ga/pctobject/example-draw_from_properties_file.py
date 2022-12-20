

from eepct.hpct import HPCTEvolveProperties
from utils.paths import get_root_path

from deap import base, creator

from epct.evolvers import CommonToolbox

from eepct.hpct import HPCTIndividual


from epct.configs import DynamicArchitecture

root = get_root_path()

file = root + 'tmp/ga/CartPoleV1/Std-InputsError-RootMeanSquareError-Mode00/ga-000.124-s001-1x1-m0-5cb8a3bb27767c9f0cd9f6df498bcc59.properties'
hep = HPCTEvolveProperties()
hep.load_db(file=file)

config = eval(hep.db['config'])
print(config)

move={'CartPoleV1': [-1, -0.2],'ICV': [-0.45, 0], 'ICP': [-0.25,  0.1], 
      'IPV': [-0.05, 0.2],'IPA': [0.1, 0.3], 'OL0C0':[0.0,0], 
      'RL0C0':[-0.0,-0], 'PL0C0':[0.0,0.0],  
      'Action1': [-1.0, 0]}
 
hpct = HPCTIndividual.from_config(config)
hpct.draw(file='draw-test.png', move=move, with_edge_labels=True)






