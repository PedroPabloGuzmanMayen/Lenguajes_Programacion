import sys
import unicodedata

class BufferHandler:
    def __init__(self, tamano_buffer=10):
        self.avance = 0
        self.lexemas = []
        self.lector = 0
        self.flag_salida = True
        self.tamano_buffer = tamano_buffer

    def quitar_tildes(self, texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    def cargar_buffer(self, entrada):
        buffer = entrada[self.lector:self.lector + self.tamano_buffer]
        if len(buffer) < self.tamano_buffer:
            buffer.append("eof")
        return buffer

    def procesar_buffer(self, buffer):
        for caracter in buffer:
            if caracter == "eof":
                self.flag_salida = False
                break
            else:
                self.lexemas.append(caracter)

    def ejecutar(self, contenido):
        contenido_sin_tildes = self.quitar_tildes(contenido)
        entrada = list(contenido_sin_tildes)

        while self.flag_salida:
            buffer = self.cargar_buffer(entrada)
            self.procesar_buffer(buffer)
            self.lector += len(buffer)

        return self.lexemas


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

    manejador = BufferHandler(tamano_buffer=10)
    resultado = manejador.ejecutar(contenido)


    for n in resultado:
        print(n)
