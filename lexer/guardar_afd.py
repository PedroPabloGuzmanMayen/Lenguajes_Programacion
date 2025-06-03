def convert_automata_structure(afd_instance, filename='automata_converted.json'):
    """
    Convierte la estructura del autómata a partir de la instancia AFD al formato deseado y lo guarda como JSON.
    
    Args:
        afd_instance: Instancia de la clase AFD
        filename: Nombre del archivo JSON donde guardar (por defecto: 'automata_converted.json')
    
    Returns:
        Diccionario con la estructura convertida
    """
    import json
    
    # Extraer transiciones de la instancia AFD
    new_transitions = {}
    
    # Inicializar diccionario de transiciones para todos los estados
    for estado in afd_instance.Q_:
        state_name = str(estado.numero)
        new_transitions[state_name] = {}
    
    # Llenar transiciones desde la instancia AFD
    for transicion in afd_instance.S_:
        q0_name = str(transicion.q0.numero)
        qf_name = str(transicion.qf.numero)
        symbol = transicion.valor
        
        if q0_name not in new_transitions:
            new_transitions[q0_name] = {}
        
        new_transitions[q0_name][symbol] = qf_name
    
    # Extraer estados de aceptación de la instancia AFD
    new_acceptance_states = []
    for estado_final in afd_instance.F_:
        state_name = str(estado_final.numero)
        new_acceptance_states.append(state_name)
    
    # Extraer estado inicial de la instancia AFD
    new_initial_state = str(afd_instance.q0.numero)
    
    # Crear states: mapear cada estado a su propio nombre
    new_states = {}
    for estado in afd_instance.Q_:
        state_name = str(estado.numero)
        # Usar el nombre del estado como clave y valor para mantener consistencia
        new_states[f"state_{state_name}"] = state_name
    
    # Extraer state_tags de la instancia AFD
    new_state_tags = {}
    if hasattr(afd_instance, 'state_tags') and afd_instance.state_tags:
        for state_name, tag in afd_instance.state_tags.items():
            new_state_tags[str(state_name)] = tag
    else:
        # Si no hay tags, crear tags genéricos para estados finales
        for i, estado_final in enumerate(afd_instance.F_):
            state_name = str(estado_final.numero)
            new_state_tags[state_name] = f"#{i+1}"
    
    # Crear la nueva estructura
    converted_structure = {
        'transitions': new_transitions,
        'acceptance_states': new_acceptance_states,
        'initial_state': new_initial_state,
        'states': new_states,
        'state_tags': new_state_tags
    }
    
    # Guardar en archivo JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(converted_structure, f, indent=2, ensure_ascii=False)
    print(f"Estructura convertida guardada en '{filename}'")
    
    return converted_structure


def load_automata_from_json(filepath):
    """
    Carga la estructura del autómata desde un archivo JSON.
    
    Args:
        filepath: Ruta completa del archivo JSON a cargar
    
    Returns:
        Diccionario con la estructura del autómata cargada desde el archivo
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el archivo no es un JSON válido
    """
    import json
    import ast
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            automata_structure = json.load(f)
        
        # Convertir strings de frozenset de vuelta a frozenset objects si es necesario
        if 'states' in automata_structure:
            new_states = {}
            for str_key, value in automata_structure['states'].items():
                # Si la clave parece ser un frozenset string, convertirla de vuelta
                if str_key.startswith('frozenset'):
                    try:
                        # Evaluar de forma segura el string del frozenset
                        frozenset_obj = ast.literal_eval(str_key)
                        new_states[frozenset_obj] = value
                    except (ValueError, SyntaxError):
                        # Si no se puede convertir, mantener como string
                        new_states[str_key] = value
                else:
                    new_states[str_key] = value
            automata_structure['states'] = new_states
        
        print(f"Estructura del autómata cargada exitosamente desde '{filepath}'")
        return automata_structure
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filepath}'")
        raise
    
    except json.JSONDecodeError as e:
        print(f"Error: El archivo '{filepath}' no contiene un JSON válido: {e}")
        raise
    
    except Exception as e:
        print(f"Error inesperado al cargar '{filepath}': {e}")
        raise
