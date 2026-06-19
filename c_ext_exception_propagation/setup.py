from setuptools import Extension, setup

setup(
    name="spam_errors",
    version="1.0",
    ext_modules=[
        Extension("spam_errors", sources=["spam_errors.c"]),
    ],
)
