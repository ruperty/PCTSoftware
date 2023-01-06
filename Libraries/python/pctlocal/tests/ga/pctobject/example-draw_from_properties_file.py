

from utils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual

test = 1

if test == 0:
      prefix = 'test-1level'
      filepath = 'Std-InputsError-RootMeanSquareError-Mode00/' + prefix +'.properties'
      move={'OL0C0p':[0.1,0]}

if test == 1:
      prefix = 'ga-000.124-s001-1x1-m1-99941c2f82fb78be27551fed5488ec27'
      filepath = 'Std-InputsError-RootMeanSquareError-Mode01/' + prefix +'.properties'
      move={'CartPoleV1': [-1, -0.2],'ICV': [-0.45, 0], 'ICP': [-0.25,  0.1], 
            'IPV': [-0.05, 0.2],'IPA': [0.1, 0.3], 'OL0C0p':[0.0,0], 
            'RL0C0c':[-0.0,-0], 'PL0C0ws':[0.0,0.0],  
            'Action1ws': [-1.0, 0]}


file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
hpct, hep = HPCTIndividual.from_properties_file(file)
hpct.set_name('Cartpole')
hpct.set_suffixes()
#print(hpct.get_config())
draw_file = 'draw-'+prefix+'.png'

hpct.draw(file=draw_file, move=move, with_edge_labels=True, font_size=8, node_size=200)
print('Image saved to '+draw_file)






