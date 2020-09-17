import setuptools


def get_long_description():
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="simple-injection",
    version="0.2.3",
    description="A simple library for typing-based dependency injection",
    long_description_content_type="text/markdown",
    long_description=get_long_description(),
    author="Bradley Lewis",
    license="MIT",
    url="https://github.com/BradLewis/simple-injection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
