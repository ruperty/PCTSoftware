from os import sep, makedirs

from utils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual

test = 2

if test == 0:
      prefix = 'test-1level'
      filepath = 'Std-InputsError-RootMeanSquareError-Mode00/' + prefix +'.properties'
      move={'OL0C0p':[0.1,0]}

if test == 1:
      prefix = 'ga-000.115-s001-2x3-m000-4292b6128e13ac2df54fd2c05a34292e'
      dir = 'Std00-InputsError-RootMeanSquareError-Mode00' 
      
      filepath = dir + sep + prefix +'.properties'
      move={'CartPoleV1': [-0.6, -0.4],'ICV': [0, -0.1], 'ICP': [0,  -0.1], 
        'IPV': [0.0, -0.1],'IPA': [0.0, -0.1], 'Action1ws': [-0.3, -0.4]}    
      font_size, node_size=8, 150
      hname='Cartpole Std00 mode00 score=0.115'
  

if test == 2:
    prefix = 'ga-000.116-s001-1x1-m000-6bd76f9ddbae2f74dc89419548c380c2'
    dir = 'Std01-InputsError-RootMeanSquareError-Mode00'
    filepath = dir + sep + prefix +'.properties'
    file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
    move={'CartPoleV1': [-1, 0.2],'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4], 
        'IPV': [0, 0.5],'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}
    # plots = [ {'plot_items': {'PL1C0ws':'PL1C0ws','PL1C0ws':'ref'}, 'title':'Goal1'},
    #          {'plot_items': {'IPA':'pa','ICP':'cp'}, 'title':'Inputs'}]
    plots = []
    font_size, node_size=10, 200
    hname='Cartpole Std01 mode00 score=0.116'

if test == 10:
      prefix = 'ga-000.124-s001-1x1-m1-99941c2f82fb78be27551fed5488ec27'
      dir = 'Std-InputsError-RootMeanSquareError-Mode01' 
      
      filepath = dir + sep + prefix +'.properties'
      move={'CartPoleV1': [-1, -0.2],'ICV': [-0.45, 0], 'ICP': [-0.25,  0.1], 
            'IPV': [-0.05, 0.2],'IPA': [0.1, 0.3], 'OL0C0p':[0.0,0], 
            'RL0C0c':[-0.0,-0], 'PL0C0ws':[0.0,0.0],  
            'Action1ws': [-1.0, 0]}




file = get_gdrive() + 'data/ga/CartPoleV1/' + filepath
outdir = 'output' + sep + dir
makedirs(outdir, exist_ok=True)
draw_file = outdir + sep + 'draw-'+prefix+'.png'

hpct, hep = HPCTIndividual.from_properties_file(file)
hpct.set_name(hname)
hpct.set_suffixes()
hpct.pretty_print()
hpct.draw(file=draw_file, move=move, with_edge_labels=True, font_size=font_size, node_size=node_size)
print('Image saved to '+draw_file)






