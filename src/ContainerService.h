#ifndef __CONTAINERSERVICE_H__
#define __CONTAINERSERVICE_H__

#include <pybind11/pybind11.h>
#include "ServiceLifetime.h"

namespace py = pybind11;
using namespace std;

class ContainerService
{
public:
    py::object Implementation;
    ServiceLifetime Lifetime;
    py::list Args;
    py::object SingletonInstance;
    bool HasMultipleImplementations;
    std::vector<py::object> Implementations;
    std::map<std::string, py::object> Annotations;

    ContainerService() {}

    ContainerService(py::object implementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations)
    {
        Implementation = implementation;
        Lifetime = lifetime;
        HasMultipleImplementations = false;
        Annotations = annotations;
    }

    ContainerService(py::object implementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations, py::list args) : ContainerService(implementation, lifetime, annotations)
    {
        Args = args;
    }
};

#endif // __CONTAINERSERVICE_H__