from simple_injection.service_collection import ServiceResolutionError
import pytest
from tests.classes import A, B, C
from simple_injection import ServiceCollection


class D:
    def __init__(self, b: B):
        self._b = b


def test_resolution_error():
    collection = ServiceCollection()
    collection.add_transient(B)

    with pytest.raises(ServiceResolutionError):
        collection.resolve(B)


def test_nested_resolution_error():
    collection = ServiceCollection()
    collection.add_transient(D)
    collection.add_transient(B)

    with pytest.raises(ServiceResolutionError):
        collection.resolve(D)
