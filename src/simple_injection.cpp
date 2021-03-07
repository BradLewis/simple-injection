#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "ServiceCollection.h"
#include "ServiceLifetime.h"
#include "ServiceResolverFlags.h"

namespace py = pybind11;

PYBIND11_MODULE(_simple_injection, m)
{
    m.doc() = "Dependency injection library for python";
    py::class_<_ServiceCollection>(m, "_ServiceCollection")
        .def(py::init())
        .def("add", static_cast<void (_ServiceCollection::*)(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations)>(&_ServiceCollection::Add))
        .def("add", static_cast<void (_ServiceCollection::*)(py::object service, py::object serviceImplementation, ServiceLifetime lifetime, std::map<std::string, py::object> annotations, py::list args)>(&_ServiceCollection::Add))
        .def("resolve", &_ServiceCollection::Resolve);

    py::enum_<ServiceLifetime>(m, "ServiceLifetime", R"pbdoc(
            Service lifetimes. There are currently 3 different service lifetimes.

            TRANSIENT: A new instance will be created every time the service is requested.
            SINGLETON: The same instance is used across all requests. Instance is created
                the first time the service is requested.
            INSTANCE: The provided instance will be used for all requests.
            )pbdoc")
        .value("TRANSIENT", ServiceLifetime::TRANSIENT)
        .value("SINGLETON", ServiceLifetime::SINGLETON)
        .value("INSTANCE", ServiceLifetime::INSTANCE);

    py::enum_<ServiceResolverFlags>(m, "ServiceResolverFlags", R"pbdoc(
        Flag to use when using args when adding a service.

        REQUIRED_SERVICE: Use this flag in the args
            and when resolving the service, it will look up the service in the service
            collection where the flag was used.

        Example:
            class Service:
                pass

            class Example:
                def __init__(self, i: int, service: Service):
                    self._i = i
                    self._service = service

            collection = ServiceCollection()
            collection.add_transient(Service)

            # This would be the same as Example(1, Service())
            collection.add_transient(Example, args=[1, ServiceResolverFlag.REQUIRED_SERVICE])
        )pbdoc")
        .value("REQUIRED_SERVICE", ServiceResolverFlags::REQUIRED_SERVICE);
}