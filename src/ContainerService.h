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
    std::vector<py::object> Args;
    py::object SingletonInstance;
    bool HasMultipleImplementations;
    std::vector<py::object> Implementations;

    ContainerService() {}

    ContainerService(py::object implementation, ServiceLifetime lifetime)
    {
        Implementation = implementation;
        Lifetime = lifetime;
        HasMultipleImplementations = false;
    }

    // ContainerService(py::object implementation, ServiceLifetime lifetime, std::vector<py::object> args) : ContainerService(implementation, lifetime)
    // {
    //     Args = args;
    // }
};

#endif // __CONTAINERSERVICE_H__