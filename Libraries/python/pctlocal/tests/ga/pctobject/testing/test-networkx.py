

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
A = np.array([[0,1,1,0],
              [1,0,1,1],
              [1,1,0,0],
              [0,1,0,0]])

plt.figure(figsize=(8,8)) 
G=nx.from_numpy_array(A)
nx.draw(G,with_labels=True)


filename = 'Std-InputsError-RootMeanSquareError-Mode00'
file= 'output/'  + filename + '/' + filename + '-test' + '.png'


plt.savefig(file)

#plt.show()


print()
