class Lexer:
    def __init__(self, automaton, token_labels, output_path='salida_logs.txt', debug=True):
        self.automaton = automaton
        self.token_labels = token_labels
        self.output_path = output_path
        self.debug = debug

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
