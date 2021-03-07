#include <pybind11/pybind11.h>
#include "ServiceCollection.h"
#include "ServiceLifetime.h"

namespace py = pybind11;

PYBIND11_MODULE(_simple_injection, m)
{
    m.doc() = "Dependency injection library for python";
    py::class_<_ServiceCollection>(m, "_ServiceCollection")
        .def(py::init())
        .def("add", &_ServiceCollection::Add)
        .def("resolve", &_ServiceCollection::Resolve);

    py::enum_<ServiceLifetime>(m, "ServiceLifetime")
        .value("TRANSIENT", ServiceLifetime::TRANSIENT)
        .value("SINGLETON", ServiceLifetime::SINGLETON)
        .value("INSTANCE", ServiceLifetime::INSTANCE);
}