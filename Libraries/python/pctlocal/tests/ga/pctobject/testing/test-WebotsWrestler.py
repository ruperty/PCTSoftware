

from pct.environments import WebotsWrestler
from pct.functions import Constant

wrestler = WebotsWrestler()
wrestler.add_link(Constant(0.1, name='mycon1'))
wrestler.add_link(Constant(0.2, name='mycon2'))
wrestler.add_link(Constant(0.3, name='mycon3'))
wrestler.add_link(Constant(0.4, name='mycon4'))
wrestler.add_link(Constant(0.5, name='mycon5'))
wrestler.add_link(Constant(0.6, name='mycon6'))

loops=1
while True:
    # if i==loops-1:
    #     wrestler.done=True
    try:
        wrestler()
        loops+=1
    except Exception as ex:
        print(f'loops={loops}')    
        break
        
print(wrestler.get_config(zero=0))