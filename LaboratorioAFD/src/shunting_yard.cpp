#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <string>
#include <set>
#include <algorithm>
#include <map>
#include <vector>
#include <stack>
#include "shunting_yard.h"

char operators[5] = {'*', '|', '(', ')', '.'};

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
    //printf("Adding concatenation...\n");
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

std::string shunting_yard(std::string& expression) {
    std::string out;
    std::stack<char> holding;
    std::map<char, int> operators_precedence = {{'|', 1}, {'.', 2}, {'*', 3}};

    for (int i = 0; i < expression.length(); i++) {
        if (!is_present(expression[i], operators)) {
            out += expression[i];
        }
        else if (expression[i] == '('){
            holding.push(expression[i]);
        }
        else if (expression[i] == ')') {
            while (!holding.empty() && holding.top() != '(') {
                out += holding.top();
                holding.pop();
            }
            if (!holding.empty() && holding.top() == '(') {
                holding.pop();
            }
        }
        else {
            while (!holding.empty() && operators_precedence[holding.top()] >= operators_precedence[expression[i]]) {
                out += holding.top();
                holding.pop();
            }
            holding.push(expression[i]);
        }
    }

    while (!holding.empty()) {
        out += holding.top();
        holding.pop();
    }

    return out;
}

std::vector<std::string> getAlphabet(std::string& expression){
    std::vector<std::string> newSet;
    for (int i = 0; i< expression.length(); i++){
        if (!is_present(expression[i], operators) && expression[i] != '#' && std::find(newSet.begin(), newSet.end(), std::string(1, expression[i])) == newSet.end() ){
            newSet.push_back(std::string(1, expression[i]));
        }
    }

    return newSet;
}

std::string parse_expression(std::string expression){
    bool flag = false; //Esta flag nos ayuda a saber si estamos en la expresión y no en el terminador
    std::string not_terminator = ""; //Aquí iremos guardando los valores de los caracteres que no sean terminadores
   
    for (int i = 0; i < expression.length(); i++){
        if (expression[i] == '['){
            flag = true; //Los corchetes indican que estamos en una expresión y no en un terminador
        }
        else if (flag == true && expression[i] != ']'){ //Si estamos en una expresión y no en un terminador, agregamos el caracter a la expresion
            not_terminator += expression[i];
        }
        else if (flag == true && expression[i] == ']'){
            flag = false; //Indicamos que  ya no estamos analizando una expresión y que empezaremos a agregar el terminador
            not_terminator = add_concatenation(not_terminator); //Agregamos la concatenación implícita
            not_terminator = shunting_yard(not_terminator); //La convertimos a postfix
            not_terminator += '.'; //Agregamos la concatenación para el terminador
        }

        else if (flag == false && expression[i] != ']' && expression[i] != '[' && expression[i] != '|'){ //Con esto agreamos el terminador a la expresión
            not_terminator += expression[i];
        }
        else if (flag == false && expression[i] == '|'){ //Con esto nos aseguramos de que es un or entre expresiones
            not_terminator += "."; //Argegamos la concatenación del terminador
            not_terminator += expression[i];
        }

    }

    return not_terminator; //Retornamos la regex parseada

}



