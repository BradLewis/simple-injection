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
        result = self._db_service.run_query(query, id)
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
