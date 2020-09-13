from simple_injection.service_collection import ServiceCollection
from tests.classes import A, B, C


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
