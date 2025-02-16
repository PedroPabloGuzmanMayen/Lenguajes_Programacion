#include <stdio.h>
#include <unistd.h>
#include <string>
#include "shunting_yard.h"


bool is_present(char symbol, char arr[]){
    int arr_length = sizeof(arr) / sizeof(arr[0]);
    for (int i = 0; i < arr_length; i++ ){
        if (arr[i] == symbol){
            return true;
        }
    }

    return false;
}

std::string add_concatenation(std::string& expression){
    char operators[4] = {'*', '|', '(', ')'};
    std::string formated_string;
    //Caso 1: la expresión solo tiene un caracter
    if (expression.length() == 1) {
        if (is_present(expression[0], operators)){
            return std::string("Error: expresión no válida ");
        }
        else {
            return expression;  
        }
    }
    else {
        for (int i=0; i < expression.length(); i++){
            formated_string += expression[i];
            if (i+1 < expression.length()){
                if ((!is_present(expression[i], operators) || expression[i] == ')' || expression[i] == '*')&&(!is_present(expression[i+1], operators))){
                    formated_string += '.';
                }
            }
        }
        return formated_string;
    }
}

