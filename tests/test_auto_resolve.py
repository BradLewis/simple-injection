from simple_injection import ServiceCollection
from tests.classes import *


def test_auto_resolve():
    collection = ServiceCollection(auto_resolve=True)
    collection.resolve(A)
    collection.resolve(B)
