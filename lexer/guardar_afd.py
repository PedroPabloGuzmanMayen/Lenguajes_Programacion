def convert_automata_structure(original_structure, state_name_to_number, filename='automata_converted.json'):
    """
    Convierte la estructura original del autómata al formato deseado y lo guarda como JSON.
    
    Args:
        original_structure: Diccionario con la estructura original
        state_name_to_number: Diccionario que mapea nombres de estados a números
        filename: Nombre del archivo JSON donde guardar (por defecto: 'automata_converted.json')
    
    Returns:
        Diccionario con la estructura convertida
    """
    
    # Crear el mapeo inverso (número a nombre)
    number_to_name = {v: k for k, v in state_name_to_number.items()}
    
    # Convertir transiciones
    new_transitions = {}
    for state_num, transitions in original_structure['transitions'].items():
        # Convertir el número de estado a nombre de estado
        state_name = number_to_name.get(state_num.replace('M', ''), state_num)
        new_transitions[state_name] = {}
        
        # Convertir cada transición
        for input_char, target_state_num in transitions.items():
            target_state_name = number_to_name.get(target_state_num.replace('M', ''), target_state_num)
            new_transitions[state_name][input_char] = target_state_name
    
    # Asegurar que todos los estados existen en transitions (incluso si están vacíos)
    for state_name in state_name_to_number.keys():
        if state_name not in new_transitions:
            new_transitions[state_name] = {}
    
    # Convertir estados de aceptación
    new_acceptance_states = []
    for state_num in original_structure['acceptance_states']:
        state_name = number_to_name.get(state_num.replace('M', ''), state_num)
        new_acceptance_states.append(state_name)
    
    # Convertir estado inicial
    initial_state_num = original_structure['initial_state']
    new_initial_state = number_to_name.get(initial_state_num.replace('M', ''), initial_state_num)
    
    # Convertir states (convertir frozenset keys a strings)
    new_states = {}
    for frozenset_key, state_num in original_structure['states'].items():
        state_name = number_to_name.get(state_num.replace('M', ''), state_num)
        # Convertir frozenset a string si es necesario
        if isinstance(frozenset_key, frozenset):
            str_key = str(frozenset_key)
        else:
            str_key = frozenset_key
        new_states[str_key] = state_name
    
    # Convertir state_tags
    new_state_tags = {}
    for state_num, tag in original_structure['state_tags'].items():
        state_name = number_to_name.get(state_num.replace('M', ''), state_num)
        new_state_tags[state_name] = tag
    
    # Crear la nueva estructura
    converted_structure = {
        'transitions': new_transitions,
        'acceptance_states': new_acceptance_states,
        'initial_state': new_initial_state,
        'states': new_states,
        'state_tags': new_state_tags
    }
    
    # Guardar en archivo JSON
    import json
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
