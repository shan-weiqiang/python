from setuptools import Extension, setup

setup(
    name="refcount_demo",
    version="1.0",
    ext_modules=[
        Extension("refcount_demo", sources=["refcount_demo.c"]),
    ],
)
