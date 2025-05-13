#include <iostream>
#include <fstream>
#include <string>
#include "outuput_file.h"

using namespace std;


void escribirArchivo(const string &contenido, const string &nombreArchivo) {
    ofstream archivoSalida(nombreArchivo, ios::out | ios::trunc);

    if (!archivoSalida) {
        cerr << "Error al abrir el archivo " << nombreArchivo << endl;
        return;
    }

    archivoSalida << contenido;
    archivoSalida.close();

    cout << "Contenido escrito correctamente en el archivo " << nombreArchivo << endl;
}