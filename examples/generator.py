import random as rand


def create_class(f, i):
    args = list()
    names = list()
    num_ints = rand.randint(0, min(i, 10))
    used = list()
    for j in range(num_ints):
        to_use = rand.randint(0, i - 1)
        if to_use not in used:
            used.append(to_use)
            args.append(f"dep{to_use}: Dep{to_use}")
            names.append(f"dep{to_use}")

    f.write(f"class Dep{i}:\n")
    f.write(f"\tdef __init__(self, {', '.join(args)}):\n")
    f.write("\t\tprint(f'Creating {self.__class__.__name__}')\n")
    for name in names:
        f.write(f"\t\tself._{name} = {name}\n")


def gen_classes():
    with open("test.py", "w") as f:
        for i in range(100):
            create_class(f, i)


def gen_timer_tree():
    with open("timer.py", "w") as f:
        f.write("from simple_injection import ServiceCollection\n")
        f.write("from test import *\n\n")
        f.write("collection = ServiceCollection()\n")

        for i in range(100):
            if rand.uniform(0, 1) < 0.2:
                f.write(f"collection.add_singleton(Dep{i})\n")
            else:
                f.write(f"collection.add_transient(Dep{i})\n")


gen_classes()
