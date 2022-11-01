# BLWZ file compression
# use encode/decode('UTF-8') for b' -> '

# gzip import for .open(file)

import gzip

# LZW compression (add mods for inverting key bias)

dictSize = 256

def inverted(entry):
    """use inverted symbols on all but first entry"""
    return dictSize - entry # allow zero as dictionary extension in transit
    # more closely matches zero being repeats
    # and high information numbers being individual small symbols

def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    global dictSize
    dictSize = 256
    dictionary = {chr(i): i for i in range(dictSize)}

    first = True
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            out = dictionary[w]
            if not first:
                out = inverted(out) # output inverted pointer for more zeros => redundancy
            else:
                first = False
            result.append(out)
            # Add wc to the dictionary.
            dictionary[wc] = dictSize
            dictSize += 1
            w = c

    # Output the code for w for final symbol
    if w:
        result.append(inverted(dictionary[w]))
    return result

def asBytes(number):
    return number.to_bytes(3, 'big')

def asNumber(bytes):
    if len(bytes) != 3:
        raise ValueError('dictionary pointers limited to 3 bytes')
    return int.from_bytes(bytes, 'big')

def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO

    # Build the dictionary.
    global dictSize
    dictSize = 256
    dictionary = {i: chr(i) for i in range(dictSize)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))  # not inverted exception
    result.write(w)
    for k in compressed:
        j = inverted(k) # eg 256 -> 0, 255 -> 1, 254 -> 2, ..., 0 -> 256 at start
        if j in dictionary:
            entry = dictionary[j]
        elif j == 0:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % j)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dictSize] = w + entry[0]
        dictSize += 1

        w = entry
    return result.getvalue()

# BWT code

def counts(s):
    """count character totals in binary string"""
    n = len(s)
    T = [0 for i in range(256)]  # bytes
    for i in range(n):
        T[s[i]] += 1    # add a char
    return T

def bwt(s):
    """Burrows-Wheeler transform"""
    n = len(s)
    m = sorted([s[i:n] + s[0:i] for i in range(n)])
    I = m.index(s)
    L = ''.join([q[-1] for q in m])
    return (I, L)

from operator import itemgetter

def ibwt(I, L):
    """inverse Burrows-Wheeler transform"""
    n = len(L)
    X = sorted([(i, x) for i, x in enumerate(L)], key=itemgetter(1))

    T = [None for i in range(n)]
    for i, y in enumerate(X):
        j, _ = y
        T[j] = i

    Tx = [I]
    for i in range(1, n):
        Tx.append(T[Tx[i - 1]])

    S = [L[i] for i in Tx]
    S.reverse()
    return ''.join(S)
