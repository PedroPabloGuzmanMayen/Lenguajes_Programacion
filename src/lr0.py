class LR0Automaton:
    def __init__(self, grammar_builder):
        """
        Inicializa el autómata LR(0) con una gramática extendida
        :param grammar_builder: Instancia de una clase GrammarBuilder ya extendida
        """
        self.grammar = grammar_builder.get_grammar()
        self.start_symbol = grammar_builder.get_start_symbol()
        self.symbols = grammar_builder.get_symbols()
        self.terminals = grammar_builder.get_terminals()
        self.non_terminals = grammar_builder.get_non_terminals()
        
        # Estructuras para el autómata
        self.states = []  # Lista de estados, cada estado es un conjunto de items LR(0)
        self.transitions = {}  # Transiciones entre estados
        self.accept_states = []  # Estados de aceptación
        self.final_state = []  # Estado final
        
        # Construir el autómata
        self.build_automaton()
    
    def closure(self, items):
        """
        Calcula la cerradura de un conjunto de items LR(0)
        :param items: Conjunto de items LR(0)
        :return: Conjunto cerradura
        """
        # Convertimos a lista para poder modificarla
        result = list(items)
        processed = set()
        
        changed = True
        while changed:
            changed = False
            # Trabajamos con una copia para poder modificar result dentro del bucle
            current_items = result.copy()
            
            for item in current_items:
                if tuple(item) in processed:
                    continue
                
                processed.add(tuple(item))
                non_terminal, production, pos = item
                
                # Si el punto no está al final y el símbolo después del punto es no terminal
                if pos < len(production) and production[pos] in self.non_terminals:
                    symbol_after_dot = production[pos]
                    
                    # Buscar todas las producciones para este no terminal
                    for prod in self.grammar[symbol_after_dot]:
                        new_item = (symbol_after_dot, prod, 0)
                        if tuple(new_item) not in processed and new_item not in result:
                            result.append(new_item)
                            changed = True
        
        # Convertimos a conjunto para asegurar unicidad
        return set(tuple(item) for item in result)
    
    def goto(self, state, symbol):
        """
        Función GOTO para un estado y un símbolo
        :param state: Estado actual (conjunto de items)
        :param symbol: Símbolo para la transición
        :return: Nuevo estado resultante
        """
        new_items = set()
        
        for item in state:
            non_terminal, production, pos = item
            
            # Si el punto no está al final y el símbolo después del punto coincide
            if pos < len(production) and production[pos] == symbol:
                # Avanzamos el punto
                new_items.add((non_terminal, production, pos + 1))
        
        # Si encontramos items, calculamos su cerradura
        if new_items:
            return self.closure(new_items)
        return set()
    
    def find_state_index(self, state):
        """
        Busca el índice de un estado en la lista de estados
        :param state: Estado a buscar
        :return: Índice del estado o -1 si no existe
        """
        for i, existing_state in enumerate(self.states):
            if existing_state == state:
                return i
        return -1
    
    def build_automaton(self):
        """
        Construye el autómata LR(0) completo
        """
        # Crear el estado inicial con el símbolo de inicio
        initial_item = (self.start_symbol, tuple(self.grammar[self.start_symbol][0]), 0)
        initial_state = self.closure({initial_item})

        
        self.states.append(initial_state)
        self.transitions[0] = {}
        
        # Cola de estados a procesar
        states_queue = [initial_state]
        processed_states = set()
        
        # Mientras haya estados por procesar
        while states_queue:
            current_state = states_queue.pop(0)
            current_state_idx = self.find_state_index(current_state)
            
            # Convertir el estado a una representación hashable
            current_state_tuple = frozenset(current_state)
            
            if current_state_tuple in processed_states:
                continue
            
            processed_states.add(current_state_tuple)
            
            # Revisar si es un estado de aceptación
            for item in current_state:
                non_terminal, production, pos = item
                if non_terminal == self.start_symbol and pos == len(production):
                    self.final_state.append(current_state_idx)
            
            # Para cada símbolo posible
            for symbol in self.symbols:
                # Calcular el nuevo estado usando GOTO
                next_state = self.goto(current_state, symbol)
                
                if not next_state:
                    continue
                
                # Buscar si el estado ya existe
                next_state_idx = self.find_state_index(next_state)
                
                # Si es un nuevo estado, agregarlo
                if next_state_idx == -1:
                    next_state_idx = len(self.states)
                    self.states.append(next_state)
                    self.transitions[next_state_idx] = {}
                    states_queue.append(next_state)
                
                # Agregar la transición
                self.transitions[current_state_idx][symbol] = next_state_idx
        
        # Identificar estados de aceptación (donde hay reducción por la producción inicial)
        for i, state in enumerate(self.states):
            for item in state:
                if item[0] == self.start_symbol and item[2] == 1:  # S' -> E·
                    self.accept_states.append(i)
                    break
    
    def get_automaton(self):
        """
        Retorna el autómata LR(0) construido
        :return: Diccionario con la información del autómata
        """
        return {
            "grammar": self.grammar,
            "start": self.start_symbol,
            "states": {i: state for i, state in enumerate(self.states)},
            "accept_states": self.accept_states,
            "final_state": self.final_state,
            "transitions": self.transitions
        }
    
    def print_automaton(self):
        """
        Imprime el autómata en un formato legible
        """
        print("Autómata LR(0):")
        print(f"Símbolo inicial: {self.start_symbol}")
        print("\nEstados:")
        for i, state in enumerate(self.states):
            print(f"Estado {i}:")
            for item in state:
                non_terminal, production, pos = item
                
                # Construir una representación del item con el punto
                prod_with_dot = list(production)
                prod_with_dot.insert(pos, "·")

                
                
                print(f"  {non_terminal} -> {' '.join(prod_with_dot)}")
            print()
        
        print("Transiciones:")
        for state_idx, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                print(f"  Estado {state_idx} --{symbol}--> Estado {next_state}")
        
        print("\nEstados de aceptación:", self.accept_states)
        print("Estado final:", self.final_state)


# Ejemplo de uso:
if __name__ == "__main__":
    class GrammarBuilder:
        def __init__(self):
            # Gramática de ejemplo: E -> E + T | T, T -> T * F | F, F -> ( E ) | id
            self.grammar = {
                "S'": [("E",)],
                "E": [("E", "+", "T"), ("T",)],
                "T": [("T", "*", "F"), ("F",)],
                "F": [("(", "E", ")"), ("id",)]
            }
            self.start_symbol = "S'"
            self.terminals = {"+", "*", "(", ")", "id"}
            self.non_terminals = {"S'", "E", "T", "F"}
            self.symbols = self.terminals.union(self.non_terminals)
        
        def get_grammar(self):
            return self.grammar
        
        def get_start_symbol(self):
            return self.start_symbol
        
        def get_terminals(self):
            return self.terminals
        
        def get_non_terminals(self):
            return self.non_terminals
        
        def get_symbols(self):
            return self.symbols
    
    # Crear la gramática y el autómata
    grammar_builder = GrammarBuilder()
    automaton = LR0Automaton(grammar_builder)
    
    # Imprimir el autómata
    automaton.print_automaton()