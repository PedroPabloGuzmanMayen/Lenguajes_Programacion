#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include <string>
#include <shunting_yard.h>

int main() {

    printf("Hello world!");
    std::string my_str = "a(bb)*c";
    std::string newStr = add_concatenation(my_str);

    std::cout << newStr << std::endl;

    std::string sht_y = shunting_yard(newStr);

    std::cout << sht_y << std::endl;

    return 0;
}