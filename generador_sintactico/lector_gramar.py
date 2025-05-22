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


  def es_nombre_produccion(self, token):
     return token.endswith(':') and not token.startswith('%') and token != 'IGNORE'
  
  def verificar_producciones(self, tokens):
    dentro_produccion = False
    ignorando_comentario = False
    encontrado_primera_produccion = False

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if ignorando_comentario:
            if '*/' in token:
                ignorando_comentario = False
            i += 1
            continue
        elif '/*' in token:
            if '*/' not in token:
                ignorando_comentario = True
            i += 1
            continue

        if self.es_nombre_produccion(token):
            if not encontrado_primera_produccion:
                encontrado_primera_produccion = True

            if dentro_produccion:
                print(f"❌ Error: producción anterior no termina con ';' antes de '{token}' en la posición {i}")
                exit(1)
                return
            dentro_produccion = True

        elif token == ';':
            if dentro_produccion:
                dentro_produccion = False

        i += 1

    if dentro_produccion:
        print("❌ Error: la última producción no termina con ';'")
        exit(1)
    elif not encontrado_primera_produccion:
        print("ℹ️ No se encontró ninguna producción que verificar.")
    else:
        pass
  def alfabeto_generator(self):
    alfabeto = []
    alfabeto.extend([chr(c) for c in range(ord('a'), ord('z') + 1)])
    alfabeto.extend([chr(c) for c in range(ord('A'), ord('Z') + 1)])
    alfabeto.extend([chr(c) for c in range(ord('0'), ord('9') + 1)])
    alfabeto.extend([
        ';','%','[', ']', "'", '=', '+', '+', 'ε', '*', '(', ')', '_',
        '\x7F', '\\', '-', '|', 'ε', '?', '.', ':', '<', '>', '/', '"'
    ])
    return alfabeto


  def verificar_comentarios(self, tokens):
    dentro_comentario = False
    for i, token in enumerate(tokens):
        if '/*' in token and '*/' in token:
            continue
        elif '/*' in token:
            if dentro_comentario:
                print(f" ❌ Error: comentario anidado sin cerrar previamente en token '{tokens[i-1]} {token} {tokens[i+1]}' (posición {i})")
                exit(1)
            dentro_comentario = True
        elif '*/' in token:
            if not dentro_comentario:
                print(f" ❌ Error: comentario cerrado sin haberse abierto en token '{tokens[i-1]} {token} {tokens[i+1]}' (posición {i})")
                exit(1)
            dentro_comentario = False

    if dentro_comentario:
        print(" ❌ Error: comentario abierto sin cerrar al final del archivo.")
        exit(1)

  def parser_grammar(self):
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
    while not (len(self.contenido) == 0):
      primer_elemento = self.contenido.pop(0)
      tempCadena = cadena_actual + primer_elemento

      if (afd.acept_Chain(tempCadena)):
        cadena_actual = tempCadena
      
      else:
         if cadena_actual != "":
            tokens.append(cadena_actual)
         cadena_actual = ""
    
    
    tokens.append(cadena_actual)
    

    print(tokens)
    self.verificar_comentarios(tokens)
    self.verificar_producciones(tokens)


    i = 0
    terminales = []
    ignorados = []
    no_terminales = []
    producciones = {}
    simbolo_inicial = ""

    while i < len(tokens):
      

      # Saltar comentarios: /* ... */
      if tokens[i] == '/*' or '/*' in tokens[i]:
          i += 1
          while i < len(tokens) and tokens[i] != '*/' and '*/' not in tokens[i]:
              i += 1
          i += 1  # Saltar el '*/'
          continue

      # Si es %token, recolectar terminales
      if tokens[i] == '%token':
          i += 1
          while i < len(tokens):
              t = tokens[i]
              if '/*' in t and '*/' in t:
                 i += 1
                 continue
              
              if t == '/*' or '/*' in t:
                  i += 1
                  while i < len(tokens) and tokens[i] != '*/' and '*/' not in tokens[i]:
                      i += 1
                  i += 1  # Saltar '*/'
                  continue
              
              

              if t == '%token' or ':' in t or t == 'IGNORE':
                  break
              
              if not t.isupper():
                 print(f"El token no esta en mayuscula {t}")
                 exit(1)
              terminales.append(t)
              i += 1
          continue
      
      
      if (tokens[i] == "IGNORE"):
        i += 1
        while i < len(tokens):
          t = tokens[i]
          if t == '/*' or '/*' in t:
              i += 1
              while i < len(tokens) and tokens[i] != '*/'  and '*/' not in tokens[i]:
                  i += 1
              i += 1  # Saltar '*/'
              continue

          if t == '%token' or ':' in t or t == 'IGNORE':
              break
          if not t.isupper():
            print(f"El token no esta en mayuscula {t}")
            exit(1)
          ignorados.append(t)
          i += 1
        continue
      
      #si es una produccion
      if ':' in tokens[i]:
        nombre = tokens[i].replace(":", "")

        if not nombre.islower():
          print(f"Las producciones deben ser en minusculas '{nombre}'")
          exit(1)
        no_terminales.append(nombre)
        i += 1
        actual = []

        while i < len(tokens):
          t = tokens[i]
          if t == '/*' or '/*' in t:
              i += 1
              while i < len(tokens) and tokens[i] != '*/'  and '*/' not in tokens[i]:
                  i += 1
              i += 1  # Saltar '*/'
              continue

          if t == ';' or ';' in t:
              
              if ';' in t:
                 
                 nueva = t.replace(";", "")
                 if nueva != "":
                    actual.append(nueva)
              if actual:
                producciones.setdefault(nombre, []).append(tuple(actual))
              break
          if t == '|':
                producciones.setdefault(nombre, []).append(tuple(actual))
                actual = []
          else:
                actual.append(t)

          i += 1
        i += 1
        continue     
      
      i += 1

    print("Terminales:", terminales)
    print("Terminales Ignorados:", ignorados)
    print("No Terminales: ", no_terminales)
    print("Producciones: ", producciones)

       
       


  def build_grammar(self):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)

    archivo_yalp = sys.argv[1]

    lector = Lector_Gramar(archivo_yalp)
    lector.parser_grammar()
