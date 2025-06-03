import sys
from lector_yal import Lector_Yal
from Lexer import Lexer
from shuting_yard import construct_syntax_tree, convert_to_postfix,  calculate_follow_positions
from AFD_lector import  create_dfa
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

    #expresion_principal_t = """(((32|9|10)).(((32|9|10)))*).#1000|(((65|66|67|68|69|70|71|72|73|74|75|76|77|78|79|80|81|82|83|84|85|86|87|88|89|90|97|98|99|100|101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116|117|118|119|120|121|122)).(((65|66|67|68|69|70|71|72|73|74|75|76|77|78|79|80|81|82|83|84|85|86|87|88|89|90|97|98|99|100|101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116|117|118|119|120|121|122))|((_)*)|((48|49|50|51|52|53|54|55|56|57)))*).#1001|((((48|49|50|51|52|53|54|55|56|57)).(((48|49|50|51|52|53|54|55|56|57)))*).((46.(((48|49|50|51|52|53|54|55|56|57)).(((48|49|50|51|52|53|54|55|56|57)))*))|949).(((69).((43|45)|949).(((48|49|50|51|52|53|54|55|56|57)).(((48|49|50|51|52|53|54|55|56|57)))*))|949)).#1002|(59).#1003|(58.61).#1004|(60).#1005|(61).#1006|(43).#1007|(45).#1008|(42).#1009|(47).#1010|(40).#1011|(41).#1012"""

    postfix = convert_to_postfix(expresion_principal)

    print(postfix)

    raiz, posiciones = construct_syntax_tree(postfix)

    followpos = calculate_follow_positions(root=raiz, position_map=posiciones)

    # Crearlo con clase principal
    afd_instance = create_dfa(root=raiz, position_map=posiciones,follow_positions=followpos )



    afd_instance.minimizumAFD()
    afd_instance.graphicminimizumAFD()
  

    convert_automata_structure(afd_instance)


    loaded_automata = load_automata_from_json('./automata_converted.json')

    lexer = Lexer(loaded_automata, reglas, debug=True)

    resultado = lexer.analyze("5.6E-3+(--**-*-*)a  ;:=<:=/ adfasdf ee5666 ---*** \t\n")
    print(resultado)










    


