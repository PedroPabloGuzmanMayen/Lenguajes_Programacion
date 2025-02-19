#include <iostream>
#include <vector>
#include <set>
#include <string>
#include <shunting_yard.h>
#include "tree.h"
#include "node.h"


class Estado {
public:
    int numero;
    bool aceptacion;

    Estado(int num, bool acept = false) : numero(num), aceptacion(acept) {}
};

class Transicion {
public:
    Estado* q0;
    Estado* qf;
    char valor;

    Transicion(Estado* inicio, Estado* fin, char simbolo) : q0(inicio), qf(fin), valor(simbolo) {}
};

class AFN {
public:
    std::set<Estado*> Q;
    std::set<char> Alfabeto;
    Estado* q0;
    Estado* F;
    std::vector<Transicion> S;

    AFN(std::set<Estado*> estados, std::set<char> alfabeto, Estado* inicial, Estado* final, std::vector<Transicion> transiciones)
        : Q(estados), Alfabeto(alfabeto), q0(inicial), F(final), S(transiciones) {}

    std::set<Estado*> epsilonClosure(std::set<Estado*> states) {
        std::set<Estado*> closure = states;
        std::vector<Estado*> stack(states.begin(), states.end());

        while (!stack.empty()) {
            Estado* state = stack.back();
            stack.pop_back();
            
            for (auto& trans : S) {
                if (trans.q0 == state && trans.valor == 'E' && closure.find(trans.qf) == closure.end()) {
                    closure.insert(trans.qf);
                    stack.push_back(trans.qf);
                }
            }
        }
        return closure;
    }

    std::set<Estado*> move(std::set<Estado*> states, char symbol) {
        std::set<Estado*> nextStates;
        for (auto& state : states) {
            for (auto& trans : S) {
                if (trans.q0 == state && trans.valor == symbol) {
                    nextStates.insert(trans.qf);
                }
            }
        }
        return nextStates;
    }

    bool acceptChain(std::string w) {
        std::set<Estado*> currentStates = epsilonClosure({q0});
        for (char symbol : w) {
            currentStates = epsilonClosure(move(currentStates, symbol));
        }
        return currentStates.find(F) != currentStates.end();
    }
};

AFN normalTransition(int& statecounter, char label) {
    Estado* q0 = new Estado(statecounter + 1);
    Estado* q1 = new Estado(statecounter + 2);
    Transicion transicion(q0, q1, label);
    statecounter += 2;
    return AFN({q0, q1}, {label}, q0, q1, {transicion});
}

AFN CleanOperator(int& statecounter, AFN Nt) {
    Estado* q0 = new Estado(statecounter + 1);
    Estado* qf = new Estado(statecounter + 2);
    statecounter += 2;
    std::vector<Transicion> transiciones = {
        Transicion(q0, Nt.q0, 'E'),
        Transicion(Nt.F, Nt.q0, 'E'),
        Transicion(Nt.F, qf, 'E'),
        Transicion(q0, qf, 'E')
    };
    transiciones.insert(transiciones.end(), Nt.S.begin(), Nt.S.end());
    return AFN({q0, qf}, {'E'}, q0, qf, transiciones);
}

AFN orOperator(int& statecounter, AFN Nt, AFN Nf) {
    Estado* q0 = new Estado(statecounter + 1);
    Estado* qf = new Estado(statecounter + 2);
    statecounter += 2;
    std::vector<Transicion> transiciones = {
        Transicion(q0, Nt.q0, 'E'),
        Transicion(q0, Nf.q0, 'E'),
        Transicion(Nt.F, qf, 'E'),
        Transicion(Nf.F, qf, 'E')
    };
    transiciones.insert(transiciones.end(), Nt.S.begin(), Nt.S.end());
    transiciones.insert(transiciones.end(), Nf.S.begin(), Nf.S.end());
    return AFN({q0, qf}, {'E'}, q0, qf, transiciones);
}

AFN Concatenate(AFN Nt, AFN Nf) {
    for (auto& trans : Nt.S) {
        if (trans.qf == Nt.F) {
            trans.qf = Nf.q0;
        }
    }
    Nt.F = Nf.F;
    Nt.S.insert(Nt.S.end(), Nf.S.begin(), Nf.S.end());
    return AFN(Nt.Q, Nt.Alfabeto, Nt.q0, Nf.F, Nt.S);
}


AFN createTransitions(int& statecounter, Node* tree) {
  if (tree != nullptr) {
      if (isalnum(tree->getValue())) {
          return normalTransition(statecounter, tree->getValue());
      } else if (tree->getValue() == '*') {
          AFN Nt = createTransitions(statecounter, tree->leftSon);
          return CleanOperator(statecounter, Nt);
      } else if (tree->getValue() == '|') {
          AFN Nt = createTransitions(statecounter, tree->leftSon);
          AFN Nf = createTransitions(statecounter, tree->rightSon);
          return orOperator(statecounter, Nt, Nf);
      } else if (tree->getValue() == '.') {
          AFN Nt = createTransitions(statecounter, tree->leftSon);
          AFN Nf = createTransitions(statecounter, tree->rightSon);
          return Concatenate(Nt, Nf);
      }
  }
  return AFN({}, {}, nullptr, nullptr, {});
}


AFN buildAFN(Node* syntaxTree) {
  int statecounter = 0;
  return createTransitions(statecounter, syntaxTree);
}


int main() {
    std::string expression = "a(bb)*c";
    std::string newStr = add_concatenation(expression);
    std::string postfix = shunting_yard(newStr);
    Tree* syntaxTree = new Tree(postfix);
    
    AFN afn = buildAFN(syntaxTree->getRoot());
    
    std::string testString = "abbc";
    if (afn.acceptChain(testString)) {
        std::cout << "Cadena aceptada" << std::endl;
    } else {
        std::cout << "Cadena rechazada" << std::endl;
    }
    
    return 0;
}
