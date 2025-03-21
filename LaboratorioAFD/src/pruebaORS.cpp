#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_VAR 100
#define MAX_LINE 512
#define MAX_NAME 64
#define MAX_EXPR 2048

typedef struct {
    char name[MAX_NAME];
    char expression[MAX_EXPR];
} Variable;

Variable variables[MAX_VAR];
int var_count = 0;

char interpret_escape(char c) {
    switch (c) {
        case 'n': return '\n';
        case 't': return '\t';
        case '\\': return '\\';
        default: return c;
    }
}

void expand_range(const char* input, char* output) {
    int i = 0;
    int out_idx = 0;
    int len = strlen(input);

    // Quitar corchetes si los hay
    if (input[0] == '[' && input[len - 1] == ']') {
        i = 1;
        len -= 1;
    }

    while (i < len) {
        // Leer carácter (posiblemente escape)
        char a, b;
        if (input[i] == '\'') {
            i++;
            if (input[i] == '\\') {
                i++;
                a = interpret_escape(input[i++]);
            } else {
                a = input[i++];
            }
            i++; // cerrar '
        } else {
            i++;
            continue;
        }

        // Ver si es un rango
        if (input[i] == '-' && input[i + 1] == '\'') {
            i += 2;
            if (input[i] == '\\') {
                i++;
                b = interpret_escape(input[i++]);
            } else {
                b = input[i++];
            }
            i++; // cerrar '

            for (char c = a; c <= b; c++) {
                if (c == '\n') {
                    out_idx += sprintf(output + out_idx, "\\n|");
                } else if (c == '\t') {
                    out_idx += sprintf(output + out_idx, "\\t|");
                } else if (c == ' ') {
                    out_idx += sprintf(output + out_idx, "' '|");
                } else {
                    out_idx += sprintf(output + out_idx, "%c|", c);
                }
            }

        } else {
            // Es carácter individual
            if (a == '\n') {
                out_idx += sprintf(output + out_idx, "\\n|");
            } else if (a == '\t') {
                out_idx += sprintf(output + out_idx, "\\t|");
            } else if (a == ' ') {
                out_idx += sprintf(output + out_idx, "' '|");
            } else {
                out_idx += sprintf(output + out_idx, "%c|", a);
            }
        }
    }

    // Quitar último '|'
    if (out_idx > 0 && output[out_idx - 1] == '|') {
        output[out_idx - 1] = '\0';
    } else {
        output[out_idx] = '\0';
    }
}



void procesar_linea(const char* linea) {
    if (strncmp(linea, "let", 3) != 0) return;

    char nombre[MAX_NAME], expr[MAX_EXPR];
    if (sscanf(linea, "let %s = %[^\n]", nombre, expr) == 2) {
        Variable nueva;
        strcpy(nueva.name, nombre);

        if (expr[0] == '[') {
            char expandida[MAX_EXPR];
            expand_range(expr, expandida);
            strcpy(nueva.expression, expandida);
        } else {
            strcpy(nueva.expression, expr);
        }



        variables[var_count++] = nueva;
        printf("%s = %s\n", nueva.name, nueva.expression);
    }
}

void cargar_yal(const char* yal) {
    char linea[MAX_LINE];
    const char* ptr = yal;
    while (*ptr) {
        int i = 0;
        while (*ptr && *ptr != '\n' && i < MAX_LINE - 1) {
            linea[i++] = *ptr++;
        }
        if (*ptr == '\n') ptr++;
        linea[i] = '\0';
        procesar_linea(linea);
    }
}

void imprimir_variables() {
    printf("\n Variables almacenadas:\n");
    for (int i = 0; i < var_count; i++) {
        printf("%s = %s\n", variables[i].name, variables[i].expression);
    }
}

int main() {
    const char* contenido_yal =
        "let delim = [' ''\\t''\\n']\n"
        "let ws = delim+\n"
        "let letter = ['A'-'Z''a'-'z']\n"
        "let str = (_)*\n"
        "let digit = ['0'-'9']\n"
        "let digits = digit+\n"
        "let id = letter(letter|str|digit)*\n"
        "let number = digits(.digits)?('E'['+''-']?digits)?\n";

    cargar_yal(contenido_yal);
    imprimir_variables();

    return 0;
}