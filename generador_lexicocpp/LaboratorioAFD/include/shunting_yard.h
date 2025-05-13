#ifndef SHUNTING_YARD_H
#define SHUNTING_YARD_H
#include <string>
#include <set>
#include <vector>

std::string add_concatenation(std::string& expression);
std::string shunting_yard(std::string& expression);
std::vector<std::string> getAlphabet(std::string& expression);
#endif
