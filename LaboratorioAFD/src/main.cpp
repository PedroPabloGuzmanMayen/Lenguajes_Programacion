#include <iostream>
#include <string>
#include <unistd.h>
#include <unordered_map>
#include "shunting_yard.h"
#include "tree.h"
#include "node.h"
#include "AFD.h"
#include "lector.h"
#include <unordered_set>
#include <vector>
#include <map>
#include "lector_yal.h"
#include "Regla_Tokens.h"
#include "outuput_file.h"
#include "buffer.h"
#include "constantes.h"
#include "pruebaORS.h"


bool isInFinalStates(const std::map<std::set<int>, char>& terminators, const std::set<int>& state) {
    return terminators.find(state) != terminators.end();
}


int main(int argc, char* argv[]) {

    string contenido, nombreArchivo;

    nombreArchivo = "Tokens.txt";

    std::string  nombreArchivo_lectura = argv[1]; 

    // Leer expresiones y cadenas desde YAML

    ReglasTokens reglasTokens;
    reglasTokens = reglas_tokens();

        std::string valor_expresion = reglasTokens.generarExpresion();
        std::string my_str_copy = valor_expresion;
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
        std::map<std::string, char> estado_terminador; //Se usa para guardar el mapeo del estado y su símbolo terminador correspondiente
        std::unordered_map<std::string, Estado> estados;
        for (const auto& state : findedStates) {
            std::string q = "q";
            q+= std::to_string(stateNum);  
            if (isInFinalStates(terminators, state)){
                estado_terminador[q] = terminators[state];
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
       




        ///aqui vamos a cargar todo

        


        std::map<char, std::string> tokensYLexemas;
       
        

        for (const auto& regla : reglasTokens.obtenerReglas()) {
            char identificador = regla.identificador[0];  // Obtiene el primer carácter
            std::string token = regla.token;  // El token de la regla
    
            //std::cout << "Token: " <<  token<< " Identificador"<< identificador<< std::endl;
            // Insertar en el std::map
            tokensYLexemas[identificador] = token;
        }

        

        std::vector<std::pair<std::string, std::string>> resultadofinal = automata.analizarCadena(estado_terminador, tokensYLexemas, "ads 55    ++++------    ");

        
        //minimizamos

        
        
        //automata.depurarAFD();

        automata.generarDot("afd_visual_min");
        automata.generarImagen("afd_visual_min");
        


        

        std::cout<<"============MINIMIZADO===========\n";
        //automata.minimizarAFD();
        
        //automata.depurarAFD();



        /// aqui voy a escribir en el outuput

        Buffer* buffer = new Buffer(nombreArchivo_lectura, 10);
        string resultado;

        while (buffer->FLAG_SALIDA) {
            string linea = buffer->obtenerSiguienteLinea();
            if (!linea.empty()) {
                std::vector<std::pair<std::string, std::string>> resultadofinal = automata.analizarCadena(estado_terminador, tokensYLexemas, linea);
                string to_write = "";
                string the_token = "";
        
                // Recorrer en orden inverso el vector resultadofinal
                for (auto it = resultadofinal.rbegin(); it != resultadofinal.rend(); ++it) {
                    const auto& [token, lexema] = *it;  // Desempaquetar el par
                    the_token = token;
                    string lexema_d;
                    lexema_d = lexema;
                    
                    reemplazar_manual(lexema_d, PUNTO_s, ".");
                    reemplazar_manual(lexema_d, RPARENTESIS_s, ")");
                    reemplazar_manual(lexema_d, LPARENTESIS_s, "(");
                    reemplazar_manual(lexema_d, TIMES_s, "*");
                    
                    
                    


                    


                    to_write = "["+the_token+","+lexema_d+"]" + to_write;
                    //std::cout << "Token: " << token << ", Lexema: " << lexema << std::endl;
                    
                }
        
                escribirArchivo(to_write, nombreArchivo);  // Escribe los tokens en el archivo
            }
            
        }
    
        std::cout << "Probando un número en notación científica (3.5E-3): " 
                << automata.acept_Chain("3%6E-3") << std::endl;

        std::cout << "Probando un número decimal (3.6): " 
                << automata.acept_Chain("36%55") << std::endl;

        std::cout << "Probando un número entero (3): " 
                << automata.acept_Chain("3") << std::endl;

    
    std::cout<<"Valor de la variable: "<<valor_expresion;    
        
    

    return 0;
}

