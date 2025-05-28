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
        self.construirGoto()
        self.construirAction() #Hacemos la contrucción de las 2 tablas

    def contruirAction(self):
        state_counter = 0
        fue_encontrado = False #Esta flag nos ayuda a determinar si la producción inicial fue encontrada
        for state in self.automata.states:
            for item in state:
                if item[0] == self.grammar.start_symbol and item[2] == 1: #Es la producción incial, lo agregamos como estado de aceptación
                    self.action_table[state_counter]['$'] = ['accept']
                else:
                    posicion_token = item[2] # Guardamos la posición del token
                    if posicion_token >= len(item[1]): #Vemos que sucede si la posición está fuera de los límites, si se da el caso aplica el caso no terminal antes de un punto (posiblemente)
                        if item[1][-1] in self.grammar.non_terminals:
                            
                            pass
                    else:
                        if item[1][posicion_token] in self.grammar.terminals: #Verficar si en la posición del token hay un terminal
                            elemento_en_comun = list(self.grammar.terminals & set(item[1])) #Guardamos el elemento en común que tienen
                            if elemento_en_comun[0] in self.automata.transitions[state_counter]:
                                self.action_table[state_counter][elemento_en_comun[0]] = ['shift', self.automata.transitions[state_counter][elemento_en_comun[0]] ]
                        #También verificar si aplica para el caso #2

            state_counter += 1 # Aumentamos la numeración de lo estados
    def construirGoto(self):
        for state in self.automata.transitions: #Verificar todos los estados
            for nt in self.grammar.non_terminals: #Verificar todos los no terminales
                if nt in self.automata.transitions[state]: #Si el no terminal tiene una transición en el estado actual
                    self.goto_table[state][nt] = self.automata.transitions[state][nt] # Agregarlo a la tabla goto
    def encontrarShifts(self): #Esta función nos ayuda a encontrar producciones que generan operaciones shift
        for state in self.automata.states: #Recorrer todos los objetos en el array
            for item in state: #Recorrer todos los ítems
                pass
    def encontrarReduce(self): #Nos ayuda a encontrar produccions que generan operaciones 
        pass
                
            
        
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
     slrtable.contruirAction()
     #print("Tabla goto: ", slrtable.goto_table)
     print("Action: ", slrtable.action_table)
     
