#ifndef REGLAS_TOKENS_H
#define REGLAS_TOKENS_H

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

class ReglasTokens {
public:
    std::vector<ReglaToken> reglas;

public:
    // Insertar una nueva regla
    void insertar(const ReglaToken& regla);

    // Extraer una regla dado un atributo
    std::vector<ReglaToken> extraer(const std::string& atributo, const std::string& valor);

    // Actualizar una regla dado un atributo
    void actualizar(const std::string& atributo, const std::string& valor, const ReglaToken& nuevaRegla);

    // Eliminar una regla dado un atributo
    void eliminar(const std::string& atributo, const std::string& valor);

    // Imprimir las reglas
    void imprimir() const;
};

#endif // REGLAS_TOKENS_H
