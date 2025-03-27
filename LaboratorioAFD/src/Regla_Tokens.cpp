#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include "Regla_Tokens.h"
#include "constantes.h"

// Insertar una nueva regla
void ReglasTokens::insertar(const ReglaToken& regla) {
    reglas.push_back(regla);
}

const std::vector<ReglaToken>& ReglasTokens::obtenerReglas() const {
    return reglas;
}

// Extraer una regla dado un atributo
std::vector<ReglaToken> ReglasTokens::extraer(const std::string& atributo, const std::string& valor) {
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
void ReglasTokens::actualizar(const std::string& atributo, const std::string& valor, const ReglaToken& nuevaRegla) {
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
void ReglasTokens::eliminar(const std::string& atributo, const std::string& valor) {
    reglas.erase(std::remove_if(reglas.begin(), reglas.end(), [&](const ReglaToken& regla) {
        return (atributo == "identificador" && regla.identificador == valor) ||
               (atributo == "nombre" && regla.nombre == valor) ||
               (atributo == "token" && regla.token == valor) ||
               (atributo == "expresion_regular" && regla.expresion_regular == valor);
    }), reglas.end());
}

// Imprimir las reglas
void ReglasTokens::imprimir() const {
    for (const auto& regla : reglas) {
        std::cout << "Identificador: " << regla.identificador << "\n"
                  << "Nombre: " << regla.nombre << "\n"
                  << "Token: " << regla.token << "\n"
                  << "Expresión Regular: " << regla.expresion_regular << "\n"
                  << "-----------------------------\n";
    }
}


std::string ReglasTokens::obtener_token_(const std::string& nombre) const {
    for (const auto& regla : reglas) {
        if (regla.nombre == nombre) {
            return regla.token;
        }
    }
    return ""; 
}



std::string ReglasTokens::generarExpresion() const {
    std::string resultado = "";
    
    for (size_t i = 0; i < reglas.size(); ++i) {
        const auto& regla = reglas[i];
        // Si la expresión regular está vacía, usar el nombre
        std::string expresion = (regla.expresion_regular.empty()) ? regla.nombre : regla.expresion_regular;
    
        
    
        if (expresion == "*") {
            expresion = TIMES;
        }
        else if (expresion == "(") {
            expresion = RPARENTESIS;
        }
        else if (expresion == ")") {
            expresion = LPARENTESIS;
        }
    
        // Concatenar la expresión y el identificador
        std::string concatenado = expresion + regla.identificador;
    
        // Si no es el primer elemento, agrega un espacio
        if (!resultado.empty()) {
            resultado += "";
        }
    
       
        if (i != reglas.size() - 1) {
            concatenado += "|";
        }
    
       
        resultado += concatenado;
    }

    std::cout<<resultado<<"\n";

    return resultado;
}


