from tests.classes import *
from simple_injection import ServiceCollection


def my_fn(a: A, b: B):
    return "Called!"


def test_run_function():
    collection = ServiceCollection()
    collection.add_transient(A)
    collection.add_transient(B)
    assert collection.call_function(my_fn) == "Called!"
