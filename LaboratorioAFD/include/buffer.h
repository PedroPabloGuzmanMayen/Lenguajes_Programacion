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
    // Constructor desde archivo
    Buffer(const string &filename, int tamano);

    // Constructor desde entrada por teclado
    Buffer(int tamano, const string &cadenaEntrada);

    // Cargar el buffer con la siguiente parte de la entrada
    void cargar_buffer();

    // Obtener el siguiente carácter procesado
    string obtenerSiguienteCaracter();
};

#endif // BUFFER_H
