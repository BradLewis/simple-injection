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
    std::map<long, ContainerService> _serviceCollection;

public:
    _ServiceCollection(){std::cout << "hello from c++";} py::object Resolve(long serviceId);
    void Add(long serviceId, py::object serviceImplementation, ServiceLifetime lifetime);
};

#endif // __SERVICECOLLECTION_H__