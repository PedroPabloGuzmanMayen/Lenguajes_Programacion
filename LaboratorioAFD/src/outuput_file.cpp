#include <iostream>
#include <fstream>
#include <string>

using namespace std;


void escribirArchivo(const string &contenido, const string &nombreArchivo) {

    ofstream archivoSalida(nombreArchivo, ios::out | ios::trunc);  // ios::trunc asegura que se sobrescriba el archivo si existe


    if (!archivoSalida) {
        cerr << "Error al abrir el archivo " << nombreArchivo << endl;
        return;
    }


    archivoSalida << contenido;


    archivoSalida.close();

    cout << "Contenido escrito correctamente en el archivo " << nombreArchivo << endl;
}