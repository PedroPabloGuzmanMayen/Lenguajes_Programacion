import sys
from lexer.shuting_yard import *
from lexer.lector_yal import *
from lexer.AFD_lector import *
from lexer.guardar_afd import *
from lexer.Lexer import *
from lexer.buffer_lexer import Buffer
from generador_sintactico.lector_gramar import Lector_Gramar
from generador_sintactico.lr0 import LR0_Automata
from generador_sintactico.TablaLR import ParsingTable


def main():
  if len(sys.argv) != 4:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)  
  archivo_yal = sys.argv[1]
  path_data = sys.argv[2]

  path_yalp = sys.argv[3]

  # LEXER
  lector = Lector_Yal(archivo_yal)
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

  # Parser
  lector = Lector_Gramar(path_yalp)
  gramatica = lector.build_grammar()
  automata = LR0_Automata(gramatica)
  automata.print_automaton()
  automata.save_graphviz_file("lr0.dot")

  automata.visualize_automaton("png", "mi_automata")
  tabla = ParsingTable(automata, gramatica)
  tabla.construirTablaSLR()
  tabla.print_tables()
  


  buffer = Buffer(path_data, 10)
  lexer_geted  = lexer.token_producer(buffer)
  tabla.parse_consumer_producer(lexer_geted)    


  

if __name__ == "__main__":
    main()
  