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

def asBytes(number, n):
    return number.to_bytes(n, 'big')

def asNumber(bytes, n):
    if len(bytes) != n:
        raise ValueError('dictionary pointers limited to 3 bytes')
    return int.from_bytes(bytes, 'big')

def lzw(uncompressed, context: OptionsDict = {}):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dictSize = 256
    dictionary = {asBytes(i, 1): i for i in range(dictSize)}
    maxDict = context['maxDict']

    def inverted(entry):
        return dictSize - entry - 1 # allow zero as dictionary extension in transit
        # more closely matches zero being repeats
        # and high information numbers being individual small symbols

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
                out = inverted(out) # output inverted pointer for more zeros => redundancy
            else:
                first = False
            result.append(asBytes(out), 3)
            # Add wc to the dictionary.
            if dictSize < maxDict:
                dictionary[wc] = dictSize   # avoid overwrite of last entry to prevent growth cascade
                dictSize += 1
            w = c

    # Output the code for w for final symbol
    if w:
        result.append(asBytes(inverted(dictionary[w]), 3))
    return result

def ilzw(compressed, context: OptionsDict = {}):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dictSize = 256
    dictionary = {i: asBytes(i, 1) for i in range(dictSize)}
    maxDict = context['maxDict']
    closed = False
    last = b''

    def inverted(entry):
        return dictSize - entry # allow zero as dictionary extension in transit
        # more closely matches zero being repeats
        # and high information numbers being individual small symbols

    if len(compressed) == 0:
        return b''  # null compressed

    # use BytesIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = BytesIO()
    first = asNumber(compressed.pop(0), 3)
    if first > 255:
        raise ValueError('bad first symbol')
    w = asBytes(first, 1)  # not inverted exception
    result.write(w)
    for k in compressed:
        j = inverted(asNumber(k, 3)) # eg 256 -> 0, 255 -> 1, 254 -> 2, ..., 0 -> 256 at start
        if j in dictionary:
            entry = dictionary[j]
        elif j == dictSize: # auto-gen
            if not closed:
                entry = w + w[0]
            else:
                # persist last dictionary entry
                entry = last
        else:
            raise ValueError('bad symbol')
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        if dictSize < maxDict - 1:  # avoid setting last for inverted(0) auto gen
            dictionary[dictSize] = w + entry[0]
            # inverse always follows a symbol behind
            dictSize += 1
        else:
            if not closed:
                last = w + entry[0]
            closed = True

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

def radixSort(values, key, step=0):
    if len(values) < 2:
        for value in values:
            yield value
        return

    bins = {}
    for value in values:
        bins.setdefault(key(value, step), []).append(value)

    for k in sorted(bins.keys()):
        for r in radixSort(bins[k], key, step + 1):
            yield r

def bwKey(text, value, step):
    return text[(value + step)] # % len(text)]

from functools import partial

def bwt(s, context: OptionsDict = {}):
    """Burrows-Wheeler transform"""
    n = len(s)
    d = s + s
    # m = sorted([s[i:n] + s[0:i] for i in range(n)])
    m = radixSort(range(n), partial(bwKey, d))
    I = 0
    #for i in m:
    #    match = True
    #    for j in range(n):
    #        if s[j] != bwKey(d, i, j):
    #            match = False
    #            break
    #    if match:
    #        break   # I right
    #    I += 1
    I = m.index(0)
    L = b''.join(d[q - 1] for q in m)
    return (I, L)

from operator import itemgetter

def ibwt(I, L, context: OptionsDict = {}):
    """inverse Burrows-Wheeler transform"""
    n = len(L)
    X = sorted([(i, x) for i, x in enumerate(L)], key = itemgetter(1))

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
import os

VERSIONS = ['1.0.0']    # index for code
SIGN_VERSIONS = ['1.0.0']  # index for code

# alter for updates to algorithms
VERSION_INDEX = 0
SIGN_INDEX = 0

# use phinka.open class as it proxies the constructor
class blwz: # capa not required for method context manager styling
    """a context manager."""
    def __init__(self, f, mode = 'rb', context: OptionsDict = {}):
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
                    'verbose': True, # explain output
                    'gzip': True
                }
                self.context = defaults | context
                if self.context['gzip']:
                    self.file = gzip.open(f, mode, **context)  # base gzip stream
                else:
                    self.file = open(f, mode)  # base raw stream
                # TODO: sign versions
                self.digest = hashlib.sha512()  # 64 bytes
                if self.reader:
                    self.size = os.stat(f).st_size  # get file size
                    version = self.r3(1)
                    if version <= VERSION_INDEX:
                        self.maybePrint('archive version ' + VERSIONS[version])
                    else:
                        ValueError('unsupported archive version')
                else:
                    self.w3(VERSION_INDEX, 1)
            else:
                raise ValueError('needs mode rb or wb')
        else:
            raise TypeError('requires a filename')
    
    # contextlib.contextmanager is too simple
    # def f(x):
    #   enter
    #   yield cm
    #   exit

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

    # raw integer read and write
    def r3(self, n):
        return asNumber(self.file.read(n), n)

    def w3(self, num, n):
        self.file.write(asBytes(num, n))

    # on stream read and write integer
    def r3Atop(self, n):
        return asNumber(self.read(n), n)

    def w3Atop(self, num, n):
        self.write(asBytes(num, n))

    def maybePrint(self, what, newline = False):
        if self.context['verbose']:
            print(what)
            if newline:
                print()

    def setMessage(self, message):
        self.message = message
        self.maybePrint(self)

    def digestRead(self):
        out = self.buffer.read(1)
        self.digest.update(out)
        return out

    def read(self, count = 1):
        out = BytesIO()
        for i in range(0, count):
            out.write(self.read1())
        return out.getvalue()   # bytes

    def read1(self):
        if not self.reader:
            raise TypeError('file type is wb')
        # process reading
        self.count += 1
        out = self.digestRead()
        if out == b'':
            # none EOF?
            self.buffer.close()
            # check EOF? No as expected check on close
            size = self.r3(3)
            index = self.r3(3)
            if index >= size:
                raise ValueError('bad index count')

            buffer = BytesIO()
            for i in range(0, 256):
                used = self.r3(3)    # symbols used
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
            out = self.digestRead()
        return out

    def digestWrite(self, data):
        self.digest.update(data)
        self.buffer.write(data)

    def write(self, data):
        blockSize = self.context['blockSize']
        if self.reader:
            raise TypeError('file type is rb')
        if isinstance(data, bytes):
            # process writing
            self.count += 1
            self.digestWrite(data)
            while self.buffer.tell() > blockSize or self.ended:
                todo = self.buffer.getvalue()
                self.buffer.close()
                self.buffer = BytesIO(todo[blockSize:])
                todo = todo[:blockSize]
                count = counts[todo]
                self.setMessage('Transforming')
                index, trans = bwt(todo, self.context)
                size = len(todo)

                self.w3(size, 3)

                # BWT index
                self.w3(index, 3)
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
                    self.w3(len(packet), 3)    # store symbols used
                    packet = swivel(packet) # transform into slow/medium/fast
                    for j in packet:
                        # write each partition
                        self.file.write(j)  # doesn't need binary convert

        else:
            raise TypeError('write only writes bytes')

    def readUTF(self):
        """maybe an archive needs filenames"""
        length = self.r3Atop(8)
        return self.read(length).decode()

    def writeUTF(self, string):
        """maybe an archive needs filenames"""
        self.w3Atop(len(string), 8)
        self.write(string.encode())

    def close(self):
        digest = self.digest.digest()
        if not self.reader:
            self.ended = True
            self.write(b'') # write the last
            self.w3(SIGN_INDEX, 1)   # version tag
            self.w3(len(digest), 3)
            self.file.write(digest)
        else:
            version = self.r3(1)
            if version <= SIGN_INDEX:
                self.maybePrint('signature digest version ' + SIGN_VERSIONS[version])
                digestFile = self.file.read(self.r3(3))
                if self.file.tell() != self.size:
                    ValueError('file length inncorrect')
                if digestFile != digest:
                    ValueError('bad digest checksum')
            else:
                ValueError('unsupported digest version')
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
        if self.reader:
            size = 10000 / size # as expansion
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
import glob

def makeContext(args):
    context = {}
    if args.quiet:
        context['verbose'] = False  # quiet
    if args.fast:
        context['compresslevel'] = 0
    if args.best:
        context['compresslevel'] = 9
    if args.level:
        context['compresslevel'] = args.level
    if args.raw:
        context['gzip'] = False
    return context

def decompress(args):
    """decompress a directory structure"""
    with blwz(args.ARCHIVE, 'rb', makeContext(args)) as input:
        count = input.r3Atop(8)
        for f in range(0, count):
            file = input.readUTF()
            size = input.r3Atop(8)
            input.maybePrint(file, True)
            with open(file, 'wb') as out:
                out.write(input.read(size)) # still inefficient but ...
            input.setMessage('Expanded to')

def compress(args):
    """compress a directory structure"""
    # TODO: context
    if isfile(args.ARCHIVE):
        ValueError('archive already exists')
    directory = args.compress   # already a directory
    if directory[-1] == '/':
        directory = directory[0:-1] # remove slash
    files = glob.glob(directory + '/**/*', recursive=True)
    with blwz(args.ARCHIVE, 'wb', makeContext(args)) as out:
        out.w3Atop(len(files), 8)
        for file in files:
            prefix = len(directory) + 1
            file = file[prefix:] # make local
            out.writeUTF(file)
            size = os.stat(file).st_size
            out.w3Atop(size, 8)  # 64 bit
            out.maybePrint(file, True)
            with open(file, 'rb') as input:
                out.write(input.read(size))
            out.setMessage('Compressed to')

# main
VERSION = VERSIONS[VERSION_INDEX]   # version of codec
SIGN_VERSION = SIGN_VERSIONS[SIGN_INDEX]    # signature version
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
    parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s ' + VERSION + '/' + SIGN_VERSION)
    parser.add_argument('-f', '--fast', action = 'store_true', help = 'fastest compression')
    parser.add_argument('-b', '--best', action = 'store_true', help = 'best compression')
    parser.add_argument('-l', '--level', help = 'compression level', type = int, choices = range(0, 10))
    parser.add_argument('-c', '--compress', help = 'compress directory')
    parser.add_argument('-q', '--quiet', action = 'store_true', help = 'no print of running status')
    parser.add_argument('-r', '--raw', action = 'store_true', help = 'don\'t gzip after')
    parser.add_argument('ARCHIVE', help = 'archive file name')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = HELP)
    parser.set_defaults(func = resolve)
    main(parser)
    args = parser.parse_args()
    args.func(args)
