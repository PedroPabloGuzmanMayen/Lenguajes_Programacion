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
private:
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
        for (const std::string& state : current_states) {
            if (Q_.find(state) != Q_.end() && F_.count(Q_.at(state).numero)) {
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
        for (const auto& grupo : P) {
            std::string rep = *grupo.begin();
            for (const std::string& q : grupo) {
                representante[q] = rep;
            }
        }
        std::unordered_map<std::string, std::unordered_map<std::string, std::string>> newS_;
        std::unordered_set<int> newF_;
        std::string newQ0 = representante[q0];
        
        for (const auto& [q, trans] : S_) {
            std::string repQ = representante[q];
            for (const auto& [sym, dest] : trans) {
                newS_[repQ][sym] = representante[dest];
            }
        }
        for (const auto& f : F_) {
            for (const auto& [q, estado] : Q_) {
                if (estado.numero == f) {
                    newF_.insert(Q_[representante[q]].numero);
                }
            }
        }
        S_ = newS_;
        F_ = newF_;
        q0 = newQ0;
        Q_.clear();
        for (const auto& p : newS_) {
            Q_[p.first] = Estado(p.first, std::stoi(p.first.substr(1))); 
        }
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

// int main() {
   
//     std::unordered_map<std::string, Estado> estados = {
//         {"q0", Estado("q0", 0)},
//         {"q1", Estado("q1", 1)},
//         {"q2", Estado("q2", 2)},
//         {"q3", Estado("q3", 3)},
//         {"q4", Estado("q4", 4)},
//         {"q5", Estado("q5", 5)}
//     };



//     std::vector<std::string> Alfabeto = {"a", "b"};
//     AFD automata("q0", {4,5}, Alfabeto, estados);

//     automata.agregarTransicion("q0", "a", "q2");
//     automata.agregarTransicion("q0", "b", "q1");

//     automata.agregarTransicion("q1", "a", "q1");
//     automata.agregarTransicion("q1", "b", "q1");
    

//     automata.agregarTransicion("q2", "a", "q4");
//     automata.agregarTransicion("q2", "b", "q3");

//     automata.agregarTransicion("q3", "a", "q4");
//     automata.agregarTransicion("q3", "b", "q3");

//     automata.agregarTransicion("q4", "a", "q1");
//     automata.agregarTransicion("q4", "b", "q5");

//     automata.agregarTransicion("q5", "a", "q1");
//     automata.agregarTransicion("q5", "b", "q5");

    
    

//     automata.mostrarTransiciones();
//     automata.minimizarAFD();
//     automata.mostrarTransiciones();

//     std::string cadena = "abab";
//     if (automata.acept_Chain(cadena)) {
//         std::cout << "La cadena '" << cadena << "' es aceptada por el AFD.\n";
//             automata.generarDot("afd_visual");
//             automata.generarImagen("afd_visual");

//     } else {
//         std::cout << "La cadena '" << cadena << "' no es aceptada por el AFD.\n";
//     }


//     return 0;
// }
