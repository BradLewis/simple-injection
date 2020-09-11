from enum import Enum, auto


class ServiceLifetime(Enum):
    TRANSIENT = auto()
    SINGLETON = auto()
    INSTANCE = auto()


class ContainerService:
    def __init__(self, service_implementation, service_lifetime, args=None):
        self.service_implementation = service_implementation
        self.service_lifetime = service_lifetime
        self.args = args
        self.instance = None


class ServiceCollection:
    def __init__(self):
        self._service_collection = dict()

    def add(self, service_to_add, service_implementation, service_lifetime, args=None):
        if service_implementation is None:
            service_implementation = service_to_add

        self._service_collection[service_to_add.__name__] = ContainerService(
            service_implementation, service_lifetime, args
        )

    def add_transient(self, service_to_add, service_implementation=None, args=None):
        self.add(service_to_add, service_implementation, ServiceLifetime.TRANSIENT, args)

    def resolve(self, service_to_resolve):
        container_service = self._service_collection[service_to_resolve.__name__]
        if container_service.args:
            return container_service.service_implementation(*container_service.args)
        annotations = container_service.__init__.__annotations__
        services_to_use = list()
        for annotation in annotations.values():
            services_to_use.append(self.resolve(annotation))
        return container_service.service_implementation(*services_to_use)
