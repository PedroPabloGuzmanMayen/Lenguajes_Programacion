import os
import graphviz
import json
from tree import TreeNode, compute_empty_transition_closure

def convert_to_postfix(infix_expr):
    """Convierte una expresión infix a postfix (notación polaca inversa)."""
    operator_precedence = {'|': 1, '.': 2, '*': 3}
    result = []
    operator_stack = []

    # Procesamiento de tokens
    i = 0
    while i < len(infix_expr):
        current = infix_expr[i]
        
        # Manejo de tokens especiales como #1000
        if current == '#' and i + 1 < len(infix_expr):
            j = i + 1
            while j < len(infix_expr) and infix_expr[j].isdigit():
                j += 1
            result.append(infix_expr[i:j])
            i = j
            continue
            
        # Manejo de números multi-dígito
        elif current.isdigit():
            j = i
            while j < len(infix_expr) and infix_expr[j].isdigit():
                j += 1
            result.append(infix_expr[i:j])
            i = j
            continue
            
        # Manejo de letras
        elif current.isalpha():
            result.append(current)
            i += 1
            continue
            
        # Manejo de paréntesis de apertura
        elif current == '(':
            operator_stack.append(current)
            i += 1
            continue
            
        # Manejo de paréntesis de cierre
        elif current == ')':
            while operator_stack and operator_stack[-1] != '(':
                result.append(operator_stack.pop())
            
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()  # Eliminar el paréntesis de apertura
            
            i += 1
            continue
            
        # Manejo de operadores
        elif current in operator_precedence:
            while (operator_stack and operator_stack[-1] != '(' and 
                   operator_precedence.get(operator_stack[-1], 0) >= operator_precedence[current]):
                result.append(operator_stack.pop())
            
            operator_stack.append(current)
            i += 1
            continue
            
        # Omitir otros caracteres
        else:
            i += 1
    
    # Vaciar la pila de operadores
    while operator_stack:
        result.append(operator_stack.pop())
        
    return result

def construct_syntax_tree(postfix_expr):
    """Construye el árbol de sintaxis abstracta a partir de la expresión postfija."""
    stack = []
    position_map = {}
    pos_counter = 1
    
    for token in postfix_expr:
        token = token.strip()
        if not token:
            continue
            
        # Si es un dígito (código ASCII)
        if token.isdigit():
            node = TreeNode(token)
            node.pos = pos_counter
            node.first_positions = node.last_positions = {pos_counter}
            node.can_be_empty = False
            position_map[pos_counter] = node
            stack.append(node)
            pos_counter += 1
            continue
            
        # Si es un token como #1000, #1001, etc.
        if token.startswith('#') and token[1:].isdigit():
            node = TreeNode(token)
            node.pos = pos_counter
            node.first_positions = node.last_positions = {pos_counter}
            node.can_be_empty = False
            position_map[pos_counter] = node
            stack.append(node)
            pos_counter += 1
            continue
            
        # Si es épsilon
        if token == '949':
            node = TreeNode(token)
            node.can_be_empty = True
            node.first_positions = node.last_positions = set()
            stack.append(node)
            continue
            
        # Operadores unarios
        if token in {'*', '?', '+'}:
            if not stack:
                raise ValueError(f"Error: El operador '{token}' necesita un operando.")
                
            child = stack.pop()
            
            if token == '*':
                node = TreeNode('*', child)
                node.can_be_empty = True
                node.first_positions = child.first_positions
                node.last_positions = child.last_positions
                
            elif token == '?':  # Opcional: A?
                node = TreeNode('|', child, TreeNode('949'))  # A | ε
                node.can_be_empty = True
                node.first_positions = child.first_positions | set()
                node.last_positions = child.last_positions | set()
                
            elif token == '+':  # Una o más: A+
                star_node = TreeNode('*', child)
                node = TreeNode('.', child, star_node)
                node.can_be_empty = child.can_be_empty
                node.first_positions = child.first_positions
                node.last_positions = star_node.last_positions
                
            stack.append(node)
            continue
            
        # Operadores binarios
        if token in {'|', '.'}:
            if len(stack) < 2:
                print(f"Estado de la pila antes del error: {stack}")
                raise ValueError(f"Error: El operador '{token}' necesita dos operandos.")
                
            right = stack.pop()
            left = stack.pop()
            node = TreeNode(token, left, right)
            
            if token == '|':  # Alternativa: A|B
                node.can_be_empty = left.can_be_empty or right.can_be_empty
                node.first_positions = left.first_positions | right.first_positions
                node.last_positions = left.last_positions | right.last_positions
                
            else:  # Concatenación: A.B
                node.can_be_empty = left.can_be_empty and right.can_be_empty
                node.first_positions = left.first_positions if not left.can_be_empty else left.first_positions | right.first_positions
                node.last_positions = right.last_positions if not right.can_be_empty else left.last_positions | right.last_positions
                
            stack.append(node)
            continue
            
        # Token desconocido
        raise ValueError(f"Token no reconocido: '{token}'")
        
    # Verificación final
    if len(stack) != 1:
        print(f"Estado final de la pila (debería contener solo un nodo): {stack}")
        raise ValueError("Error: Expresión inválida, no se puede construir el árbol.")
        
    return stack[0], position_map

def visualize_syntax_tree(root):
    """Genera una visualización gráfica del árbol de sintaxis."""
    dot = graphviz.Digraph('SyntaxTree')
    
    def add_node_to_graph(node, parent_id=None):
        if node:
            node_id = str(id(node))
            label = f"{node.symbol}"
            
            if node.pos:
                label += f" ({node.pos})"
                
            dot.node(node_id, label)
            
            if parent_id:
                dot.edge(parent_id, node_id)
                
            add_node_to_graph(node.left, node_id)
            add_node_to_graph(node.right, node_id)
    
    add_node_to_graph(root)
    return dot

def calculate_follow_positions(root, position_map):
    """Calcula las posiciones de seguimiento para cada posición en el árbol."""
    follow_pos = {pos: set() for pos in position_map}
    
    def traverse(node):
        if node:
            if node.symbol == '.':  # Para cada posición en lastpos(c1), añadir firstpos(c2)
                for i in node.left.last_positions:
                    follow_pos[i] |= node.right.first_positions
                    
            elif node.symbol == '*':  # Para cada posición en lastpos(n), añadir firstpos(n)
                for i in node.last_positions:
                    follow_pos[i] |= node.first_positions
                    
            traverse(node.left)
            traverse(node.right)
    
    traverse(root)
    return follow_pos

def clean_text(text):
    """Elimina espacios en blanco al inicio y final del texto."""
    start = 0
    while start < len(text) and text[start] in [' ', '\t', '\n', '\r']:
        start += 1
        
    end = len(text) - 1
    while end >= 0 and text[end] in [' ', '\t', '\n', '\r']:
        end -= 1
        
    return text[start:end+1] if start <= end else ''

def create_dfa(root, position_map, follow_positions):
    """Genera un autómata finito determinista (DFA) a partir del árbol sintáctico."""
    dfa = graphviz.Digraph('DFA')
    dfa.attr(rankdir='LR')
    
    # Calcular el estado inicial con cierre epsilon
    initial_state = frozenset(compute_empty_transition_closure(root.first_positions, position_map, follow_positions))
    states_dict = {initial_state: 'A'}
    pending_states = [initial_state]
    state_counter = 0
    
    # Crear diccionario para almacenar el DFA
    dfa_structure = {
        'transitions': {}, 
        'acceptance_states': [], 
        'initial_state': 'A', 
        'states': {},
    }
    
    # Crear nodo inicial invisible
    dfa.node('', shape='none')
    dfa.edge('', 'A', label='')
    
    # Identificar posiciones de aceptación (nodos marcados con '#')
    acceptance_positions = {pos for pos, node in position_map.items() if node.symbol.startswith('#')}
    
    while pending_states:
        current_state = pending_states.pop(0)
        current_name = states_dict[current_state]
        dfa_structure['states'][current_state] = current_name
        
        # Marcar estado de aceptación si contiene alguna posición final
        if any(p in current_state for p in acceptance_positions):
            dfa_structure['acceptance_states'].append(current_name)
        
        # Calcular transiciones
        transitions = {}
        for pos in current_state:
            symbol = position_map[pos].symbol
            if symbol == '949' or symbol.startswith('#'):
                continue
                
            if symbol not in transitions:
                transitions[symbol] = set()
                
            transitions[symbol] |= follow_positions[pos]
        
        # Registrar transiciones en el DFA
        dfa_structure['transitions'][current_name] = {}
        for symbol, next_pos in transitions.items():
            if not next_pos:
                continue
                
            next_state = frozenset(compute_empty_transition_closure(next_pos, position_map, follow_positions))
            
            if next_state not in states_dict:
                state_counter += 1
                states_dict[next_state] = chr(ord('A') + state_counter)
                pending_states.append(next_state)
                
            dfa.edge(current_name, states_dict[next_state], label=str(symbol))
            dfa_structure['transitions'][current_name][symbol] = states_dict[next_state]
    
    # Agregar todos los estados al gráfico
    for state_set, name in states_dict.items():
        shape = 'doublecircle' if name in dfa_structure['acceptance_states'] else 'circle'
        dfa.node(name, shape=shape)
    
    # Asignar etiquetas (tags) a estados de aceptación
    state_tags = {}
    for state_set, name in states_dict.items():
        # Buscar nodos hoja que sean tags
        tag_candidates = [int(position_map[pos].symbol[1:]) 
                         for pos in state_set if position_map[pos].symbol.startswith('#')]
        if tag_candidates:
            # Seleccionar el tag con menor valor (mayor prioridad)
            min_tag = min(tag_candidates)
            state_tags[name] = '#' + str(min_tag)
            
    dfa_structure['state_tags'] = state_tags
    
    return dfa, dfa_structure

def minimize_dfa(dfa_structure):
    """Minimiza un autómata finito determinista mediante partición de estados."""
    acceptance_states = set(dfa_structure['acceptance_states'])
    groups = {}
    state_mapping = {}
    
    # Agrupar estados por sus transiciones y si son de aceptación
    for state, transitions in dfa_structure['transitions'].items():
        tag = dfa_structure.get('state_tags', {}).get(state, None)
        key = (frozenset(transitions.items()), state in acceptance_states, tag)
        if key not in groups:
            groups[key] = []
        groups[key].append(state)
    
    # Asignar nombres a los grupos
    for i, group in enumerate(groups.values()):
        name = f"M{i}"
        state_mapping[frozenset(group)] = name
    
    # Crear gráfico del DFA minimizado
    min_dfa = graphviz.Digraph('MinimizedDFA')
    min_dfa.attr(rankdir='LR')
    min_dfa.node("", shape="none")
    
    # Encontrar grupo que contiene el estado inicial
    initial_group = next(g for g in state_mapping if dfa_structure['initial_state'] in g)
    min_dfa.edge("", state_mapping[initial_group], label="")
    
    # Crear estructura para el DFA minimizado
    min_dfa_structure = {
        'transitions': {},
        'acceptance_states': [],
        'initial_state': state_mapping[initial_group],
        'states': {},
        'state_tags': {}
    }
    
    # Calcular transiciones minimizadas
    min_transitions = {}
    for group, rep_name in state_mapping.items():
        if any(s in acceptance_states for s in group):
            min_dfa_structure['acceptance_states'].append(rep_name)
            
        min_dfa_structure['states'][group] = rep_name
        min_transitions[rep_name] = {}
        
        # Tomar un estado representativo del grupo
        original_state = next(iter(group))
        
        # Mapear sus transiciones a los nuevos estados
        for symbol, dest in dfa_structure['transitions'][original_state].items():
            for g, g_name in state_mapping.items():
                if dest in g:
                    min_transitions[rep_name][symbol] = g_name
                    min_dfa_structure['transitions'].setdefault(rep_name, {})[symbol] = g_name
                    break
    
    # Propagar tags desde estados originales a estados minimizados
    min_state_tags = {}
    if 'state_tags' in dfa_structure:
        for group, rep_name in state_mapping.items():
            tag_candidates = []
            for state in group:
                if state in dfa_structure['state_tags']:
                    tag_candidates.append(dfa_structure['state_tags'][state])
                    
            if tag_candidates:
                # Seleccionar tag con menor valor numérico (mayor prioridad)
                tag_candidates.sort(key=lambda tag: int(tag[1:]))
                min_state_tags[rep_name] = tag_candidates[0]
                
    min_dfa_structure['state_tags'] = min_state_tags
    
    # Dibujar estados y transiciones
    for state, transitions in min_transitions.items():
        shape = 'doublecircle' if state in min_dfa_structure['acceptance_states'] else 'circle'
        min_dfa.node(state, shape=shape)
        
        for symbol, dest in transitions.items():
            min_dfa.edge(state, dest, symbol)
    
    return min_dfa, min_dfa_structure


class DFAInspector:
    """
    Clase para inspeccionar y mostrar información de un Autómata Finito Determinista (DFA)
    guardado en un archivo JSON.
    """
    
    @staticmethod
    def mostrar_informacion_dfa(ruta_archivo):
        """
        Carga un DFA desde un archivo .json y muestra su información en formato de texto:
        - Estado inicial
        - Estados de aceptación
        - Transiciones por estado
        
        Args:
            ruta_archivo (str): Ruta al archivo JSON que contiene el DFA
        """
        if not os.path.exists(ruta_archivo):
            print(f" Archivo no encontrado: {ruta_archivo}")
            return

        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                dfa = json.load(archivo)

            if not isinstance(dfa, dict):
                raise ValueError("El archivo no contiene un diccionario de DFA válido.")

            print(f"DFA cargado desde: {ruta_archivo}")
            
            # Mostrar estado inicial
            estado_inicial = dfa.get('initial_state', dfa.get('initial', 'No definido'))
            print(f" Estado inicial: {estado_inicial}")

            # Mostrar estados de aceptación
            estados_aceptacion = dfa.get('acceptance_states', dfa.get('accepted', []))
            if estados_aceptacion:
                print(f"Estados de aceptación: {', '.join(estados_aceptacion)}")
            else:
                print("Estados de aceptación: Ninguno")

            # Mostrar transiciones
            transiciones = dfa.get('transitions', {})
            print(f" Tabla de transiciones:")
            for estado_origen, trans in transiciones.items():
                for simbolo, estado_destino in trans.items():
                    print(f"    {estado_origen} --{simbolo}--> {estado_destino}")
            
            # Mostrar etiquetas de estados si existen
            if 'state_tags' in dfa and dfa['state_tags']:
                print(f" Etiquetas de estados:")
                for estado, etiqueta in dfa['state_tags'].items():
                    print(f"    Estado {estado}: {etiqueta}")

        except json.JSONDecodeError:
            print(f"Error: El archivo no contiene un JSON válido.")
        except Exception as e:
            print(f"Error al inspeccionar el DFA: {e}")



class DFASerializer:
    """
    Clase para serializar y deserializar Autómatas Finitos Deterministas (DFA)
    usando el formato JSON, más estándar y legible que pickle.
    """
    
    @staticmethod
    def _convertir_para_json(objeto):
        """
        Convierte tipos de datos no serializables en JSON (como sets y frozensets)
        a tipos serializables (listas).
        
        Args:
            objeto: Cualquier objeto Python a convertir
            
        Returns:
            Versión serializable a JSON del objeto
        """
        if isinstance(objeto, (set, frozenset)):
            return list(objeto)
        elif isinstance(objeto, dict):
            return {str(k): DFASerializer._convertir_para_json(v) for k, v in objeto.items()}
        elif isinstance(objeto, list) or isinstance(objeto, tuple):
            return [DFASerializer._convertir_para_json(item) for item in objeto]
        return objeto
    
    @staticmethod
    def _reconvertir_desde_json(data):
        """
        Reconstruye tipos de datos complejos desde el formato JSON.
        Algunas estructuras (como frozensets como claves de diccionarios) no se pueden
        reconstruir exactamente, pero no afecta la funcionalidad del DFA.
        
        Args:
            data: Datos cargados desde JSON
            
        Returns:
            Datos convertidos a estructura Python adecuada para el DFA
        """
        if isinstance(data, dict):
            return {k: DFASerializer._reconvertir_desde_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            # Si la clave es 'states', mantenerla como diccionario
            return data
        return data
    
    @staticmethod
    def guardar_dfa(dfa_dict, ruta_destino):
        """
        Guarda un diccionario DFA en un archivo JSON (.json)
        
        Args:
            dfa_dict (dict): El diccionario del DFA generado
            ruta_destino (str): Ruta completa donde se guardará el archivo
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            # Asegurarse de que tenga extensión .json
            if not ruta_destino.endswith('.json'):
                ruta_destino += '.json'
                
            # Asegurarse de que el directorio exista
            directorio = os.path.dirname(ruta_destino)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Convertir a formato serializable en JSON
            dfa_json = DFASerializer._convertir_para_json(dfa_dict)
            
            # Guardar el archivo JSON con formato legible
            with open(ruta_destino, 'w', encoding='utf-8') as archivo:
                json.dump(dfa_json, archivo, indent=2)
                
            print(f"✅ DFA guardado exitosamente en: {ruta_destino}")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar el DFA: {e}")
            return False
    
    @staticmethod
    def cargar_dfa(ruta_archivo):
        """
        Carga un DFA desde un archivo JSON (.json)
        
        Args:
            ruta_archivo (str): Ruta del archivo JSON que contiene el DFA
            
        Returns:
            dict: El diccionario del DFA con su estructura completa
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el archivo no contiene un DFA válido
            RuntimeError: Otros errores durante la carga
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"❌ El archivo no existe: {ruta_archivo}")

        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                dfa_dict = json.load(archivo)

            # Validación básica de la estructura
            if not isinstance(dfa_dict, dict):
                raise ValueError("❌ El archivo no contiene un diccionario válido.")

            # Verificar campos obligatorios, adaptándose a ambas convenciones de nombres
            campos_requeridos = [
                ('transitions', 'transitions'),
                ('acceptance_states', 'accepted'), 
                ('initial_state', 'initial')
            ]
            
            for campo_nuevo, campo_alt in campos_requeridos:
                if not (campo_nuevo in dfa_dict or campo_alt in dfa_dict):
                    raise ValueError(f"❌ El DFA no tiene el campo requerido: {campo_nuevo} o {campo_alt}")

            # Normalizar nombres de campos si es necesario
            if 'accepted' in dfa_dict and 'acceptance_states' not in dfa_dict:
                dfa_dict['acceptance_states'] = dfa_dict['accepted']
                
            if 'initial' in dfa_dict and 'initial_state' not in dfa_dict:
                dfa_dict['initial_state'] = dfa_dict['initial']
            
            # Reconvertir a tipos de datos adecuados
            dfa_dict = DFASerializer._reconvertir_desde_json(dfa_dict)

            print(f"✅ DFA cargado correctamente desde: {ruta_archivo}")
            print(f"   Estados: {len(dfa_dict['transitions'])}, Estados de aceptación: {len(dfa_dict['acceptance_states'])}")
            
            return dfa_dict

        except json.JSONDecodeError:
            raise ValueError(f"❌ El archivo no contiene un JSON válido.")
        except Exception as e:
            if isinstance(e, (FileNotFoundError, ValueError)):
                raise
            raise RuntimeError(f"❌ Error al cargar el DFA: {e}")