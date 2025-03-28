#include <iostream>
#include <vector>
#include <unordered_map>
#include "AFD.h"
#include "buffer.h"
#include "Regla_Tokens.h"
#include <set>
#include "pruebaORS.h"
#include <string>
#include "constantes.h"
#include "lector_yal.h"

std::vector<std::string> alfabetoGriego = {
     "\x03", "\x04", "\x05", "\x06", "\x07", "\x08", "\x09",
     "\x13", "\x14", "\x15",
    "\x16", "\x17", "\x18", "\x19",
};


// std::vector<std::string> alfabetoGriego = {
//     "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ",
//     "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ", 
//     "φ", "χ", "ψ", "ω"
// };

std::unordered_map<std::string, std::string> var;

std::set<std::string> processed;
std::vector<std::string> generarAlfabeto() {
    std::vector<std::string> alfabeto;
    for (char c = 'a'; c <= 'z'; ++c) alfabeto.push_back(std::string(1, c));
    for (char c = 'A'; c <= 'Z'; ++c) alfabeto.push_back(std::string(1, c));
    for (char c = '0'; c <= '9'; ++c) alfabeto.push_back(std::string(1, c));

    alfabeto.push_back("[");
    alfabeto.push_back("]");
    alfabeto.push_back("'");
    alfabeto.push_back("=");
    alfabeto.push_back("+");
    alfabeto.push_back("+");
    alfabeto.push_back("ε");
    alfabeto.push_back("\t");
    alfabeto.push_back("\n");
    alfabeto.push_back("*");
    alfabeto.push_back("(");
    alfabeto.push_back(")");
    alfabeto.push_back("_");
    alfabeto.push_back("\x7F");
    alfabeto.push_back("\\");
    alfabeto.push_back("-");
    alfabeto.push_back("|");
    alfabeto.push_back("ε");
    alfabeto.push_back("?");
    alfabeto.push_back(".");
    alfabeto.push_back(":");
    alfabeto.push_back("<");
    alfabeto.push_back(">");
    alfabeto.push_back("/");
    alfabeto.push_back("\"");
    alfabeto.push_back("\x1A");
    alfabeto.push_back("\x1D");

    return alfabeto;
}

ReglasTokens reglas_tokens() {
    
    ReglasTokens reglasTokens;
    
    

    std::string estadoInicial = "q0";
    std::vector<int> estadosFinales = {3, 4, 5, 6, 7, 8};  
    std::vector<std::string> alfabeto = generarAlfabeto();

    std::unordered_map<std::string, Estado> estados = {
        {"q0", Estado("q0", 0)},  
        {"q1", Estado("q1", 1)},  
        {"q2", Estado("q2", 2)},  
        {"q3", Estado("q3", 3)},  
        {"q4", Estado("q4", 4)},  
        {"q5", Estado("q5", 5)},  
        {"q6", Estado("q6", 6)},  
        {"q7", Estado("q7", 7)},  
        {"q8", Estado("q8", 8)}   
    };

    AFD automata(estadoInicial, estadosFinales, alfabeto, estados);

    automata.agregarTransicion("q0", "l", "q1");
    automata.agregarTransicion("q1", "e", "q2");
    automata.agregarTransicion("q2", "t", "q3"); 

    std::string alfabetoCompleto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_*?.;-|[]+():/<>'=ε\"\x7F\\\x1A\x1D";

    // Transiciones para todo el alfabeto
    for (char c : alfabetoCompleto) {
        automata.agregarTransicion("q0", std::string(1, c), "q4");
        automata.agregarTransicion("q4", std::string(1, c), "q4");
    }

    
    

    std::vector<std::string> caracteres ;
    std::vector<std::string> caracteres_no_limpio ;

    //caracteres_no_limpio = buffer.caracteres;

    
    



    std::string cadenaActual = "";
    std::vector<std::string> tokens;
    bool dentroCorchetes = false;
    bool dentroComentario = false;


    //Primero aqui vamos a quitar los comentarios
    Buffer* buffer = nullptr;

    buffer = new Buffer("../slr.yal", 10);

    string caracter;
    while (buffer->FLAG_SALIDA) {
        buffer->cargar_buffer();
        while (buffer->FLAG_SALIDA) {
            caracter = buffer->obtenerSiguienteCaracter();
            if (caracter.empty()) break;

            

          
            if (caracter == "(") {
                string siguiente = buffer->obtenerSiguienteCaracter();
                if (siguiente == "*") {
                    dentroComentario = true;  
                    continue; 
                } else {
                    caracteres.push_back(caracter);
                    caracteres.push_back(siguiente);
                    continue;
                }
            }

            // Si estamos dentro del comentario, ignoramos los caracteres hasta encontrar "*)"
            if (dentroComentario) {
                if (caracter == "*" && buffer->obtenerSiguienteCaracter() == ")") {
                    dentroComentario = false;  
                    buffer->obtenerSiguienteCaracter();  
                    continue;
                }
            } else {
                caracteres.push_back(caracter);
            }
        }
    }

    // cout << "Resultado limpio: [";
    // for (size_t i = 0; i < caracteres.size(); ++i) {
    //     cout << caracteres[i];
    //     if (i < caracteres.size() - 1) {
    //         cout << " , ";  // Agrega coma entre los caracteres
    //     }
    // }
    // cout << "]" << endl;
    

    delete buffer;

    
    //ahora ya hacemos nuestros tokens

    while (!caracteres.empty()) {
        std::string caracter = caracteres.front();
        caracteres.erase(caracteres.begin());


        std::string tempCadena = cadenaActual + caracter;

        if (automata.acept_Chain(tempCadena)) {
            cadenaActual = tempCadena;
        } else {
            if (!cadenaActual.empty()) {
                tokens.push_back(cadenaActual);
            }
            cadenaActual = "";
        }

        
    }

    std::cout<<"Siguiente\n";

    if (!cadenaActual.empty()) {
        tokens.push_back(cadenaActual);
    }

    std::cout<<"Siguiente3\n";

        


    
    std::unordered_map<std::string, std::string> reglas;

    bool modo_reglas = false;

    
 
        
    while (!tokens.empty()) {

        // std::cout<<"Siguiente: "<<tokens[0]<<"\n";
        // std::cout << "\n{  ";
        // for (const auto& token : tokens) {
        //     std::cout << token << ",";
        // }
        // std::cout << "      }\n"<<std::endl;
        if (modo_reglas == false){
            
            if ( 
                tokens[0] == "let" &&
                isalpha(tokens[1][0]) &&  // La variable debe iniciar con una letra
                tokens[2] == "="  // Valor: número o texto
                ) 
            {
                // Guardar en el mapa

                std::string expresion = "";
                expresion = tokens[3];

                char resultado[MAX_EXPR];
                std::sprintf(resultado, "%s", expresion.c_str()); 
                reemplazar_manual(expresion, "\\t", "\t");
                reemplazar_manual(expresion, "\\n", "\n");
                expand_single_expression(expresion.c_str(), resultado);
                expresion = resultado;

                for (const auto& pair : var) {
                    reemplazar_manual(expresion, pair.first, pair.second);
                }

                
                //reemplazar_manual(expresion, "|t", "|\t");
                //reemplazar_manual(expresion, "|n", "|\n");
                
                reemplazar_manual(expresion, "\' \'", " ");
                reemplazar_manual(expresion, WHITESPACE2, " ");



                var[tokens[1]] = expresion;
                tokens.erase(tokens.begin());
                tokens.erase(tokens.begin());
                tokens.erase(tokens.begin());
                tokens.erase(tokens.begin());



                //vamos a hacer un reemplazo si lo encontramos

                
            }

    
            else if (tokens[0] =="rule"  && 
                tokens[1] == "tokens" && tokens[2] == "="){
                tokens.erase(tokens.begin()); //quitamos rules
                tokens.erase(tokens.begin());//quitamos tokens
                tokens.erase(tokens.begin()); //quitamos =
                modo_reglas = true;
    
    
    
            }
        }else{

            if (tokens[0] == "|"  &&
                tokens[2] == "return" ){
                    
                

                    std::string identificador = alfabetoGriego.back();
                    alfabetoGriego.pop_back();


                    std::string valor = tokens[1];

                    if (valor.front() == '\'' && valor.back() == '\'') {
                        valor = valor.substr(1, valor.size() - 2);  // Elimina las comillas
                    }
                    reglas[valor] = tokens[3];

                    std::string expresion_regular = var[valor];
                    reglasTokens.insertar({identificador, valor, tokens[3], expresion_regular});

                    tokens.erase(tokens.begin());
                    tokens.erase(tokens.begin());
                    tokens.erase(tokens.begin());
                    tokens.erase(tokens.begin());
                    

            }else if (tokens[0] != "|" && tokens[1] == "return"){
                std::string identificador = alfabetoGriego.back();
                alfabetoGriego.pop_back();
                reglas[tokens[0]] = "NONE";


                std::string expresion_regular = var[tokens[0]];
                std::string token_return = "";
                
                token_return = tokens[2];
                

                reglasTokens.insertar({identificador, tokens[0],token_return,expresion_regular});
                
                tokens.erase(tokens.begin());
                tokens.erase(tokens.begin());
                tokens.erase(tokens.begin());
            }
            else if(tokens[0] != "|"){

                std::string identificador = alfabetoGriego.back();
                alfabetoGriego.pop_back();
                reglas[tokens[0]] = "NONE";


                std::string expresion_regular = var[tokens[0]];
                std::string token_return = "";
                

                reglasTokens.insertar({identificador, tokens[0],token_return,expresion_regular});
                
                tokens.erase(tokens.begin());
                


            }

        }
   }

   
   

   return reglasTokens; 
}




// int main () {
//     ReglasTokens reglasTokens;

//     reglasTokens = reglas_tokens();
//     //reglasTokens.imprimir();

//     std::set<std::string> processed;

//     // std::vector<ReglaToken> reglasExtraidas = reglasTokens.extraer("identificador", "\x01");

//     // Imprimir las reglas extraídas
//     // std::cout << "\nReglas extraídas (por nombre 'Regla2'):\n";
//     // for (const auto& regla : reglasExtraidas) {
//     //     std::cout << "Identificador: " << regla.identificador << "\n"
//     //               << "Nombre: " << regla.nombre << "\n"
//     //               << "Token: " << regla.token << "\n"
//     //               << "Expresión Regular: " << regla.expresion_regular << "\n"
//     //               << "-----------------------------\n";
//     // }
    

//     // for (auto& pair : var) {
//     //     char resultado[MAX_EXPR];
        
       
//     //     std::sprintf(resultado, "%s", pair.second.c_str()); 
        
//     //     expand_single_expression(pair.second.c_str(), resultado);
//     //     pair.second = resultado;
        
//     // }
    
    

//     for (const auto& pair : var) {
//         if (processed.find(pair.first) != processed.end()) {
//             std::cout << "Variable: " << pair.first << ", Valor: " << pair.second 
//                       <<  std::endl;
//         } else {
//             std::cout << "Variable: " << pair.first << ", Valor: " << pair.second 
//                       << std::endl;
//             processed.insert(pair.first);  // Marca la variable como procesada
//         }
//     }



   

//     // std::string key = "number";  // Variable que queremos buscar

//     // auto it = var.find(key);

//     // if (it != var.end()) {
//     //     // Si la clave fue encontrada
//     //     std::cout << "La variable '" << key << "' tiene el valor: " << it->second << std::endl;
//     // } else {
//     //     // Si la clave no fue encontrada
//     //     std::cout << "La variable '" << key << "' no existe en el mapa." << std::endl;
//     // }

// }





