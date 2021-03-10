#ifndef __SERVICECOLLECTION_H__
#define __SERVICECOLLECTION_H__

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
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
    py::object ResolveAnnotations(ContainerService& containerService);
    py::object ResolveArgs(ContainerService& containerService);
    py::object ResolveSingleton(ContainerService& containerService);
    py::object ResolveTransient(ContainerService& containerService);
    py::object ResolveInstance(ContainerService& containerService);

public:
    _ServiceCollection() {}
    py::object Resolve(py::object service);
    void Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations);
    void Add(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations, py::list args);
};

#endif // __SERVICECOLLECTION_H__