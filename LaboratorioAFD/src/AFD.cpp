#include <vector>
#include <string>
#include <unordered_set>
#include <iostream>








class AFD {
public:
    AFD(const std::vector<char>& alfabeto, const std::string& estadoInicial, const std::vector<std::string>& estadosFinales) 
        : Alfabeto_(alfabeto), q0(estadoInicial), F_(estadosFinales), state_count(0) {}

    void setQ0(const std::string& nuevoQ0) {
        q0 = nuevoQ0;
    }

    void setQF(const std::vector<std::string>& nuevosQF) {
        F_ = nuevosQF;
    }

private:
    std::vector<char> Alfabeto_;
    std::string q0;
    std::vector<std::string> F_;
    int state_count;
};


/*
#include <iostream>
#include <unordered_map>
#include <string>

int main() {
    
    std::unordered_map<std::string, std::unordered_map<char, std::string>> transiciones;
    
   
    transiciones["q0"]['a'] = "q1";
    
   
    std::string estadoInicial = "q0";
    char valor = 'a';
    
    
    if (transiciones.find(estadoInicial) != transiciones.end() &&
        transiciones[estadoInicial].find(valor) != transiciones[estadoInicial].end()) {
        std::string estadoFinal = transiciones[estadoInicial][valor];
        std::cout << "Desde el estado '" << estadoInicial << "', con el valor '" 
                  << valor << "', se transita a '" << estadoFinal << "'.\n";
    } else {
        std::cout << "No existe transición definida para ese estado y valor.\n";
    }
    
    return 0;
}
*/