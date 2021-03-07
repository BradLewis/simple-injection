#ifndef __SERVICECOLLECTION_H__
#define __SERVICECOLLECTION_H__

#include <pybind11/pybind11.h>
#include <map>
#include <iostream>
#include "ServiceLifetime.h"
#include "ContainerService.h"

namespace py = pybind11;
using namespace std;

class _ServiceCollection
{
private:
    std::map<ssize_t, ContainerService> _serviceCollection;
    py::object ResolveAnnotations(ContainerService containerService);
    py::object ResolveArgs(ContainerService containerService);

public:
    _ServiceCollection() { std::cout << "hello from c++" << std::endl; }
    py::object Resolve(py::object service);
    void Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, py::dict annotaitons);
    void Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, py::dict annotaitons, py::list args);
};

#endif // __SERVICECOLLECTION_H__