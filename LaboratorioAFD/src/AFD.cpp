#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <fstream>
#include <cstdlib>
#include <list>

class Estado {
public:
    std::string nombre;
    int numero;
    Estado() = default;
    Estado(std::string nombre, int numero) : nombre(nombre), numero(numero) {}
};

class AFD {
public:
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> S_;
    std::string q0; 
    std::unordered_set<int> F_;
    std::vector<std::string> Alfabeto;
    std::unordered_map<std::string, Estado> Q_;

public:
    AFD(std::string estadoInicial, 
        const std::vector<int>& estadosFinales,
        const std::vector<std::string>& alfabeto,
        const std::unordered_map<std::string, Estado> & estados ) : 
            q0(estadoInicial), 
            F_(estadosFinales.begin(), estadosFinales.end()),
            Alfabeto(alfabeto.begin(), alfabeto.end()),
            Q_(estados.begin(), estados.end())
        {}


    void agregarTransicion(const std::string& estado, const std::string& simbolo, const std::string& nuevoEstado) {
        S_[estado][simbolo] = nuevoEstado;
    }

    
    std::vector<std::string> move_AFD(const std::vector<std::string>& states, const std::string& symbol) {
        std::unordered_set<std::string> nuevosEstados;

        for (const std::string& state : states) {
            if (S_.find(state) != S_.end() && S_[state].find(symbol) != S_[state].end()) {
                nuevosEstados.insert(S_[state][symbol]);
            }
        }

        return std::vector<std::string>(nuevosEstados.begin(), nuevosEstados.end());
    }

   
    bool acept_Chain(const std::string& w) {
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
    

    void depurarAFD() {
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
        for (const auto& estado : S_) {
            for (const auto& transicion : estado.second) {
                archivo << "    " << estado.first << " -> " << transicion.second << " [label=\"" << transicion.first << "\"];\n";
            }
        }

        archivo << "}\n";
        archivo.close();

        std::cout << "Archivo " << nombreArchivo << ".dot generado correctamente.\n";
    }

    void generarImagen(const std::string& nombreArchivo) {  
        std::string comando = "dot -Tpng " + nombreArchivo + ".dot -o " + nombreArchivo + ".png";
        int resultado = system(comando.c_str());

        if (resultado == 0) {
            std::cout << "Imagen " << nombreArchivo << ".png generada correctamente.\n";
        } else {
            std::cerr << "Error al generar la imagen.\n";
        }
    }

    void mostrarTransiciones() {
        std::cout << "Transiciones del AFD:" << std::endl;
        for (const auto& [estado, transiciones] : S_) {
            for (const auto& [simbolo, destino] : transiciones) {
                std::cout << estado << " --(" << simbolo << ")--> " << destino << std::endl;
            }
        }
        std::cout << std::endl;
    }

    void reconstruirAFD(const std::vector<std::unordered_set<std::string>>& P) {
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
    

    std::vector<std::unordered_set<std::string>> separarEstados() {
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

    void minimizarAFD() {
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




};