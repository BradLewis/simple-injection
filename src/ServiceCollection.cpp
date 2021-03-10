#include <pybind11/pybind11.h>
#include "ServiceCollection.h"
#include "ContainerService.h"
#include "ServiceLifetime.h"
#include "Exceptions.h"

using namespace pybind11::literals;

py::object _ServiceCollection::Resolve(py::object service)
{
    ssize_t serviceId = py::hash(service);
    auto it = _serviceCollection.find(serviceId);
    if (it == _serviceCollection.end())
    {
        throw ServiceResolutionError("Requested service not found in collection.", service);
    }
    ContainerService &serviceToResolve = _serviceCollection[serviceId];
    if (serviceToResolve.Lifetime == ServiceLifetime::INSTANCE)
        return ResolveInstance(serviceToResolve);
    if (serviceToResolve.Lifetime == ServiceLifetime::SINGLETON)
        return ResolveSingleton(serviceToResolve);
    return ResolveTransient(serviceToResolve);
}

void _ServiceCollection::Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations)
{
    ssize_t serviceId = py::hash(service);
    _serviceCollection[serviceId] = ContainerService(serviceImplementation, lifetime, annotations);
}

void _ServiceCollection::Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations, py::list args)
{
    ssize_t serviceId = py::hash(service);
    _serviceCollection[serviceId] = ContainerService(serviceImplementation, lifetime, annotations, args);
}

py::object _ServiceCollection::ResolveAnnotations(ContainerService &containerService)
{
    if (!containerService.Args.empty())
    {
        return ResolveArgs(containerService);
    }
    auto implementation = containerService.Implementation;
    auto annotations = containerService.Annotations;
    std::vector<py::object> services_to_use;
    for (const auto &[name, annotation] : annotations)
    {

        if (name != "return")
        {
            services_to_use.push_back(Resolve(annotation));
        }
    }
    return implementation(*py::cast(services_to_use));
}

py::object _ServiceCollection::ResolveArgs(ContainerService &containerService)
{
    return containerService.Implementation(*containerService.Args);
}

py::object _ServiceCollection::ResolveSingleton(ContainerService &containerService)
{
    if (containerService.SingletonInstance.is_none())
    {
        containerService.SingletonInstance = ResolveAnnotations(containerService);
    }
    return containerService.SingletonInstance;
}

py::object _ServiceCollection::ResolveTransient(ContainerService &containerService)
{
    return ResolveAnnotations(containerService);
}

py::object _ServiceCollection::ResolveInstance(ContainerService &containerService)
{
    return containerService.Implementation;
}
