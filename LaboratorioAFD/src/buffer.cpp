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
            if (caracter == '\r') {
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
    string Buffer::obtenerSiguienteCaracter2() {
        if (avance >= buffer.size()) {
            inicioLexema += buffer.size();
            cargar_buffer();
        }

        if (avance < buffer.size()) {
            char caracter = buffer[avance];
            string caracterSalida(1, caracter);

            

            if (caracter == '.') {
                caracterSalida = PUNTO;

            }
            if (caracter == '\r') {
                caracterSalida = " ";  // Reemplazo por espacio
            }
            if (caracter == ')'){
                caracterSalida = RPARENTESIS;  // Reemplazo por épsilon

            }

            if (caracter == '('){
                caracterSalida = LPARENTESIS;  // Reemplazo por épsilon

            }
            if (caracter == '*'){
                caracterSalida = TIMES;  // Reemplazo por épsilon

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

    string Buffer::obtenerSiguienteLinea() {
        string linea;
        string caracter;
    
        while (FLAG_SALIDA) {
            caracter = obtenerSiguienteCaracter2();
            
            if (caracter.empty()) {
                break;
            }
    
            if (caracter == " ") {
                linea += " ";
            }
    
            if (caracter == "\n" || caracter == "") { // Si encontramos un salto de línea o EOF
                return linea; // Devolvemos la línea completa
            }
    
            linea += caracter; // Agregamos el caracter al final de la línea
        }
        return linea;
    }

    bool Buffer::validarLinea(const string& linea, int numeroLinea) {
        int comillas_simples = 0;
        int comillas_dobles = 0;
        int par_abierto = 0;
        int par_cerrado = 0;

        for (char c : linea) {
            if (c == '\'') comillas_simples++;
            if (c == '"') comillas_dobles++;
            if (c == '(') par_abierto++;
            if (c == ')') par_cerrado++;
        }

        // paracomillas desbalanceadas
        if (comillas_simples % 2 != 0) {
            cerr << "Error en el yal línea " << numeroLinea << ": comillas simples desbalanceadas.\n";
            exit(1);
        }

        if (comillas_dobles % 2 != 0) {
            cerr << "Error en el yal línea " << numeroLinea << ": comillas dobles desbalanceadas.\n";
            exit(1);
        }

        if (par_abierto != par_cerrado) {
            cerr << "Error en el yal línea " << numeroLinea << ": paréntesis desbalanceados.\n";
            exit(1);
        }

        // saber ssi hay "let" con corchetes
        if (linea.find("let") != string::npos &&
            linea.find("[") != string::npos &&
            linea.find("]") != string::npos) {

            size_t desde = linea.find("[");
            size_t hasta = linea.find("]");
            string contenido = linea.substr(desde + 1, hasta - desde - 1);

            // Detecta si hay rangos pegados como 'Z'a' sin operador
            for (size_t i = 0; i + 5 < contenido.size(); i++) {
                if (contenido[i] == '\'' &&
                    contenido[i+2] == '\'' &&
                    contenido[i+3] != '|' &&
                    contenido[i+3] != '-' &&
                    contenido[i+3] != ',' &&
                    contenido[i+3] != ']') {

                    string problema = contenido.substr(i, 5);
                    cerr << "Error en yal en la línea " << numeroLinea << ": posible rango mal formado cerca de: " << problema << "\n";
                    exit(1);
                }
            }
        }

        return true;
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