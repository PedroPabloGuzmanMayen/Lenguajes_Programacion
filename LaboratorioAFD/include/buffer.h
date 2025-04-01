#ifndef BUFFER_H
#define BUFFER_H

#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Buffer {
public:
    vector<char> buffer;
    int inicioLexema;
    int avance;
    bool FLAG_SALIDA;
    string entrada;
    const int tamano_buffer;
    char ultimoCaracter;

public:
    
    Buffer(const string &filename, int tamano);

    
    Buffer(int tamano, const string &cadenaEntrada);

    
    void cargar_buffer();

    
    string obtenerSiguienteCaracter();

    string obtenerSiguienteCaracter2();
    string obtenerSiguienteLinea();
    bool validarLinea(const string &linea, int numeroLinea);

};

#endif