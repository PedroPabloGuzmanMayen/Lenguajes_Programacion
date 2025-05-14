from constantes import *

class Buffer:
    def __init__(self, filename=None, tamano=0, cadena_entrada=None):
        self.buffer = []
        self.inicioLexema = 0
        self.avance = 0
        self.FLAG_SALIDA = True
        self.tamano_buffer = tamano
        self.ultimoCaracter = '\0'
        self.entrada = ""
        
        # Initialize from file
        if filename is not None:
            try:
                with open(filename, 'r') as archivo:
                    self.entrada = archivo.read()
            except Exception as e:
                print(f"Error al abrir el archivo '{filename}': {e}")
                exit(1)
        # Initialize from string input
        elif cadena_entrada is not None:
            self.entrada = cadena_entrada
    
    def cargar_buffer(self):
        """Load the buffer with the next part of the input"""
        self.buffer = []
        for i in range(self.inicioLexema, min(self.inicioLexema + self.tamano_buffer, len(self.entrada))):
            self.buffer.append(self.entrada[i])
        
        if len(self.buffer) < self.tamano_buffer:
            self.buffer.append('\0')  # EOF
        
        self.avance = 0
    
    def obtenerSiguienteCaracter(self):
        """Get the next processed character"""
        if self.avance >= len(self.buffer):
            self.inicioLexema += len(self.buffer)
            self.cargar_buffer()
        
        if self.avance < len(self.buffer):
            caracter = self.buffer[self.avance]
            caracterSalida = caracter
            
            if caracter == ' ' and self.ultimoCaracter == '\'' and self.avance + 1 < len(self.buffer) and self.buffer[self.avance + 1] == '\'':
                caracterSalida = WHITESPACE
                print("Imprimir \n")
            
            if caracter == '.':
                caracterSalida = PUNTO
            
            if caracter == '\n':
                caracterSalida = " "  # Replace with space
            
            if caracter == '\r':
                caracterSalida = " "  # Replace with space
            
            if caracter == '\0':
                self.FLAG_SALIDA = False
                return ""
            
            self.ultimoCaracter = caracter
            self.avance += 1
            
            return caracterSalida
        
        return ""
    
    def obtenerSiguienteCaracter2(self):
        """Get the next processed character (alternate version)"""
        if self.avance >= len(self.buffer):
            self.inicioLexema += len(self.buffer)
            self.cargar_buffer()
        
        if self.avance < len(self.buffer):
            caracter = self.buffer[self.avance]
            caracterSalida = caracter
            
            if caracter == '.':
                caracterSalida = PUNTO
            
            if caracter == '\r':
                caracterSalida = " "  # Replace with space
            
            if caracter == ')':
                caracterSalida = RPARENTESIS
            
            if caracter == '  ':
                caracterSalida = " "
            
            if caracter == '\v':
                caracterSalida = " "  # Replace with space
            
            if caracter == '(':
                caracterSalida = LPARENTESIS
            
            if caracter == '*':
                caracterSalida = TIMES
            
            if caracter == '\n':
                caracterSalida = " "  # Replace with space
            
            if caracter == '\0':
                self.FLAG_SALIDA = False
                return ""
            
            self.ultimoCaracter = caracter
            self.avance += 1
            
            return caracterSalida
        
        return ""
    
    def obtenerSiguienteLinea(self):
        """Get the next complete line from the buffer"""
        linea = ""
        caracter = ""
        
        while self.FLAG_SALIDA:
            caracter = self.obtenerSiguienteCaracter2()
            
            if not caracter:
                break
            
            if caracter == " ":
                linea += " "
            
            if caracter == "\n" or caracter == "":  # If we find a newline or EOF
                return linea  # Return the complete line
            
            linea += caracter  # Add the character to the end of the line
        
        return linea
    
    def validarLinea(self, linea, numeroLinea):
        """Validate a line for balanced quotes and parentheses"""
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
        
        # Check for unbalanced quotes
        if comillas_simples % 2 != 0:
            print(f"Error en el yal línea {numeroLinea}: comillas simples desbalanceadas.")
            exit(1)
        
        if comillas_dobles % 2 != 0:
            print(f"Error en el yal línea {numeroLinea}: comillas dobles desbalanceadas.")
            exit(1)
        
        if par_abierto != par_cerrado:
            print(f"Error en el yal línea {numeroLinea}: paréntesis desbalanceados.")
            exit(1)
        
        # Check if there's "let" with brackets
        if "let" in linea and "[" in linea and "]" in linea:
            desde = linea.find("[")
            hasta = linea.find("]")
            contenido = linea[desde + 1:hasta]
            
            # Detect if there are adjacent ranges like 'Z'a' without an operator
            for i in range(len(contenido) - 5):
                if (contenido[i] == '\'' and
                    contenido[i+2] == '\'' and
                    contenido[i+3] != '|' and
                    contenido[i+3] != '-' and
                    contenido[i+3] != ',' and
                    contenido[i+3] != ']'):
                    
                    problema = contenido[i:i+5]
                    print(f"Error en yal en la línea {numeroLinea}: posible rango mal formado cerca de: {problema}")
                    exit(1)
        
        return True