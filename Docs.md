# Documentación del Proyecto - Analizador Léxico y Sintáctico

## Descripción General

Este proyecto implementa un **generador de analizadores léxicos y sintácticos** que puede procesar archivos de especificación de gramáticas (YALP) y archivos de especificación léxica (YAL) para generar analizadores automáticos.

### Características Principales

- **Analizador Léxico**: Genera autómatas finitos deterministas (AFD) a partir de expresiones regulares
- **Analizador Sintáctico**: Implementa analizador SLR(1) con construcción de tablas LR(0)
- **Procesamiento de Archivos**: Manejo de archivos YAL y YALP con buffer optimizado
- **Visualización**: Generación de gráficos de autómatas usando Graphviz

---

## Estructura del Proyecto

```
proyecto/
├── lexer/                      # Módulo del analizador léxico
│   ├── AFD_lector.py          # Autómata Finito Determinista
│   ├── Lexer.py               # Analizador léxico principal
│   ├── buffer_lexer.py        # Manejo de buffer para entrada
│   ├── guardar_afd.py         # Serialización de autómatas
│   ├── lector_yal.py          # Parser de archivos YAL
│   ├── main_lexer.py          # Punto de entrada del lexer
│   ├── shuting_yard.py        # Algoritmo Shunting Yard
│   └── tree.py                # Estructura de árbol sintáctico
├── generador_sintactico/       # Módulo del analizador sintáctico
│   ├── AFD_normal.py          # AFD para gramáticas
│   ├── Gramatica_Builder.py   # Constructor de gramáticas
│   ├── TablaLR.py             # Tabla de parsing LR
│   ├── lr0.py                 # Autómata LR(0)
│   ├── lector_gramar.py       # Parser de archivos YALP
│   ├── main.py                # Punto de entrada del parser
│   └── mibuffer.py            # Buffer para procesamiento
└── main_parser_lexer.py       # Integración completa
```

---

## Módulo Léxico (`lexer/`)

### `AFD_lector.py`

**Propósito**: Implementa la clase `AFD` (Autómata Finito Determinista) para el reconocimiento de tokens.

#### Clases Principales

##### `AFD`
```python
class AFD:
    def __init__(self, alfabeto, estados, transiciones, estado_inicial, estados_finales, state_tags=None)
```

**Métodos Clave**:
- `move_AFD(states, symbol)`: Calcula transiciones entre estados
- `acept_Chain(w)`: Verifica si una cadena es aceptada
- `minimizumAFD()`: Minimiza el autómata eliminando estados redundantes
- `graphicAFD()`: Genera visualización con Graphviz

##### `Estado_AFD`
Representa un estado del autómata con número identificador y estados AFN asociados.

##### `Transicion`
Define transiciones entre estados con símbolo de entrada.

#### Funciones Utilitarias

- `create_dfa(root, position_map, follow_positions)`: Genera AFD desde árbol sintáctico
- Manejo de etiquetas de estados para identificación de tokens

### `Lexer.py`

**Propósito**: Analizador léxico principal que procesa entrada y genera tokens.

#### Clase `Lexer`

```python
class Lexer:
    def __init__(self, automaton, token_labels, output_path='salida_logs.txt', debug=True)
```

**Métodos Principales**:

- `analyze(input_string)`: Analiza cadena completa y retorna lista de tokens
- `token_producer(buffer)`: Generador que produce tokens usando buffer (patrón productor-consumidor)

**Algoritmo de Análisis**:
1. **Longest Match**: Selecciona el token más largo posible
2. **Backtracking**: Retrocede cuando no hay transición válida
3. **Error Recovery**: Maneja errores léxicos y continúa análisis

### `buffer_lexer.py`

**Propósito**: Manejo eficiente de entrada con buffer de tamaño fijo.

#### Clase `Buffer`

```python
class Buffer:
    def __init__(self, filename_or_size, tamano_or_entrada=None)
```

**Características**:
- Lectura desde archivo o cadena
- Buffer circular con gestión automática
- Soporte para retroceso (`retroceder_caracter()`)
- Reemplazo de caracteres especiales (espacios, saltos de línea)

**Métodos Clave**:
- `cargar_buffer()`: Carga nuevo bloque de datos
- `obtener_siguiente_caracter()`: Lee siguiente carácter con transformaciones
- `retroceder_caracter()`: Permite backtracking para longest match

### `lector_yal.py`

**Propósito**: Parser de archivos YAL (especificación de tokens) que procesa definiciones y reglas.

#### Clase `Lector_Yal`

**Formato YAL Soportado**:
```
let DIGIT = ['0'-'9']
let LETTER = ['a'-'z','A'-'Z']

rule tokens =
| DIGIT+ { return NUMBER }
| LETTER(LETTER|DIGIT)* { return ID }
| [ \t\n]+ { None }
```

**Funciones de Procesamiento**:

- `parse_lexers()`: Analiza archivo YAL completo
- `expand_sets_and_ranges()`: Expande rangos de caracteres `[a-z]`
- `transform_repetition_syntax()`: Convierte `A+` → `A(A)*`, `A?` → `(A|ε)`
- `merge_rule_expressions()`: Combina todas las reglas en expresión maestra

**Algoritmo de Expansión**:
1. **Rangos**: `[a-z]` → `(97|98|99|...)`
2. **Conjuntos**: `[abc]` → `(97|98|99)`
3. **Negación**: `[^abc]` → `(todos_ascii - {a,b,c})`
4. **Repetición**: Transformación a operadores básicos `*`, `|`, `.`

### `shuting_yard.py`

**Propósito**: Implementa algoritmo Shunting Yard para conversión infix→postfix y construcción de árboles sintácticos.

#### Funciones Principales

##### `convert_to_postfix(infix_expr)`
Convierte expresión regular a notación postfija:
```
Entrada: "a|b*"
Salida: ["a", "b", "*", "|"]
```

**Precedencia de Operadores**:
1. `#` (etiquetas) - Precedencia 4
2. `*`, `+`, `?` - Precedencia 3  
3. `.` (concatenación) - Precedencia 2
4. `|` (alternación) - Precedencia 1

##### `construct_syntax_tree(postfix_expr)`
Construye árbol sintáctico desde expresión postfija:
- Calcula `first_positions` y `last_positions`
- Determina `can_be_empty` para cada nodo
- Mapea posiciones para construcción de AFD

##### `calculate_follow_positions(root, position_map)`
Calcula conjuntos FOLLOW para construcción de AFD:
- **Concatenación**: `lastpos(c1)` → `firstpos(c2)`
- **Estrella**: `lastpos(n)` → `firstpos(n)`

### `tree.py`

**Propósito**: Estructura de datos para árbol sintáctico de expresiones regulares.

#### Clase `TreeNode`
```python
class TreeNode:
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol           # Operador o símbolo terminal
        self.left = left              # Hijo izquierdo
        self.right = right            # Hijo derecho
        self.first_positions = set()   # Conjunto FIRST
        self.last_positions = set()    # Conjunto LAST
        self.can_be_empty = False     # Puede derivar épsilon
        self.pos = None               # Posición única en el árbol
```

#### Funciones Utilitarias
- `compute_empty_transition_closure()`: Cierre épsilon para estados
- `add_concat_operators()`: Inserta operadores de concatenación explícitos

---

## Módulo Sintáctico (`generador_sintactico/`)

### `Gramatica_Builder.py`

**Propósito**: Constructor de gramáticas con cálculo de conjuntos FIRST y FOLLOW.

#### Clase `Gramatica_Builder`

```python
class Gramatica_Builder:
    def __init__(self, producciones, no_terminales, terminales, ignorados=None)
```

**Algoritmos Implementados**:

##### Conjunto FIRST
```python
def compute_first(self):
    # Algoritmo iterativo hasta punto fijo
    # Para cada producción A → α:
    #   FIRST(A) ∪= FIRST(α)
```

##### Conjunto FOLLOW  
```python
def compute_follow(self, start_symbol):
    # Para cada producción A → αBβ:
    #   FOLLOW(B) ∪= FIRST(β) - {ε}
    #   Si ε ∈ FIRST(β): FOLLOW(B) ∪= FOLLOW(A)
```

**Ejemplo de Uso**:
```python
grammar = Gramatica_Builder(
    producciones={
        "S'": [("expression",)],
        'expression': [('expression', 'PLUS', 'term'), ('term',)], 
        'term': [('term', 'TIMES', 'factor'), ('factor',)], 
        'factor': [('LPAREN', 'expression', 'RPAREN'), ('ID',)]
    },
    no_terminales=['expression', 'term', 'factor', "S'"],
    terminales=['ID', 'PLUS', 'TIMES', 'LPAREN', 'RPAREN']
)
```

### `lr0.py`

**Propósito**: Construcción de autómata LR(0) para análisis sintáctico.

#### Clase `LR0_Automata`

**Algoritmo de Construcción**:

1. **Estado Inicial**: Ítem `S' → ·S`
2. **Función CLOSURE**: Cierre de conjunto de ítems
3. **Función GOTO**: Transición con símbolo
4. **Construcción**: Exploración exhaustiva de estados

##### Funciones Clave

```python
def closure(self, items):
    # Para cada ítem A → α·Bβ donde B es no-terminal:
    #   Agregar todos los ítems B → ·γ
```

```python
def goto(self, state, symbol):
    # Para todos los ítems A → α·symbβ en state:
    #   Crear nuevo estado con ítems A → αsymb·β
```

**Ejemplo de Estados**:
```
Estado 0:
  S' → ·E
  E → ·E + T
  E → ·T
  T → ·T * F
  T → ·F
  F → ·( E )
  F → ·int

Estado 1 (GOTO(0, E)):
  S' → E·
  E → E· + T
```

### `TablaLR.py`

**Propósito**: Construcción de tabla de parsing SLR(1) y algoritmo de análisis.

#### Clase `ParsingTable`

**Estructura de Tablas**:
- **ACTION**: `shift/reduce/accept/error` para terminales
- **GOTO**: transiciones para no-terminales

##### Construcción SLR(1)

```python
def construirTablaSLR(self):
    self.construirGoto()    # Tabla GOTO
    self.construirAction()  # Tabla ACTION
```

**Reglas de Construcción**:

1. **SHIFT**: Si `A → α·aβ` y `GOTO(I, a) = J` → `ACTION[I,a] = shift J`
2. **REDUCE**: Si `A → α·` → `ACTION[I,a] = reduce A→α` para `a ∈ FOLLOW(A)`
3. **ACCEPT**: Si `S' → S·` → `ACTION[I,$] = accept`

##### Algoritmo de Parsing

```python
def parse(self, input_tokens):
    stack = [0]  # Pila con estados
    idx = 0      # Índice en entrada
    
    while True:
        state = stack[-1]
        token = input_tokens[idx]
        action = self.action_table[state][token]
        
        if action[0] == "shift":
            stack.extend([token, action[1]])
            idx += 1
        elif action[0] == "reduce":
            # Reducir según producción
        elif action[0] == "accept":
            return True
```

### `lector_gramar.py`

**Propósito**: Parser de archivos YALP (especificación de gramáticas).

#### Formato YALP

```
%token ID PLUS TIMES LPAREN RPAREN

expression: expression PLUS term
          | term
          ;

term: term TIMES factor
    | factor
    ;

factor: LPAREN expression RPAREN
      | ID
      ;
```

#### Clase `Lector_Gramar`

**Procesamiento**:
1. **Tokenización**: AFD simple para separar tokens
2. **Validación**: Verificación de sintaxis (comentarios, producciones)
3. **Extracción**: Separación de terminales, no-terminales y producciones
4. **Construcción**: Creación de `Gramatica_Builder`

---

## Integración y Uso

### `main_parser_lexer.py`

**Propósito**: Punto de entrada principal que integra analizador léxico y sintáctico.

#### Flujo de Ejecución

```bash
python main_parser_lexer.py archivo.yal datos.txt gramatica.yalp
```

**Proceso Completo**:

1. **Fase Léxica**:
   ```python
   # Procesar archivo YAL
   lector = Lector_Yal(archivo_yal)
   lector.parse_lexers()
   expresion_principal, reglas = lector.merge_rule_expressions(lector.contenido)
   
   # Construir AFD
   postfix = convert_to_postfix(expresion_principal)
   raiz, posiciones = construct_syntax_tree(postfix)
   followpos = calculate_follow_positions(root=raiz, position_map=posiciones)
   afd_instance = create_dfa(root=raiz, position_map=posiciones, follow_positions=followpos)
   afd_instance.minimizumAFD()
   ```

2. **Fase Sintáctica**:
   ```python
   # Procesar archivo YALP
   lector = Lector_Gramar(path_yalp)
   gramatica = lector.build_grammar()
   
   # Construir LR(0) y tabla
   automata = LR0_Automata(gramatica)
   tabla = ParsingTable(automata, gramatica)
   tabla.construirTablaSLR()
   ```

3. **Análisis Integrado**:
   ```python
   # Crear lexer y parser integrados
   buffer = Buffer(path_data, 10)
   lexer_generator = lexer.token_producer(buffer)
   tabla.parse_consumer_producer(lexer_generator)
   ```

---

## Algoritmos Clave

### Construcción de AFD desde Expresión Regular

1. **Conversión a Postfijo**: Shunting Yard
2. **Árbol Sintáctico**: Construcción bottom-up
3. **Cálculo de Posiciones**: FIRST, LAST, FOLLOW
4. **Estados AFD**: Subconjuntos de posiciones
5. **Minimización**: Partición de estados equivalentes

### Análisis SLR(1)

1. **Autómata LR(0)**: Estados = conjuntos de ítems
2. **Tabla ACTION/GOTO**: Construcción determinística
3. **Parsing**: Algoritmo shift-reduce con pila

### Patrón Productor-Consumidor

- **Lexer**: Produce tokens bajo demanda
- **Parser**: Consume tokens conforme necesita
- **Buffer**: Gestión eficiente de memoria para archivos grandes

---

## Características Avanzadas

### Minimización de Autómatas
- Separación inicial por estados finales y tags
- Refinamiento iterativo de particiones
- Preservación de etiquetas semánticas

### Manejo de Errores
- **Léxicos**: Carácter inválido → continuar análisis
- **Sintácticos**: Estado sin acción → reporte de error
- **Logging**: Archivo de salida con información detallada

### Optimizaciones
- **Longest Match**: Máximo munch para tokens
- **Buffer Circular**: Memoria eficiente para archivos grandes
- **Lazy Evaluation**: Tokens generados bajo demanda

### Visualización
- **Graphviz**: Diagramas de autómatas AFD y LR(0)
- **Archivos DOT**: Exportación para herramientas externas
- **PNG/SVG**: Renderizado automático

---

## Ejemplos de Uso

### Archivo YAL (Tokens)
```
let DIGIT = ['0'-'9']
let LETTER = ['a'-'z','A'-'Z']

rule tokens =
| DIGIT+ { return NUMBER }
| LETTER(LETTER|DIGIT)* { return ID }
| '+' { return PLUS }
| '*' { return TIMES }
| '(' { return LPAREN }
| ')' { return RPAREN }
| [ \t\n]+ { }
```

### Archivo YALP (Gramática)
```
%token NUMBER ID PLUS TIMES LPAREN RPAREN

expr: expr PLUS term
    | term
    ;

term: term TIMES factor
    | factor
    ;

factor: LPAREN expr RPAREN
      | NUMBER
      | ID
      ;
```

### Entrada de Datos
```
x + 123 * (y + 456)
```

### Salida Esperada
```
✔️ Token: ID, lexeme: 'x'
✔️ Token: PLUS, lexeme: '+'
✔️ Token: NUMBER, lexeme: '123'
✔️ Token: TIMES, lexeme: '*'
✔️ Token: LPAREN, lexeme: '('
✔️ Token: ID, lexeme: 'y'
✔️ Token: PLUS, lexeme: '+'
✔️ Token: NUMBER, lexeme: '456'
✔️ Token: RPAREN, lexeme: ')'
✅ Cadena aceptada correctamente. 😁👍
```

---

## Dependencias

- **Python 3.7+**
- **Graphviz**: Para visualización de autómatas
  ```bash
  pip install graphviz
  ```

---
