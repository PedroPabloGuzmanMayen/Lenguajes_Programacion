import sys
import unicodedata


AVANCE = 0
INICIOLEXEMA = 0
LEXEMAS = []
LECTOR = 0
LEXEMA = ""
FLAG_SALIDA = True


def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def cargar_buffer(entrada, inicio, tamano_buffer):
    buffer = entrada[inicio:inicio + tamano_buffer]
    if len(buffer) < tamano_buffer:
        buffer.append("eof")
    return buffer


def procesar_buffer(buffer):
    global AVANCE, INICIOLEXEMA, LEXEMAS, LEXEMA, FLAG_SALIDA
    AVANCE = 0
    INICIOLEXEMA = 0
    for i in range(len(buffer)):
      caracter = buffer[AVANCE]
      if caracter in (" ", "\n", "\t"):
          if LEXEMA:
              LEXEMAS.append(LEXEMA)
          INICIOLEXEMA = i + 1
          AVANCE = INICIOLEXEMA
          LEXEMA = ""
      elif caracter == "eof":
          if LEXEMA:
              LEXEMAS.append(LEXEMA)
          FLAG_SALIDA = False
          break
      else:
          AVANCE = i + 1
          LEXEMA += caracter


# Punto de entrada del programa
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)

    archivo_yalp = sys.argv[1]

    try:
        with open(archivo_yalp, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_yalp}")
        sys.exit(1)

    
    contenido_sin_tildes = quitar_tildes(contenido)

    BUFFER = []
    tamano_buffer = 10
    entrada = list(contenido_sin_tildes.strip())

    while FLAG_SALIDA:
        BUFFER1 = cargar_buffer(entrada, LECTOR, tamano_buffer)
        procesar_buffer(BUFFER1)
        LECTOR += len(BUFFER1)

    print(LEXEMAS)

