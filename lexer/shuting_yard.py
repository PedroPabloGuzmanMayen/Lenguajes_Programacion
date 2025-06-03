from tree import *
import graphviz

def convert_to_postfix(infix_expr):
    """Convierte una expresión infix a postfix (notación polaca inversa)."""
    operator_precedence = {"#": 4,
    "*": 3,
    "+": 3,
    "?": 3,
    ".": 2,
    "|": 1}
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
        elif current == '_':
            result.append('949')  # <-- Convertir _ a 949
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
