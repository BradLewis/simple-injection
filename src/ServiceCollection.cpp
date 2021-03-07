#include <pybind11/pybind11.h>
#include "ServiceCollection.h"
#include "ContainerService.h"
#include "ServiceLifetime.h"

py::object _ServiceCollection::Resolve(py::object service)
{
    std::cout << "here" << std::endl;

    ssize_t serviceId = py::hash(service);
    auto service_to_resolve = _serviceCollection[serviceId];

    std::cout << serviceId << std::endl;

    return service_to_resolve.Implementation();
}

void _ServiceCollection::Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, py::dict annotaitons)
{
    ssize_t serviceId = py::hash(service);
    _serviceCollection[serviceId] = ContainerService(serviceImplementation, lifetime);
    std::cout << serviceId << std::endl;
}

void _ServiceCollection::Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, py::dict annotaitons, py::list args)
{
    ssize_t serviceId = py::hash(service);
    _serviceCollection[serviceId] = ContainerService(serviceImplementation, lifetime, args);
    std::cout << serviceId << std::endl;
}

// py::object _ServiceCollection::ResolveAnnotations(ContainerService containerService)
// {
//     if (!containerService.Args.empty())
//     {
//         return ResolveArgs(containerService);
//     }
//     auto implementation = containerService.Implementation;
//     auto annotations = getattr(implementation.attr("__init__"), "__annotations__", py::dict());
//     for (const auto &[name, annotation])
//     {
//         py::type_id
//     }
// }

py::object _ServiceCollection::ResolveArgs(ContainerService containerService)
{
    return containerService.Implementation(*containerService.Args);
}
