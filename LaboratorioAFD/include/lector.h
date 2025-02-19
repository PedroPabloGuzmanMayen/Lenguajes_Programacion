#ifndef LECTOR_H
#define LECTOR_H

#include <vector>
#include <string>

struct Config {
    std::vector<std::string> expresiones_regulares;
    std::vector<std::string> cadenas;
};

Config leerConfig(const std::string &archivo);

#endif
