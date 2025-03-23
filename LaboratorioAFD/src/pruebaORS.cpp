#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <string>
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

void expand_single_expression(const char* expr, char* output) {
    char expanded[MAX_EXPR];
    if (expr[0] == '[') {
        expand_expression(expr, expanded);
    } else {
        expand_embedded_ranges(expr, expanded);
    }
    strcpy(output, expanded);
}


void reemplazar_manual(std::string& expresion, const std::string& buscar, const std::string& reemplazo) {
    std::string resultado;
    size_t len_buscar = buscar.length();
    
    for (size_t i = 0; i < expresion.length(); ++i) {
        bool coincide = true;

        // Comparar manualmente carácter por carácter
        for (size_t j = 0; j < len_buscar; ++j) {
            if (i + j >= expresion.length() || expresion[i + j] != buscar[j]) {
                coincide = false;
                break;
            }
        }

        // Si coincide, agregar el reemplazo y saltar la longitud de `buscar`
        if (coincide) {
            resultado += reemplazo;
            i += len_buscar - 1; // Saltar los caracteres reemplazados
        } else {
            resultado += expresion[i];
        }
    }

    expresion = resultado;
}



// int main() {
//     // Expresiones a expandir
//     const char* expresiones[] = {
//         "['\x17''\x15']",
//         "delim+",
//         "['A'-'Z''a'-'z']",
//         "(_)*",
//         "['0'-'9']",
//         "digit+",
//         "letter(letter|str|digit)*",
//         "digits(.digits)?('E'['+''-']?digits)?"
//     };

//     for (int i = 0; i < sizeof(expresiones) / sizeof(expresiones[0]); i++) {
//         char resultado[MAX_EXPR];
//         expand_single_expression(expresiones[i], resultado);
//         printf("Expresión original: %s\n", expresiones[i]);
//         printf("Expresión expandida: %s\n\n", resultado);
//     }

//     return 0;
// }
