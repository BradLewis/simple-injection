#include <pybind11/pybind11.h>
#include "ServiceCollection.h"
#include "ContainerService.h"
#include "ServiceLifetime.h"

using namespace pybind11::literals;

py::object _ServiceCollection::Resolve(py::object service)
{

    ssize_t serviceId = py::hash(service);
    auto service_to_resolve = _serviceCollection[serviceId];

    return ResolveAnnotations(service_to_resolve);
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

py::object _ServiceCollection::ResolveAnnotations(ContainerService containerService)
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

py::object _ServiceCollection::ResolveArgs(ContainerService containerService)
{
    return containerService.Implementation(*containerService.Args);
}
