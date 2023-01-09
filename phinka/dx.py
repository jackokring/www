# dx specific module
# vjp -- it's alright
# the back propergator likely is just an easy f identity
# as differential of integral of f -> f
# the forms are for activity of x * f(x) / x where the x behaviour is x / x ...

# adapt parameter order for partial applications

# TODO: create partial applications and add autograd vjp registration

import autograd.numpy as np
from autograd import grad
#from autograd import elementwise_grad as egrad

import math # mumpy.vectorize ...

def seriesList(n, f, x):
    """the series of gradient evaluations"""
    l = []
    diff = f
    for i in range(0, n):
        l.append(diff(x))
        diff = grad(diff)     
    return l     

def cumulateList(l):
    """accumulates a list as a cumulative total"""
    m = []
    sum = 0
    for i in len(l):  
        sum = sum + l[i]
        m.append(sum)
    return m  

def integralAsymtotic(n, method, f, x):
    """integral end point series terms"""
    d = seriesList(n, f, x)
    m = method(n, x)
    out = []
    for i in range(0, n):
        out.append(d[i] * m[i])
    return cumulateList(out)    

def aitkin(a, b, c):
    """calculate the Aitkin series term from 3 terms"""
    deltaCB = (c - b)
    return c - deltaCB * deltaCB / (deltaCB - (b - a))

def seriesAccelerate(l):
    """perform series aymtotic convergence if possible"""
    argc = len(l)
    if argc <= 0:
        raise TypeError('seriesAccelerate must have one positive length input')
    elif argc == 1:
        return l[0]
    elif argc == 2:
        # second should be more accurate
        return l[1]
    elif argc == 3:
        return aitkin(l[0], l[1], l[2])
    out = []
    for i in range(0, argc - 2):
        out.append(aitkin(l[i], l[i + 1], l[i + 2]))
    # tail recurse
    return seriesAccelerate(out)

# singularity asymmtotics
def integralNorm(n, f, x):
    """use normal x^0 -> 1 approximation"""
    def multiply(n, x):
        l = []
        xp = -x
        for i in range(0, n):
            l.append(-xp)
            xp = xp * -x / (i + 2)  # as = 0 at calc for 1
        return l
    return seriesAccelerate(integralAsymtotic(n, multiply, f, x))

def integralPole(n, f, x):
    """use pole Laurent approximation"""
    def multiply(n, x):
        l = []
        xp = -x * x / 2
        for i in range(0, n):
            l.append(-xp)
            xp = xp * -x / (i + 3)  # as = 0 at calc for 1
        return l
    return seriesAccelerate(integralAsymtotic(n, multiply, lambda x: (f(x) / x), x))

def log(x):
    return math.log(x)

def integralLog(n, f, x):
    """use log nested series approximation"""
    # warning a fourth form exist by virtue of commutivity of terms in series
    # if they commute then this form is valid
    # when they don't ... more symbolic calculus required
    # N.B. Can't wait for it to heat uuuuup to try out my new Mathamatica T-shirt
    # #WithWolfram
    # although if they don't doesn't mean it doesn't of 3
    # An unproven on the https://en.wikipedia.org/wiki/Poincar%C3%A9_conjecture
    # extension of space about singularities?

    # Um, so when fusing hydrogen, it kind of escapes control.
    # So exactly what is its future? Is prediction dependent on
    # motion through a space-time near an expanding pre-singular
    # event? Wo exactly are the Romulans? :D
    def integralLogAssistant(n, k, f, x):
        """assistant function for nested series in log approximation"""
        def multiply(n, x):
            l = []
            xp = -x * x * math.pow(x, k) / (k + 2) # as = 0 at calc for 1
            for j in range(0, n):
                l.append(-xp)
                xp = xp * -x / (k + j + 3)
            return l
        return seriesAccelerate(integralAsymtotic(n, multiply, lambda x: grad(grad(x * f(x))), x))  
    def multiply(n, x):
        l = []
        xp = -1
        for i in range(0, n):
            l.append(-xp)
            xp = xp * -x / (i + 2)  # as = 0 at calc for 1
        return l
    lnx = log(x)
    logPart = x * f(x) * lnx
    entropyPart = -(x - x * lnx) * seriesAccelerate(integralAsymtotic(n, multiply, lambda x: grad(x * f(x)), x))  
    total = logPart + entropyPart
    doubleSumParts = []
    scale = -1 / 2
    for i in range(0, n):
        part = integralLogAssistant(n, i, f, x) * -scale  
        doubleSumParts.append(part)  
        scale = scale / -(i + 3) # as = 0 at calc for 1
    doubleSum = seriesAccelerate(cumulateList(doubleSumParts))
    return total + doubleSum    # the total

def preScale(f, xmax, magConverge = 0.5):
    """keep x in convergent domain"""
    return lambda x2: f(x2 / xmax * magConverge)

def postScale(result, xmax, magConverge = 0.5):
    """rescale x back to full integral domain"""
    return lambda x2: result * xmax / magConverge




# main
VERSION = '1.0.0'   # version of algorithm
HELP = 'dx calculus tool'

import argparse

def resolve(args):
    """argument action resolver"""
    return

def main(parser: argparse.ArgumentParser):
    # adder = parser.add_subparsers(help = 'sub-command')
    parser.add_argument('--version', action = 'version', version = '%(prog)s ' + VERSION)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = HELP)
    parser.set_defaults(func = resolve)
    main(parser)
    args = parser.parse_args()
    args.func(args)
