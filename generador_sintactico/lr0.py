import graphviz
class LR0_Automata:
    def __init__(self, grammar_builder):
       
        self.grammar = grammar_builder.get_grammar()
        self.start_symbol = grammar_builder.get_start_symbol()
        self.symbols = grammar_builder.get_symbols()
        self.terminals = grammar_builder.get_terminals()
        self.non_terminals = grammar_builder.get_non_terminals()
        
       
        self.states = []  
        self.transitions = {}  
        self.accept_states = []
        self.final_state = [] 
        
       
        self.build_automaton()
    
    def closure(self, items):
       
        result = list(items)
        processed = set()
        
        changed = True
        while changed:
            changed = False
          
            current_items = result.copy()
            
            for item in current_items:
                if tuple(item) in processed:
                    continue
                
                processed.add(tuple(item))
                non_terminal, production, pos = item
                
                
                if pos < len(production) and production[pos] in self.non_terminals:
                    symbol_after_dot = production[pos]
                    

                    for prod in self.grammar[symbol_after_dot]:
                        new_item = (symbol_after_dot, prod, 0)
                        if tuple(new_item) not in processed and new_item not in result:
                            result.append(new_item)
                            changed = True
        
        # Convertimos a conjunto para asegurar unicidad
        return set(tuple(item) for item in result)
    
    def goto(self, state, symbol):
       
        new_items = set()
        
        for item in state:
            non_terminal, production, pos = item
            
            
            if pos < len(production) and production[pos] == symbol:

                new_items.add((non_terminal, production, pos + 1))
        

        if new_items:
            return self.closure(new_items)
        return set()
    
    def find_state_index(self, state):

        for i, existing_state in enumerate(self.states):
            if existing_state == state:
                return i
        return -1
    
    def build_automaton(self):
       
        initial_item = (self.start_symbol, tuple(self.grammar[self.start_symbol][0]), 0)
        initial_state = self.closure({initial_item})

        
        self.states.append(initial_state)
        self.transitions[0] = {}
        
       
        states_queue = [initial_state]
        processed_states = set()
       
        while states_queue:
            current_state = states_queue.pop(0)
            current_state_idx = self.find_state_index(current_state)
            
       
            current_state_tuple = frozenset(current_state)
            
            if current_state_tuple in processed_states:
                continue
            
            processed_states.add(current_state_tuple)
            
           
            for item in current_state:
                non_terminal, production, pos = item
                if non_terminal == self.start_symbol and pos == len(production):
                    self.final_state.append(current_state_idx)
            
            
            for symbol in self.symbols:
              
                next_state = self.goto(current_state, symbol)
                
                if not next_state:
                    continue
                
              
                next_state_idx = self.find_state_index(next_state)
                
              
                if next_state_idx == -1:
                    next_state_idx = len(self.states)
                    self.states.append(next_state)
                    self.transitions[next_state_idx] = {}
                    states_queue.append(next_state)
                
                
                self.transitions[current_state_idx][symbol] = next_state_idx
        
       
        for i, state in enumerate(self.states):
            for item in state:
                if item[0] == self.start_symbol and item[2] == 1:  # S' -> E·
                    self.accept_states.append(i)
                    break
    
    def get_automaton(self):
       
        return {
            "grammar": self.grammar,
            "start": self.start_symbol,
            "states": {i: state for i, state in enumerate(self.states)},
            "accept_states": self.accept_states,
            "final_state": self.final_state,
            "transitions": self.transitions
        }
    
    def print_automaton(self):
       
        print("Autómata LR(0):")
        print(f"Símbolo inicial: {self.start_symbol}")
        print("\nEstados:")
        for i, state in enumerate(self.states):
            print(f"Estado {i}:")
            for item in state:
                non_terminal, production, pos = item
                

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

    def generate_graphviz(self):
        dot_code = "digraph LR0_Automaton {\n"
        dot_code += "    rankdir=LR;\n"
        dot_code += "    node [shape=circle];\n\n"
        
        # Nodo inicial invisible para la flecha de entrada
        dot_code += "    start [shape=point, style=invis];\n"
        
        # Crear nodos para cada estado
        for i, state in enumerate(self.states):
            # Formatear el contenido del estado
            state_label = f"Estado {i}\\n"
            for item in state:
                non_terminal, production, pos = item
                
                # Insertar el punto en la posición correcta
                prod_with_dot = list(production)
                prod_with_dot.insert(pos, "·")
                
                # Crear la representación de la producción
                prod_str = " ".join(prod_with_dot)
                state_label += f"{non_terminal} → {prod_str}\\l"
            
            # Determinar el estilo del nodo
            if i in self.final_state:
                # Estado final (doble círculo)
                dot_code += f'    {i} [label="{state_label}", shape=doublecircle];\n'
            else:
                # Estado normal
                dot_code += f'    {i} [label="{state_label}"];\n'
        
        dot_code += "\n"
        
        # Flecha inicial al estado 0
        dot_code += "    start -> 0;\n\n"
        
        # Crear las transiciones
        for state_idx, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                dot_code += f"    {state_idx} -> {next_state} [label=\"{symbol}\"];\n"
        
        dot_code += "}\n"
        
        return dot_code

    def save_graphviz_file(self, filename="lr0_automaton.dot"):
        dot_code = self.generate_graphviz()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(dot_code)
        print(f"Archivo DOT guardado como: {filename}")
        print("Para generar la imagen, ejecuta:")
        print(f"dot -Tpng {filename} -o lr0_automaton.png")

    def visualize_automaton(self, output_format="png", filename="lr0_automaton"):               
        dot_code = self.generate_graphviz()
        
        # Crear el objeto Source de graphviz
        graph = graphviz.Source(dot_code)
        
        # Renderizar y guardar
        graph.render(filename, format=output_format, cleanup=True)
        print(f"Gráfico generado: {filename}.{output_format}")
        
        return graph
            
        


if __name__ == "__main__":
     class GrammarBuilder:
        def __init__(self):
            
            self.grammar = {
                "S'": [("E",)],
                "E": [("E", "+", "T"), ("T",)],
                "T": [("T", "*", "F"), ("F",)],
                "F": [("(", "E", ")"), ("int",)]
            }
            self.start_symbol = "S'"
            self.terminals = {"+", "*", "(", ")", "int"}
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
    
#     # Crear la gramática y el autómata
     grammar_builder = GrammarBuilder()
     automaton = LR0_Automata(grammar_builder)
    
#     # Imprimir el autómata
     automaton.print_automaton()
     print(len(automaton.states))

     

     print(automaton.states[8])

     for element in automaton.states[8]:
         print(element)
         print(len(element[1]))
     print(automaton.transitions)

     print('int' in automaton.transitions[0])

     automaton.save_graphviz_file("mi_automata.dot")

     automaton.visualize_automaton("png", "mi_automata")

     #print(automaton.goto({3}, '('))