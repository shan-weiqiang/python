import ctypes
import dis

"""
ctypes itself is a C extension module. Even though both extension and ctypes can load .so and
execute C functions, they are essentially different:
1. C extension is Python module(ctypes itself), which means that the functions are laoded directly
    by Python interpreter and added into runtime environment namespace
2. ctypes itself is C extension, inside ctypes, it loads .so and also loads libffi to interact with it
    before calling the user functions, it has to do data marshalling and prepare for the calling conventions
    using libffi. This is also the work for values returned from the C function
3. Simply put: ctypes is a normal C extension that manipulates other C .so 
"""

def f():
    print('Hello World')


def g():
    addfunc = ctypes.CDLL('clib/libadd.so')
    addfunc.add.argtypes = [ctypes.c_int, ctypes.c_int]
    addfunc.add(2, 3)
    print("disassemply of addfunc.add: ")
    f=addfunc.add
    # <class 'ctypes.CDLL.__init__.<locals>._FuncPtr'>
    # Note this is different from C extension functions, which is <class 'builtin_function_or_method'>
    print(type(f))
    print(dir(f))
    print(dis.dis(f))
    # TypeError: don't know how to disassemble method-wrapper objects
    print(dis.dis(f.__call__))


print(dis.dis(f))

print(dis.dis(g))
g()
