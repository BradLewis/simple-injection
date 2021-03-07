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


def test_multiple():
    collection = ServiceCollection()
    impl1 = Impl1()
    impl2 = Impl2()
    collection.add_instance(Base, impl1)
    collection.add_instance(Base, impl2)
    collection.add_transient(UsesMultiple)

    um = collection.resolve(UsesMultiple)
    assert len(um._multiple) == 2
    assert um._multiple[0] == impl1
    assert um._multiple[1] == impl2


def test_service_override():
    collection = ServiceCollection()
    collection.add_instance(Base, Impl1())
    impl2 = Impl2()
    collection.add_instance(Base, impl2)
    collection.add_transient(UsesBase)

    ub = collection.resolve(UsesBase)
    assert isinstance(ub._base, Impl2)
    assert ub._base == impl2
