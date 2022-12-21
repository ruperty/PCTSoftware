

from utils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual


file = get_gdrive() + 'data/ga/CartPoleV1/Std-InputsError-RootMeanSquareError-Mode00/ga-000.121-s001-3x4-m0-924f41bf8c5ff68654b05da500579fea.properties'
#ga-000.124-s001-1x1-m0-a8ab4cf3151b29a13abb2680bc574781.properties'
#ga-000.124-s001-1x1-m0-8b0d9b3da7c984766efd233b07bec593.properties'
#ga-000.124-s001-1x1-m0-5cb8a3bb27767c9f0cd9f6df498bcc59.properties'

# hep = HPCTEvolveProperties()
# hep.load_db(file=file)
# config = eval(hep.db['config'])
# hpct = HPCTIndividual.from_config(config)

hpct = HPCTIndividual.from_properties_file(file)

hpct.set_name('Cartpole')
hpct.set_suffixes()
#print(hpct.get_config())


move={'CartPoleV1': [-1, -0.2],'ICV': [-0.45, 0], 'ICP': [-0.25,  0.1], 
      'IPV': [-0.05, 0.2],'IPA': [0.1, 0.3], 'OL0C0p':[0.0,0], 
      'RL0C0c':[-0.0,-0], 'PL0C0ws':[0.0,0.0],  
      'Action1ws': [-1.0, 0]}
move={}
hpct.draw(file='draw-test.png', move=move, with_edge_labels=True, font_size=8, node_size=200)






