

from pct.environments import WebotsWrestler

wrestler = WebotsWrestler()

loops=100
for i in range(loops):
    if i==loops-1:
        wrestler.done=True
    wrestler()