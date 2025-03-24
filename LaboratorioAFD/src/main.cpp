#include <iostream>
#include <string>
#include <unistd.h>
#include <unordered_map>
#include "shunting_yard.h"
#include "tree.h"
#include "node.h"
#include "AFD.cpp"
#include "lector.h"
#include <unordered_set>


bool isInFinalStates(const std::map<std::set<int>, char>& terminators, const std::set<int>& state) {
    return terminators.find(state) != terminators.end();
}


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
        newTree->displayAcceptedPos();
        auto [findedStates, accepted_states, DSTATES, alphabet, transitions, terminators] = newTree->convertToAFD();

        for (const auto& pair : terminators) {
            
            std::cout << "Set: {";
            for (auto it = pair.first.begin(); it != pair.first.end(); ++it) {
                if (it != pair.first.begin()) {
                    std::cout << ", ";  
                }
                std::cout << *it;
            }
            std::cout << "} : " << pair.second << std::endl;
        }

        //mapeamos los estados
        int stateNum = 0;
        std::map<int, std::set<int>> stateMap;
        std::map<int, char> estado_terminador; //Se usa para guardar el mapeo del estado y su símbolo terminador correspondiente
        std::unordered_map<std::string, Estado> estados;
        for (const auto& state : findedStates) {
            std::string q = "q";
            q+= std::to_string(stateNum);  
            if (isInFinalStates(terminators, state)){
                estado_terminador[stateNum] = terminators[state];
            }
            estados[q] = Estado(q, stateNum);
            stateMap[stateNum++] = state;
            
        }
        // Obtenemos estados de aceptacion
        std::unordered_set<int> mySet; 
        //std::map<std::set<int>, char> terminators;
        
        for (size_t i = 0; i < accepted_states.size(); ++i) {
            std::set<int> target = accepted_states[i];
            int key = -1;
            for (const auto& entry : stateMap) {
                if (entry.second == target) { 
                    key = entry.first;
                    break;
                }
            }
            mySet.insert(key);
        }


        std::vector<int> myVector(mySet.begin(), mySet.end());  // Convertir a vector

        AFD automata("q0",myVector, alphabet, estados);
 
 
        // Definir transiciones

        for (const auto& [state, symbolMap] : transitions) {
            
            std::set<int> target = state;
            int key = -1;
            for (const auto& entry : stateMap) {
                if (entry.second == target) { 
                    key = entry.first;
                    break;
                }
            }

            std::string q_from = "q";
            q_from+= std::to_string(key);

            for (const auto& [symbol, nextState] : symbolMap) {
                

                std::set<int> target = nextState;
                int key = -1;
                for (const auto& entry : stateMap) {
                    if (entry.second == target) { 
                        key = entry.first;
                        break;
                    }
                }
                std::string q_to = "q";
                q_to+= std::to_string(key);

                std::string str_q_from(q_from);
                std::string str_symbol(1,symbol);
                std::string str_q_to(q_to);   
                automata.agregarTransicion(str_q_from, str_symbol, str_q_to);


            }
        }
        
        

        
        for (const auto& pair : estado_terminador) {
            std::cout << "Estado: " << pair.first << " -> Terminador: " << pair.second << std::endl;
        }
        
        automata.depurarAFD();
        automata.generarDot("afd_visual");
        automata.generarImagen("afd_visual");
        for (const std::string& cadena : config.cadenas) {
            if (automata.acept_Chain(cadena)) {
                std::cout << "La cadena '" << cadena << "' es aceptada por el AFD.\n";
                
            } else {
                
                std::cout << "La cadena '" << cadena << "' no es aceptada por el AFD.\n";
            }
        }


        //minimizamos

        std::cout<<"============MINIMIZADO===========\n";
        automata.minimizarAFD();
        
        automata.depurarAFD();
        
        //automata.depurarAFD();

        automata.generarDot("afd_visual_min");
        automata.generarImagen("afd_visual_min");
        

        for (const std::string& cadena : config.cadenas) {
            if (automata.acept_Chain(cadena)) {
                std::cout << "La cadena '" << cadena << "' es aceptada por el AFD.\n";
                
            } else {
                
                std::cout << "La cadena '" << cadena << "' no es aceptada por el AFD.\n";
            }
        }
        
    }

    return 0;
}

