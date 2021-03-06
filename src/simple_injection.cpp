#include <pybind11/pybind11.h>
#include "ServiceCollection.h"

namespace py = pybind11;

PYBIND11_MODULE(_simple_injection, m)
{
    m.doc() = "Dependency injection library for python";
    py::class_<_ServiceCollection>(m, "_ServiceCollection")
        .def(py::init())
        .def("add", &_ServiceCollection::Add)
        .def("resolve", &_ServiceCollection::Resolve);
}