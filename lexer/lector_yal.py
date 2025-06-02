from AFD_lector import *
import sys
from buffer_lexer import Buffer

class Lector_Yal:
    def __init__(self, path_yalp):
        self.contenido = {
        'definiciones': {},
        'reglas': []
        }
        self.buffer = Buffer(path_yalp, 10)
        self.printable_chars = self._generate_printable_ascii()
    

  
    def alfabeto_generator(self):
        alfabeto = []
        alfabeto.extend([chr(c) for c in range(ord('a'), ord('z') + 1)])
        alfabeto.extend([chr(c) for c in range(ord('A'), ord('Z') + 1)])
        alfabeto.extend([chr(c) for c in range(ord('0'), ord('9') + 1)])
        alfabeto.extend([
            ';','%','[', ']', "'", '=', '+', '+', 'ε', '*', '(', ')', '_',
            '\x7F', '\\', '-', '|', 'ε', '?', '.', ':', '<', '>', '/', '"', '{', '}'
        ])
        return alfabeto


    def verificar_comentarios(self, tokens):
        dentro_comentario = False
        for i, token in enumerate(tokens):
            if '(*' in token and '*)' in token:
                continue
            elif '(*' in token:
                if dentro_comentario:
                    print(f" ❌ Error: comentario anidado sin cerrar previamente en token '{tokens[i-1]} {token} {tokens[i+1]}' (posición {i})")
                    exit(1)
                dentro_comentario = True
            elif '*)' in token:
                if not dentro_comentario:
                    print(f" ❌ Error: comentario cerrado sin haberse abierto en token '{tokens[i-1]} {token} {tokens[i+1]}' (posición {i})")
                    exit(1)
                dentro_comentario = False

        if dentro_comentario:
            print(" ❌ Error: comentario abierto sin cerrar al final del archivo.")
            exit(1)

    def parse_lexers(self):
        alfabeto = self.alfabeto_generator()

        q0, q1, q2, q3, q4, q5, q6, q7, q8 = (
        Estado_AFD("q0"), Estado_AFD("q1"), Estado_AFD("q2"),
        Estado_AFD("q3"), Estado_AFD("q4"), Estado_AFD("q5"),
        Estado_AFD("q6"), Estado_AFD("q7"), Estado_AFD("q8")
        )

        estados = [q0, q1, q2, q3, q4, q5, q6, q7, q8]

        transiciones = [Transicion(q0, q7, simbolo) for simbolo in alfabeto]
        transiciones += [Transicion(q7, q7, simbolo) for simbolo in alfabeto]


        finales = {q7}
        
        afd = AFD(
        alfabeto=alfabeto,
        estados=estados,
        transiciones=transiciones,
        estado_inicial=q0,
        estados_finales=finales)

        

        cadena_actual = ""
        tokens = []
        while self.buffer.FLAG_SALIDA:
            self.buffer.cargar_buffer()
            while self.buffer.FLAG_SALIDA:
                caracter = self.buffer.obtener_siguiente_caracter()
                tempCadena = cadena_actual + str(caracter)

                if (afd.acept_Chain(tempCadena)):
                    cadena_actual = tempCadena
                    
                
                else:
                    if cadena_actual != "":
                        tokens.append(cadena_actual)
                    cadena_actual = ""
            
            
            tokens.append(cadena_actual)
        tokens = [token.replace('ε', ' ') for token in tokens]

    
        self.verificar_comentarios(tokens)


        # self.verificar_producciones(tokens)


        i = 0
        # terminales = []
        # ignorados = []
        # no_terminales = []
        # producciones = {}
        # simbolo_inicial = ""

        i = 0
        while i < len(tokens):
            # Quitar comentarios multilínea
            if tokens[i] == '(*' or ('(*' in tokens[i]):
                i += 1
                while i < len(tokens) and tokens[i] != '*)' and '*)' not in tokens[i]:
                    i += 1
                i += 1  # Saltar el '*)'
                continue

            # Procesar definiciones let
            if tokens[i] == 'let':
                i += 1
                if i >= len(tokens):
                    return  # o manejar error

                nombre = tokens[i]
                i += 1

                # Asegurar que el siguiente token sea '='
                if i >= len(tokens) or tokens[i] != '=':
                    print(f"❌ Error: Se esperaba '=' después del nombre {nombre}")
                    exit(1)
                i += 1

                definicion = []
                while i < len(tokens):
                    t = tokens[i]

                    # Saltar comentarios de una sola línea o embebidos en una línea
                    if '(*' in t and '*)' in t:
                        i += 1
                        continue

                    # Comentario multilínea
                    if t == '(*' or ('(*' in t):
                        i += 1
                        while i < len(tokens) and '*)' not in tokens[i]:
                            i += 1
                        i += 1
                        continue

                    # Fin de la definición si empieza otra o un delimitador importante
                    if t == 'let' or t == 'rule':
                        break

                    definicion.append(t)
                    i += 1

                self.contenido['definiciones'][nombre] = ' '.join(definicion)
                continue

            # Procesar regla "rule tokens ="
            if (i + 2 < len(tokens) and tokens[i] == 'rule' and tokens[i+1] == 'tokens' and tokens[i+2] == '='):
                i += 3  # saltar 'rule', 'tokens', '='
                
                while i < len(tokens):
                    # Saltar comentarios multilínea en reglas
                    if tokens[i] == '(*' or ('(*' in tokens[i]):
                        i += 1
                        while i < len(tokens) and '*)' not in tokens[i]:
                            i += 1
                        i += 1
                        continue
                    
                    # Saltar '|', si está
                    if tokens[i] == '|':
                        i += 1
                        if i >= len(tokens):
                            break
                    
                    if i >= len(tokens):
                        break
                    
                    expresion = tokens[i]
                    i += 1
                    
                    # Verificar si hay una acción (entre llaves)
                    if i < len(tokens) and tokens[i] == '{':
                        i += 1  # saltar '{'
                        
                        accion_tokens = []
                        nivel_llaves = 1  # Contador para balancear llaves
                        
                        while i < len(tokens) and nivel_llaves > 0:
                            if tokens[i] == '{':
                                nivel_llaves += 1
                            elif tokens[i] == '}':
                                nivel_llaves -= 1
                            
                            if nivel_llaves > 0:  # Solo agregar si no es la llave de cierre final
                                accion_tokens.append(tokens[i])
                            
                            i += 1
                        
                        if nivel_llaves > 0:
                            print(f" ❌ Error: No se encontró '}}' para cerrar la acción de '{expresion}'")
                            sys.exit(1)
                            break
                        
                        # Verificar si la acción tiene 'return'
                        if 'return' in accion_tokens:
                            idx = accion_tokens.index('return')
                            accion = accion_tokens[idx + 1] if (idx + 1) < len(accion_tokens) else 'None'
                            
                            self.contenido['reglas'].append({
                                'expresion': expresion,
                                'accion': 'return ' + accion
                            })
                        else:
                            # Acción sin return: asignar None
                            self.contenido['reglas'].append({
                                'expresion': expresion,
                                'accion': 'None'
                            })
                    else:
                        # No hay acción (sin llaves): asignar None
                        self.contenido['reglas'].append({
                            'expresion': expresion,
                            'accion': None
                        })
                    
                    continue
                
                # Avanzar para evitar ciclo infinito en tokens no reconocidos
                i += 1
        
    def _generate_printable_ascii(self):
        return set(chr(code) for code in range(32, 127))
    
    def trim_whitespace_manual(self, text):
            start_pos = 0
            while start_pos < len(text) and text[start_pos] in [' ', '\t', '\n', '\r']:
                start_pos += 1

            end_pos = len(text) - 1
            while end_pos >= 0 and text[end_pos] in [' ', '\t', '\n', '\r']:
                end_pos -= 1

            return text[start_pos:end_pos+1] if start_pos <= end_pos else ''
    
    
    def strip_custom_chars(self, text, chars_to_remove=" ()"):
            start_pos = 0
            while start_pos < len(text) and text[start_pos] in chars_to_remove:
                start_pos += 1

            end_pos = len(text) - 1
            while end_pos >= 0 and text[end_pos] in chars_to_remove:
                end_pos -= 1

            return text[start_pos:end_pos+1] if start_pos <= end_pos else ''
    
    def convert_to_ascii_code(self, token):
            """Convierte tokens de un carácter a su código ASCII."""
            if len(token) == 1:
                return str(ord(token))
            return token
    
    def advance_past_whitespace(self, line, current_pos):
        """Avanza el índice saltando espacios en blanco."""
        while current_pos < len(line) and line[current_pos] in [' ', '\t', '\n', '\r']:
            current_pos += 1
        return current_pos
    def extract_variable_definitions(self, text_lines):
        """Extrae definiciones de variables (let <name> = <expression>)."""
        variable_map = {}
        for line in text_lines:
            pos = self.advance_past_whitespace(line, 0)
            if pos >= len(line):
                continue
            if pos + 3 <= len(line) and line[pos:pos+3] == "let":
                pos += 3
                pos = self.advance_past_whitespace(line, pos)
                name_start = pos
                while pos < len(line) and not line[pos].isspace() and line[pos] != '=':
                    pos += 1
                var_name = line[name_start:pos]
                pos = self.advance_past_whitespace(line, pos)
                if pos < len(line) and line[pos] == '=':
                    pos += 1
                pos = self.advance_past_whitespace(line, pos)
                definition = ""
                while pos < len(line):
                    definition += line[pos]
                    pos += 1
                variable_map[var_name] = definition
        return variable_map

    def handle_literal_dot_replacement(self, expression):
        """Reemplaza puntos literales por su código ASCII para evitar confusión con concatenación."""
        output = ""
        pos = 0
        while pos < len(expression):
            if expression[pos] == '.':
                # Verifica si después hay un grupo o número
                if pos + 1 < len(expression) and (expression[pos+1].isdigit() or expression[pos+1] == '('):
                    output += '46.'
                    pos += 1
                else:
                    output += '.'
                    pos += 1
            else:
                output += expression[pos]
                pos += 1
        return output

    def split_by_delimiter_manual(self, expression, separator):
        """Separa una cadena por el delimitador especificado."""
        segments = []
        current_segment = ""
        for char in expression:
            if char == separator:
                segments.append(self.trim_whitespace_manual(current_segment))
                current_segment = ""
            else:
                current_segment += char
        if current_segment:
            segments.append(self.trim_whitespace_manual(current_segment))
        return segments

    def transform_repetition_syntax(self, expression: str) -> str:
        """Transforma operadores de repetición: A+ → A(A)*, A? → (A|949)."""
        pos = 0
        output = ""
        while pos < len(expression):
            if expression[pos] in ['+', '?'] and pos > 0:
                # Buscar el operando anterior
                search_pos = len(output) - 1

                # Si termina en ')', retrocede para encontrar grupo
                if output[search_pos] == ')':
                    paren_count = 1
                    search_pos -= 1
                    while search_pos >= 0:
                        if output[search_pos] == ')':
                            paren_count += 1
                        elif output[search_pos] == '(':
                            paren_count -= 1
                            if paren_count == 0:
                                break
                        search_pos -= 1
                    operand = output[search_pos:]
                    output = output[:search_pos]
                else:
                    # Si es un número posiblemente con punto antes
                    k = search_pos
                    while k >= 0 and (output[k].isdigit() or output[k] == '.'):
                        k -= 1
                    operand = output[k+1:]
                    output = output[:k+1]

                if expression[pos] == '+':
                    output += f"{operand}({operand})*"
                elif expression[pos] == '?':
                    output += f"({operand}|949)"
                pos += 1
            else:
                output += expression[pos]
                pos += 1
        return output

    def locate_top_level_difference_op(self, expression):
        """Busca el operador '#' a nivel superior."""
        nesting_level = 0
        inside_quotes = False
        quote_type = ''
        for index, char in enumerate(expression):
            if inside_quotes:
                if char == quote_type:
                    inside_quotes = False
                continue
            if char in ["'", '"']:
                inside_quotes = True
                quote_type = char
            elif char == '(':
                nesting_level += 1
            elif char == ')':
                nesting_level -= 1
            elif char == '#' and nesting_level == 0:
                return index
        return -1

    def process_character_set(self, set_content):
        """Procesa el contenido de un conjunto de caracteres."""
        # Si el contenido está completamente entre comillas
        if (set_content.startswith('"') and set_content.endswith('"')) or (set_content.startswith("'") and set_content.endswith("'")):
            literal_content = set_content[1:-1]
            token_list = []
            k = 0
            while k < len(literal_content):
                if literal_content[k] == '\\' and k + 1 < len(literal_content):
                    escape_char = literal_content[k+1]
                    if escape_char == 's':
                        token_list.append(self.convert_to_ascii_code(' '))
                    elif escape_char == 't':
                        token_list.append(self.convert_to_ascii_code('\t'))
                    elif escape_char == 'n':
                        token_list.append(self.convert_to_ascii_code('\n'))
                    else:
                        token_list.append(self.convert_to_ascii_code(escape_char))
                    k += 2
                else:
                    token_list.append(self.convert_to_ascii_code(literal_content[k]))
                    k += 1
            return set(token_list)
        
        # Procesamiento del conjunto sin comillas externas
        token_list = []
        k = 0
        while k < len(set_content):
            # Procesa escapes explícitos
            if set_content[k] == '\\' and k+1 < len(set_content):
                next_char = set_content[k+1]
                if next_char == 's':
                    token_list.append(self.convert_to_ascii_code(' '))
                elif next_char == 't':
                    token_list.append(self.convert_to_ascii_code('\t'))
                elif next_char == 'n':
                    token_list.append(self.convert_to_ascii_code('\n'))
                else:
                    token_list.append(self.convert_to_ascii_code(next_char))
                k += 2
                continue

            # Manejo de literales entre comillas
            if set_content[k] in ["'", '"']:
                quote_char = set_content[k]
                k += 1
                literal = ""
                while k < len(set_content) and set_content[k] != quote_char:
                    if set_content[k] == '\\' and k+1 < len(set_content):
                        seq = set_content[k:k+2]
                        if seq == '\\t':
                            literal += '\t'
                        elif seq == '\\n':
                            literal += '\n'
                        elif seq == '\\s':
                            literal += ' '
                        else:
                            literal += set_content[k+1]
                        k += 2
                    else:
                        literal += set_content[k]
                        k += 1
                if k < len(set_content) and set_content[k] == quote_char:
                    k += 1
                for char in literal:
                    token_list.append(self.convert_to_ascii_code(char))
                continue

            # Manejo de espacios y rangos
            elif set_content[k].isspace():
                token_list.append(self.convert_to_ascii_code(set_content[k]))
                k += 1
                continue
            elif (k+2 < len(set_content) and set_content[k+1] == '-' and set_content[k] not in ["'", '"']):
                start_char = set_content[k]
                end_char = set_content[k+2]
                for c in range(ord(start_char), ord(end_char)+1):
                    token_list.append(chr(c))
                k += 3
                continue
            else:
                token_list.append(set_content[k])
                k += 1
        return set(token_list)

    def expand_sets_and_ranges(self, expression):
        """Expande rangos y conjuntos en la expresión."""
        if expression == "_":
            union_parts = "|".join(token for token in sorted(self.convert_to_ascii_code(x) for x in self.printable_chars) if token)
            return "(" + union_parts + ")"
        
        expression = self.remove_outer_parentheses(expression)
        diff_pos = self.locate_top_level_difference_op(expression)
        if diff_pos != -1:
            left_part = expression[:diff_pos]
            right_part = expression[diff_pos+1:]
            left_expanded = self.expand_sets_and_ranges(left_part)
            right_expanded = self.expand_sets_and_ranges(right_part)
            left_clean = self.remove_outer_parentheses(left_expanded)
            right_clean = self.remove_outer_parentheses(right_expanded)
            left_tokens = [self.strip_custom_chars(p, " ()") for p in self.split_by_delimiter_manual(left_clean, '|')]
            right_tokens = [self.strip_custom_chars(p, " ()") for p in self.split_by_delimiter_manual(right_clean, '|')]
            diff_result = sorted(set(left_tokens) - set(right_tokens))
            return "(" + "|".join(token for token in (self.convert_to_ascii_code(token) for token in diff_result) if token) + ")"
        
        result = ""
        pos = 0
        while pos < len(expression):
            if expression[pos] == '[':
                closing_pos = expression.find(']', pos)
                if closing_pos == -1:
                    result += expression[pos:]
                    break
                bracket_content = expression[pos+1:closing_pos]
                if bracket_content.startswith('^'):
                    char_set = self.process_character_set(bracket_content[1:])
                    difference_set = self.printable_chars - char_set
                    union_parts = "|".join(sorted(self.convert_to_ascii_code(x) for x in difference_set))
                    expanded_result = "(" + union_parts + ")"
                else:
                    token_list = []        
                    k = 0
                    while k < len(bracket_content):
                        if bracket_content[k] in ["'", '"']:
                            quote_char = bracket_content[k]
                            k += 1
                            literal = ""
                            while k < len(bracket_content) and bracket_content[k] != quote_char:
                                if bracket_content[k] == '\\' and k+1 < len(bracket_content):
                                    seq = bracket_content[k:k+2]
                                    if seq == '\\t':
                                        literal += '\t'
                                    elif seq == '\\n':
                                        literal += '\n'
                                    elif seq == '\\s':
                                        literal += ' '
                                    else:
                                        literal += bracket_content[k+1]
                                    k += 2
                                else:
                                    literal += bracket_content[k]
                                    k += 1
                            if k < len(bracket_content) and bracket_content[k] == quote_char:
                                k += 1
                            # Manejo de rangos dentro de comillas
                            if k < len(bracket_content) and bracket_content[k] == '-' and (k+1 < len(bracket_content)) and bracket_content[k+1] in ["'", '"']:
                                k += 1
                                next_quote = bracket_content[k]
                                k += 1
                                literal2 = ""
                                while k < len(bracket_content) and bracket_content[k] != next_quote:
                                    if bracket_content[k] == '\\' and k+1 < len(bracket_content):
                                        seq = bracket_content[k:k+2]
                                        if seq == '\\t':
                                            literal2 += '\t'
                                        elif seq == '\\n':
                                            literal2 += '\n'
                                        else:
                                            literal2 += bracket_content[k+1]
                                        k += 2
                                    else:
                                        literal2 += bracket_content[k]
                                        k += 1
                                if k < len(bracket_content) and bracket_content[k] == next_quote:
                                    k += 1
                                if len(literal) == 1 and len(literal2) == 1:
                                    for c in range(ord(literal), ord(literal2)+1):
                                        token_list.append(chr(c))
                                else:
                                    if len(literal) > 1:
                                        for char in literal:
                                            token_list.append(char)
                                    else:
                                        token_list.append(literal)
                                    token_list.append('-')
                                    token_list.append(literal2)
                            else:
                                if len(literal) > 1:
                                    for char in literal:
                                        token_list.append(char)
                                else:
                                    token_list.append(literal)

                        elif bracket_content[k].isspace():
                            token_list.append(bracket_content[k])
                            k += 1
                        elif (k+2 < len(bracket_content) and bracket_content[k+1] == '-' and bracket_content[k] not in ["'", '"']):
                            start_char = bracket_content[k]
                            end_char = bracket_content[k+2]
                            for c in range(ord(start_char), ord(end_char)+1):
                                token_list.append(chr(c))
                            k += 3
                        else:
                            token_list.append(bracket_content[k])
                            k += 1
                    
                    ascii_token_list = [self.convert_to_ascii_code(token) for token in token_list]
                    ascii_token_list = [token for token in ascii_token_list if token and token != '|']

                    if not ascii_token_list:
                        expanded_result = '949'  # Épsilon explícito cuando no hay tokens válidos
                    else:
                        expanded_result = "(" + "|".join(ascii_token_list) + ")"

                result += expanded_result
                pos = closing_pos + 1
            else:
                # Manejo de literales entre comillas
                if expression[pos] in ["'", '"']:
                    quote_char = expression[pos]
                    pos += 1
                    literal = ""
                    while pos < len(expression) and expression[pos] != quote_char:
                        if expression[pos] == '\\' and pos+1 < len(expression):
                            esc = expression[pos+1]
                            if esc == 's':
                                literal += ' '
                            elif esc == 't':
                                literal += '\t'
                            elif esc == 'n':
                                literal += '\n'
                            else:
                                literal += esc
                            pos += 2
                        else:
                            literal += expression[pos]
                            pos += 1
                    pos += 1  # Saltar comilla final
                    result += "(" + "|".join(token for token in (self.convert_to_ascii_code(c) for c in literal) if token) + ")"
                else:
                    result += expression[pos]
                    pos += 1

        return result

    def substitute_identifiers(self, expression, definitions_map):
        """Reemplaza identificadores por sus definiciones de forma recursiva."""
        result = ""
        pos = 0
        while pos < len(expression):
            current_char = expression[pos]
            if current_char in ["'", '"']:
                quote_char = current_char
                result += current_char
                pos += 1
                while pos < len(expression):
                    result += expression[pos]
                    if expression[pos] == quote_char:
                        pos += 1
                        break
                    pos += 1
            elif current_char.isalpha() or current_char == '_':
                token_start = pos
                while pos < len(expression) and (expression[pos].isalnum() or expression[pos] == '_'):
                    pos += 1
                identifier = expression[token_start:pos]
                if identifier in definitions_map:
                    sub_expression = self.substitute_identifiers(definitions_map[identifier], definitions_map)
                    sub_expression = self.simplify_parentheses(sub_expression)
                    result += f"({sub_expression})"
                else:
                    if identifier == ["_", "(_)"]:
                        union_parts = "|".join(token for token in sorted(self.convert_to_ascii_code(x) for x in self.printable_chars) if token)
                        result += "(" + union_parts + ")"
                    else:
                        result += identifier
            else:
                result += current_char
                pos += 1
        return result

    def remove_outer_parentheses(self, expression):
        """Elimina paréntesis externos redundantes."""
        while expression.startswith("(") and expression.endswith(")"):
            paren_count = 0
            is_redundant = True
            for index, char in enumerate(expression):
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                if paren_count == 0 and index < len(expression) - 1:
                    is_redundant = False
                    break
            if is_redundant:
                expression = expression[1:-1]
            else:
                break
        return expression

    def simplify_parentheses(self, expression):
        """Simplifica paréntesis redundantes."""
        while expression.startswith('(') and expression.endswith(')'):
            inner_content = expression[1:-1]
            paren_count = 0
            is_balanced = True
            for char in inner_content:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                if paren_count < 0:
                    is_balanced = False
                    break
            if is_balanced and paren_count == 0:
                expression = inner_content
            else:
                break
        return expression

    def process_optional_operators(self, expression):
        """Procesa operadores opcionales (actualmente sin transformación)."""
        return expression

    def clean_expression_syntax(self, expression):
        """Limpia la expresión eliminando operadores duplicados y paréntesis vacíos."""
        previous = None
        while previous != expression:
            previous = expression
            expression = expression.replace("||", "|")
            expression = expression.replace("..", ".")
            expression = expression.replace("()", "949")
        return expression

    def insert_concatenation_operators(self, expression):
        """Inserta operadores de concatenación '.' donde sea necesario."""
        result = ""
        pos = 0

        def needs_concatenation(char):
            return char.isdigit() or char == ')' or char == '*' or char == '949'

        def can_start_token(char):
            return char.isdigit() or char == '(' or char == '949'

        while pos < len(expression):
            current_char = expression[pos]

            token = ""
            if current_char.isdigit():
                while pos < len(expression) and expression[pos].isdigit():
                    token += expression[pos]
                    pos += 1
            else:
                token = current_char
                pos += 1

            if result:
                previous_char = result[-1]
                if needs_concatenation(previous_char) and can_start_token(token[0]):
                    result += '.'

            result += token

        return result

    def merge_rule_expressions(self, config_data):
        """Combina todas las expresiones de reglas en una expresión maestra."""
        combined_expressions = []
        tag_mapping = {}
        rule_counter = 0

        for rule_data in config_data["reglas"]:
            raw_pattern = rule_data["expresion"]

            # Convertir caracteres literales a ASCII
            if ((raw_pattern.startswith("'") and raw_pattern.endswith("'")) or 
                (raw_pattern.startswith('"') and raw_pattern.endswith('"'))):
                # Procesar cada caracter como ASCII y concatenarlo con '.'
                content = raw_pattern[1:-1]
                ascii_literals = [self.convert_to_ascii_code(ch) for ch in content]
                processed_pattern = ".".join(ascii_literals)
            elif len(raw_pattern) == 1:
                processed_pattern = self.convert_to_ascii_code(raw_pattern)
            else:
                with_identifiers = self.substitute_identifiers(raw_pattern, config_data["definiciones"])
                expanded_pattern = self.expand_sets_and_ranges(with_identifiers)
                cleaned_pattern = self.remove_outer_parentheses(expanded_pattern)
                cleaned_pattern = self.handle_literal_dot_replacement(cleaned_pattern)
                processed_pattern = self.transform_repetition_syntax(self.process_optional_operators(cleaned_pattern))

            # Caso especial: si la expresión está vacía o es solo épsilon
            if not processed_pattern or processed_pattern in ['|', '.', '()', '', '949']:
                processed_pattern = '949'

            # Agregar puntos de concatenación explícitos
            processed_pattern = self.insert_concatenation_operators(processed_pattern)

            tag_id = 1000 + rule_counter

            # Concatenar la expresión con su tag
            processed_pattern = self.simplify_parentheses(processed_pattern)
            processed_pattern = f"({processed_pattern})"
            tagged_expression = f"{processed_pattern}.#{tag_id}"

            combined_expressions.append(tagged_expression)
            tag_mapping[f"#{tag_id}"] = rule_data["accion"]
            rule_counter += 1

        # Unir todas las expresiones usando unión
        master_pattern = "|".join(expr for expr in combined_expressions if self.trim_whitespace_manual(expr))
        master_pattern = self.clean_expression_syntax(master_pattern)

        return master_pattern, tag_mapping
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python buffer.py archivo.yalp")
        sys.exit(1)

    archivo_yalp = sys.argv[1]

    lector = Lector_Yal(archivo_yalp)
    lector.parse_lexers()
    expresion_principal, reglas = lector.merge_rule_expressions(lector.contenido)

    print(lector.contenido)
    print(expresion_principal)
    print(reglas)
