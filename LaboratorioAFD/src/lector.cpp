#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <yaml-cpp/yaml.h>
#include "lector.h"

Config leerConfig(const std::string &archivo) {
    Config config;
    
    try {
        YAML::Node data = YAML::LoadFile(archivo);

        if (data["expresiones_regulares"]) {
            for (const auto& expr : data["expresiones_regulares"]) {
                config.expresiones_regulares.push_back(expr.as<std::string>());
            }
        } else {
            std::cerr << "Error: No se encontró la clave 'expresiones_regulares' en el YAML.\n";
        }

        if (data["cadenas"]) {
            for (const auto& cadena : data["cadenas"]) {
                config.cadenas.push_back(cadena.as<std::string>());
            }
        } else {
            std::cerr << "Error: No se encontró la clave 'cadenas' en el YAML.\n";
        }

    } catch (const YAML::Exception &e) {
        std::cerr << "Error al leer el archivo YAML: " << e.what() << std::endl;
    }

    return config;
}
