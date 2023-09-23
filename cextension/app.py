
"""
Process of loading and calling of C extension functions:
1. When import the extension moduel, Python interpreter will find the .so of the module, load it into the
    interpreter process. In the load time, PyInit_myModule will be called to initialize the moduel, which
    might include add the namesapce of the module into current interpreter execution environment. After 
    initialization, the namespace of the module is visible to interpreter
2. Extension module and functions inside these module is similar to other modules and funtions written in
    Python:
        a. They are both PyObject
        b. The both participate name resolution
        c. For the functions and methods, they are both executed inside the CALL_FUNTION or CALL_METHOD 
            Python byte code instructions
    The differences are:
        a. Extension functions are built-in functions, they can not be disassemlied into Python byte code
        b. When doing name resolution, built-in funtions are looked after normal Python functions
        c. When called inside CALL_FUNCTION or CALL_METHOD, not like other Python functions, which might
            involve create new frames and load function code objects and execute byte code inside this 
            normal Python function, extension functions are C functions, they are called directly inside 
            the CALL_FUNCTION and CALL_METHOD's C implementation of the interpreter. Possible implementation
            could be that the PyObject of extension functions have a flag telling the CALL_FUNCTION or
            CALL_METHOD instruction implementation that it's C extension with a function pointer, then this
            C funtion will be called directly

"""

from myModule import *
import myModule
import dis


def fib(num):
    return 10


def f(num):
    # if fib not defined above, myModule.fib will be resoved and called
    return fib(num)


def g():
    return 'hello'


b = myModule.fib


print(f(10))

# <class 'builtin_function_or_method'>
# ! Note that this is very different from C functions in ctypes, which is of <class 'ctypes.CDLL.__init__.<locals>._FuncPtr'>
print(type(myModule.fib))

# TypeError: don't know how to disassemble builtin_function_or_method objects
print(dis.dis(b))
