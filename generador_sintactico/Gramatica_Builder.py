class Gramatica_Builder:
    EPSILON = 'ε'
    END_MARKER = '$'

    def __init__(self , producciones, no_terminales, terminales):
        self.grammar = producciones
        self.non_terminals = set(no_terminales)
        self.terminals = set(terminales)
        self.first = {nt: set() for nt in self.non_terminals}
        self.follow = {nt: set() for nt in self.non_terminals}
        self.compute_first()
        self.compute_follow("S'")
        self.start_symbol = "S'"
        self.symbols =self.terminals.union(self.non_terminals)

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

    def _extract_terminals(self):
        terms = set()
        for rules in self.grammar.values():
            for rule in rules:
                for symbol in rule:
                    if symbol not in self.grammar:
                        terms.add(symbol)
        return terms

    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for rule in self.grammar[nt]:
                    rule_first = self.first_of_rule(rule)
                    before_size = len(self.first[nt])
                    self.first[nt] |= rule_first
                    if len(self.first[nt]) > before_size:
                        changed = True

    def first_of_rule(self, rule):
        result = set()
        
        for i, symbol in enumerate(rule):
            if symbol in self.terminals:
                result.add(symbol)
                break
            elif symbol in self.non_terminals:
                symbol_first = self.first[symbol] - {self.EPSILON}
                result |= symbol_first
                
                if self.EPSILON not in self.first[symbol]:
                    break
                    
                if i == len(rule) - 1:
                    result.add(self.EPSILON)
        
        if not rule:
            result.add(self.EPSILON)
            
        return result

    def first_of(self, symbols):
        """Compute FIRST set for a sequence of symbols"""
        if not symbols:
            return {self.EPSILON}
            
        result = set()
        for i, sym in enumerate(symbols):
            if sym in self.terminals:
                result.add(sym)
                break
            elif sym in self.non_terminals:
                
                result |= self.first[sym] - {self.EPSILON}
                
                if self.EPSILON not in self.first[sym]:
                    break
                
                if i == len(symbols) - 1:
                    result.add(self.EPSILON)
        
        return result

    def compute_follow(self, start_symbol):
        self.follow[start_symbol].add(self.END_MARKER)
        changed = True
        while changed:
            changed = False
            for A in self.grammar:
                for rule in self.grammar[A]:
                    for i, B in enumerate(rule):
                        if B in self.non_terminals:
                            beta = rule[i+1:]
                            first_beta = self.first_of(beta)
                            before = len(self.follow[B])
                            
                            
                            self.follow[B] |= first_beta - {self.EPSILON}
                            
                            
                            if self.EPSILON in first_beta or not beta:
                                self.follow[B] |= self.follow[A]
                            
                            changed |= (len(self.follow[B]) > before)

    def print_sets(self):
        print("== FIRST sets ==")
        for nt in sorted(self.first.keys()):
            symbols = sorted(list(self.first[nt]))
            print(f"FIRST({nt}) = {{ {', '.join(symbols)} }}")
        
        print("\n== FOLLOW sets ==")
        for nt in sorted(self.follow.keys()):
            symbols = sorted(list(self.follow[nt]))
            print(f"FOLLOW({nt}) = {{ {', '.join(symbols)} }}")

# if __name__ == "__main__":
#     ff = Gramatica_Builder(producciones=
#                            {
#                             "S'": [("expression",)],
#                             'expression': [('expression', 'PLUS', 'term'), ('term',)], 
#                             'term': [('term', 'TIMES', 'factor'), ('factor',)], 
#                             'factor': [('LPAREN', 'expression', 'RPAREN'), ('ID',)]
#                             },
#                             no_terminales=['expression', 'term', 'factor', "S'"],
#                             terminales=['ID', 'PLUS', 'TIMES', 'LPAREN', 'RPAREN'],
                            
#                            )
#     ff.print_grammar()
#     ff.print_sets()
   