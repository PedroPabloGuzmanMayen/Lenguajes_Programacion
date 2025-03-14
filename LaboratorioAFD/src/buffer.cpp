#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

// Variables globales
int AVANCE = 0;
int INICIOLEXEMA = 0;
vector<string> LEXEMAS;
int LECTOR = 0;
string LEXEMA = "";
bool FLAG_SALIDA = true;

// Función para cargar el buffer desde la entrada
vector<char> cargar_buffer(const string &entrada, int inicio, int tamano_buffer) {
    vector<char> buffer;
    for (int i = inicio; i < inicio + tamano_buffer && i < entrada.size(); i++) {
        buffer.push_back(entrada[i]);
    }
    if (buffer.size() < tamano_buffer) {
        buffer.push_back('\0'); // EOF
    }
    return buffer;
}

// Función para procesar el buffer e identificar lexemas
void procesar_buffer(const vector<char> &buffer) {
    AVANCE = 0;
    INICIOLEXEMA = 0;

    for (int i = 0; i < buffer.size(); i++) {
        char caracter = buffer[i];

        if (caracter == ' ' || caracter == '\n' || caracter == '\0') { 
            if (!LEXEMA.empty()) {
                cout << "Lexema procesado: " << LEXEMA << endl;
                LEXEMAS.push_back(LEXEMA);
                LEXEMA.clear();
            }
            INICIOLEXEMA = i + 1;
            AVANCE = INICIOLEXEMA;

            if (caracter == '\0') {
                FLAG_SALIDA = false;
                break;
            }
        } else {
            AVANCE = i + 1;
            LEXEMA += caracter;
        }
    }
}

int main() {
    const int tamano_buffer = 10;
    string entrada = "";

    // 📂 Abrir archivo y leer contenido
    ifstream archivo("entrada.txt");
    if (!archivo) {
        cerr << "Error al abrir el archivo 'entrada.txt'" << endl;
        return 1;
    }

    // Leer archivo completo en un string
    string linea;
    while (getline(archivo, linea)) {
        entrada += linea + " "; // Añadir espacio entre líneas para separar lexemas
    }
    archivo.close();

    // 🔄 Procesar la entrada en buffers de tamaño fijo
    while (FLAG_SALIDA) {
        vector<char> BUFFER = cargar_buffer(entrada, LECTOR, tamano_buffer);
        procesar_buffer(BUFFER);
        LECTOR += BUFFER.size();
    }

    return 0;
}
