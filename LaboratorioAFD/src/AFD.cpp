#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <fstream>
#include <cstdlib>

class Estado {
public:
    std::string nombre;
    int numero;

    Estado(std::string nombre, int numero) : nombre(nombre), numero(numero) {}
};

class AFD {
private:
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> transiciones;
    std::string q0; 
    std::unordered_set<int> F_;

public:
    AFD(std::string estadoInicial, const std::vector<int>& estadosFinales) : q0(estadoInicial), F_(estadosFinales.begin(), estadosFinales.end()) {}


    void agregarTransicion(const std::string& estado, const std::string& simbolo, const std::string& nuevoEstado) {
        transiciones[estado][simbolo] = nuevoEstado;
    }

    
    std::vector<std::string> move_AFD(const std::vector<std::string>& states, const std::string& symbol) {
        std::unordered_set<std::string> nuevosEstados;

        for (const std::string& state : states) {
            if (transiciones.find(state) != transiciones.end() && transiciones[state].find(symbol) != transiciones[state].end()) {
                nuevosEstados.insert(transiciones[state][symbol]);
            }
        }

        return std::vector<std::string>(nuevosEstados.begin(), nuevosEstados.end());
    }

   
    bool acept_Chain(const std::string& w, const std::unordered_map<std::string, Estado>& estados) {
        std::vector<std::string> current_states = {q0};

        for (char symbol : w) {
            current_states = move_AFD(current_states, std::string(1, symbol));
        }

        // Verificar si algún estado actual es de aceptación
        for (const std::string& state : current_states) {
            if (estados.find(state) != estados.end() && F_.count(estados.at(state).numero)) {
                return true;
            }
        }

        return false;
    }

    void generarDot(const std::string& nombreArchivo) {
        std::ofstream archivo(nombreArchivo + ".dot");
        if (!archivo.is_open()) {
            std::cerr << "Error al abrir el archivo " << nombreArchivo << ".dot" << std::endl;
            return;
        }

        archivo << "digraph AFD {\n";
        archivo << "    rankdir=LR;\n";
        archivo << "    node [shape=circle];\n";

        // Estados finales
        for (int estadoFinal : F_) {
            archivo << "    q" << estadoFinal << " [shape=doublecircle];\n";
        }

        // Transiciones
        for (const auto& estado : transiciones) {
            for (const auto& transicion : estado.second) {
                archivo << "    " << estado.first << " -> " << transicion.second << " [label=\"" << transicion.first << "\"];\n";
            }
        }

        archivo << "}\n";
        archivo.close();

        std::cout << "Archivo " << nombreArchivo << ".dot generado correctamente.\n";
    }

};

int main() {
   
    std::unordered_map<std::string, Estado> estados = {
        {"q0", Estado("q0", 0)},
        {"q1", Estado("q1", 1)},
        {"q2", Estado("q2", 2)},
        {"q3", Estado("q3", 3)}
    };

   
    AFD automata("q0", {2});

    automata.agregarTransicion("q0", "a", "q1");
    automata.agregarTransicion("q0", "b", "q3");

    automata.agregarTransicion("q1", "a", "q2");
    automata.agregarTransicion("q1", "b", "q1");

    automata.agregarTransicion("q2", "b", "q2");
    automata.agregarTransicion("q2", "a", "q3");


    automata.agregarTransicion("q3", "a", "q3");
    automata.agregarTransicion("q3", "b", "q3");


    std::string cadena = "abab";
    if (automata.acept_Chain(cadena, estados)) {
        std::cout << "La cadena '" << cadena << "' es aceptada por el AFD.\n";
            automata.generarDot("afd_visual");

    } else {
        std::cout << "La cadena '" << cadena << "' no es aceptada por el AFD.\n";
    }


    return 0;
}
