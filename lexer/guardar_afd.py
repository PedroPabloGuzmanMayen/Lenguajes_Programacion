import json
from datetime import datetime
from AFD_lector import *

def afd_to_json(afd, filename=None, include_metadata=True):
    """
    Convierte un AFD a formato JSON y lo guarda en un archivo.
    
    Args:
        afd: Instancia de la clase AFD
        filename: Nombre del archivo JSON (opcional)
        include_metadata: Si incluir metadatos como fecha de creación
    
    Returns:
        dict: Diccionario con la estructura del AFD
    """
    
    # Crear estructura JSON
    afd_dict = {
        "alfabeto": afd.Alfabeto_,
        "estados": [],
        "transiciones": [],
        "estado_inicial": afd.q0.numero,
        "estados_finales": [estado.numero for estado in afd.F_],
        "total_estados": len(afd.Q_),
        "total_transiciones": len(afd.S_)
    }
    
    # Agregar estados
    for estado in afd.Q_:
        estado_dict = {
            "numero": estado.numero,
            "estados_AFN": estado.estados_AFN if hasattr(estado, 'estados_AFN') else []
        }
        afd_dict["estados"].append(estado_dict)
    
    # Agregar transiciones
    for transicion in afd.S_:
        transicion_dict = {
            "estado_origen": transicion.q0.numero,
            "estado_destino": transicion.qf.numero,
            "simbolo": transicion.valor
        }
        afd_dict["transiciones"].append(transicion_dict)
    
    # Agregar metadatos si se solicita
    if include_metadata:
        afd_dict["metadatos"] = {
            "fecha_creacion": datetime.now().isoformat(),
            "tipo": "AFD",
            "version": "1.0"
        }
    
    # Guardar en archivo si se especifica nombre
    if filename:
        if not filename.endswith('.json'):
            filename += '.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(afd_dict, f, indent=4, ensure_ascii=False)
        
        print(f"AFD guardado en: {filename}")
    
    return afd_dict

def json_to_afd(filename_or_dict):
    """
    Carga un AFD desde un archivo JSON o diccionario.
    
    Args:
        filename_or_dict: Nombre del archivo JSON o diccionario con la estructura
    
    Returns:
        AFD: Instancia de la clase AFD
    """
    
    # Cargar datos desde archivo o usar el diccionario directamente
    if isinstance(filename_or_dict, str):
        with open(filename_or_dict, 'r', encoding='utf-8') as f:
            afd_dict = json.load(f)
        print(f"AFD cargado desde: {filename_or_dict}")
    else:
        afd_dict = filename_or_dict
    
    # Crear estados
    estados = []
    estados_dict = {}
    
    for estado_data in afd_dict["estados"]:
        estado = Estado_AFD(
            numero=estado_data["numero"],
            estados_AFN=estado_data.get("estados_AFN", [])
        )
        estados.append(estado)
        estados_dict[estado_data["numero"]] = estado
    
    # Crear transiciones
    transiciones = []
    for trans_data in afd_dict["transiciones"]:
        q0 = estados_dict[trans_data["estado_origen"]]
        qf = estados_dict[trans_data["estado_destino"]]
        transicion = Transicion(q0, qf, trans_data["simbolo"])
        transiciones.append(transicion)
    
    # Identificar estado inicial
    estado_inicial = estados_dict[afd_dict["estado_inicial"]]
    
    # Identificar estados finales
    estados_finales = set()
    for numero_final in afd_dict["estados_finales"]:
        estados_finales.add(estados_dict[numero_final])
    
    # Crear instancia AFD
    afd = AFD(
        alfabeto=afd_dict["alfabeto"],
        estados=estados,
        transiciones=transiciones,
        estado_inicial=estado_inicial,
        estados_finales=estados_finales
    )
    
    return afd

def save_afd_with_info(afd, base_filename, dfa_structure=None, test_results=None):
    """
    Guarda el AFD con información adicional completa.
    
    Args:
        afd: Instancia AFD
        base_filename: Nombre base del archivo
        dfa_structure: Estructura original del DFA (opcional)
        test_results: Resultados de pruebas (opcional)
    """
    
    # Crear estructura completa
    complete_structure = {
        "afd": afd_to_json(afd, filename=None),
        "informacion_adicional": {
            "estructura_original": dfa_structure,
            "resultados_pruebas": test_results,
            "estadisticas": {
                "total_estados": len(afd.Q_),
                "total_transiciones": len(afd.S_),
                "alfabeto_size": len(afd.Alfabeto_),
                "estados_finales_count": len(afd.F_)
            }
        }
    }
    
    # Guardar archivo completo
    filename = f"{base_filename}_completo.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(complete_structure, f, indent=4, ensure_ascii=False)
    
    # Guardar solo el AFD
    afd_to_json(afd, f"{base_filename}_afd.json")
    
    print(f"Archivos guardados:")
    print(f"  - AFD completo: {filename}")
    print(f"  - AFD simple: {base_filename}_afd.json")

def compare_afds(afd1, afd2):
    """
    Compara dos AFDs y devuelve las diferencias.
    
    Args:
        afd1, afd2: Instancias de AFD a comparar
    
    Returns:
        dict: Diccionario con las diferencias encontradas
    """
    
    differences = {
        "alfabeto": afd1.Alfabeto_ != afd2.Alfabeto_,
        "total_estados": len(afd1.Q_) != len(afd2.Q_),
        "total_transiciones": len(afd1.S_) != len(afd2.S_),
        "estado_inicial": afd1.q0.numero != afd2.q0.numero,
        "estados_finales": {e.numero for e in afd1.F_} != {e.numero for e in afd2.F_}
    }
    
    return differences