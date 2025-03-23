#include <vector>
#include <string>
#include <algorithm>
#include <iostream>


struct ReglaToken {
    std::string identificador;
    std::string nombre;
    std::string token;
    std::string expresion_regular;
};

struct ReglasTokens {
    std::vector<ReglaToken> reglas;

    // Insertar una nueva regla
    void insertar(const ReglaToken& regla) {
        reglas.push_back(regla);
    }

    // Extraer una regla dado un atributo
    std::vector<ReglaToken> extraer(const std::string& atributo, const std::string& valor) {
        std::vector<ReglaToken> resultado;
        for (const auto& regla : reglas) {
            if ((atributo == "identificador" && regla.identificador == valor) ||
                (atributo == "nombre" && regla.nombre == valor) ||
                (atributo == "token" && regla.token == valor) ||
                (atributo == "expresion_regular" && regla.expresion_regular == valor)) {
                resultado.push_back(regla);
            }
        }
        return resultado;
    }

    // Actualizar una regla dado un atributo
    void actualizar(const std::string& atributo, const std::string& valor, const ReglaToken& nuevaRegla) {
        for (auto& regla : reglas) {
            if ((atributo == "identificador" && regla.identificador == valor) ||
                (atributo == "nombre" && regla.nombre == valor) ||
                (atributo == "token" && regla.token == valor) ||
                (atributo == "expresion_regular" && regla.expresion_regular == valor)) {
                regla = nuevaRegla;
            }
        }
    }

    // Eliminar una regla dado un atributo
    void eliminar(const std::string& atributo, const std::string& valor) {
        reglas.erase(std::remove_if(reglas.begin(), reglas.end(), [&](const ReglaToken& regla) {
            return (atributo == "identificador" && regla.identificador == valor) ||
                   (atributo == "nombre" && regla.nombre == valor) ||
                   (atributo == "token" && regla.token == valor) ||
                   (atributo == "expresion_regular" && regla.expresion_regular == valor);
        }), reglas.end());
    }


     void imprimir() const {
        for (const auto& regla : reglas) {
            std::cout << "Identificador: " << regla.identificador << "\n"
                      << "Nombre: " << regla.nombre << "\n"
                      << "Token: " << regla.token << "\n"
                      << "Expresión Regular: " << regla.expresion_regular << "\n"
                      << "-----------------------------\n";
        }
    }
};
