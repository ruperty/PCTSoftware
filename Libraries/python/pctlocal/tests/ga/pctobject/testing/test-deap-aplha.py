


import random
from deap import tools






for i in range(1,10):
    alpha = i/10.0
    print(f'alpha={alpha}')
    wts1=[0.3]
    wts2=[0.7]
    w1=wts1[0]
    w2=wts2[0]
    random.seed(1)
    wts1, wts2 = tools.cxBlend(wts1, wts2, alpha)
    diff = abs(w1-wts1[0])
    p1=100*diff
    p2=100*(diff/wts1[0])
    print(f'{w1:0.3f} {w2:0.3f}')
    print(f'{wts1[0]:0.3f} {wts2[0]:0.3f}')
    print(f'*** {p1:0.1f}% {p2:0.1f}%')