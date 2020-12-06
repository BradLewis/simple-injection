#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(simple_injection, m)
{
    m.doc() = "Dependency injection library for python";
}