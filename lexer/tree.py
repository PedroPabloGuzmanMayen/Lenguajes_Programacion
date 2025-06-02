class TreeNode:
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right
        self.first_positions = set()
        self.last_positions = set()
        self.can_be_empty = False
        self.pos = None

def is_symbol_operator(ch):
    """Verifica si un carácter es un operador."""
    return ch in {'|', '.', '*', '(', ')', '#'}

def is_symbol_operand(ch):
    """Verifica si un carácter es un operando."""
    return ch.isalnum() and not is_symbol_operator(ch)

def compute_empty_transition_closure(state_set, position_map, follow_positions):
    """Calcula el cierre epsilon de un conjunto de estados."""
    closure = set(state_set)
    pending = list(state_set)
    
    while pending:
        current_pos = pending.pop()
        symbol = position_map[current_pos].symbol
        
        if symbol == '949':  # Código para épsilon
            for next_pos in follow_positions.get(current_pos, set()):
                if next_pos not in closure:
                    closure.add(next_pos)
                    pending.append(next_pos)
    
    return closure

def add_concat_operators(expression):
    """Inserta operadores de concatenación explícitos en la expresión."""
    result = []
    
    for i in range(len(expression)):
        result.append(expression[i])
        
        if i + 1 < len(expression):
            current = expression[i]
            next_char = expression[i + 1]
            
            # Si el actual es operando o cierre y el siguiente es apertura o operando
            if (is_symbol_operand(current) or current in {')', '*'}) and \
               (is_symbol_operand(next_char) or next_char in {'(', '#'}):
                result.append('.')
    
    return ''.join(result)

