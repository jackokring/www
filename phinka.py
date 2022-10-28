# phinka specific python
# vjp -- it's alright

import autograd.numpy as np
from autograd import grad
#from autograd import elementwise_grad as egrad

def seriesList(f, x, n):
    """the series of gradient evaluations"""
    l = []
    diff = f
    for i in range(0, n):
        l.append(diff(x))
        diff = grad(diff)     # type: ignore
    return l     

def cumulateList(l):
    """accumulates a list as a cumulative total"""
    m = []
    sum = 0
    for i in len(l):  # type: ignore
        sum = sum + l[i]
        m.append(sum)
    return m  

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

def integralNorm(f, x, n):
    """use normal x^0 -> 1 approximation"""
    def multiply(x, n): # use a differential generator?
        l = []
        for i in range(0, n):
            l.append()
        return l
    return seriesAccelerate(integralAsymtotic(f, x, n, multiply))

def integralPole(f, x, n):
    """use pole Laurent approximation"""

    return seriesAccelerate(integralAsymtotic(f, x, n, multiply))

def integralLog(f, x, n):
    """use log nested series approximation"""

    return seriesAccelerate(integralAsymtotic(f, x, n, multiply))
