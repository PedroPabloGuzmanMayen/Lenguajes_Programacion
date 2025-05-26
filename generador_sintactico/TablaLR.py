from lr0 import LR0_Automata
from Gramatica_Builder import Gramatica_Builder
class ParsingTable:
    def __init__(self, lr0_automata, grammar):
        self.automata = lr0_automata # El autómata mediante el cuál armaremos la tabla
        self.grammar = grammar #La gramática que usaremos
        self.action_table = {}  #Aquí guardamos todas las acciones de action
        self.goto_table = {}   #Aquí guardamos todas las acciones goto
        for i in range(len(self.automata.states)): #Inicializar las tablas
            self.action_table[i] = {}
            self.goto_table[i] = {}
        
    
    def construirTablaSLR(self):
        
        for state in self.automata.states:
            pass

    def contruirAction(self):
        pass
    def construirGoto(self):
        for state in self.automata.transitions: #Verificar todos los estados
            for nt in self.grammar.non_terminals: #Verificar todos los no terminales
                if nt in self.automata.transitions[state]: #Si el no terminal tiene una transición en el estado actual
                    self.goto_table[state][nt] = self.automata.transitions[state][nt] # Agregarlo a la tabla goto
                
            
        
    def parse(self, input_tokens):
        
        pass


#Ejemplo de uso

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

     automaton.print_automaton()
     print(automaton.transitions)
     slrtable = ParsingTable(automaton, grammar_builder)
     slrtable.construirGoto()
     print("Tabla goto: ", slrtable.goto_table)