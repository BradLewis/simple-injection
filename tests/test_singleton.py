from simple_injection import ServiceCollection, ServiceResolverFlags
from tests.classes import *


def test_with_args():
    collection = ServiceCollection()
    collection.add_singleton(NoTyping, args=["a", "b"])
    collection.add_transient(
        SomeTyping, args=[ServiceResolverFlags.REQUIRED_SERVICE, "b"]
    )

    some_typing = collection.resolve(SomeTyping)
    no_typing = collection.resolve(NoTyping)
    assert some_typing._no_typing == no_typing


def test_basic_singleton():
    collection = ServiceCollection()
    collection.add_singleton(A)
    collection.add_transient(B)
    collection.add_transient(C)

    b = collection.resolve(B)
    c = collection.resolve(C)
    a = collection.resolve(A)

    assert b != c.b
    assert b.a == c.a
    assert b.a == c.b.a
    assert a == b.a


def test_subclass():
    collection = ServiceCollection()
    collection.add_transient(C)
    collection.add_singleton(B)
    collection.add_transient(A)
    collection.add_singleton(ParentClass, SubClass)
    collection.add_transient(UsesSubClass)

    usc = collection.resolve(UsesSubClass)
    pc = collection.resolve(ParentClass)

    assert isinstance(usc._pc, SubClass)
    assert usc._pc == pc


def test_multiple():
    collection = ServiceCollection()
    collection.add_singleton(Base, Impl1)
    collection.add_singleton(Base, Impl2)
    collection.add_transient(UsesMultiple)

    um1 = collection.resolve(UsesMultiple)
    um2 = collection.resolve(UsesMultiple)
    assert len(um1._multiple) == 2
    assert len(um2._multiple) == 2
    assert um1._multiple[0] == um2._multiple[0]
    assert um1._multiple[1] == um2._multiple[1]


def test_service_override():
    collection = ServiceCollection()
    collection.add_singleton(Base, Impl1)
    collection.add_singleton(Base, Impl2)
    collection.add_transient(UsesBase)

    ub = collection.resolve(UsesBase)
    base = collection.resolve(Base)
    assert isinstance(ub._base, Impl2)
    assert ub._base == base
