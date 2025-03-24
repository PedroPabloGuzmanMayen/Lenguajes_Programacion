#ifndef EXPANSION_H
#define EXPANSION_H

#include <string.h>

// Definir los máximos valores para las variables
#define MAX_VAR 100
#define MAX_LINE 512
#define MAX_NAME 64
#define MAX_EXPR 2048

// Estructura para almacenar variables
typedef struct {
    char name[MAX_NAME];
    char expression[MAX_EXPR];
} Variable;

extern Variable variables[MAX_VAR];
extern int var_count;

// Declaraciones de funciones
char interpret_escape(char c);

void expand_expression(const char* input, char* output);
void expand_embedded_ranges(const char* input, char* output);
void expand_single_expression(const char* expr, char* output);

void reemplazar_manual(std::string& expresion, const std::string& buscar, const std::string& reemplazo);

#endif // EXPANSION_H
