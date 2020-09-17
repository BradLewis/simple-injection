# Simple Injection

[![Build Status](https://travis-ci.com/BradLewis/simple-injection.svg?branch=master)](https://travis-ci.com/BradLewis/simple-injection) [![codecov](https://codecov.io/gh/BradLewis/simple-injection/branch/master/graph/badge.svg)](https://codecov.io/gh/BradLewis/simple-injection) [![Documentation Status](https://readthedocs.org/projects/simple-injection/badge/?version=latest)](https://simple-injection.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/simple-injection.svg)](https://pypi.python.org/pypi/simple-injection/) [![PyPI license](https://img.shields.io/pypi/l/simple-injection.svg)](https://pypi.python.org/pypi/simple-injection/)


## Introduction

Simple Injection is a simple, objected-oriented approach to dependency injection in python.
The goal of Simple Injection is to allow simple and effective dependency injection in python applications without the use of anything other than what is natively in your application. This means no decorators or anything else anywhere in your code is required for Simple Injection. All that is required is python typings.

## Features

* Only dependent on native python code and typings. Services are injected through typing annotations, rather than variable names or decorators in your code.
* Easily define service lifetimes.
* Enforces typings in your application.
* Bind abstract services to their implementations.
* Add services in any order, resolution occurs when a service is request.

## Installation

Simply install Simple Injection through  [pip](https://pip.pypa.io/en/stable/).

```bash
pip install simple-injection
```

## Usage

Due to Simple Injection relying only on typings, it is easy to add to your application.

```python
from simple_injection import ServiceCollection


class Dependency:
    def hello(self):
        print("Hello from Dependency!")

class Service:
    def __init__(self, dependency: Dependency):
        self._dependency = dependency

    def hello(self):
        self._dependency.hello()

collection = ServiceCollection()
collection.add_transient(Dependency)
collection.add_transient(Service)

collection.resolve(Service).hello()
# Outputs: Hello from Dependency!
```

This approach to dependency injection makes it easy to use mocks when developing and unit testing.

```python
class MockDependency:
    def hello(self):
        print("Hello from MockDependency!")

collection = ServiceCollection()
collection.add_transient(Dependency, MockDependency)
collection.add_transient(Service)

collection.resolve(Service).hello()
# Outputs: Hello from MockDependency!
```

This can also be achieved through the use of an interface (or base class) that both the dependency and the mock inherit from, but as the above example shows, it is not required.

Simple Injection will also allow you to simply inject strings and other constants to your dependencies, easily injecting the needed dependency to your class with the constant.

```python
from simple_injection import ServiceCollection, ServiceResolverFlags


class Dependency:
    def __init__(self, my_str: str):
        self.my_str = my_str

class Service:
    def __init__(self, dependency: Dependency, my_int: int):
        self.my_int
        self._dependency = dependency

    def get_str(self):
        return self._dependency.my_str

collection = ServiceCollection()
collection.add_transient(Dependency, args=["Example string!"])
collection.add_transient(Service, args=[ServiceResolverFlags.REQUIRED_SERVICE ,23])

service = collection.resolve(Service)
service.my_int # 23
service.get_str() # Example string!
```

See [examples](./examples) for more examples.

## Documentation

Documentation for Simple Injection can be found on [readthedocs](https://simple-injection.readthedocs.io/en/latest/).

## Contributing

Contributions are more than welcome. Feel welcome to add issues or make pull requests!

## License

[MIT](https://choosealicense.com/licenses/mit/)
