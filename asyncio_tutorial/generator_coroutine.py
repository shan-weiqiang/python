"""
Native coroutines in Python are based in Generators. However they have key differences:
1. Native coroutines use asyc keyword to define a native coroutine function. While any 
    function that contains yield/yield from keywords are generators
2. Inside native coroutines, if there is yield keyword, it makes the function a asynchrous
    generator, which itself is not awaitable anymore. So if one wants to make async function
    awaitable, do not use yield inside it
3. One can use @types.coroutine decorator to make a generator awaitable, this create a
    generator-based coroutine
4. Another way to make a object awaitable is to implement __await__() method, this method
    can be a generator
"""

import types
import asyncio


# generator
def say_12():
    print(1)
    yield
    print(2)


# generator with yield from
def say_1234():
    print(3)
    yield from say_12()
    print(4)


# generator-based coroutine
@types.coroutine
def cor_say_1234():
    yield from say_1234()


# normal native coroutine
async def say_hello():
    print("hello")


async def nat_say_12345():
    # gather returns a future, it must be waited, otherwise after nat_say_12345 goes
    # out of scope, all async function gathered inside this future is cancelled
    await asyncio.gather(cor_say_1234(), say_hello())
    print(5)


asyncio.run(nat_say_12345())
