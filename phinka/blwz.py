# BLWZ file compression

from phinka.types import OptionsDict

# use encode/decode('UTF-8') for b' -> '

# gzip import for .open(file)

import gzip

# hashlib for signatures

import hashlib

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

def lzw(uncompressed, context):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dictSize = 256
    dictionary = {chr(i): i for i in range(dictSize)}
    maxDict = context['maxDict']

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
            if dictSize < maxDict:
                dictSize += 1
            w = c

    # Output the code for w for final symbol
    if w:
        result.append(asBytes(inverted(dictSize, dictionary[w])))
    return result

def ilzw(compressed, context):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dictSize = 256
    dictionary = {i: i.to_bytes(1) for i in range(dictSize)}
    maxDict = context['maxDict']

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
        if dictSize < maxDict:
            dictSize += 1

        w = entry
    return result.getvalue()

# swivel codes

def swivel(list):
    """splits 3 bytes into slow, medium and fast changing stream parts"""
    result = []
    if len(list) < 1:
        return result
    length = len(list[0])
    for i in range(0, length):
        buffer = BytesIO()
        for j in range(0, len(list)):
            buffer.write(list[j][i])
        result.append(buffer.getvalue())
    return result

# BWT code

def counts(s):
    """count character totals in binary string"""
    n = len(s)
    T = [0 for i in range(256)]  # bytes
    for i in range(n):
        T[s[i]] += 1    # add a char
    return T

def bwt(s, context: OptionsDict):
    """Burrows-Wheeler transform"""
    n = len(s)
    m = sorted([s[i:n] + s[0:i] for i in range(n)])
    I = m.index(s)
    L = b''.join([q[-1] for q in m])
    return (I, L)

from operator import itemgetter

def ibwt(I, L, context: OptionsDict):
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
    def __init__(self, f, mode, context: OptionsDict):
        if isinstance(f, str):
            if mode == 'rb' or mode == 'wb':
                self.reader = (mode == 'rb')
                self.buffer = BytesIO()    # new buffer
                self.ended = False
                self.count = 0
                self.message = 'Initilizing'
                defaults = {
                    'blockSize': pow(2, 24) - 1, # large size
                    'maxDict': pow(2, 24) - 1, # maximum size
                    'compresslevel': 9,  # default level
                    'verbose': True # explain output
                }
                if context is not None:
                    self.context = defaults | context
                self.file = gzip.open(f, mode, **context)  # base gzip stream
            else:
                raise ValueError('needs mode rb or wb')
        else:
            raise TypeError('requires a filename')

    def __enter__(self):
        if self.context['verbose']:
            print()
            print(self) # set up display line
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

    def setMessage(self, message):
        self.message = message
        print(self)

    def read(self):
        if not self.reader:
            raise TypeError('file type is wb')
        # process reading
        self.count += 1
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

            buffer = BytesIO()
            for i in range(0, 256):
                used = self.r3()    # symbols used
                packet = [self.file.read(used) for j in range(0, 3)]    # 3 swivel
                self.setMessage('Unpacking')
                packet = swivel(packet)     # reverse transform
                packet = ilzw(packet, self.context)
                buffer.write(packet)
                if buffer.tell() > size:
                    ValueError('bad length count')
            self.setMessage('Inverting')
            self.buffer = BytesIO(ibwt(index, buffer.getvalue(), self.context))
            buffer.close()
            return self.buffer.read(1)

    def write(self, data):
        blockSize = self.context['blockSize']
        if self.reader:
            raise TypeError('file type is rb')
        if isinstance(data, bytes):
            # process writing
            self.count += 1
            self.buffer.write(data)
            while self.buffer.tell() > blockSize or self.ended:
                todo = self.buffer.getvalue()
                self.buffer.close()
                self.buffer = BytesIO(todo[blockSize:])
                todo = todo[:blockSize]
                count = counts[todo]
                self.setMessage('Transforming')
                index, trans = bwt(todo, self.context)
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
                    self.setMessage('Packing')
                    packet = lzw(packet, self.context)
                    self.w3(len(packet))    # store symbols used
                    packet = swivel(packet) # transform into slow/medium/fast
                    for j in packet:
                        # write each partition
                        self.file.write(j)  # doesn't need binary convert

        else:
            raise TypeError('write only writes bytes')

    def readUTF(self):
        """maybe an archive needs filenames"""
        length = int.from_bytes(self.read(8), 'big')
        return self.read(length).decode()

    def writeUTF(self, string):
        """maybe an archive needs filenames"""
        self.write(len(string).to_bytes(8, 'big'))
        self.write(string.encode())

    def close(self):
        self.ended = True
        self.write(b'') # write the last
        self.file.flush()   # flush stream
        self.file.close()

    def flush(self):
        raise TypeError('inefficiency by attempt to flush block')

    def __repr__(self) -> str:
        """show compression details on same line"""
        print('\033[1A', end = '\x1b[2K')   # return to previous line
        if self.file.tell() == 0 or self.count == 0:
            size = 100
        else:
            size = self.file.tell() / self.count
            size *= 100   # percent
            size = int(size)    # as integer

        message = self.message + ': ' + self.file.tell() + '/' + self.count + ' ' + size + '%'
        print(message)

    def __iter__(self):
        return self

    def __next__(self):
        value = self.read()
        if value != b'':
            return value
        else:
            raise StopIteration

from os.path import isfile, isdir

def decompress(args):
    """"""

def compress(args):
    """"""

# main
VERSION = '1.0.0'   # version of codec
HELP = 'blwz compression tool'

import argparse

def resolve(args):
    """argument action resolver"""
    if isdir(args.compress):
        # compress
        compress(args)
    elif isfile(args.ARCHIVE):
        # yes it might be
        decompress(args)
    else:
        # no so can't
        raise TypeError('something wrong with the file names or directories named')

def main(parser: argparse.ArgumentParser):
    parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s ' + VERSION)
    parser.add_argument('-f', '--fast', action = 'store_true', help = 'fastest compression')
    parser.add_argument('-b', '--best', action = 'store_true', help = 'best compression')
    parser.add_argument('-l', '--level', help = 'compression level', type = int, choices = range(0, 10))
    parser.add_argument('-c', '--compress', help = 'compress directory')
    parser.add_argument('ARCHIVE', help = 'archive file name')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = HELP)
    parser.set_defaults(func = resolve)
    main(parser)
    args = parser.parse_args()
    args.func(args)
