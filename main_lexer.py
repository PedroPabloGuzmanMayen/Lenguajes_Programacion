import sys
from lexer.lector_yal import Lector_Yal
from lexer.Lexer import Lexer
from lexer.shuting_yard import construct_syntax_tree, convert_to_postfix,  calculate_follow_positions
from lexer.AFD_lector import  create_dfa
from lexer.guardar_afd import *

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)

    archivo_yalp = sys.argv[1]
    archivo_contenido = sys.argv[2]

    # CONTENIDO DE YAL
    lector = Lector_Yal(archivo_yalp)
    lector.parse_lexers()
    expresion_principal, reglas = lector.merge_rule_expressions(lector.contenido)
    postfix = convert_to_postfix(expresion_principal)
    raiz, posiciones = construct_syntax_tree(postfix)
    followpos = calculate_follow_positions(root=raiz, position_map=posiciones)
    afd_instance = create_dfa(root=raiz, position_map=posiciones,follow_positions=followpos )
    afd_instance.minimizumAFD()
    afd_instance.graphicminimizumAFD()
    convert_automata_structure(afd_instance)
    loaded_automata = load_automata_from_json('./automata_converted.json')
    lexer = Lexer(loaded_automata, reglas, debug=True)

    with open(archivo_contenido, "r", encoding="utf-8") as f:
        contenido = f.read()

    resultado = lexer.analyze(contenido)

    #print(resultado)
    










    


