#include <iostream>
#include <vector>
#include <regex>
//Esta función sirve para hallar las regex
 
std::vector<std::string> extractBrackets(const std::string& input) {
    bool flag = false;
    std::string formated_string;
    std::vector<std::string> result;
    std::string str = input;
    for (int i = 0; i < str.size(); i++) {
        if (str[i] == '[') {
            flag = true;
        }
        else if (str[i] == ']') {
            flag = false;
            result.push_back(formated_string);
            formated_string = "";
        }
        else if (str[i] == '|' && flag == false) {
            continue;
        }
        else {
            formated_string += str[i]; 
        }
    }
    return result;
}