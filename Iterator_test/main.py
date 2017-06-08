#!/usr/bin/env python2.7

from collections import Iterable,Iterator

class Iterator_Test():
    def __init__(self):
        self.data = 1
    def __iter__(self):
        return self
    def next(self):
        if self.data > 15:
            raise StopIteration
        self.data += 4
        return self.data

t = Iterator_Test()

print isinstance(t, Iterable)

print isinstance(t, Iterator)

print next(t)

print next(t)

print next(t)

print next(t)

#next(t)

