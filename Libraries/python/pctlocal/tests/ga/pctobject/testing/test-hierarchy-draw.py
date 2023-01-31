
from pct.hierarchy import PCTHierarchy
from eepct.hpct import HPCTIndividual

test = 4
if test ==2:
    ahpct = PCTHierarchy(2,2)
    ahpct.draw(file="ahpct-single.png",  node_size=1500, figsize=(10,10))# with_labels=True, font_weight='bold', node_color='red',  node_size=500, arrowsize=25, align='vertical'
    
if test ==3:
    ahpct = PCTHierarchy(2,2, links="dense")
    ahpct.draw(file="ahpct-dense.png",  node_size=1500, figsize=(10,10), with_labels=True, with_edge_labels=True)# with_labels=True, font_weight='bold', node_color='red',  node_size=500, arrowsize=25, align='vertical'
    
    
if test ==4:
    ahpct = HPCTIndividual(levels=2,cols=2)
    ahpct.draw(file="ahpct.png",  node_size=1500, figsize=(10,10), with_labels=True, with_edge_labels=True)# with_labels=True, font_weight='bold', node_color='red',  node_size=500, arrowsize=25, align='vertical'    