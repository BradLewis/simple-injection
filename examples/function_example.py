from flask import Flask
from simple_injection import ServiceCollection


class DependencyA:
    def call(self):
        print("calling depA!")


class DependencyB:
    def __init__(self, depA: DependencyA):
        self.depA = depA
        print(f"Creating {self.__class__.__name__}")

    def call(self):
        self.depA.call()


def create_app(depA: DependencyA, depB: DependencyB) -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        depB.call()
        return "Testing!"

    return app


if __name__ == "__main__":
    collection = ServiceCollection()
    collection.add_transient(DependencyB)
    collection.add_transient(DependencyA)

    app = collection.run_function(create_app)
    app.run()