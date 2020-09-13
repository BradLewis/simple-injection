from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

T = TypeVar("T")


class ServiceLifetime(Enum):
    TRANSIENT = auto()
    SINGLETON = auto()
    INSTANCE = auto()


class ServiceResolverFlags(Enum):
    REQUIRED_SERVICE = auto()


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
        self._service_collection: Dict[Type[T], ContainerService] = dict()

    def add(
        self,
        service_to_add: Type[T],
        service_implementation: Union[T, Type[T]],
        service_lifetime: ServiceLifetime,
        args: Optional[List[Any]] = None,
    ) -> None:
        if service_implementation is None:
            service_implementation = service_to_add

        self._service_collection[service_to_add] = ContainerService(
            service_implementation, service_lifetime, args
        )

    def add_transient(
        self,
        service_to_add: Type[T],
        service_implementation: Optional[Type[T]] = None,
        args: Optional[List[Any]] = None,
    ) -> None:
        self.add(
            service_to_add, service_implementation, ServiceLifetime.TRANSIENT, args
        )

    def add_singleton(
        self,
        service_to_add: Type[T],
        service_implementation: Optional[Type[T]] = None,
        args: Optional[List[Any]] = None,
    ) -> None:
        self.add(
            service_to_add, service_implementation, ServiceLifetime.SINGLETON, args
        )

    def add_instance(self, service_to_add: Type[T], instance: T) -> None:
        self.add(service_to_add, instance, ServiceLifetime.INSTANCE)

    def run_function(self, function: Callable) -> Any:
        args = list()
        for name, annotation in function.__annotations__.items():
            if name != "return":
                args.append(self.resolve(annotation))
        return function(*args)

    def resolve(self, service_to_resolve: Type[T]) -> T:
        container_service = self._service_collection[service_to_resolve]
        if container_service.service_lifetime == ServiceLifetime.INSTANCE:
            return self._resolve_instance(container_service)
        if container_service.service_lifetime == ServiceLifetime.SINGLETON:
            return self._resolve_singleton(container_service)
        return self._resolve_annotations(container_service)

    def _resolve_annotations(self, container_service: ContainerService):
        if container_service.args:
            return self._resolve_args(container_service)
        annotations = getattr(
            container_service.service_implementation.__init__, "__annotations__", dict()
        )
        services_to_use = list()
        for name, annotation in annotations.items():
            if name != "return":
                services_to_use.append(self.resolve(annotation))
        return container_service.service_implementation(*services_to_use)

    def _resolve_singleton(self, container_service: ContainerService):
        if container_service.instance is None:
            container_service.instance = self._resolve_annotations(container_service)
        return container_service.instance

    def _resolve_instance(self, container_service: ContainerService):
        return container_service.instance

    def _resolve_args(self, container_service: ContainerService):
        args = list()
        for i in range(len(container_service.args)):
            arg = container_service.args[i]
            if arg == ServiceResolverFlags.REQUIRED_SERVICE:
                required_service = container_service.service_implementation
                annotations = list(required_service.__init__.__annotations__.values())
                arg = self.resolve(annotations[i])
            args.append(arg)
        return container_service.service_implementation(*args)
