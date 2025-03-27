#ifndef AFD_H
#define AFD_H

#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <fstream>

class Estado {
public:
    std::string nombre;
    int numero;
    Estado() = default;
    Estado(std::string nombre, int numero) : nombre(nombre), numero(numero) {}
};

class AFD {
public:
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> S_;
    std::string q0; 
    std::unordered_set<int> F_;
    std::vector<std::string> Alfabeto;
    std::unordered_map<std::string, Estado> Q_;

    AFD(std::string estadoInicial, const std::vector<int>& estadosFinales,
        const std::vector<std::string>& alfabeto, const std::unordered_map<std::string, Estado>& estados);

    void agregarTransicion(const std::string& estado, const std::string& simbolo, const std::string& nuevoEstado);
    bool acept_Chain(const std::string& w);
    void depurarAFD();
    void generarDot(const std::string& nombreArchivo);
    void generarImagen(const std::string& nombreArchivo);
    void mostrarTransiciones();
    void minimizarAFD();
    std::vector<std::pair<std::string, std::string>> analizarCadena(
        const std::map<std::string, char>& estadosAceptacion,
        const std::map<char, std::string>& terminadorToken,
        const std::string& entrada);
    std::vector<std::string> move_AFD(const std::vector<std::string>& states, const std::string& symbol);
    void reconstruirAFD(const std::vector<std::unordered_set<std::string>>& P);
    std::vector<std::unordered_set<std::string>> separarEstados();
    std::vector<std::map<std::string, std::string>>  findTokens(std::string cadena, std::map<int, char> Terminator_State, 
        std::map<char, std::string> tokens );

        
};

#endif // AFD_H
