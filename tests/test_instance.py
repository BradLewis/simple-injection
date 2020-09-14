from simple_injection import ServiceCollection
from tests.classes import *


def test_instance():
    collection = ServiceCollection()
    collection.add_transient(C)
    collection.add_transient(B)
    a = A()
    collection.add_instance(A, a)

    b = collection.resolve(B)
    c = collection.resolve(C)

    assert a == b.a
    assert a == c.b.a


def test_subclass():
    collection = ServiceCollection()
    a = A()
    b = B(a)
    c = C(a, b)
    sc = SubClass(c, b)
    collection.add_instance(ParentClass, sc)
    collection.add_transient(UsesSubClass)

    usc = collection.resolve(UsesSubClass)
    pc = collection.resolve(ParentClass)

    assert isinstance(usc._pc, SubClass)
    assert usc._pc == pc