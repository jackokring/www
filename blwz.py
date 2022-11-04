# BLWZ file compression
# use encode/decode('UTF-8') for b' -> '

# gzip import for .open(file)

import gzip

# for quick string buffers

from io import BytesIO 

# LZW compression (add mods for inverting key bias)

def inverted(size, entry):
    """use inverted symbols on all but first entry"""
    return size - entry # allow zero as dictionary extension in transit
    # more closely matches zero being repeats
    # and high information numbers being individual small symbols

def asBytes(number):
    return number.to_bytes(3, 'big')

def asNumber(bytes):
    if len(bytes) != 3:
        raise ValueError('dictionary pointers limited to 3 bytes')
    return int.from_bytes(bytes, 'big')

def lzw(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dictSize = 256
    dictionary = {chr(i): i for i in range(dictSize)}

    first = True
    w = b''
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            out = dictionary[w]
            if not first:
                out = inverted(dictSize, out) # output inverted pointer for more zeros => redundancy
            else:
                first = False
            result.append(asBytes(out))
            # Add wc to the dictionary.
            dictionary[wc] = dictSize
            dictSize += 1
            w = c

    # Output the code for w for final symbol
    if w:
        result.append(asBytes(inverted(dictSize, dictionary[w])))
    return result

def ilzw(compressed):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dictSize = 256
    dictionary = {i: i.to_bytes(1) for i in range(dictSize)}

    if len(compressed) == 0:
        return b''  # null compressed

    # use BytesIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = BytesIO()
    first = asNumber(compressed.pop(0))
    if first > 255:
        raise ValueError('bad first symbol')
    w = first.to_bytes(1)  # not inverted exception
    result.write(w)
    for k in compressed:
        j = asNumber(inverted(dictSize, k)) # eg 256 -> 0, 255 -> 1, 254 -> 2, ..., 0 -> 256 at start
        if j in dictionary:
            entry = dictionary[j]
        elif j == 0:
            entry = w + w[0]
        else:
            raise ValueError('bad symbol')
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dictSize] = w + entry[0]
        dictSize += 1

        w = entry
    return result.getvalue()

# BWT code

blockSize = 65536   # set the block size

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
    L = b''.join([q[-1] for q in m])
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
    return b''.join(S)

# context manager

class open: # capa not required for method context manager styling
    """a context manager."""
    def __init__(self, f, mode):
        if isinstance(f, str):
            if mode == 'rb' or mode == 'wb':
                self.file = gzip.open(f, mode)  # base gzip stream
                self.read = (mode == 'rb')
                self.buffer = BytesIO()    # new buffer
                self.ended = False
            else:
                raise ValueError('needs mode rb or wb')
        else:
            raise ValueError('requires a filename')

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        # clean up
        self.close()

    def __getattr__(self, attr):
        return getattr(self.file, attr)

    def r3(self):
        return asNumber(self.read(3))

    def w3(self, num):
        self.file.write(asBytes(num))

    def read(self):
        if not self.read:
            raise TypeError('file type is wb')
        # process reading
        out = self.buffer.read(1)
        if out == b'':
            # none EOF?
            self.buffer.close()
            # check EOF?
            if self.file.peek(1) == b'':
                return out
            size = self.r3()
            index = self.r3()
            if index >= size:
                raise ValueError('bad index count')
            count = [self.r3() for i in range(256)]

            buffer = BytesIO()
            for i in count:
                used = self.r3()    # symbols used
                packet = [self.r3() for j in range(used)]
                packet = ilzw(packet)
                buffer.write(packet)
                if buffer.tell() > size:
                    ValueError('bad length count')
            self.buffer = BytesIO(ibwt(index, buffer.getvalue()))
            buffer.close()
            return self.buffer.read(1)

    def write(self, data):
        if self.read:
            raise TypeError('file type is rb')
        if isinstance(data, bytes):
            # process writing
            self.buffer.write(data)
            while self.buffer.tell() > blockSize or self.ended:
                todo = self.buffer.getvalue()
                self.buffer.close()
                self.buffer = BytesIO(todo[blockSize:])
                todo = todo[:blockSize]
                count = counts[todo]
                index, trans = bwt(todo)
                size = len(todo)

                self.w3(size)

                # BWT index
                self.w3(index)
                # counts of partition
                # information fission by self-partition mutual information redundancy
                # elimination and is much more efficient than prime factorization
                # so 256 partitions represents upto 8 bits per symbol
                # saved by dictionary reset per partition and BWT following symbol
                # commonality

                for i in count:
                    packet = trans[:i]
                    trans = trans[i:]
                    packet = lzw(packet)
                    self.w3(len(packet))    # store symbols used
                    for j in packet:
                        # write each partition
                        self.file.write(j)  # doesn't need binary convert

        else:
            raise ValueError('write only writes bytes')

    def close(self):
        self.ended = True
        self.write(b'') # write the last
        self.file.flush()   # flush stream
        self.file.close()

    def flush(self):
        raise TypeError('inefficiency error by attempt to flush block')

    # TODO: iteration interface, but assume read is dynamic binding
    def __iter__(self):
        return iter(self.file)
        