from lector_gramar import Lector_Gramar
from lr0 import LR0_Automata
from TablaLR import ParsingTable
import os

def lexer_simulado(linea):
    mapa = {
        "+": "PLUS",
        "*": "TIMES",
        "(": "LPAREN",
        ")": "RPAREN"
    }
    tokens = []
    for palabra in linea.strip().split():
        if palabra in mapa:
            tokens.append(mapa[palabra])
        else:
            tokens.append("ID")  # Si mo es simbolo pues lo camos a dejar como ID
    return tokens

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_yalp = os.path.join(base_dir, "archivos_yalp", "slr-1.yalp")

    lector = Lector_Gramar(ruta_yalp)
    gramatica = lector.build_grammar()
    automata = LR0_Automata(gramatica)
    tabla = ParsingTable(automata, gramatica)
    tabla.construirTablaSLR()

    archivo_cadenas = os.path.join(base_dir, "random_data", "random_data_2.txt")
    with open(archivo_cadenas, "r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, 1):
            if not linea.strip():
                continue
            print(f"\n Línea {num_linea}: {linea.strip()}")  #primero lee la línea, luego llama al lexer, luego pasa los tokens al parser,
            tokens = lexer_simulado(linea)
            tokens.append('$')
            aceptada = tabla.parse(tokens)
            if aceptada:
                print(f"Cadena aceptada (línea {num_linea})")
            else:
                print(f"Cadena con error (línea {num_linea})")

if __name__ == "__main__":
    main()
