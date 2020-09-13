from simple_injection import ServiceCollection, ServiceResolverFlags
from tests.classes import SomeTyping, NoTyping, A, B, C


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
