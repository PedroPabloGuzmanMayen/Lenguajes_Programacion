from AFD_lector import *
import sys
from buffer_lexer import Buffer

class Lector_Yal:
  def __init__(self, path_yalp):
    self.contenido = {
       'definiciones': {},
       'reglas': []
    }
    self.buffer = Buffer(path_yalp, 10)

  # def es_nombre_produccion(self, token):
  #    return token.endswith(':') and not token.startswith('%') and token != 'IGNORE'
  
  # def verificar_producciones(self, tokens):
  #   dentro_produccion = False
  #   ignorando_comentario = False
  #   encontrado_primera_produccion = False

  #   i = 0
  #   while i < len(tokens):
  #       token = tokens[i]
  #       if ignorando_comentario:
  #           if '*/' in token:
  #               ignorando_comentario = False
  #           i += 1
  #           continue
  #       elif '/*' in token:
  #           if '*/' not in token:
  #               ignorando_comentario = True
  #           i += 1
  #           continue

  #       if self.es_nombre_produccion(token):
  #           if not encontrado_primera_produccion:
  #               encontrado_primera_produccion = True

  #           if dentro_produccion:
  #               print(f"❌ Error: producción anterior no termina con ';' antes de '{token}' en la posición {i}")
  #               exit(1)
  #               return
  #           dentro_produccion = True

  #       elif token == ';':
  #           if dentro_produccion:
  #               dentro_produccion = False

  #       i += 1

  #   if dentro_produccion:
  #       print("❌ Error: la última producción no termina con ';'")
  #       exit(1)
  #   elif not encontrado_primera_produccion:
  #       print("ℹ️ No se encontró ninguna producción que verificar.")
  #   else:
  #       pass
  def alfabeto_generator(self):
    alfabeto = []
    alfabeto.extend([chr(c) for c in range(ord('a'), ord('z') + 1)])
    alfabeto.extend([chr(c) for c in range(ord('A'), ord('Z') + 1)])
    alfabeto.extend([chr(c) for c in range(ord('0'), ord('9') + 1)])
    alfabeto.extend([
        ';','%','[', ']', "'", '=', '+', '+', 'ε', '*', '(', ')', '_',
        '\x7F', '\\', '-', '|', 'ε', '?', '.', ':', '<', '>', '/', '"', '{', '}'
    ])
    return alfabeto


  def verificar_comentarios(self, tokens):
    dentro_comentario = False
    for i, token in enumerate(tokens):
        if '(*' in token and '*)' in token:
            continue
        elif '(*' in token:
            if dentro_comentario:
                print(f" ❌ Error: comentario anidado sin cerrar previamente en token '{tokens[i-1]} {token} {tokens[i+1]}' (posición {i})")
                exit(1)
            dentro_comentario = True
        elif '*)' in token:
            if not dentro_comentario:
                print(f" ❌ Error: comentario cerrado sin haberse abierto en token '{tokens[i-1]} {token} {tokens[i+1]}' (posición {i})")
                exit(1)
            dentro_comentario = False

    if dentro_comentario:
        print(" ❌ Error: comentario abierto sin cerrar al final del archivo.")
        exit(1)

  def parse_lexers(self):
    alfabeto = self.alfabeto_generator()

    q0, q1, q2, q3, q4, q5, q6, q7, q8 = (
      Estado_AFD("q0"), Estado_AFD("q1"), Estado_AFD("q2"),
      Estado_AFD("q3"), Estado_AFD("q4"), Estado_AFD("q5"),
      Estado_AFD("q6"), Estado_AFD("q7"), Estado_AFD("q8")
    )

    estados = [q0, q1, q2, q3, q4, q5, q6, q7, q8]

    transiciones = [Transicion(q0, q7, simbolo) for simbolo in alfabeto]
    transiciones += [Transicion(q7, q7, simbolo) for simbolo in alfabeto]


    finales = {q7}
    
    afd = AFD(
    alfabeto=alfabeto,
    estados=estados,
    transiciones=transiciones,
    estado_inicial=q0,
    estados_finales=finales)

    

    cadena_actual = ""
    tokens = []
    while self.buffer.FLAG_SALIDA:
       self.buffer.cargar_buffer()
       while self.buffer.FLAG_SALIDA:
          caracter = self.buffer.obtener_siguiente_caracter()
          print(caracter)
          tempCadena = cadena_actual + str(caracter)

          if (afd.acept_Chain(tempCadena)):
            cadena_actual = tempCadena
            
          
          else:
            if cadena_actual != "":
                tokens.append(cadena_actual)
            cadena_actual = ""
    
    
    tokens.append(cadena_actual)
    tokens = [token.replace('ε', ' ') for token in tokens]

    print(tokens)
    self.verificar_comentarios(tokens)


    # self.verificar_producciones(tokens)


    i = 0
    # terminales = []
    # ignorados = []
    # no_terminales = []
    # producciones = {}
    # simbolo_inicial = ""

    i = 0
    while i < len(tokens):
        # Quitar comentarios multilínea
        if tokens[i] == '(*' or ('(*' in tokens[i]):
            i += 1
            while i < len(tokens) and tokens[i] != '*)' and '*)' not in tokens[i]:
                i += 1
            i += 1  # Saltar el '*)'
            continue

        # Procesar definiciones let
        if tokens[i] == 'let':
            i += 1
            if i >= len(tokens):
                return  # o manejar error

            nombre = tokens[i]
            i += 1

            # Asegurar que el siguiente token sea '='
            if i >= len(tokens) or tokens[i] != '=':
                print(f"Se esperaba '=' después del nombre {nombre}")
                exit(1)
            i += 1

            definicion = []
            while i < len(tokens):
                t = tokens[i]

                # Saltar comentarios de una sola línea o embebidos en una línea
                if '(*' in t and '*)' in t:
                    i += 1
                    continue

                # Comentario multilínea
                if t == '(*' or ('(*' in t):
                    i += 1
                    while i < len(tokens) and '*)' not in tokens[i]:
                        i += 1
                    i += 1
                    continue

                # Fin de la definición si empieza otra o un delimitador importante
                if t == 'let' or t == 'rule':
                    break

                definicion.append(t)
                i += 1

            self.contenido['definiciones'][nombre] = ' '.join(definicion)
            continue

        # Procesar regla "rule tokens ="
        if (i + 2 < len(tokens) and tokens[i] == 'rule' and tokens[i+1] == 'tokens' and tokens[i+2] == '='):
          i += 3  # saltar 'rule', 'tokens', '='
          
          while i < len(tokens):
              # Saltar comentarios multilínea en reglas
              if tokens[i] == '(*' or ('(*' in tokens[i]):
                  i += 1
                  while i < len(tokens) and '*)' not in tokens[i]:
                      i += 1
                  i += 1
                  continue
              
              # Saltar '|', si está
              if tokens[i] == '|':
                  i += 1
                  if i >= len(tokens):
                      break
              
              if i >= len(tokens):
                  break
              
              expresion = tokens[i]
              i += 1
              
              # Verificar si hay una acción (entre llaves)
              if i < len(tokens) and tokens[i] == '{':
                  i += 1  # saltar '{'
                  
                  accion_tokens = []
                  nivel_llaves = 1  # Contador para balancear llaves
                  
                  while i < len(tokens) and nivel_llaves > 0:
                      if tokens[i] == '{':
                          nivel_llaves += 1
                      elif tokens[i] == '}':
                          nivel_llaves -= 1
                      
                      if nivel_llaves > 0:  # Solo agregar si no es la llave de cierre final
                          accion_tokens.append(tokens[i])
                      
                      i += 1
                  
                  if nivel_llaves > 0:
                      print(f"Error: No se encontró '}}' para cerrar la acción de '{expresion}'")
                      break
                  
                  # Verificar si la acción tiene 'return'
                  if 'return' in accion_tokens:
                      idx = accion_tokens.index('return')
                      accion = accion_tokens[idx + 1] if (idx + 1) < len(accion_tokens) else 'None'
                      
                      self.contenido['reglas'].append({
                          'expresion': expresion,
                          'accion': 'return ' + accion
                      })
                  else:
                      # Acción sin return: asignar None
                      self.contenido['reglas'].append({
                          'expresion': expresion,
                          'accion': 'None'
                      })
              else:
                  # No hay acción (sin llaves): asignar None
                  self.contenido['reglas'].append({
                      'expresion': expresion,
                      'accion': None
                  })
              
              continue
          
          # Avanzar para evitar ciclo infinito en tokens no reconocidos
          i += 1

    print("Tokens", tokens)
    print("\nContenido",self.contenido)

      
    #   if (tokens[i] == "IGNORE"):
    #     i += 1
    #     while i < len(tokens):
    #       t = tokens[i]
    #       if t == '/*' or '/*' in t:
    #           i += 1
    #           while i < len(tokens) and tokens[i] != '*/'  and '*/' not in tokens[i]:
    #               i += 1
    #           i += 1  # Saltar '*/'
    #           continue

    #       if t == '%token' or ':' in t or t == 'IGNORE':
    #           break
    #       if not t.isupper():
    #         print(f"El token no esta en mayuscula {t}")
    #         exit(1)
    #       ignorados.append(t)
    #       i += 1
    #     continue
      
    #   #si es una produccion
    #   if ':' in tokens[i]:
    #     nombre = tokens[i].replace(":", "")

    #     if not nombre.islower():
    #       print(f"Las producciones deben ser en minusculas '{nombre}'")
    #       exit(1)
    #     no_terminales.append(nombre)
    #     i += 1
    #     actual = []

    #     while i < len(tokens):
    #       t = tokens[i]
    #       if t == '/*' or '/*' in t:
    #           i += 1
    #           while i < len(tokens) and tokens[i] != '*/'  and '*/' not in tokens[i]:
    #               i += 1
    #           i += 1  # Saltar '*/'
    #           continue

    #       if t == ';' or ';' in t:
              
    #           if ';' in t:
                 
    #              nueva = t.replace(";", "")
    #              if nueva != "":
    #                 actual.append(nueva)
    #           if actual:
    #             producciones.setdefault(nombre, []).append(tuple(actual))
    #           break
    #       if t == '|':
    #             producciones.setdefault(nombre, []).append(tuple(actual))
    #             actual = []
    #       else:
    #             actual.append(t)

    #       i += 1
    #     i += 1
    #     continue     
      
    #   i += 1
    # simbolo_inicial = next(iter(producciones))

    # return simbolo_inicial, terminales, ignorados, no_terminales, producciones

       
       


  # def build_grammar(self):
  #   simbolo_inicial, terminales, ignorados, no_terminales, producciones = self.parser_grammar()
  #   no_terminales+= ["S'"]
  #   producciones["S'"] = [(simbolo_inicial,)]
  #   ff = Gramatica_Builder(
  #                           producciones=producciones,
  #                           no_terminales=no_terminales,
  #                           terminales=terminales

  #                           )
  #   return ff

# Para ejecutarlo vaya a generador_sintactico y ejecute:
# python lector_gramar.py ./archivos_yalp/slr-1.yalp  el archivo yalp puede probar con todos los que estan
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)

    archivo_yalp = sys.argv[1]

    lector = Lector_Yal(archivo_yalp)
    contenido = lector.parse_lexers()
