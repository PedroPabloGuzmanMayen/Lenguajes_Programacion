
import graphviz
from tree import compute_empty_transition_closure



import graphviz

class AFD:
    def __init__(self, alfabeto, estados, transiciones, estado_inicial, estados_finales, state_tags=None):
        self.Alfabeto_ = [s for s in alfabeto if s != 'ε']
        self.Q_ = estados
        self.S_ = transiciones
        self.q0 = estado_inicial
        self.F_ = estados_finales
        self.state_count = len(estados)
        self.state_tags = state_tags if state_tags is not None else {}

    def set_q0(self, q0):
        self.q0 = q0

    def set_qf(self, qf):
        self.F_ = {qf}
    
    def move_AFD(self, states, symbol):
        next_states = set()
        for state in states:
            for transicion in self.S_:
                if transicion.q0.numero == state.numero and transicion.valor == symbol:
                    next_states.add(transicion.qf)
        return next_states

    def acept_Chain(self, w):
        current_states = [self.q0]
        for symbol in w:
            current_states = list(self.move_AFD(current_states, symbol))
        numeros = [x.numero for x in self.F_]
        return any(state.numero in numeros for state in current_states)
    
    def get_tags(self):
        """Retorna los tags actuales del AFD"""
        return self.state_tags.copy()
    
    def graphicAFD(self):
        f = graphviz.Digraph('finite_state_machine', filename='AFD_automata', format='png')
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')
        for l in self.F_:
            f.node(str(l.numero))
        f.attr('node', shape='circle')
        for transicion in self.S_:
            if transicion.q0.numero == self.q0.numero:
                f.node('', style='invis')
                f.edge('', str(transicion.q0.numero))
            f.edge(str(transicion.q0.numero), str(transicion.qf.numero), label=str(transicion.valor))
        f.view()
    
    def graphicminimizumAFD(self):
        f = graphviz.Digraph('finite_state_machine', filename='AFD_automata_minimizum', format='png')
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')
        for l in self.F_:
            f.node(str(l.numero))
        f.attr('node', shape='circle')
        for transicion in self.S_:
            if transicion.q0.numero == self.q0.numero:
                f.node('', style='invis')
                f.edge('', str(transicion.q0.numero))
            f.edge(str(transicion.q0.numero), str(transicion.qf.numero), label=str(transicion.valor))
        f.view()

    def separate_states(self):
        groups = {}
        
        for q in self.Q_:
            # Crear clave basada en: (es_final, tag)
            is_final = q in self.F_
            tag = self.state_tags.get(str(q.numero), None)
            key = (is_final, tag)
            
            if key not in groups:
                groups[key] = []
            groups[key].append(q)
        
        return list(groups.values())

    def minimizumAFD(self):
        P = self.separate_states()
        W = self.separate_states()
        
        while len(W) != 0:
            A = W.pop()
            for s in self.Alfabeto_:
                X = set()
                for q in self.Q_:
                    if self.move_AFD([q], s) & set(A):
                        X.add(q)
                for Y in P.copy():
                    Y_set = set(Y)
                    Y1 = Y_set & X
                    Y2 = Y_set - X
                    if Y1 and Y2:
                        Y1_list = list(Y1)
                        Y2_list = list(Y2)
                        for p in P:
                            if set(p) == Y_set:
                                P.remove(p)
                                break
                        P.append(Y1_list)
                        P.append(Y2_list)
                        if Y in W:
                            W.remove(Y)
                            W.append(Y1_list)
                            W.append(Y2_list)
                        else:
                            W.append(min(Y1_list, Y2_list, key=len))
        self.rebuildAFN(P)

    def rebuildAFN(self, P):
        states = []
        final_states = []
        transicions = []
        state_initial = []
        new_state_tags = {}
        
        for i, p in enumerate(P):
            # Crear nombre único para el grupo de estados
            group_name = f"G{i}"
            estado = Estado_AFD(numero=group_name)
            
            # Verificar si algún estado del grupo es final
            if any(q in self.F_ for q in p):
                final_states.append(estado)
            
            # Verificar si el estado inicial está en este grupo
            if self.q0 in p:
                state_initial.append(estado)
            
            # Preservar tags: buscar el tag de cualquier estado del grupo que lo tenga
            for state in p:
                state_key = str(state.numero)
                if state_key in self.state_tags:
                    new_state_tags[group_name] = self.state_tags[state_key]
                    break  # Tomar el primer tag encontrado y salir
            
            states.append(estado)

        # Crear transiciones entre grupos
        for i, p in enumerate(P):
            for s in self.Alfabeto_:
                next_States = self.move_AFD(p, s)
                lista_nex_states = list(next_States)
                if not lista_nex_states:
                    continue
                
                # Encontrar el estado actual (grupo fuente)
                q0 = states[i]
                
                # Encontrar el grupo destino
                for j, p_dest in enumerate(P):
                    if any(state in p_dest for state in lista_nex_states):
                        qf = states[j]
                        transicions.append(Transicion(q0, qf, s))
                        break

        self.F_ = final_states
        self.Q_ = states
        self.S_ = transicions
        self.state_tags = new_state_tags  # Actualizar tags
        if state_initial:
            self.q0 = state_initial[0]

class Estado_AFD:
    def __init__(self, numero, estados_AFN=None):
        self.numero = numero
        self.estados_AFN = estados_AFN if estados_AFN is not None else []

class Transicion:
    def __init__(self, q0, qf, valor):
        self.q0 = q0
        self.qf = qf
        self.valor = valor








## Creacion del AFD

def create_dfa(root, position_map, follow_positions):
    """Genera un autómata finito determinista (DFA) a partir del árbol sintáctico."""
    
    # Calcular el estado inicial con cierre epsilon
    initial_state = frozenset(compute_empty_transition_closure(root.first_positions, position_map, follow_positions))
    states_dict = {initial_state: 'A'}
    pending_states = [initial_state]
    state_counter = 0
    
    # Identificar posiciones de aceptación (nodos marcados con '#')
    acceptance_positions = {pos for pos, node in position_map.items() if node.symbol.startswith('#')}
    
    # Listas para construir el AFD
    estados = []
    transiciones = []
    estados_finales = []
    alfabeto = set()
    state_tags = {}
    
    while pending_states:
        current_state = pending_states.pop(0)
        current_name = states_dict[current_state]
        
        # Calcular transiciones
        transitions = {}
        for pos in current_state:
            symbol = position_map[pos].symbol
            if symbol == '949' or symbol.startswith('#'):
                continue
                
            if symbol not in transitions:
                transitions[symbol] = set()
                
            transitions[symbol] |= follow_positions[pos]
            alfabeto.add(symbol)  # Agregar símbolo al alfabeto
        
        # Registrar transiciones
        for symbol, next_pos in transitions.items():
            if not next_pos:
                continue
                
            next_state = frozenset(compute_empty_transition_closure(next_pos, position_map, follow_positions))
            
            if next_state not in states_dict:
                state_counter += 1
                states_dict[next_state] = chr(ord('A') + state_counter)
                pending_states.append(next_state)
    
    # Crear objetos Estado_AFD
    estado_objects = {}
    for state_set, name in states_dict.items():
        estado_obj = Estado_AFD(numero=name)
        estado_objects[name] = estado_obj
        estados.append(estado_obj)
        
        # Marcar estado de aceptación si contiene alguna posición final
        if any(p in state_set for p in acceptance_positions):
            estados_finales.append(estado_obj)
        
        # Asignar tags a estados de aceptación
        tag_candidates = [int(position_map[pos].symbol[1:])
                         for pos in state_set if position_map[pos].symbol.startswith('#')]
        if tag_candidates:
            # Seleccionar el tag con menor valor (mayor prioridad)
            min_tag = min(tag_candidates)
            state_tags[name] = '#' + str(min_tag)
    
    # Crear objetos Transicion
    for state_set, name in states_dict.items():
        current_state = state_set
        
        # Recalcular transiciones para crear objetos Transicion
        transitions = {}
        for pos in current_state:
            symbol = position_map[pos].symbol
            if symbol == '949' or symbol.startswith('#'):
                continue
                
            if symbol not in transitions:
                transitions[symbol] = set()
                
            transitions[symbol] |= follow_positions[pos]
        
        # Crear objetos Transicion
        for symbol, next_pos in transitions.items():
            if not next_pos:
                continue
                
            next_state = frozenset(compute_empty_transition_closure(next_pos, position_map, follow_positions))
            
            if next_state in states_dict:
                q0 = estado_objects[name]
                qf = estado_objects[states_dict[next_state]]
                transicion = Transicion(q0, qf, symbol)
                transiciones.append(transicion)
    
    # Crear y retornar instancia de AFD con tags
    estado_inicial = estado_objects['A']
    
    afd_instance = AFD(
        alfabeto=list(alfabeto),
        estados=estados,
        transiciones=transiciones,
        estado_inicial=estado_inicial,
        estados_finales=estados_finales,
        state_tags=state_tags
    )
    
    return afd_instance
def create_afd_instance_numeric(root, position_map, follow_positions):
    """
    Crea una instancia de AFD con nombres numéricos para evitar problemas en minimización.
    """
    # Obtener la estructura del DFA
    dfa_graph, dfa_structure = create_dfa(root, position_map, follow_positions)
    
    # Extraer el alfabeto del position_map
    alfabeto = set()
    for pos, node in position_map.items():
        symbol = node.symbol
        if symbol != '949' and not symbol.startswith('#'):
            alfabeto.add(symbol)
    alfabeto = list(alfabeto)
    
    # Crear mapeo de nombres de letras a números
    state_name_to_number = {}
    number_counter = 0
    
    # Crear estados AFD con números
    estados = []
    estados_dict = {}
    
    for state_set, name in dfa_structure['states'].items():
        # Asignar número único a cada estado
        state_number = str(number_counter)
        state_name_to_number[name] = state_number
        number_counter += 1
        
        # Convertir el frozenset a lista para estados_AFN
        estados_afn = list(state_set)
        estado = Estado_AFD(numero=state_number, estados_AFN=estados_afn)
        estados.append(estado)
        estados_dict[name] = estado
    
    # Crear transiciones
    transiciones = []
    for state_name, transitions in dfa_structure['transitions'].items():
        q0 = estados_dict[state_name]
        for symbol, target_state in transitions.items():
            qf = estados_dict[target_state]
            transiciones.append(Transicion(q0, qf, symbol))
    
    # Identificar estado inicial
    estado_inicial = estados_dict[dfa_structure['initial_state']]
    
    # Identificar estados finales
    estados_finales = set()
    for state_name in dfa_structure['acceptance_states']:
        estados_finales.add(estados_dict[state_name])
    
    # Crear y retornar la instancia AFD
    afd_instance = AFD(
        alfabeto=alfabeto,
        estados=estados,
        transiciones=transiciones,
        estado_inicial=estado_inicial,
        estados_finales=estados_finales
    )
    
    return afd_instance, dfa_structure, state_name_to_number


#===============USO DE AFD=====================
# Crear estados
# q0 = Estado_AFD("0")
# q1 = Estado_AFD("1")
# q2 = Estado_AFD("2")

# # Lista de estados
# estados = [q0, q1, q2]

# # Crear transiciones (reconoce cadenas que terminan en "ab")
# transiciones = [
#     Transicion(q0, q0, 'a'),
#     Transicion(q0, q1, 'a'),
#     Transicion(q1, q2, 'b'),
#     Transicion(q1, q1, 'a'),
#     Transicion(q2, q0, 'a'),  # para hacerlo más dinámico
# ]

# # Crear AFD
# afd = AFD(
#     alfabeto=['a', 'b'],
#     estados=estados,
#     transiciones=transiciones,
#     estado_inicial=q0,
#     estados_finales={q2}
# )

# # Probar cadena
# print(afd.acept_Chain("aaab"))  # True, termina en "ab"
# print(afd.acept_Chain("bb"))   # False
