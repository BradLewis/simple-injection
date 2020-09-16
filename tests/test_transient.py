from simple_injection import ServiceCollection, ServiceResolverFlags
from tests.classes import *


def test_all_transient():
    collection = ServiceCollection()
    collection.add_transient(A)
    collection.add_transient(B)
    collection.add_transient(C)

    a = collection.resolve(A)
    b = collection.resolve(B)
    c = collection.resolve(C)

    assert a != b.a
    assert b != c.b
    assert a != c.b.a


def test_with_args():
    collection = ServiceCollection()
    collection.add_transient(NoTyping, args=["a", "b"])
    collection.add_transient(
        SomeTyping, args=[ServiceResolverFlags.REQUIRED_SERVICE, "b"]
    )

    some_typing = collection.resolve(SomeTyping)
    no_typing = collection.resolve(NoTyping)
    assert some_typing._no_typing != no_typing


def test_subclass():
    collection = ServiceCollection()
    collection.add_transient(C)
    collection.add_transient(B)
    collection.add_transient(A)
    collection.add_transient(ParentClass, SubClass)
    collection.add_transient(UsesSubClass)

    usc = collection.resolve(UsesSubClass)
    pc = collection.resolve(ParentClass)

    assert isinstance(usc._pc, SubClass)
    assert usc._pc != pc


def test_multiple():
    collection = ServiceCollection()
    collection.add_transient(Base, Impl1)
    collection.add_transient(Base, Impl2)
    collection.add_transient(UsesMultiple)

    um = collection.resolve(UsesMultiple)
    assert len(um._multiple) == 2
    assert isinstance(um._multiple[0], Impl1)
    assert isinstance(um._multiple[1], Impl2)


def test_service_override():
    collection = ServiceCollection()
    collection.add_transient(Base, Impl1)
    collection.add_transient(Base, Impl2)
    collection.add_transient(UsesBase)

    ub = collection.resolve(UsesBase)
    assert isinstance(ub._base, Impl2)
