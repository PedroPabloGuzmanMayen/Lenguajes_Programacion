#include <stdio.h>
#include <unistd.h>
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

char* add_concatenation(char* expression){
    char operators[4] = {'*', '|', '(', ')'};

    for (int i=0; &expression[i] != "\0"; i++){

        

    }


}

