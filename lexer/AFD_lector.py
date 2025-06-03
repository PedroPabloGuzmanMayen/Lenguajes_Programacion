
import graphviz
class AFD:
    def __init__(self, alfabeto, estados, transiciones, estado_inicial, estados_finales):
        self.Alfabeto_ = [s for s in alfabeto if s != 'ε']
        self.Q_ = estados
        self.S_ = transiciones
        self.q0 = estado_inicial
        self.F_ = estados_finales
        self.state_count = len(estados)

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
        acept = []
        not_acept = []
        to_return = []
        for q in self.Q_:
            if q in self.F_:
                acept.append(q)
            else:
                not_acept.append(q)
        if len(not_acept) > 0:
            to_return.append(not_acept)
        to_return.append(acept)
        return to_return

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
        for p in P:
            state = p[0]
            estado = Estado_AFD(numero=f"{[int(i.numero) for i in p]}")
            if state.numero in [x.numero for x in self.F_]:
                final_states.append(estado)
            if self.q0.numero in estado.numero:
                state_initial.append(estado)
            states.append(estado)

        for p in P:
            for s in self.Alfabeto_:
                next_States = self.move_AFD(p, s)
                lista_nex_states = list(next_States)
                if not lista_nex_states:
                    continue
                state_actual = str([int(i.numero) for i in p])
                q0 = [i for i in states if state_actual == i.numero][0]
                qf = [i for i in states if lista_nex_states[0].numero in i.numero][0]
                transicions.append(Transicion(q0, qf, s))

        self.F_ = final_states
        self.Q_ = states
        self.S_ = transicions
        self.q0 = state_initial.pop()

class Estado_AFD:
    def __init__(self, numero, estados_AFN=None):
        self.numero = numero
        self.estados_AFN = estados_AFN if estados_AFN is not None else []

class Transicion:
    def __init__(self, q0, qf, valor):
        self.q0 = q0
        self.qf = qf
        self.valor = valor




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
