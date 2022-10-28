# phinka specific python
# vjp -- it's alright

import autograd.numpy as np
from autograd import grad
#from autograd import elementwise_grad as egrad

def seriesListItem(f, x):
    """yields the series of gradient evaluations"""
    diff = f
    while True:
        yield diff(x)
        diff = grad(diff)     # type: ignore

def seriesList(f, x, n):
    """creates a list of differentials of increasing order"""
    l = []
    for i in range(0, n):
        l.append(seriesListItem(f, x))
    return l        

def cumulateList(l):
    """accumulates a list as a cumulative total"""
    m = []
    sum = 0
    for i in len(l):  # type: ignore
        sum = sum + l[i]
        m.append(sum)
    return m

def multipliedListNorm(x, n): # use a differential generator?
    l = []
    for i in range(0, n):
        l.append(??)
    return l   

def integralAsymtotic(f, x, n, method):
    """integral end point series terms"""
    d = seriesList(f, x, n)
    m = method(x, n)
    out = []
    for i in range(0, n):
        out.append(d[i] * m[i])
    return cumulateList(out)    

def seriesAccelerate(l):
    """perform series convergence"""