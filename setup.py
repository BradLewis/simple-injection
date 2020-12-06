from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
from glob import glob

__version__ = "0.3.0"

ext_modules = [
    Pybind11Extension(
        "simple_injection",
        sorted(glob("src/*.cpp")),  # Sort source files for reproducibility
    ),
]


def get_long_description():
    with open("README.md") as f:
        return f.read()


setup(
    name="simple-injection",
    version=__version__,
    description="A simple library for typing-based dependency injection",
    long_description_content_type="text/markdown",
    long_description=get_long_description(),
    author="Bradley Lewis",
    license="MIT",
    url="https://github.com/BradLewis/simple-injection",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
)
