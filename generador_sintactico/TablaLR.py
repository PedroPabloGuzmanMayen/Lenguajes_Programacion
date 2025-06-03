from generador_sintactico.lr0 import LR0_Automata
from generador_sintactico.Gramatica_Builder import Gramatica_Builder
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

    def construirAction(self):
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

    def print_tables(self):
        print("\n=== ACTION TABLE ===")
        for state in sorted(self.action_table.keys()):
            print(f"Estado {state}:")
            for symbol, action in self.action_table[state].items():
                if action[0] == "shift":
                    print(f"  {symbol} -> shift {action[1]}")
                elif action[0] == "reduce":
                    lhs, rhs = action[1]
                    rhs_str = ' '.join(rhs)
                    print(f"  {symbol} -> reduce {lhs} → {rhs_str}")
                elif action[0] == "accept":
                    print(f"  {symbol} -> accept")
            if not self.action_table[state]:
                print("  (vacío)")

        print("\n=== GOTO TABLE ===")
        for state in sorted(self.goto_table.keys()):
            print(f"Estado {state}:")
            for symbol, target in self.goto_table[state].items():
                print(f"  {symbol} -> {target}")
            if not self.goto_table[state]:
                print("  (vacío)")
        
    def parse(self, input_tokens):
        stack = [0]
        idx = 0

        print("\n== Proceso de Parsing ==")
        print(f"{'Stack':<30} {'Entrada':<30} {'Acción'}")

        while True:
            state = stack[-1]
            token = input_tokens[idx] if idx < len(input_tokens) else '$'

            while True:  # ciclo para aplicar múltiples reducciones antes de un shift
                action = self.action_table.get(state, {}).get(token, None)
                entrada_restante = ' '.join(input_tokens[idx:])
                pila_actual = ' '.join(map(str, stack))
                accion_str = "Error" if not action else f"{action[0]} {action[1] if len(action) > 1 else ''}"
                print(f"{pila_actual:<30} {entrada_restante:<30} {accion_str}")
                print(f"DEBUG - Acción obtenida: {action}")

                if action is None:
                    print(" Error de sintaxis.")
                    return False

                if action[0] == "shift":
                    stack.append(token)
                    stack.append(action[1])
                    idx += 1
                    break  # salimos del ciclo interno y continuamos con el siguiente token
                elif action[0] == "reduce":
                    lhs, rhs = action[1]
                    if rhs != ('ε',):
                        for _ in range(len(rhs) * 2):
                            stack.pop()
                    top_state = stack[-1]
                    stack.append(lhs)
                    goto_state = self.goto_table.get(top_state, {}).get(lhs)
                    if goto_state is None:
                        print(f"Error: no hay transición GOTO desde estado {top_state} con símbolo {lhs}")
                        return False
                    stack.append(goto_state)
                    state = goto_state  # importante: actualizar `state` después de reducción
                    # y seguimos en el ciclo interno sin avanzar `idx`
                elif action[0] == "accept":
                    print(" Cadena aceptada correctamente. 😁👍")
                    return True
    

    def parse_consumer_producer(self, lexer):
        stack = [0]
        token = next(lexer)

        print("Token", token)
        print("\n== Proceso de Parsing ==")
        print(f"{'Stack':<30} {'Entrada':<30} {'Acción'}")

        while True:
            # Ignorar tokens vacíos
            while token[0] is None:
                token = next(lexer)

            # Extraer solo el tipo de token (por ejemplo, de "return NUMBER" → "NUMBER")
            entrada = token[0].split()[-1] if token[0] != '$' else '$'
            state = stack[-1]

            while True:
                action = self.action_table.get(state, {}).get(entrada, None)
                pila_actual = ' '.join(map(str, stack))
                entrada_str = f"{entrada} '{token[1]}'" if entrada != '$' else '$'
                accion_str = "Error" if not action else f"{action[0]} {action[1] if len(action) > 1 else ''}"
                print(f"{pila_actual:<30} {entrada_str:<30} {accion_str}")
                print(f"DEBUG - Acción obtenida: {action}")

                if action is None:
                    print("❌ Error de sintaxis.")
                    return False

                if action[0] == "shift":
                    stack.append(entrada)
                    stack.append(action[1])
                    token = next(lexer)
                    while token[0] is None:
                        token = next(lexer)
                    entrada = token[0].split()[-1] if token[0] != '$' else '$'
                    break
                elif action[0] == "reduce":
                    lhs, rhs = action[1]
                    if rhs != ('ε',):
                        for _ in range(len(rhs) * 2):
                            stack.pop()
                    top_state = stack[-1]
                    stack.append(lhs)
                    goto_state = self.goto_table.get(top_state, {}).get(lhs)
                    if goto_state is None:
                        print(f"❌ Error: no hay transición GOTO desde estado {top_state} con símbolo {lhs}")
                        return False
                    stack.append(goto_state)
                    state = goto_state
                elif action[0] == "accept":
                    print("✅ Cadena aceptada correctamente. 😁👍")
                    return True

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
     automaton = LR0_Automata(gramatica) #Hacer un autómata en base a la gramática

     automaton.print_automaton()
     slrtable = ParsingTable(automaton, gramatica) #Crear la tabla pasando como argumentos la tabla y la gramática
     slrtable.construirGoto() #Usar la función para construir la tabala goto
     slrtable.construirAction() #Usar la función para construir la tabla action
     print("Tabla goto: ", slrtable.goto_table)
     print("Action: ", slrtable.action_table)
     
