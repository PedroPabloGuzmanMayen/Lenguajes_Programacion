#include <iostream>
#include <vector>
#include <fstream>
using namespace std;





class Buffer {
public:
    vector<char> buffer;
    int inicioLexema;
    int avance;
    bool FLAG_SALIDA;
    string entrada;
    const int tamano_buffer;
    char ultimoCaracter;  // Guarda el último carácter leído
    std::vector<std::string> caracteres;


public:
    Buffer(const string &filename, int tamano) 
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


    // Constructor desde cadena directa
    Buffer(int tamano, const string &cadenaEntrada)
        : inicioLexema(0), avance(0), FLAG_SALIDA(true), tamano_buffer(tamano), 
          ultimoCaracter('\0'), entrada(cadenaEntrada) {}
          
    void cargar_buffer() {
        buffer.clear();
        for (int i = inicioLexema; i < inicioLexema + tamano_buffer && i < entrada.size(); i++) {
            buffer.push_back(entrada[i]);
        }
        if (buffer.size() < tamano_buffer) {
            buffer.push_back('\0'); // EOF
        }
        avance = 0;
    }

    void procesar_buffer() {
        while (avance < buffer.size()) {
            char caracter = buffer[avance];
            string caracterSalida(1, caracter);  // Convertimos el caracter a string

            // Si encontramos un espacio y el último caracter fue una comilla, lo reemplazamos por "ε"
            if (caracter == ' ' && ultimoCaracter == '\'' &&buffer[avance +1 ] == '\'' ) {
                caracterSalida = "\x7F";  // Reemplazo por épsilon
            }
            
            if (caracter == '\n' ) {
                caracterSalida = " ";  // Reemplazo por épsilon
            }


            if (caracter == '\0') {
                FLAG_SALIDA = false;
                break;
            }

            caracteres.push_back(caracterSalida);

            // cout << "InicioLexema: " << inicioLexema << ", Avance: " << avance 
            //      << ", Caracter: " << caracterSalida << endl;

            // Guardamos el último caracter leído para la próxima iteración
            ultimoCaracter = caracter;

            avance++;
            if (avance >= buffer.size()) {
                inicioLexema += buffer.size();
                cargar_buffer();
            }
        }
    }

    void ejecutar() {
        while (FLAG_SALIDA) {
            cargar_buffer();
            procesar_buffer();
        }
    }

    string cadenaString() {
        string resultado;
        for (const auto& c : caracteres) {
            resultado += c;
        }
        return resultado;
    }


};


/*
int main() {
    string input;
    cout << "Escribe la cadena: ";
    getline(cin, input); 

    Buffer buffer(10, input); // aca el parametro primero va el tamano del bufer y luego el input a diferencia del otro constructor con filename. 
    buffer.ejecutar();

    string resultado = buffer.cadenaString();
    cout << "Resultado string: " << resultado << endl;

    return 0;
}
*/