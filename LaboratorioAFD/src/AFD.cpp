#include <iostream>
#include <vector>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <fstream>
#include <cstdlib>
#include <list>
#include "AFD.h"



    AFD::AFD(std::string estadoInicial, 
        const std::vector<int>& estadosFinales,
        const std::vector<std::string>& alfabeto,
        const std::unordered_map<std::string, Estado> & estados ) : 
            q0(estadoInicial), 
            F_(estadosFinales.begin(), estadosFinales.end()),
            Alfabeto(alfabeto.begin(), alfabeto.end()),
            Q_(estados.begin(), estados.end())
        {}


    void AFD::agregarTransicion(const std::string& estado, const std::string& simbolo, const std::string& nuevoEstado) {
        S_[estado][simbolo] = nuevoEstado;
    }
    
    /* --- Parámetros ---
        - Cadena: un string que es la cadena que se debe recorrer
        - TokenList: un map con todos token y sus respectivos terminadores
        - Terminator_State: un map con el string del estado y su respectivo terminador
    */
   
    std::vector<std::map<std::string, std::string>> AFD::findTokens(std::string cadena, std::map<int, char> Terminator_State, 
    std::map<char, std::string> tokens ){
        std::string current = "q0"; //Iniciar en el estado inicial
        std::string lexeme = "";
        std::vector<std::map<std::string, std::string>> result;
        for (int i = 0; i < cadena.length(); i++){
            current = S_[current][std::string() + cadena[i]]; //Hallar el siguiente estado con el símbolo dado
            //Verificamos el int correspondiente del nuevo estado
            auto it = Q_.find(current);
            int numeroDeEstado = it->second.numero; // Guardamos el número de estado
            if (F_.find(numeroDeEstado) != F_.end()) { //Verifiamos si el nuevo estado es un estado final
                //Si el nuevo estado es un estado final
                result.push_back({{tokens[Terminator_State[numeroDeEstado]], lexeme}});
                lexeme = ""; //Limpiar el lexema 
            } 
        }
        return result;
    }
    
    
    

    
    std::vector<std::string> AFD::move_AFD(const std::vector<std::string>& states, const std::string& symbol) {
        std::unordered_set<std::string> nuevosEstados;

        for (const std::string& state : states) {
            if (S_.find(state) != S_.end() && S_[state].find(symbol) != S_[state].end()) {
                nuevosEstados.insert(S_[state][symbol]);
            }
        }

        return std::vector<std::string>(nuevosEstados.begin(), nuevosEstados.end());
    }

   
    bool AFD::acept_Chain(const std::string& w) {
        std::vector<std::string> current_states = {q0};
        for (char symbol : w) {
            current_states = move_AFD(current_states, std::string(1, symbol));
        }
    
        // Depuración antes del 'if'
        for (const std::string& state : current_states) {
           
            if (Q_.find(state) != Q_.end() && F_.count(Q_.at(state).numero)) {
                return true;
            }
        }
    
        return false;
    }

    std::vector<std::pair<std::string, std::string>> AFD::analizarCadena(
        const std::map<std::string, char>& estadosAceptacion,
        const std::map<char, std::string>& terminadorToken,
        const std::string& entrada) {
        
        std::vector<std::pair<std::string, std::string>> tokens;
        std::vector<std::string> current_states = {q0};
        std::string lexema;
        bool tokenFound = false;
    
        for (size_t i = 0; i < entrada.length(); ++i) {
            char symbol = entrada[i];
            //if (std::isspace(symbol) && lexema.empty()) continue;
            lexema += symbol;
            //std::cout << "\nProcesando símbolo: " << symbol << std::endl;
            std::cout << "Estados actuales: ";
            for (const auto& s : current_states) std::cout << s << " ";
            current_states = move_AFD(current_states, std::string(1, symbol));
            
            for (const std::string& state : current_states) {
                if (estadosAceptacion.find(state) != estadosAceptacion.end()) {
                    char terminador = estadosAceptacion.at(state);
                    if (terminadorToken.find(terminador) != terminadorToken.end()) {
                        std::string token = terminadorToken.at(terminador);
                        std::cout << "✅ Estado de aceptación encontrado: " << state << " -> Token: " << token << " Terminador asociado: "<< terminador << std::endl;
                        
                        size_t lookAhead = i + 1;
                        while (lookAhead < entrada.length()) {
                            std::vector<std::string> nextStates = move_AFD(current_states, std::string(1, entrada[lookAhead]));
                            bool stillValid = false;
                            
                            for (const std::string& nextState : nextStates) {
                                if (estadosAceptacion.find(nextState) != estadosAceptacion.end()) {
                                    lexema += entrada[lookAhead];
                                    current_states = nextStates;
                                    stillValid = true;
                                    break;
                                }
                            }
                            
                            if (!stillValid) break;
                            lookAhead++;
                        }
                        tokens.emplace_back(token, lexema);
                        i = lookAhead - 1;
                        lexema.clear();
                        current_states = {q0};
                        tokenFound = true;
                        break;
                    }
                }
            }
        }
    
        return tokens;
    }
    
    

    void AFD::depurarAFD() {
        std::cout << "Estado inicial: " << q0 << std::endl;
        std::cout << "Estados finales:\n";
        for (int f : F_) std::cout << "  q" << f << "\n";
        std::cout << "Transiciones:\n";
        for (const auto& [estado, transiciones] : S_) {
            for (const auto& [simbolo, destino] : transiciones) {
                std::cout << "  " << estado << " --(" << simbolo << ")--> " << destino << "\n";
            }
        }
    }

    void AFD::generarDot(const std::string& nombreArchivo) {
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
        for (const auto& estado : S_) {
            for (const auto& transicion : estado.second) {
                archivo << "    " << estado.first << " -> " << transicion.second << " [label=\"" << transicion.first << "\"];\n";
            }
        }

        archivo << "}\n";
        archivo.close();

        std::cout << "Archivo " << nombreArchivo << ".dot generado correctamente.\n";
    }

    void AFD::generarImagen(const std::string& nombreArchivo) {  
        std::string comando = "dot -Tpng " + nombreArchivo + ".dot -o " + nombreArchivo + ".png";
        int resultado = system(comando.c_str());

        if (resultado == 0) {
            std::cout << "Imagen " << nombreArchivo << ".png generada correctamente.\n";
        } else {
            std::cerr << "Error al generar la imagen.\n";
        }
    }

    void AFD::mostrarTransiciones() {
        std::cout << "Transiciones del AFD:" << std::endl;
        for (const auto& [estado, transiciones] : S_) {
            for (const auto& [simbolo, destino] : transiciones) {
                std::cout << estado << " --(" << simbolo << ")--> " << destino << std::endl;
            }
        }
        std::cout << std::endl;
    }

    void AFD::reconstruirAFD(const std::vector<std::unordered_set<std::string>>& P) {
        std::unordered_map<std::string, std::string> representante;
    
        // Asignar representantes a cada conjunto de estados equivalentes
        for (const auto& grupo : P) {
            if (!grupo.empty()) {
                std::string rep = *grupo.begin();
                for (const std::string& q : grupo) {
                    representante[q] = rep;
                }
            }
        }
    
        // Verificar si el estado inicial tiene un representante válido
        if (representante.find(q0) == representante.end()) {
            std::cerr << "Error: No se encontró representante para el estado inicial.\n";
            return;
        }
        std::string newQ0 = representante[q0];
    
        std::unordered_map<std::string, std::unordered_map<std::string, std::string>> newS_;
        std::unordered_set<int> newF_;
    
        // Construir nuevos estados
        Q_.clear();
        for (const auto& p : representante) {
            Q_[p.first] = Estado(p.first, std::stoi(p.first.substr(1)));  // Asignación segura del número
        }
    
        // Construir nuevas transiciones
        for (const auto& [q, trans] : S_) {
            if (representante.find(q) != representante.end()) {
                std::string repQ = representante[q];
                for (const auto& [sym, dest] : trans) {
                    if (representante.find(dest) != representante.end()) {
                        newS_[repQ][sym] = representante[dest];
                        
                    }
                }
            }
        }
    
        // Construir nuevos estados finales
        for (const auto& f : F_) {
            for (const auto& [q, estado] : Q_) {
                if (estado.numero == f && representante.find(q) != representante.end()) {
                    auto it = Q_.find(representante[q]);
                    if (it != Q_.end()) {
                        newF_.insert(it->second.numero);
                        
                    }
                }
            }
        }
    
        // Actualizar el AFD con la nueva estructura minimizada
        q0 = newQ0;
        F_ = newF_;
        S_ = newS_;
    
       
    }
    

    std::vector<std::unordered_set<std::string>> AFD::separarEstados() {
        std::unordered_set<std::string> aceptacion, noAceptacion;
        for (const auto& q : Q_) {
            if (F_.count(q.second.numero)) {
                aceptacion.insert(q.first);
            } else {
                noAceptacion.insert(q.first);
            }
        }
        return {noAceptacion, aceptacion};
    }

    void AFD::minimizarAFD() {
        std::vector<std::unordered_set<std::string>> P = separarEstados();
        std::vector<std::unordered_set<std::string>> W = P;
        
        while (!W.empty()) {
            auto A = W.back();
            W.pop_back();
            
            for (const std::string& s : Alfabeto) {
                std::unordered_set<std::string> X;
                for (const auto& q : Q_) {
                    if (S_.count(q.first) && S_[q.first].count(s) && A.count(S_[q.first][s])) {
                        X.insert(q.first);
                    }
                }
                
                for (auto it = P.begin(); it != P.end(); ++it) {
                    std::unordered_set<std::string> Y1, Y2;
                    for (const std::string& q : *it) {
                        if (X.count(q)) {
                            Y1.insert(q);
                        } else {
                            Y2.insert(q);
                        }
                    }
                    if (!Y1.empty() && !Y2.empty()) {
                        P.erase(it);
                        P.push_back(Y1);
                        P.push_back(Y2);
                        W.push_back(Y1.size() <= Y2.size() ? Y1 : Y2);
                        break;
                    }
                }
            }
        }
        reconstruirAFD(P);
    }


