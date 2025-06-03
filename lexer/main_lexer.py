import sys
from lector_yal import Lector_Yal
from Lexer import Lexer
from shuting_yard import construct_syntax_tree, convert_to_postfix,  calculate_follow_positions
from AFD_lector import create_afd_instance_numeric
from guardar_afd import *
from afd_reconocedora import minimize_dfa, create_dfa, DFASerializer

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

    # afd_instance, dfa_structure, state_name_to_number = create_afd_instance_numeric(root=raiz, position_map=posiciones,follow_positions=followpos )

    dfa, dfa_structure = create_dfa(root=raiz, position_map=posiciones, follow_positions=followpos)

    minimized_afd, afd_dict_min = minimize_dfa(dfa_structure)

    afd_Serial = DFASerializer()

    afd_Serial.guardar_dfa(afd_dict_min, "afd.json")

    afd_dict = afd_Serial.cargar_dfa("afd.json")

    lexer = Lexer(afd_dict, reglas)
    resultado = lexer.analyze("9.35E-2+()  aa")
    print(resultado)
    # afd_dict = afd_to_json(afd_instance, "afd.json")

    # lexer = Lexer(afd_dict, reglas, debug=True)

    # resultado = lexer.analyze("ass")
    # print(resultado)










    


