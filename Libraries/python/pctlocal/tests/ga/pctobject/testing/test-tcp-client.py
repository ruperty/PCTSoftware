

from pct.environments import WebotsWrestler
from pct.functions import Constant

wrestler = WebotsWrestler()
wrestler.add_link(Constant(1, name='mycon'))

loops=2
for i in range(loops):
    if i==loops-1:
        wrestler.done=True
    wrestler()