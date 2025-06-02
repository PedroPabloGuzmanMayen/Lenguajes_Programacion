"""
Implementación simplificada de ReglasTokens usando solo diccionarios y funciones
"""

# Usaremos una lista de diccionarios para almacenar las reglas
# Cada regla es un diccionario con las claves: 'identificador', 'nombre', 'token', 'expresion_regular'

def crear_reglas():
    """Crear una estructura de datos vacía para las reglas"""
    return []

def crear_regla(identificador, nombre, token, expresion_regular=""):
    """Crear una nueva regla como un diccionario"""
    return {
        'identificador': identificador,
        'nombre': nombre,
        'token': token,
        'expresion_regular': expresion_regular
    }

def insertar(reglas, regla):
    """Insertar una nueva regla"""
    reglas.append(regla)
    return reglas

def extraer(reglas, atributo, valor):
    """Extraer reglas que coincidan con un atributo y valor"""
    return [regla for regla in reglas if regla.get(atributo) == valor]

def actualizar(reglas, atributo, valor, nueva_regla):
    """Actualizar reglas que coincidan con un atributo y valor"""
    for i, regla in enumerate(reglas):
        if regla.get(atributo) == valor:
            reglas[i] = nueva_regla
    return reglas

def eliminar(reglas, atributo, valor):
    """Eliminar reglas que coincidan con un atributo y valor"""
    return [regla for regla in reglas if regla.get(atributo) != valor]

def imprimir(reglas):
    """Imprimir todas las reglas"""
    for regla in reglas:
        print(f"Identificador: {regla['identificador']}")
        print(f"Nombre: {regla['nombre']}")
        print(f"Token: {regla['token']}")
        print(f"Expresión Regular: {regla['expresion_regular']}")
        print("-----------------------------")

def obtener_token_por_nombre(reglas, nombre):
    """Obtener token por nombre"""
    for regla in reglas:
        if regla['nombre'] == nombre:
            return regla['token']
    return ""

def obtener_token_primer_elemento(reglas):
    """Obtener token del primer elemento"""
    if reglas:
        return reglas[0]['token']
    return ""

def obtener_token_token(reglas, token_n):
    """Obtener token por nombre de token"""
    for regla in reglas:
        if regla['token'] == token_n:
            return regla['token']
    return token_n

def obtener_token_expresion(reglas, token_n):
    """Obtener expresión regular para un token"""
    for regla in reglas:
        if regla['token'] == token_n:
            return regla['expresion_regular']
    return token_n

def generar_expresion(reglas):
    """Generar una expresión regular compuesta de todas las reglas"""
    # Diccionario para reemplazos de caracteres especiales
    reemplazos = {
        "*": "\\*",  # Símbolo de multiplicación
        "(": "\\(",  # Paréntesis izquierdo
        ")": "\\)",  # Paréntesis derecho
        ".": "\\."   # Punto
    }
    
    resultado = ""
    for i, regla in enumerate(reglas):
        # Usar expresión regular si está disponible, de lo contrario usar nombre
        expresion = regla['expresion_regular'] if regla['expresion_regular'] else regla['nombre']
        
        # Reemplazar caracteres especiales si es necesario
        if expresion in reemplazos:
            expresion = reemplazos[expresion]
        
        # Crear expresión concatenada con identificador
        concatenado = f"({expresion}){regla['identificador']}"
        
        # Agregar separador si no es el último elemento
        if i < len(reglas) - 1:
            concatenado += "|"
        
        resultado += concatenado
    
    print(resultado)
    return resultado


# Ejemplo de uso
if __name__ == "__main__":
    # Crear una estructura de reglas vacía
    mis_reglas = crear_reglas()
    
    # Agregar algunas reglas
    regla1 = crear_regla("ID1", "entero", "INT", "[0-9]+")
    regla2 = crear_regla("ID2", "suma", "+", "\\+")
    regla3 = crear_regla("ID3", "multiplicacion", "*", "\\*")
    
    mis_reglas = insertar(mis_reglas, regla1)
    mis_reglas = insertar(mis_reglas, regla2)
    mis_reglas = insertar(mis_reglas, regla3)
    
    # Imprimir todas las reglas
    print("Todas las reglas:")
    imprimir(mis_reglas)
    
    # Extraer reglas por atributo
    print("\nReglas con token 'INT':")
    reglas_int = extraer(mis_reglas, 'token', 'INT')
    imprimir(reglas_int)
    
    # Actualizar una regla
    nueva_regla = crear_regla("ID1", "entero", "INTEGER", "[0-9]+")
    mis_reglas = actualizar(mis_reglas, 'identificador', 'ID1', nueva_regla)
    print("\nDespués de actualizar ID1:")
    imprimir(mis_reglas)
    
    # Generar expresión compuesta
    print("\nExpresión generada:")
    generar_expresion(mis_reglas)
    
    # Eliminar una regla
    mis_reglas = eliminar(mis_reglas, 'token', 'INTEGER')
    print("\nDespués de eliminar el token INTEGER:")
    imprimir(mis_reglas)