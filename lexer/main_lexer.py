import sys
from lector_yal import Lector_Yal
from Lexer import Lexer
from shuting_yard import construct_syntax_tree, convert_to_postfix,  calculate_follow_positions
from AFD_lector import create_afd_instance_numeric, create_dfa
from guardar_afd import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)

    archivo_yalp = sys.argv[1]

    lector = Lector_Yal(archivo_yalp)
    lector.parse_lexers()
    expresion_principal, reglas = lector.merge_rule_expressions(lector.contenido)

    print(lector.contenido)
    print(expresion_principal)
    print(reglas)

    postfix = convert_to_postfix(expresion_principal)

    print(postfix)

    raiz, posiciones = construct_syntax_tree(postfix)

    followpos = calculate_follow_positions(root=raiz, position_map=posiciones)

    # Crearlo con clase principal
    afd_instance = create_dfa(root=raiz, position_map=posiciones,follow_positions=followpos )


    print("\nTags", afd_instance.state_tags)
    afd_instance.minimizumAFD()
    print("\nNext tags",afd_instance.state_tags)
    

    convert_automata_structure(afd_instance)


    loaded_automata = load_automata_from_json('./automata_converted.json')

    lexer = Lexer(loaded_automata, reglas, debug=True)

    resultado = lexer.analyze("5.6E-3+()a   adfasdf ee5666 ---*** \t\n")
    print(resultado)










    


