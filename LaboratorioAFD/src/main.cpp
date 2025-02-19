#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include <string>
#include <shunting_yard.h>
#include "tree.h"
#include "node.h"
#include "AFD.cpp"

int main() {

    printf("Hello world!");
    std::string my_str = "(a|b)*abb#";
    std::string newStr = add_concatenation(my_str);
    std::cout << "Expresión con concatenación explícita: " << newStr << std::endl;

    std::string sht_y = shunting_yard(newStr);
    std::cout << "Expresión en notación postfix: " << sht_y << std::endl;

    Tree* newTree = new Tree(sht_y);
    newTree->calcNullable(newTree->getRoot());
    newTree->calclFirstPos(newTree->getRoot());
    newTree->calcLastPos(newTree->getRoot());
    newTree->display(newTree->getRoot());
    newTree->computeFollowPos(newTree->getRoot());
    newTree->displayFollowPos();

    return 0;
}
