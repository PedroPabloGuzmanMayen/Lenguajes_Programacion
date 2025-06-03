from lector_gramar import Lector_Gramar
from lr0 import LR0_Automata
from TablaLR import ParsingTable
import os
 

def main():
    print("== YAPar: Generador de Analizadores Sintácticos SLR(1) ==")
    archivo = input("Ingresa el nombre del archivo YALP (ej. slr-1.yalp): ")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir, "archivos_yalp", archivo)

    # 1. Leer y construir la gramática
    lector = Lector_Gramar(ruta)
    gramatica = lector.build_grammar()

    # 2. Construir autómata LR(0)
    automata = LR0_Automata(gramatica)
    print("\n=== Autómata LR(0) ===")
    automata.print_automaton()

    # 3. Construir tabla de parseo
    tabla = ParsingTable(automata, gramatica)
    tabla.construirTablaSLR()
    tabla.print_tables()

    # 4. Ingresar cadena de prueba
    print("\n== Prueba de Parsing ==")
    cadena = input("Ingresa una cadena de tokens separados por espacio (ej. ID PLUS ID): ")
    tokens = cadena.strip().split()
    tokens.append('$')  # Fin de entrada
    print(tokens)
    print("\n== Resultado del Análisis ==")
    tabla.parse(tokens)


if __name__ == "__main__":
    main()



"""
from Buffer import Buffer

def main():
    opcion = 0
    input_text = ""
    filename = ""
    
    print("Selecciona la opción de entrada:")
    print("1. Ingresar texto manualmente")
    print("2. Leer desde un archivo")
    
    try:
        opcion = int(input("Opción: "))
    except ValueError:
        print("Opción no válida.")
        return 1
    
    buffer = None
    
    if opcion == 1:
        input_text = input("Escribe la cadena: ")
        buffer = Buffer(tamano=10, cadena_entrada=input_text)
    elif opcion == 2:
        filename = input("Ingresa el nombre del archivo: ")
        buffer = Buffer(filename=filename, tamano=10)
    else:
        print("Opción no válida.")
        return 1
    
    resultado = ""
    
    # Process the buffer
    while buffer.FLAG_SALIDA:
        buffer.cargar_buffer()
        while buffer.FLAG_SALIDA:
            caracter = buffer.obtenerSiguienteCaracter()
            print(f"Procesado: {caracter}")
            if caracter:
                resultado += caracter
    
    print(f"Resultado final: {resultado}")
    
    return 0

if __name__ == "__main__":
    main()"""