

from pct.environments import WebotsWrestler
from pct.functions import Constant

wrestler = WebotsWrestler()
wrestler.add_link(Constant(0.1, name='mycon1'))
wrestler.add_link(Constant(0.2, name='mycon2'))
wrestler.add_link(Constant(0.3, name='mycon3'))
wrestler.add_link(Constant(0.4, name='mycon4'))
wrestler.add_link(Constant(0.5, name='mycon5'))
wrestler.add_link(Constant(0.6, name='mycon6'))

loops=100
for i in range(loops):
    if i==loops-1:
        wrestler.done=True
    wrestler()
    
print(wrestler.get_config())