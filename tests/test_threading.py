import threading

from tests.classes import A, B, C
from simple_injection import ServiceCollection


def resolve(collection, cls, instances):
    instances[cls] = collection.resolve(cls)


def test_singletons():
    collection = ServiceCollection()
    collection.add_singleton(A)
    collection.add_singleton(B)
    collection.add_transient(C)

    thread_list = list()

    instances = dict()
    thread_list.append(
        threading.Thread(target=resolve, args=[collection, A, instances])
    )
    thread_list.append(
        threading.Thread(target=resolve, args=[collection, B, instances])
    )
    thread_list.append(
        threading.Thread(target=resolve, args=[collection, C, instances])
    )

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    a = instances[A]
    b = instances[B]
    c = instances[C]
    assert a == b.a
    assert b.a == c.b.a
