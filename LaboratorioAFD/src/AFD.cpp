#include <vector>
#include <string>
#include <unordered_set>



#pragma once
#include <string>

class Transicion {
public:
    Transicion(const std::string& initialState, const std::string& finalState, char valor)
        : q0(initialState), qf(finalState), valor(valor) {}

    std::string getInitialState() const { return q0; }
    std::string getFinalState() const { return qf; }
    char getValor() const { return valor; }

private:
    std::string q0;
    std::string qf;
    char valor;
};

class Estado {
public:
    Estado(const std::string& numero, bool aceptacion = false)
        : numero(numero), aceptacion(aceptacion) {}

    void setToAcept() { aceptacion = true; }
    bool isAceptacion() const { return aceptacion; }
    std::string getNumero() const { return numero; }

private:
    std::string numero;
    bool aceptacion;
};



class AFD {
public:
    AFD(const std::vector<char>& alfabeto, const std::string& estadoInicial, const std::vector<std::string>& estadosFinales) 
        : Alfabeto_(alfabeto), q0(estadoInicial), F_(estadosFinales), state_count(0) {}

    void setQ0(const std::string& nuevoQ0) {
        q0 = nuevoQ0;
    }

    void setQF(const std::vector<std::string>& nuevosQF) {
        F_ = nuevosQF;
    }

private:
    std::vector<char> Alfabeto_;
    std::string q0;
    std::vector<std::string> F_;
    int state_count;
};