#ifndef LECTOR_YAL_H
#define LECTOR_YAL_H

#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include "Regla_Tokens.h"  // Asegúrate de que este esté incluido antes de usar ReglasTokens

// Declaración de la función que genera las reglas de tokens
ReglasTokens reglas_tokens();   // Ahora debería funcionar correctamente

// Declaración de las variables globales
extern std::unordered_map<std::string, std::string> var;
extern std::set<std::string> processed;

#endif // REGLAS_TOKENS_H
