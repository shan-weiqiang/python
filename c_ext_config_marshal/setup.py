from setuptools import Extension, setup

setup(
    name="mymodule_marshal",
    version="1.0",
    ext_modules=[
        Extension("mymodule", sources=["mymodule.c"]),
    ],
)
