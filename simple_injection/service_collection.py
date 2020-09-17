from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

T = TypeVar("T")


class ServiceLifetime(Enum):
    """Service lifetimes. There are currently 3 different service lifetimes.

    TRANSIENT: A new instance will be created every time the service is requested.
    SINGLETON: The same instance is used across all requests. Instance is created
        the first time the service is requested.
    INSTANCE: The provided instance will be used for all requests.
    """

    TRANSIENT = auto()
    SINGLETON = auto()
    INSTANCE = auto()


class ServiceResolverFlags(Enum):
    """Flag to use when using args when adding a service.

    REQUIRED_SERVICE: Use this flag in the args
        and when resolving the service, it will look up the service in the service
        collection where the flag was used.

    Example:
        class Service:
            pass

        class Example:
            def __init__(self, i: int, service: Service):
                self._i = i
                self._service = service

        collection = ServiceCollection()
        collection.add_transient(Service)

        # This would be the same as Example(1, Service())
        collection.add_transient(Example, args=[1, ServiceResolverFlag.REQUIRED_SERVICE])
    """

    REQUIRED_SERVICE = auto()


class _ContainerService:
    def __init__(
        self,
        service_implementation: Union[Type[T], T],
        service_lifetime: ServiceLifetime,
        args: Optional[List[Any]] = None,
    ):
        self.service_implementation = service_implementation
        self.service_lifetime = service_lifetime
        self.args = args
        self.singleton_instance: T = None
        self.multiple_implementations: bool = False
        self.implementations: List[Union[Type[T], T]] = list()


class ServiceCollection:
    def __init__(self):
        self._service_collection: Dict[Type[T], _ContainerService] = dict()

    def add(
        self,
        service_to_add: Type[T],
        service_implementation: Union[T, Type[T]],
        service_lifetime: ServiceLifetime,
        args: Optional[List[Any]] = None,
    ) -> None:
        """Add a service to the service collection.

        If adding a service that has already been added. The new service will
            override the old service. It will also keep track of the old and new
            service/s so they can all injected when requesting a List[ServiceType]
            from the ServiceCollection.

        Args:
            service_to_add (Type[T]): Service to add to the collection.
            service_implementation (Union[T, Type[T]]): Implementation of the service.
                Can either be a class or an instance of a class. If is an instance, then
                service lifetime must be set to ServiceLifetime.INSTANCE.
            service_lifetime (ServiceLifetime): The lifetime policy for the service.
            args (List[Any], optional): Args to be passed to the class when
                instanciating. If None, the args will be deduced by the service collection.
                Will be used when service_lifetime is not ServiceLifetime.INSTANCE.
                Defaults to None.
        """
        if service_implementation is None:
            service_implementation = service_to_add

        if service_to_add in self._service_collection.keys():
            if not List[service_to_add] in self._service_collection.keys():
                self._create_list_service(service_to_add)
            self.add(
                service_implementation, service_implementation, service_lifetime, args
            )
            self._service_collection[List[service_to_add]].implementations.append(
                service_implementation
            )
        self._service_collection[service_to_add] = _ContainerService(
            service_implementation, service_lifetime, args
        )

    def add_transient(
        self,
        service_to_add: Type[T],
        service_implementation: Optional[Type[T]] = None,
        args: Optional[List[Any]] = None,
    ) -> None:
        """Add a transient service to the service collection. A transient service
            will have a new instance created everytime the service is requested
            from the collection.

        If adding a service that has already been added. The new service will
            override the old service. It will also keep track of the old and new
            service/s so they can all injected when requesting a List[ServiceType]
            from the ServiceCollection.


        Args:
            service_to_add (Type[T]): Service to add to the collection.
            service_implementation (Type[T], optional): Implementation of the service.
                If None, it will use service_to_add. Deafaults None.
            args (List[Any], optional): Args to be passed to the class when
                instanciating. If None, the args will be deduced by the service collection.
                Defaults to None.
        """
        self.add(
            service_to_add, service_implementation, ServiceLifetime.TRANSIENT, args
        )

    def add_singleton(
        self,
        service_to_add: Type[T],
        service_implementation: Optional[Type[T]] = None,
        args: Optional[List[Any]] = None,
    ) -> None:
        """Add a singleton service to the service collection. A singleton service
            will share the same instance for request from the collection, and will
            be created the first time it is requested.

        If adding a service that has already been added. The new service will
            override the old service. It will also keep track of the old and new
            service/s so they can all injected when requesting a List[ServiceType]
            from the ServiceCollection.


        Args:
            service_to_add (Type[T]): Service to add to the collection.
            service_implementation (Type[T], optional): Implementation of the service.
                If None, it will use service_to_add. Deafaults None.
            args (List[Any], optional): Args to be passed to the class when
                instanciating. If None, the args will be deduced by the service collection.
                Defaults to None.
        """
        self.add(
            service_to_add, service_implementation, ServiceLifetime.SINGLETON, args
        )

    def add_instance(self, service_to_add: Type[T], instance: T) -> None:
        """Add an instance service to the service collection. The provided instance will
            be used each time the service is requested.

        If adding a service that has already been added. The new service will
            override the old service. It will also keep track of the old and new
            service/s so they can all injected when requesting a List[ServiceType]
            from the ServiceCollection.

        Args:
            service_to_add (Type[T]): Service to add to the collection.
            instance (T): Instance for the service.
        """
        self.add(service_to_add, instance, ServiceLifetime.INSTANCE)

    def call_function(self, function: Callable[[], T]) -> T:
        """Call a function resolving inputs using the service collection.

        Args:
            function (Callable): The function to call.

        Returns:
            Any: The return value from the function.
        """
        args = list()
        for name, annotation in function.__annotations__.items():
            if name != "return":
                args.append(self.resolve(annotation))
        return function(*args)

    def resolve(self, service_to_resolve: Type[T]) -> T:
        """Resolve a service declared in the container. The service must be
            declared in one of the add methods for it to be resolved.

        Args:
            service_to_resolve (Type[T]): Service to resolve.

        Returns:
            T: An instance of the resolved service.
        """
        container_service = self._service_collection[service_to_resolve]
        if container_service.multiple_implementations:
            return self._resolve_multiple(container_service)
        if container_service.service_lifetime == ServiceLifetime.INSTANCE:
            return self._resolve_instance(container_service)
        if container_service.service_lifetime == ServiceLifetime.SINGLETON:
            return self._resolve_singleton(container_service)
        return self._resolve_annotations(container_service)

    def _resolve_multiple(self, container_service: _ContainerService):
        services_to_resolve = container_service.implementations
        services = list()
        for service in services_to_resolve:
            services.append(self.resolve(service))
        return services

    def _resolve_annotations(self, container_service: _ContainerService):
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

    def _resolve_singleton(self, container_service: _ContainerService):
        if container_service.singleton_instance is None:
            container_service.singleton_instance = self._resolve_annotations(
                container_service
            )
        return container_service.singleton_instance

    def _resolve_instance(self, container_service: _ContainerService):
        return container_service.service_implementation

    def _resolve_args(self, container_service: _ContainerService):
        args = list()
        for i in range(len(container_service.args)):
            arg = container_service.args[i]
            if arg == ServiceResolverFlags.REQUIRED_SERVICE:
                required_service = container_service.service_implementation
                annotations = list(required_service.__init__.__annotations__.values())
                arg = self.resolve(annotations[i])
            args.append(arg)
        return container_service.service_implementation(*args)

    def _create_list_service(self, service_to_add):
        service = self._service_collection[service_to_add]
        self.add(
            service.service_implementation,
            service.service_implementation,
            service.service_lifetime,
            service.args,
        )
        self.add(List[service_to_add], None, None, None)
        self._service_collection[List[service_to_add]].multiple_implementations = True
        self._service_collection[List[service_to_add]].implementations.append(
            service.service_implementation
        )
