class Lexer:
    def __init__(self, automaton, token_labels, output_path='salida_logs.txt', debug=True):
        self.automaton = automaton
        self.token_labels = token_labels
        self.output_path = output_path
        self.debug = debug
        self.buffer = None

    def analyze(self, input_string):
        current_pos = 0
        token_list = []

        with open(self.output_path, 'w', encoding='utf-8') as log_file:
            while current_pos < len(input_string):
                current_state = self.automaton['initial_state']
                transitions = self.automaton['transitions']
                accepting_states = set(self.automaton['acceptance_states'])

                last_valid_state = None
                lexeme_end = current_pos

                index = current_pos
                path_trace = []

                while index < len(input_string):
                    char = input_string[index]
                    ascii_code = str(ord(char))

                    if current_state in transitions and ascii_code in transitions[current_state]:
                        next_state = transitions[current_state][ascii_code]
                        path_trace.append((current_state, ascii_code, next_state))
                        current_state = next_state
                        index += 1

                        if current_state in accepting_states:
                            last_valid_state = current_state
                            lexeme_end = index
                    else:
                        break

                if last_valid_state is None:
                    log_file.write(f"❌ Lexical error: unexpected symbol '{input_string[current_pos]}' at position {current_pos}\n")
                    current_pos += 1
                    continue

                lexeme = input_string[current_pos:lexeme_end]
                if last_valid_state in self.automaton.get('state_tags', {}):
                    tag = self.automaton['state_tags'][last_valid_state]
                    token = self.token_labels.get(tag, 'UNKNOWN')
                else:
                    token = 'UNKNOWN'

                token_list.append((token, lexeme))
                if self.debug:
                    log_file.write(f"✔️ Token: {token}, lexeme: '{lexeme}'\n")

                current_pos = lexeme_end

        return token_list

    def token_producer(self, buffer):
        self.buffer = buffer
        
        with open(self.output_path, 'w', encoding='utf-8') as log_file:
            # Bucle externo: mientras hay datos en el archivo
            while self.buffer.FLAG_SALIDA:
                self.buffer.cargar_buffer()
                
                # Bucle interno: procesa cada carácter del buffer actual
                while self.buffer.FLAG_SALIDA:
                    # Inicializar variables para el análisis del token actual
                    current_state = self.automaton['initial_state']
                    transitions = self.automaton['transitions']
                    accepting_states = set(self.automaton['acceptance_states'])
                    
                    last_valid_state = None
                    lexeme_chars = []
                    chars_processed = 0
                    
                    # Buscar el token más largo posible (longest match)
                    while self.buffer.FLAG_SALIDA:
                        caracter = self.buffer.obtener_siguiente_caracter()
                        if caracter is None:  # Buffer vacío
                            break
                            
                        ascii_code = str(ord(caracter))
                        chars_processed += 1
                        
                        # Verificar si hay transición válida
                        if current_state in transitions and ascii_code in transitions[current_state]:
                            next_state = transitions[current_state][ascii_code]
                            current_state = next_state
                            lexeme_chars.append(caracter)
                            
                            # Verificar si es estado de aceptación
                            if current_state in accepting_states:
                                last_valid_state = current_state
                                # Continuar buscando match más largo
                        else:
                            # No hay transición válida, retroceder
                            # Devolver el último caracter leído al buffer
                            self.buffer.retroceder_caracter()
                            chars_processed -= 1
                            break
                    
                    # Procesar el resultado
                    if last_valid_state is None:
                        # Error léxico - no se encontró token válido
                        if lexeme_chars:
                            error_char = lexeme_chars[0]
                            log_file.write(f"❌ Lexical error: unexpected symbol '{error_char}' at current position\n")
                            log_file.flush()
                            # Avanzar solo un caracter para continuar
                            if chars_processed > 1:
                                # Retroceder todos los caracteres excepto el primero
                                for _ in range(chars_processed - 1):
                                    self.buffer.retroceder_caracter()
                        continue
                    
                    # Token válido encontrado
                    # Retroceder caracteres que no forman parte del token válido
                    valid_lexeme_length = len([c for c in lexeme_chars])
                    if chars_processed > valid_lexeme_length:
                        for _ in range(chars_processed - valid_lexeme_length):
                            self.buffer.retroceder_caracter()
                    
                    # Construir el lexema válido
                    lexeme = ''.join(lexeme_chars)
                    
                    # Obtener el tipo de token
                    if last_valid_state in self.automaton.get('state_tags', {}):
                        tag = self.automaton['state_tags'][last_valid_state]
                        token_type = self.token_labels.get(tag, 'UNKNOWN')
                    else:
                        token_type = 'UNKNOWN'
                    
                    # Producir el token
                    token = (token_type, lexeme)
                    
                    if self.debug:
                        log_file.write(f"✔️ Token: {token_type}, lexeme: '{lexeme}'\n")
                        log_file.flush()
                    
                    # Yield para hacer esta función un generador
                    yield token
        yield ('$', '$')