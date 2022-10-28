# phinka specific python
# vjp -- it's alright

import autograd.numpy as np
from autograd import grad
#from autograd import elementwise_grad as egrad

import math

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
    def multiply(x, n):
        l = []
        xp = -x
        for i in range(0, n):
            l.append(-xp)
            xp = xp * -x / (i + 2)  # as = 0 at calc for 1
        return l
    return seriesAccelerate(integralAsymtotic(f, x, n, multiply))

def integralPole(f, x, n):
    """use pole Laurent approximation"""
    def multiply(x, n):
        l = []
        xp = -x * x / 2
        for i in range(0, n):
            l.append(-xp)
            xp = xp * -x / (i + 3)  # as = 0 at calc for 1
        return l
    return seriesAccelerate(integralAsymtotic(lambda x: (f(x) / x), x, n, multiply))

def integralLogAssistant(f, x, n, k):
    def multiply(x, n):
        l = []
        xp = -x * x * math.pow(x, k) / (k + 2) # as = 0 at calc for 1
        for j in range(0, n):
            l.append(-xp)
            xp = xp * -x / (k + j + 3)
        return l
    return seriesAccelerate(integralAsymtotic(lambda x: grad(grad(x * f(x))), x, n, multiply))  # type: ignore

def integralLog(f, x, n):
    """use log nested series approximation"""
    def multiply(x, n):
        l = []
        xp = -1
        for i in range(0, n):
            l.append(-xp)
            xp = xp * -x / (i + 2)  # as = 0 at calc for 1
        return l
    logPart = x * f(x) * math.log(x)
    entropyPart = -(x - x * math.log(x)) * seriesAccelerate(integralAsymtotic(lambda x: grad(x * f(x)), x, n, multiply))  # type: ignore
    total = logPart + entropyPart
    doubleSumParts = []
    scale = -1 / 2
    for i in range(0, n):
        part = integralLogAssistant(f, x, n, i) * -scale  # type: ignore
        doubleSumParts.append(part)  # type: ignore
        scale = scale / -(i + 3) # as = 0 at calc for 1
    doubleSum = seriesAccelerate(cumulateList(doubleSumParts))
    return total + doubleSum    # the total
