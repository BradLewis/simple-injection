#!/bin/bash

python setup.py clean --all bdist_wheel
pip install --force-reinstall dist/simple_injection_cpp-0.3.0-cp39-cp39-linux_x86_64.whl