#include <iostream>
#include <vector>
#include <fstream>
#include "constantes.h"
#include "buffer.h"
using namespace std;





    
    Buffer::Buffer(const string &filename, int tamano) 
        : inicioLexema(0), avance(0), FLAG_SALIDA(true), tamano_buffer(tamano), ultimoCaracter('\0') {
        
        ifstream archivo(filename);
        if (!archivo) {
            cerr << "Error al abrir el archivo '" << filename << "'" << endl;
            exit(1);
        }
        char caracter;
        while (archivo.get(caracter)) {
            entrada += caracter;
        }
        archivo.close();
    }

    // Constructor desde entrada por teclado
    Buffer::Buffer(int tamano, const string &cadenaEntrada)
        : inicioLexema(0), avance(0), FLAG_SALIDA(true), tamano_buffer(tamano), 
          ultimoCaracter('\0'), entrada(cadenaEntrada) {}

    // Cargar el buffer con la siguiente parte de la entrada
    void Buffer::cargar_buffer() {
        buffer.clear();
        for (int i = inicioLexema; i < inicioLexema + tamano_buffer && i < entrada.size(); i++) {
            buffer.push_back(entrada[i]);
        }
        if (buffer.size() < tamano_buffer) {
            buffer.push_back('\0'); // EOF
        }
        avance = 0;
    }

    // Obtener el siguiente carácter procesado
    string Buffer::obtenerSiguienteCaracter() {
        if (avance >= buffer.size()) {
            inicioLexema += buffer.size();
            cargar_buffer();
        }

        if (avance < buffer.size()) {
            char caracter = buffer[avance];
            string caracterSalida(1, caracter);

            if (caracter == ' ' && ultimoCaracter == '\'' && buffer[avance + 1] == '\'') {
                caracterSalida = WHITESPACE;  // Reemplazo por épsilon
                std::cout<<"Imprimir \n";
            }

            if (caracter == '.'){
                caracterSalida = PUNTO;  // Reemplazo por épsilon

            }

            
            
            if (caracter == '\n') {
                caracterSalida = " ";  // Reemplazo por espacio
            }

            if (caracter == '\0') {
                FLAG_SALIDA = false;
                return "";
            }

            ultimoCaracter = caracter;
            avance++;

            return caracterSalida;
        }

        return "";
    }

// int main() {
//     int opcion;
//     string input, filename;

//     cout << "Selecciona la opción de entrada:\n";
//     cout << "1. Ingresar texto manualmente\n";
//     cout << "2. Leer desde un archivo\n";
//     cout << "Opción: ";
//     cin >> opcion;
//     cin.ignore();  // Para limpiar el buffer de entrada

//     Buffer* buffer = nullptr;  // Puntero a Buffer

//     if (opcion == 1) {
//         cout << "Escribe la cadena: ";
//         getline(cin, input);
//         buffer = new Buffer(10, input);
//     } else if (opcion == 2) {
//         cout << "Ingresa el nombre del archivo: ";
//         getline(cin, filename);
//         buffer = new Buffer(filename, 10);
//     } else {
//         cout << "Opción no válida.\n";
//         return 1;
//     }

//     string resultado;

//     // Procesar el buffer en main()
//     while (buffer->FLAG_SALIDA) {
//         buffer->cargar_buffer();
//         while (buffer->FLAG_SALIDA) {
//             string caracter = buffer->obtenerSiguienteCaracter();
//             std::cout<<"Procesado: "<<caracter<<"\n";
//             if (!caracter.empty()) {
//                 resultado += caracter;
//             }
//         }
//     }

//     cout << "Resultado final: " << resultado << endl;

//     delete buffer;  // Liberar memoria
//     return 0;
// }
