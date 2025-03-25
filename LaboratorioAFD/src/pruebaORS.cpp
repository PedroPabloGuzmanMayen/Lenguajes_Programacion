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
    int profundidad_parentesis = 0;
    
    while (i < len) {
        if (input[i] == '[') {
            // Procesar rangos [ ... ]
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
            profundidad_parentesis++;
            for (int j = 0; expanded[j]; j++) {
                output[out_i++] = expanded[j];
            }
            output[out_i++] = ')';
            profundidad_parentesis--;
            i++;
        } else if (input[i] == '\'') {  // caso para comillas simples
            // Procesar caracteres entre comillas simples, ej: 'E'
            i++; // Saltar la primera comilla
            if (i >= len) break;

            char c = input[i++]; // Leer el carácter dentro de las comillas

            // Manejar escapes simples, ej: '\n'
            if (c == '\\') {
                if (i >= len) break;
                c = interpret_escape(input[i++]);
            }

            // Saltar la comilla de cierre si existe
            if (i < len && input[i] == '\'') i++;

            output[out_i++] = c; // Escribir el carácter sin comillas
        }   
         else {
            // Copiar otros caracteres directamente
            output[out_i++] = input[i++];
        }
    }

    while (profundidad_parentesis > 0) {    
        output[out_i++] = ')';
        profundidad_parentesis--;
    }
    output[out_i] = '\0';
}

void expand_internal_patterns(char* expr) {
    char buffer[MAX_EXPR] = "";
    int i = 0, j = 0;
    int len = strlen(expr);

    while (i < len) {
        if (isalnum(expr[i]) || expr[i] == '_') {
            // Manejar identificadores seguidos de + o ?
            char token[MAX_NAME] = "";
            int k = 0;
            while (isalnum(expr[i]) || expr[i] == '_') {
                token[k++] = expr[i++];
            }
            token[k] = '\0';

            if (expr[i] == '+') {
                j += sprintf(buffer + j, "%s(%s)*", token, token);
                i++;
            } else if (expr[i] == '?') {
                j += sprintf(buffer + j, "(%s|\x02)", token);
                i++;
            } else {
                j += sprintf(buffer + j, "%s", token);
            }
        } else if (expr[i] == ')') {
            buffer[j++] = expr[i++];
            // Verificar si después de ')' hay un operador
            if (i < len && (expr[i] == '+' || expr[i] == '?')) {
                char op = expr[i++];
                // Buscar el '(' correspondiente en el buffer
                int balance = 1;
                int k = j - 2; // posición antes de ')'
                while (k >= 0 && balance > 0) {
                    if (buffer[k] == ')') balance++;
                    else if (buffer[k] == '(') balance--;
                    k--;
                }
                if (balance == 0) {
                    k++; // k es el índice del '('
                    int group_len = (j - 1) - k;
                    char group[MAX_EXPR];
                    strncpy(group, buffer + k, group_len);
                    group[group_len] = '\0';

                    j = k; // Sobrescribir desde '('
                    if (op == '?') {
                        j += sprintf(buffer + j, "(%s|\x02)", group);
                    } else if (op == '+') {
                        j += sprintf(buffer + j, "%s(%s)*", group, group);
                    }
                } else {
                    // Paréntesis no balanceados, dejar como está
                    buffer[j++] = op;
                }
            }
        } else {
            buffer[j++] = expr[i++];
        }
    }

    buffer[j] = '\0';
    strcpy(expr, buffer);
}


void expand_single_expression(const char* expr, char* output) {
    char expanded[MAX_EXPR];

    // Expandimos primero (rangos, comillas, etc.)
    if (expr[0] == '[') {
        expand_expression(expr, expanded);
    } else {
        expand_embedded_ranges(expr, expanded);
    }

    // Regla: X+ → X(X)*
    // Regla: X? → (X|ε) dejaremos vacio aca. 
    int len = strlen(expanded);

    char transformada[MAX_EXPR];

    if (len > 1 && expanded[len - 1] == '+') {
        // Regla para +
        char base[MAX_NAME];
        strncpy(base, expanded, len - 1);
        base[len - 1] = '\0';
        sprintf(transformada, "%s(%s)*", base, base);

    } else if (len > 1 && expanded[len - 1] == '?') {
        // Regla para ?
        char base[MAX_NAME];
        strncpy(base, expanded, len - 1);
        base[len - 1] = '\0';
        sprintf(transformada, "(%s|\x02)", base); // aca lo estamos dejando vacio porque luego los espacios vacios nos encargamos de reemplazarlos por epsilon

    } else {
        strcpy(transformada, expanded);
    }

    // Envolver en paréntesis si contiene '|', y no lo está ya
    if (strchr(transformada, '|') && transformada[0] != '(') {
        sprintf(output, "(%s)", transformada);
    } else {
        strcpy(output, transformada);
    }


    // Expandir X+ y X? dentro de la expresión
    expand_internal_patterns(output);
    // para verificar que no haya parentesis sin cerrar
    int balance = 0;
    for (int i = 0; output[i]; i++) {
        if (output[i] == '(') balance++;
        else if (output[i] == ')') balance--;
    }
    
    // agrega cualquier parentis que falte
    while (balance > 0) {
        strcat(output, ")");
        balance--;
    }
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


int main() {
    // Expresiones a expandir
    const char* expresiones[] = {
        "['\x17''\x15']",
        "delim+",
        "['A'-'Z''a'-'z']",
        "(_)*",
        "digit+(letter|digit)*",
        "digit+",
        "letter(letter|str|digit)*",
        "digits(.digits)?('E'['+''-']?digits)?"
    };

    for (int i = 0; i < sizeof(expresiones) / sizeof(expresiones[0]); i++) {
        char resultado[MAX_EXPR];
        expand_single_expression(expresiones[i], resultado);

        // Convertir a std::string para reemplazo visual
        //std::string corregida = resultado; //si quieres ver el caracter descomenta esto
        //reemplazar_manual(corregida, "\x02", "ε"); //esto tambien descomentalo


        printf("Expresión original: %s\n", expresiones[i]);
        printf("Expresión expandida: %s\n\n", resultado); //esto comentalo

        //printf("Expresión expandida: %s\n\n", corregida.c_str()); // y esto tambien descomentalo
    }

    return 0;
}
