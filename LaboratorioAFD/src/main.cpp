#include <iostream>
#include <string>
#include <unistd.h>
#include <unordered_map>
#include "shunting_yard.h"
#include "tree.h"
#include "node.h"
#include "AFD.cpp"
#include "lector.h"

int main() {
    // Leer expresiones y cadenas desde YAML
    Config config = leerConfig("../expresiones.yml");

    for (const std::string& my_str : config.expresiones_regulares) {
        std::cout << "\nProcesando expresión regular: " << my_str << std::endl;
        std::string my_str_copy = my_str;
        std::string newStr = add_concatenation(my_str_copy);
        std::cout << "Expresión con concatenación explícita: " << newStr << std::endl;

        std::string sht_y = shunting_yard(newStr);
        std::cout << "Expresión en notación postfix: " << sht_y << std::endl;

        Tree* newTree = new Tree(sht_y);
        newTree->calcNullable(newTree->getRoot());
        newTree->calclFirstPos(newTree->getRoot());
        newTree->calcLastPos(newTree->getRoot());
        newTree->display(newTree->getRoot());
        newTree->computeFollowPos(newTree->getRoot());
        newTree->displayFollowPos();
        newTree->getIdValues(newTree->getRoot());
        newTree->displayIDValues();
        newTree->convertToAFD();

        // Definir AFD 
        std::unordered_map<std::string, Estado> estados = {
            {"q0", Estado("q0", 0)}, {"q1", Estado("q1", 1)},
            {"q2", Estado("q2", 2)}, {"q3", Estado("q3", 3)},
            {"q4", Estado("q4", 4)}, {"q5", Estado("q5", 5)}
        };
        std::vector<std::string> Alfabeto = {"a", "b"};
        AFD automata("q0", {4,5}, Alfabeto, estados);

        // Definir transiciones
        automata.agregarTransicion("q0", "a", "q2");
        automata.agregarTransicion("q0", "b", "q1");
        automata.agregarTransicion("q1", "a", "q1");
        automata.agregarTransicion("q1", "b", "q1");
        automata.agregarTransicion("q2", "a", "q4");
        automata.agregarTransicion("q2", "b", "q3");
        automata.agregarTransicion("q3", "a", "q4");
        automata.agregarTransicion("q3", "b", "q3");
        automata.agregarTransicion("q4", "a", "q1");
        automata.agregarTransicion("q4", "b", "q5");
        automata.agregarTransicion("q5", "a", "q1");
        automata.agregarTransicion("q5", "b", "q5");

        std::cout << "\nTransiciones antes de la minimización:" << std::endl;
        automata.mostrarTransiciones();
        automata.minimizarAFD();
        std::cout << "\nTransiciones después de la minimización:" << std::endl;
        automata.mostrarTransiciones();

        for (const std::string& cadena : config.cadenas) {
            if (automata.acept_Chain(cadena)) {
                std::cout << "La cadena '" << cadena << "' es aceptada por el AFD.\n";
                automata.generarDot("afd_visual");
                automata.generarImagen("afd_visual");
            } else {
                std::cout << "La cadena '" << cadena << "' no es aceptada por el AFD.\n";
            }
        }
    }

    return 0;
}