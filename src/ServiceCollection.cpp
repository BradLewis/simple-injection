#include <pybind11/pybind11.h>
#include "ServiceCollection.h"
#include "ContainerService.h"
#include "ServiceLifetime.h"

py::object _ServiceCollection::Resolve(long serviceId)
{
    std::cout << "here" << std::endl;
    py::object service = _serviceCollection[serviceId].Implementation;

    std::cout << serviceId << std::endl;

    return service();
}

void _ServiceCollection::Add(long serviceId, py::object serviceImplementation, ServiceLifetime lifetime)
{
    _serviceCollection[serviceId] = ContainerService(serviceImplementation, lifetime);
    std::cout << serviceId << std::endl;
}
