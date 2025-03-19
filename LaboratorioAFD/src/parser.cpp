
#include <iostream>
#include <vector>
#include <regex>

//Esta función sirve para hallar las regex
std::vector<std::string> extractBrackets(const std::string& input) {
    std::vector<std::string> result;
    std::regex pattern(R"(\[([^\]]+)\])"); //Con esto encontramos todo lo que esté dentro de corchetes
    std::smatch match;
    std::string str = input;
    
    while (std::regex_search(str, match, pattern)) {
        result.push_back(match[1]); // Agregamos lo que está dentro de los corchetes
        str = match.suffix().str(); // Seguimos buscando en el resto de la cadena
    }
    
    return result;
}




