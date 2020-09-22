# Simple-Injection with Flask

Using Simple Injection with Flask is very easy and does not require any additional dependencies to use. 

Here is a simple approach that doesn't require any changes to existing code. Here we inject the instances in a `create_app` function.
```python
from flask import Flask
from flask.json import jsonify
from simple_injection import ServiceCollection


class IDatabaseService:
    def run_query(self, query):
        raise NotImplementedError()


class DatabaseService(IDatabaseService):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def run_query(self, query, *params):
        return "Query ran!"


class IUserRepository:
    def get_by_id(self, id: int):
        raise NotImplementedError()


class UserRepository(IUserRepository):
    def __init__(self, db_service: IDatabaseService):
        self._db_serive = db_service

    def get_by_id(self, id: int):
        query = "SELECT * FROM users WHERE id = ?"
        result = self._db_serive.run_query(query, id)
        return {"name": "test name", "id": id}


def create_app(user_repo: IUserRepository) -> Flask:
    app = Flask(__name__)

    @app.route("/<int:id>")
    def index(id):
        result = user_repo.get_by_id(id)
        return jsonify(result)

    return app


def configure_services():
    collection = ServiceCollection()
    collection.add_transient(
        IDatabaseService, DatabaseService, args=["my connection string"]
    )
    collection.add_transient(IUserRepository, UserRepository)
    return collection


if __name__ == "__main__":
    collection = configure_services()
    app = collection.call_function(create_app)
    app.run()
```

The issue with this approach, however, is that the instances created will never be recycled by the application. Since the instances will all be created when the `call_function` method is run, these instances will stay alive for the lifetime of the application.

Often, we would prefer a new instance would be created each time we receive a new request to our server. 

This is where the below approach comes in. The advantage to this approach being that transient instances are created and deleted for each request (singletons will not be deleted). However, in order to achieve this we resolve our dependencies from the collection we create when starting the application. This works well, but unfortunately requires Simple-Injection specific code in each of the API endpoints.

``` python
from flask import Flask
from flask.json import jsonify
from simple_injection import ServiceCollection


class IDatabaseService:
    def run_query(self, query):
        raise NotImplementedError()


class DatabaseService(IDatabaseService):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def run_query(self, query, *params):
        return "Query ran!"


class IUserRepository:
    def get_by_id(self, id: int):
        raise NotImplementedError()


class UserRepository(IUserRepository):
    def __init__(self, db_service: IDatabaseService):
        self._db_serive = db_service

    def get_by_id(self, id: int):
        query = "SELECT * FROM users WHERE id = ?"
        result = self._db_serive.run_query(query, id)
        return {"name": "test name", "id": id}


app = Flask(__name__)
collection: ServiceCollection = None


@app.route("/<int:id>")
def index(id):
    user_repo = collection.resolve(IUserRepository)
    result = user_repo.get_by_id(id)
    return jsonify(result)


def configure_services():
    collection = ServiceCollection()
    collection.add_transient(
        IDatabaseService, DatabaseService, args=["my connection string"]
    )
    collection.add_transient(IUserRepository, UserRepository)
    return collection


if __name__ == "__main__":
    collection = configure_services()
    app.run()

```