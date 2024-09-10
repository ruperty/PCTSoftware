
from pct.plotarrays import PlotArrays  

pas = PlotArrays()
image_filename = pas.to_image('/tmp/ARC', [[1,1,1],[1,1,1],[1,1,1]], [[2,2,2],[2,2,2],[2,2,2]], [[2.6,3,3],[3,3,3],[3,3,3]], 'train', '00000001')
print(image_filename)