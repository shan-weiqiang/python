from setuptools import setup

setup(
    name="add_cffi",
    version="1.0",
    cffi_modules=["add_build.py:ffibuilder"],
    setup_requires=["cffi>=1.0.0"],
    install_requires=["cffi>=1.0.0"],
)
