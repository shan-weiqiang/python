import ctypes
import dis


def f():
    print('Hello World')


def g():
    addfunc = ctypes.CDLL('clib/libadd.so')
    addfunc.add.argtypes = [ctypes.c_int, ctypes.c_int]
    addfunc.add(2, 3)


print(dis.dis(f))

print(dis.dis(g))
