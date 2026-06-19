from setuptools import Extension, setup

setup(
    name="mymodule_basic",
    version="1.0",
    ext_modules=[
        Extension("mymodule", sources=["mymodule.c"]),
    ],
)
