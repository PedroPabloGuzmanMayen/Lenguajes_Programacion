class Gramatica_Builder:
  def __init__(self, producciones, terminales, no_terminales, simbolo_inicial):
    self.productions=producciones
    self.terminals = terminales
    self.non_terminals = no_terminales
    self.start_simbols = simbolo_inicial
  