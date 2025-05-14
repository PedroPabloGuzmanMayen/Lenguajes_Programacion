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
    main()