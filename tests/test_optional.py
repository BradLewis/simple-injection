from simple_injection import ServiceCollection
from typing import Optional
from tests.classes import A, B, C


class HasOptional:
    def __init__(self, a: A, b: Optional[B] = None):
        self._a = a
        self._b = b


class HasOptionalWithDeps:
    def __init__(self, a: A, c: Optional[C] = None):
        self._a = a
        self._c = c


def test_optional_declared():
    collection = ServiceCollection()
    collection.add_transient(A)
    collection.add_transient(B)
    collection.add_transient(HasOptional)

    has_optional = collection.resolve(HasOptional)
    assert isinstance(has_optional._a, A)
    assert isinstance(has_optional._b, B)


def test_optional_not_declared():
    collection = ServiceCollection()
    collection.add_transient(A)
    collection.add_transient(HasOptional)

    has_optional = collection.resolve(HasOptional)
    assert isinstance(has_optional._a, A)
    assert has_optional._b is None


def test_optional_with_dependencies():
    collection = ServiceCollection()
    collection.add_transient(A)
    collection.add_transient(B)
    collection.add_transient(C)
    collection.add_transient(HasOptionalWithDeps)

    has_optional_with_deps = collection.resolve(HasOptionalWithDeps)
    assert isinstance(has_optional_with_deps._a, A)
    assert isinstance(has_optional_with_deps._c, C)
