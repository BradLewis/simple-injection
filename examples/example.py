class A:
    def __init__(self):
        print("created a")


class B:
    def __init__(self, a: A):
        self.a = a
        print("created b")


class C:
    def __init__(self, a: A, b: B):
        self.a = a
        self.b = b
        print("created c")


from simple_injection import ServiceCollection

collection = ServiceCollection()
collection.add_transient(A)
collection.add_transient(C)
collection.add_transient(B)

c = collection.resolve(C)

collection2 = ServiceCollection()
collection2.add_singleton(A)
collection2.add_singleton(C)
collection2.add_singleton(B)

c = collection2.resolve(C)

collection3 = ServiceCollection()
b = B(1)
collection3.add_transient(A)
collection3.add_transient(C)
collection3.add_instance(B, b)

c = collection3.resolve(C)
