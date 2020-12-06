#include <pybind11/pybind11.h>
#include <map>
#include "ServiceLifetime.h"
#include "ContainerService.h"

namespace py = pybind11;
using namespace std;

class ServiceCollection
{
private:
    std::map<py::object, ContainerService> _service_collection;

public:
    ServiceCollection();
};