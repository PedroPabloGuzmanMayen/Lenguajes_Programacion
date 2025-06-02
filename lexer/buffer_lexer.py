import sys

# Constantes (asumiendo valores basados en el uso en el código)
WHITESPACE = "ε"  # Epsilon para espacios en blanco
PUNTO = "."
RPARENTESIS = ")"
LPARENTESIS = "("
TIMES = "*"


class Buffer:
    def __init__(self, filename_or_size, tamano_or_entrada=None):
        """
        Constructor que puede trabajar con archivo o entrada manual
        - Si filename_or_size es str: lee desde archivo
        - Si filename_or_size es int: usa entrada manual
        """
        self.inicio_lexema = 0
        self.avance = 0
        self.FLAG_SALIDA = True
        self.ultimo_caracter = ''
        self.buffer = []
        
        if isinstance(filename_or_size, str):
            # Constructor desde archivo
            self.tamano_buffer = tamano_or_entrada
            try:
                with open(filename_or_size, 'r', encoding='utf-8') as archivo:
                    self.entrada = archivo.read()
            except FileNotFoundError:
                print(f"Error al abrir el archivo '{filename_or_size}'")
                sys.exit(1)
        else:
            # Constructor desde entrada por teclado
            self.tamano_buffer = filename_or_size
            self.entrada = tamano_or_entrada or ""

    def cargar_buffer(self):
        """Cargar el buffer con la siguiente parte de la entrada"""
        self.buffer = []
        inicio = self.inicio_lexema
        fin = min(inicio + self.tamano_buffer, len(self.entrada))
        
        for i in range(inicio, fin):
            self.buffer.append(self.entrada[i])
        
        if len(self.buffer) < self.tamano_buffer:
            self.buffer.append('\0')  # EOF
        
        self.avance = 0

    def obtener_siguiente_caracter(self):
        """Obtener el siguiente carácter procesado"""
        if self.avance >= len(self.buffer):
            self.inicio_lexema += len(self.buffer)
            self.cargar_buffer()

        if self.avance < len(self.buffer):
            caracter = self.buffer[self.avance]
            caracter_salida = caracter

            # Lógica de reemplazo específica
            if (caracter == ' ' and self.ultimo_caracter == '\'' and 
                self.avance + 1 < len(self.buffer) and self.buffer[self.avance + 1] == '\''):
                caracter_salida = WHITESPACE  # Reemplazo por épsilon
                print("Imprimir")

            if caracter == '.':
                caracter_salida = PUNTO

            if caracter == '\n':
                caracter_salida = " "  # Reemplazo por espacio
            
            if caracter == '\r':
                caracter_salida = " "  # Reemplazo por espacio

            if caracter == '\0':
                self.FLAG_SALIDA = False
                return ""

            self.ultimo_caracter = caracter
            self.avance += 1

            return caracter_salida

        return ""

    def obtener_siguiente_caracter2(self):
        """Segunda versión del método para obtener caracteres"""
        if self.avance >= len(self.buffer):
            self.inicio_lexema += len(self.buffer)
            self.cargar_buffer()

        if self.avance < len(self.buffer):
            caracter = self.buffer[self.avance]
            caracter_salida = caracter

            if caracter == '.':
                caracter_salida = PUNTO

            if caracter == '\r':
                caracter_salida = " "  # Reemplazo por espacio

            if caracter == ')':
                caracter_salida = RPARENTESIS

            # Nota: En C++ había '  ' (dos espacios), en Python sería:
            if caracter == ' ':  # Espacio simple
                caracter_salida = " "

            if caracter == '\v':  # Tab vertical
                caracter_salida = " "  # Reemplazo por espacio

            if caracter == '(':
                caracter_salida = LPARENTESIS

            if caracter == '*':
                caracter_salida = TIMES

            if caracter == '\n':
                caracter_salida = " "  # Reemplazo por espacio

            if caracter == '\0':
                self.FLAG_SALIDA = False
                return ""

            self.ultimo_caracter = caracter
            self.avance += 1

            return caracter_salida

        return ""

    def obtener_siguiente_linea(self):
        """Obtener la siguiente línea completa"""
        linea = ""
        
        while self.FLAG_SALIDA:
            caracter = self.obtener_siguiente_caracter2()
            
            if not caracter:
                break

            if caracter == " ":
                linea += " "

            if caracter == "\n" or caracter == "":  # Si encontramos salto de línea o EOF
                return linea  # Devolvemos la línea completa

            linea += caracter  # Agregamos el caracter al final de la línea

        return linea

    def validar_linea(self, linea, numero_linea):
        """Validar que una línea tenga la sintaxis correcta"""
        comillas_simples = 0
        comillas_dobles = 0
        par_abierto = 0
        par_cerrado = 0

        for c in linea:
            if c == '\'':
                comillas_simples += 1
            if c == '"':
                comillas_dobles += 1
            if c == '(':
                par_abierto += 1
            if c == ')':
                par_cerrado += 1

        # Para comillas desbalanceadas
        if comillas_simples % 2 != 0:
            print(f"Error en el yal línea {numero_linea}: comillas simples desbalanceadas.")
            sys.exit(1)

        if comillas_dobles % 2 != 0:
            print(f"Error en el yal línea {numero_linea}: comillas dobles desbalanceadas.")
            sys.exit(1)

        if par_abierto != par_cerrado:
            print(f"Error en el yal línea {numero_linea}: paréntesis desbalanceados.")
            sys.exit(1)

        # Saber si hay "let" con corchetes
        if ("let" in linea and "[" in linea and "]" in linea):
            desde = linea.find("[")
            hasta = linea.find("]")
            contenido = linea[desde + 1:hasta]

            # Detecta si hay rangos pegados como 'Z'a' sin operador
            for i in range(len(contenido) - 5):
                if (contenido[i] == '\'' and 
                    i + 2 < len(contenido) and contenido[i+2] == '\'' and
                    i + 3 < len(contenido) and 
                    contenido[i+3] not in ['|', '-', ',', ']']):
                    
                    problema = contenido[i:i+5]
                    print(f"Error en yal en la línea {numero_linea}: posible rango mal formado cerca de: {problema}")
                    sys.exit(1)

        return True


# def main():
#     """Función principal para probar la clase Buffer"""
#     print("Selecciona la opción de entrada:")
#     print("1. Ingresar texto manualmente")
#     print("2. Leer desde un archivo")
    
#     try:
#         opcion = int(input("Opción: "))
#     except ValueError:
#         print("Opción no válida.")
#         return 1

#     buffer = None

#     if opcion == 1:
#         input_text = input("Escribe la cadena: ")
#         buffer = Buffer(10, input_text)
#     elif opcion == 2:
#         filename = input("Ingresa el nombre del archivo: ")
#         buffer = Buffer(filename, 10)
#     else:
#         print("Opción no válida.")
#         return 1

#     resultado = ""

#     # Procesar el buffer
#     while buffer.FLAG_SALIDA:
#         buffer.cargar_buffer()
#         while buffer.FLAG_SALIDA:
#             caracter = buffer.obtener_siguiente_caracter()
#             print(f"Procesado: {caracter}")
#             if caracter:
#                 resultado += caracter

#     print(f"Resultado final: {resultado}")
#     return 0


# if __name__ == "__main__":
#     main()