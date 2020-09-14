import setuptools

setuptools.setup(
    name="simple-injection",
    version="0.2.0",
    description="A simple library for typing-based dependency injection",
    author="Bradley Lewis",
    license="MIT",
    url="https://github.com/BradLewis/simple-injection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
