from enum import Enum, auto
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

T = TypeVar("T")


class ServiceLifetime(Enum):
    TRANSIENT = auto()
    SINGLETON = auto()
    INSTANCE = auto()


class ContainerService:
    def __init__(
        self,
        service_implementation: Union[Type[T], T],
        service_lifetime: ServiceLifetime,
        args: Optional[List[Any]] = None,
    ):
        self.service_implementation = service_implementation
        self.service_lifetime = service_lifetime
        self.args = args
        self.instance: T = None


class ServiceCollection:
    def __init__(self):
        self._service_collection: Dict[str, ContainerService] = dict()

    def add(
        self,
        service_to_add: Type[T],
        service_implementation: Union[T, Type[T]],
        service_lifetime: ServiceLifetime,
        args: Optional[List[Any]] = None,
    ):
        if service_implementation is None:
            service_implementation = service_to_add

        self._service_collection[service_to_add.__name__] = ContainerService(
            service_implementation, service_lifetime, args
        )

    def add_transient(
        self,
        service_to_add: Type[T],
        service_implementation: Optional[Type[T]] = None,
        args: Optional[List[Any]] = None,
    ):
        self.add(
            service_to_add, service_implementation, ServiceLifetime.TRANSIENT, args
        )

    def resolve(self, service_to_resolve: Type[T]):
        container_service = self._service_collection[service_to_resolve.__name__]
        if container_service.args:
            return container_service.service_implementation(*container_service.args)
        return self._resolve_transient(container_service)

    def _resolve_transient(self, container_service: ContainerService):
        annotations = container_service.__init__.__annotations__
        services_to_use = list()
        for annotation in annotations.values():
            services_to_use.append(self.resolve(annotation))
        return container_service.service_implementation(*services_to_use)
