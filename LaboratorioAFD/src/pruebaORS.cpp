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

void expand_expression(const char* input, char* output) {
    int i = 0, out_idx = 0;
    int len = strlen(input);

    if (!(input[0] == '[' && input[len - 1] == ']')) {
        strcpy(output, input);
        return;
    }

    i = 1;
    len -= 1;

    while (i < len) {
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

            if (input[i] == '-' && input[i+1] == '\'') {
                i += 2;
                if (input[i] == '\\') {
                    i++;
                    b = interpret_escape(input[i++]);
                } else {
                    b = input[i++];
                }
                i++; // cerrar '
                for (char c = a; c <= b; c++) {
                    out_idx += sprintf(output + out_idx,
                        (c == '\n') ? "\\n|" :
                        (c == '\t') ? "\\t|" :
                        (c == ' ') ? "' '|"
                        : "%c|", c);
                }
            } else {
                out_idx += sprintf(output + out_idx,
                    (a == '\n') ? "\\n|" :
                    (a == '\t') ? "\\t|" :
                    (a == ' ') ? "' '|"
                    : "%c|", a);
            }
        } else if (input[i] == '"') {
            i++;
            while (i < len && input[i] != '"') {
                if (input[i] == '\\') {
                    i++;
                    switch (input[i]) {
                        case 'n': out_idx += sprintf(output + out_idx, "\\n|"); break;
                        case 't': out_idx += sprintf(output + out_idx, "\\t|"); break;
                        case 's': out_idx += sprintf(output + out_idx, "' '|"); break;
                        default:  out_idx += sprintf(output + out_idx, "\\%c|", input[i]); break;
                    }
                } else {
                    if (input[i] == ' ') {
                        out_idx += sprintf(output + out_idx, "' '|");
                    } else {
                        out_idx += sprintf(output + out_idx, "%c|", input[i]);
                    }
                }
                i++;
            }
            i++; // cerrar comillas
        } else {
            i++;
        }
    }

    if (out_idx > 0 && output[out_idx - 1] == '|') {
        output[out_idx - 1] = '\0';
    } else {
        output[out_idx] = '\0';
    }
}

void expand_embedded_ranges(const char* input, char* output) {
    int i = 0, out_i = 0;
    int len = strlen(input);

    while (i < len) {
        if (input[i] == '[') {
            int start = i;
            while (i < len && input[i] != ']') i++;
            if (i >= len) break;

            int end = i;
            char temp[128];
            strncpy(temp, input + start, end - start + 1);
            temp[end - start + 1] = '\0';

            char expanded[256];
            expand_expression(temp, expanded);

            output[out_i++] = '(';
            for (int j = 0; expanded[j]; j++) {
                output[out_i++] = expanded[j];
            }
            output[out_i++] = ')';

            i++;
        } else {
            output[out_i++] = input[i++];
        }
    }

    output[out_i] = '\0';
}

void procesar_linea(const char* linea) {
    if (strncmp(linea, "let", 3) != 0) return;

    char nombre[MAX_NAME], expr[MAX_EXPR];
    if (sscanf(linea, "let %s = %[^\n]", nombre, expr) == 2) {
        Variable nueva;
        strcpy(nueva.name, nombre);

        char expandida[MAX_EXPR];
        if (expr[0] == '[') {
            expand_expression(expr, expandida);
        } else {
            expand_embedded_ranges(expr, expandida);
        }

        strcpy(nueva.expression, expandida);
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
    printf("\nVariables almacenadas:\n");
    for (int i = 0; i < var_count; i++) {
        printf("%s = %s\n", variables[i].name, variables[i].expression);
    }
}

/*
int main() {
    const char* contenido_yal =
        "let delim = [\"\\s\\t\\n\"]\n"
        "let ws = delim+\n"
        "let letter = ['A'-'Z''a'-'z']\n"
        "let str = (_)*\n"
        "let digit = [\"0123456789\"]\n"
        "let digits = digit+\n"
        "let id = letter(letter|str|digit)*\n"
        "let number = digits(.digits)?('E'['+''-']?digits)?\n";

    cargar_yal(contenido_yal);
    imprimir_variables();

    return 0;
}
*/