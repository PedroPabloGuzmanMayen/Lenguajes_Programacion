#include <stdio.h>
#include <unistd.h>
#include <string>
#include <map>
#include <stack>
#include "shunting_yard.h"

char operators[4] = {'*', '|', '(', ')'};

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
                if ((!is_present(expression[i], operators) || expression[i] == ')' || expression[i] == '*')&&(
                    !is_present(expression[i+1], operators) || expression[i+1] == '(')){
                    formated_string += '.';
                }
            }
        }
        return formated_string;
    }
}

std::string shunting_yard(std::string& expression){

    std::string out;
    std::stack<char> holding;
    std::map <char, int> operators_precedence;
    operators_precedence['|'] = 1;
    operators_precedence['.'] = 2;
    operators_precedence['*'] = 3;

    for (int i = 0; i< expression.length(); i++){
        if (!is_present(expression[i], operators) || expression[i] == '('){
            out += expression[i];
        }
        else if (expression[i] == ')'){
            while (holding.top() != '('){
                out += holding.top();
                holding.pop();
            }
            holding.pop();

        }
        else {
            if (holding.empty()){
                holding.push(expression[i]);
            }
            else {
                if (operators_precedence[expression[i]] > operators_precedence[holding.top()]){
                    holding.push(expression[i]);
                }
                else {
                    while (operators_precedence[holding.top()] >= operators_precedence[expression[i]]){
                        out += holding.top();
                        holding.pop();
                    }
                    holding.push(expression[i]);   
                }
            }
        }
    }
    while (!holding.empty()) {
        out += holding.top();
        holding.pop();
    }

    return out;
}

