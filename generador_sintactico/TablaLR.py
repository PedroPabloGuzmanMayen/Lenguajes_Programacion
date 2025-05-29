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
        copia = [state.copy() for state in self.automata.states] #Copiamos la tabla de estados 
        self.encontrarShifts(copia)
        self.encontrarReduceYAccept(copia)
   
        
    def construirGoto(self):
        for state in self.automata.transitions: #Verificar todos los estados
            for nt in self.grammar.non_terminals: #Verificar todos los no terminales
                if nt in self.automata.transitions[state]: #Si el no terminal tiene una transición en el estado actual
                    self.goto_table[state][nt] = self.automata.transitions[state][nt] # Agregarlo a la tabla goto
    def encontrarShifts(self, estados): #Esta función nos ayuda a encontrar producciones que generan operaciones shift
        state_counter = 0
        for state in estados: #Recorrer todos los objetos en el array
            items_a_eliminar = [] #Aquí almacenamos los ítems que vamos a eliminar
            for item in state: #Recorrer todos los ítems
                posicion_token = item[2] # Guardamos la posición del token
                if posicion_token >= len(item[1]): #Si la posición del punto esta fuera de los límtes, omitimos el caso
                    continue
                else:
                    if item[1][posicion_token] in self.grammar.terminals: #Verficar si en la posición del token hay un terminal
                        terminal = item[1][posicion_token] #Guardamos el terminal que encontramos
                        if terminal in self.automata.transitions[state_counter]:
                            self.action_table[state_counter][terminal] = ['shift', self.automata.transitions[state_counter][terminal] ]
                            items_a_eliminar.append(item)
            for item in items_a_eliminar:
                state.discard(item)
            state_counter += 1
    def encontrarReduceYAccept(self, estados): #Nos ayuda a encontrar reduce y accepts
        state_counter = 0
        for state in estados:
            for item in state:
                posicion_token = item[2]
                if item[0] == "S'" and item[2] == 1:#Primer caso: Hallamos el caso de aceptación
                    self.action_table[state_counter]['$'] = ['accept']
                elif posicion_token >= len(item[1]):  # El punto está al final
                # Para reduce, usamos FOLLOW del lado izquierdo de la producción
                    for terminal in self.grammar.follow[item[0]]:
                        self.action_table[state_counter][terminal] = ['reduce', (item[0], item[1])]
            state_counter += 1
                
            
        
    def parse(self, input_tokens):
        
        pass


#Ejemplo de uso

if __name__ == "__main__":
     
    
#     # Crear la gramática y el autómata
     gramatica = Gramatica_Builder(
        producciones={
        "S'": [("E",)],
        "E": [("E", "+", "T"), ("T",)],
        "T": [("T", "*", "F"), ("F",)],
        "F": [("(", "E", ")"), ("int",)]
        },
        no_terminales=["S'", "E", "T", "F"],
        terminales=["+", "*", "(", ")", "int"]
    )
     automaton = LR0_Automata(gramatica)

     automaton.print_automaton()
     slrtable = ParsingTable(automaton, gramatica)
     slrtable.construirGoto()
     slrtable.contruirAction()
     #print("Tabla goto: ", slrtable.goto_table)
     print("Action: ", slrtable.action_table)
     
