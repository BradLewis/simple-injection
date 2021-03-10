#ifndef __EXCEPTIONS_H__
#define __EXCEPTIONS_H__

#include <exception>
#include <string>
#include <pybind11/pybind11.h>

class ServiceResolutionError : public std::exception
{
public:
    explicit ServiceResolutionError(const char *m, py::object service) : message{m}
    {
        this->message = this->message + " " + py::cast<std::string>(py::str(service));
    }
    const char *what() const noexcept override { return message.c_str(); }

private:
    std::string message = "";
};

#endif // __EXCEPTIONS_H__