from AFD_normal import *
import sys
from mibuffer import *

class Lector_Gramar:
  def __init__(self, path_yalp):
    self.gramar = {}
    self.contenido = []
    try:
        with open(path_yalp, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Archivo no encontrado: {path_yalp}")
        sys.exit(1)
    manejador = BufferHandler(tamano_buffer=10)
    self.contenido = manejador.ejecutar(contenido)


  

  def alfabeto_generator(self):
    alfabeto = []
    alfabeto.extend([chr(c) for c in range(ord('a'), ord('z') + 1)])
    alfabeto.extend([chr(c) for c in range(ord('A'), ord('Z') + 1)])
    alfabeto.extend([chr(c) for c in range(ord('0'), ord('9') + 1)])
    alfabeto.extend([
        '%','[', ']', "'", '=', '+', '+', 'ε', '\t', '\n', '*', '(', ')', '_',
        '\x7F', '\\', '-', '|', 'ε', '?', '.', ':', '<', '>', '/', '"', '\x1A', '\x1D'
    ])
    return alfabeto



  def parser_grammar(self):
    alfabeto = self.alfabeto_generator()
    
    q0, q1, q2, q3, q4, q5, q6, q7, q8 = (
      Estado_AFD("q0"), Estado_AFD("q1"), Estado_AFD("q2"),
      Estado_AFD("q3"), Estado_AFD("q4"), Estado_AFD("q5"),
      Estado_AFD("q6"), Estado_AFD("q7"), Estado_AFD("q8")
    )

    estados = [q0, q1, q2, q3, q4, q5, q6, q7, q8]

    transiciones = [Transicion(q0, q1, '%'),
                    Transicion(q1, q2, 't'),
                    Transicion(q2, q3, 'o'),
                    Transicion(q3, q4, 'k'),
                    Transicion(q4, q5, 'e'),
                    Transicion(q5, q6, 'n')]
    finales = {q6}
    
    # afd = AFD(
    # alfabeto=['a', 'b'],
    # estados=estados,
    # transiciones=transiciones,
    # estado_inicial=q0,
    # estados_finales={q2})


  
  def build_grammar(self):
    pass
  
  def get_gramar(self):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)

    archivo_yalp = sys.argv[1]

    lector = Lector_Gramar(archivo_yalp)
