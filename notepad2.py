# import logging
#
#
# def log_sth():
#     logger2 = logging.getLogger("mylogger")
#     logger2.debug("something happend")
#
#
# log_sth()

import collections

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):

        self._cards = [Card(suit, rank)
                       for suit in self.suits for rank in self.rank]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


# import dis
#
# a = 1
# b = 2
# c = None
# # dis.dis("c = a + b")
#
# import array
#
# a = array.array("h", [1,2,3,4])
# b = memoryview(a)
# print(len(b))
# print(type(a))
#
#
# print(b)
#

# import builtins
# import struct
#
# fmt = "<3s3sHH"
# with open("joy.jpeg", "rb") as fp:
#     img = memoryview(fp.read())
#
# print(img)
# print(img[:10])
# print(bytes(img[:10]))
#
# b = struct.unpack(fmt, img[:10])
# print(b)
#


# def my_func(a, b, **kwargs):
#     print(a, b)
#     print(kwargs)
#     return a + b
#
#
# import inspect
#
#
# sig = inspect.signature(my_func)
#
# param = {"b": 3, "dfd": 123, "ene": 456}
# bound = sig.bind(**param)
# print(bound)


import ctypes


a = 1234

class IntStruct(ctypes.Structure):
    _fields_ = [("ob_refcnt", ctypes.c_long),
                ("ob_type", ctypes.c_void_p),
                ("ob_size", ctypes.c_ulong),
                ("ob_digit", ctypes.c_long)]

    def __repr__(self):
        return ("IntStruct(ob_digit={self.ob_digit}, "
                "refcount={self.ob_refcnt})").format(self=self)


class ListStruct(ctypes.Structure):
    _fields_ = [("ob_refcnt", ctypes.c_long),
                ("ob_type", ctypes.c_void_p),
                ("ob_size", ctypes.c_ulong),
                ("ob_item", ctypes.c_long),
                ("allocated", ctypes.c_ulong)]

    def __repr__(self):
        return ("ListStruct(len={}, refcount={})".format(self.ob_size,
                                                         self.ob_refcnt))

L = [1,2,3,4,5]
Lstruct = ListStruct.from_address(id(L))
PtrArray = Lstruct.ob_size * ctypes.POINTER(IntStruct)
L_values = PtrArray.from_address(Lstruct.ob_item)
a = [ptr for ptr in L_values]
print(a)
#


class NumpyStruct(ctypes.Structure):
    _fields_ = [("ob_refcnt", ctypes.c_long),
                ("ob_type", ctypes.c_void_p),
                ("ob_data", ctypes.c_long),
                ("ob_ndim", ctypes.c_int),
                ("ob_shape", ctypes.c_void_p),
                ("ob_strides", ctypes.c_void_p)]

    @property
    def shape(self):
        return tuple(
            (self.ob_ndim * ctypes.c_int64).from_address(self.ob_shape))

    @property
    def strides(self):
        return tuple(
            (self.ob_ndim * ctypes.c_int64).from_address(self.ob_strides))

    def __repr__(self):
        return ("ListStruct(len={}, refcount={})".format(self.shape,
                                                         self.ob_refcnt))

import numpy as np

# x = np.array([1,2,3,4,5])
# x = np.random.random((10, 20))
x = np.arange(10)
x_struct = NumpyStruct.from_address(id(x))
arraytype = np.prod(x_struct.shape) * ctypes.c_long
arraytype = np.prod(x_struct.shape) * ctypes.POINTER(NumpyStruct)
data = arraytype.from_address(x_struct.ob_data)
a = [d for d in data]
print(a)


a = 1
b = 1

c = (a == b)
print(c)








