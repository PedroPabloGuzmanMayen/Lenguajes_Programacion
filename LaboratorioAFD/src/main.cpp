#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include <string>
#include <shunting_yard.h>
#include "tree.h"
#include "node.h"

int main() {

    printf("Hello world!");
    std::string my_str = "(a|b)*aaaaabbbbbb(a|c)*";
    std::string newStr = add_concatenation(my_str);

    std::cout << newStr << std::endl;

    std::string sht_y = shunting_yard(newStr);

    Tree* newTree = new Tree(sht_y);
    newTree->calcNullable(newTree->getRoot());
    newTree->calclFirstPos(newTree->getRoot());
    newTree->display(newTree->getRoot());


    return 0;
}