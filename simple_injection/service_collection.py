from _simple_injection import _ServiceCollection, ServiceLifetime
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

T = TypeVar("T")


class ServiceCollection:
    def __init__(self):
        self._collection = _ServiceCollection()

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
        self._collection.add(
            id(service_to_add), service_implementation, service_lifetime
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
        self.add(service_to_add, service_implementation, ServiceLifetime.TRANSIENT)

    def resolve(self, service_to_resolve: Type[T]) -> T:
        """Resolve a service declared in the container. The service must be
            declared in one of the add methods for it to be resolved.

        Args:
            service_to_resolve (Type[T]): Service to resolve.

        Returns:
            T: An instance of the resolved service.
        """
        return self._collection.resolve(id(service_to_resolve))