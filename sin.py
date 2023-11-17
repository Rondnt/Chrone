import pandas as pd
import numpy as np
import json

class Token:
    def __init__(self, symbol, lexeme, nroline, col):
        self.symbol = symbol
        self.lexeme = lexeme
        self.nroline = nroline
        self.col = col

        if pd.isnull(self.nroline):
            self.nroline = np.NaN
        if pd.isnull(self.col):
            self.col = np.NaN

class NodeStack:
    def __init__(self, symbol, lexeme):
        global count
        self.symbol = symbol
        self.lexeme = lexeme
        self.id = count + 1
        count += 1

class NodeTree:
  def __init__(self, id, symbol, lexeme, nroline, col, data_type=None):
      self.id = id
      self.symbol = symbol
      self.lexeme = lexeme
      self.nroline = nroline
      self.col = col
      self.data_type = data_type  # Nuevo atributo para almacenar el tipo de dato
      self.children = []
      self.father = None


class SymbolTable:
  def __init__(self):
      self.symbols = {}
      self.current_scope = 'global'  # Ámbito global por defecto
      self.scopes_stack = []

  def enter_scope(self, scope_name):
      self.scopes_stack.append(self.current_scope)
      self.current_scope = scope_name

  def exit_scope(self):
      self.current_scope = self.scopes_stack.pop()

  def declare_variable(self, token_dict, data_type):
      name = token_dict['lexeme']
      full_name = f"{self.current_scope}:{name}"
      if full_name in self.symbols:
          print(f"Error semántico: La variable {name} ya está declarada en el ámbito {self.current_scope} como tipo {self.symbols[full_name]['tipo']}.")
      else:
          self.symbols[full_name] = {'tipo': data_type}
          print(f"Variable {name} declarada en el ámbito {self.current_scope} como tipo {data_type}.")
          print("Tabla de símbolos después de la declaración:", self.symbols)

  def declare_function(self, token_dict):
    name = token_dict['lexeme']
    full_name = f"{self.current_scope}:{name}"
    if full_name in self.symbols:
        print(f"Error semántico: La función {name} ya está declarada en el ámbito {self.current_scope}.")
    else:
        self.symbols[full_name] = {'tipo': 'funcion', 'parametros': []}
        print(f"Función {name} declarada en el ámbito {self.current_scope}.")
        print("Tabla de símbolos después de la declaración:", self.symbols)

  def declare_function_parameter(self, token_dict):
    name = token_dict['lexeme']
    full_name = f"{self.current_scope}:{name}"
    if full_name in self.symbols:
        print(f"Error semántico: El parámetro {name} de la función ya está declarado en el ámbito {self.current_scope}.")
    else:
        self.symbols[full_name] = {'tipo': 'parametro'}
        # Agregar el parámetro a la lista de parámetros de la función actual
        function_name = self.scopes_stack[-1]
        function_full_name = f"{self.current_scope}:{function_name}"
        if function_full_name in self.symbols:
            self.symbols[function_full_name]['parametros'].append(name)
        print(f"Parámetro {name} de la función {function_name} declarado en el ámbito {self.current_scope}.")
        print("Tabla de símbolos después de la declaración:", self.symbols)


  def get_symbol_type(self, name):
      full_name = f"{self.current_scope}:{name}"
      if full_name in self.symbols:
          return self.symbols[full_name]['tipo']
      else:
          print(f"Error semántico: El símbolo {name} no está declarado en el ámbito {self.current_scope}.")
          return 'desconocido'


def buscar_node(id, node):
    if node.id == id:
        return node
    for child in node.children:
        result = buscar_node(id, child)
        if result:
            return result
    return None

def convertir_arbol_espejo(nodo):
    if nodo is None:
        return None
    # Invierte los hijos del nodo actual
    nodo.children = list(reversed(nodo.children))
    # Recorre los hijos y realiza la inversión en cada uno de ellos
    for hijo in nodo.children:
        convertir_arbol_espejo(hijo)
    return nodo

# Cargar la tabla CSV
tabla = pd.read_csv("gramatica.csv", index_col=0)
count = 0

def analizador_sintactico(tokens_list):
  global count
  stack = []

  # Inicializar la pila
  symbol_E = NodeStack('PROGRAMA', None)
  symbol_dollar = NodeStack('$', None)
  stack.append(symbol_dollar)
  stack.append(symbol_E)

  # Inicializar el árbol sintáctico
  root = NodeTree(symbol_E.id, symbol_E.symbol, symbol_E.lexeme, 0, 0)

  # Crear una instancia de la tabla de símbolos
  symbol_table = SymbolTable()

  # Analizador sintáctico LL(1)
  while stack and tokens_list:  
    top_of_stack = stack[-1]
    current_input = tokens_list[0]

    if top_of_stack.symbol == current_input['symbol']:
        stack.pop()
        tokens_list.pop(0)
    else:
        try:
            production = tabla.loc[top_of_stack.symbol, current_input['symbol']]
        except KeyError:
            print(f"Error sintáctico: No se encontró una regla para {top_of_stack.symbol} y {current_input['symbol']}")
            return

        if pd.isna(production):
            print(f"Error sintáctico: No se encontró una producción para {top_of_stack.symbol} y {current_input['symbol']}")
            return

        stack.pop()
        if production != '':
            production_symbols = production.split()
            production_symbols.reverse()

            for symbol in production_symbols:
                if symbol != 'e':
                    new_node = NodeStack(symbol, current_input['lexeme'])
                    stack.append(new_node)

                    data_type = inferir_tipo_dato(new_node, current_input['lexeme'], symbol_table)
                    new_node_tree = NodeTree(new_node.id, new_node.symbol, new_node.lexeme, current_input['nroline'], current_input['col'], data_type)
                    father = buscar_node(top_of_stack.id, root)
                    father.children.append(new_node_tree)
                    new_node_tree.father = father

                    if new_node.symbol == 'id':
                        if production.split()[0] == 'TPVAR':
                            symbol_table.declare_variable(tokens_list[0], data_type)
                        elif production.split()[0] == 'TPFUNC':
                            symbol_table.declare_function(tokens_list[0])
                        elif production.split()[0] == 'TPPARAM':
                            symbol_table.declare_function_parameter(tokens_list[0])

                        if data_type != 'desconocido':
                            print(f"{new_node.symbol} {tokens_list[0]['lexeme']} declarado como tipo {data_type} en el ámbito {symbol_table.current_scope}.")

                    # Verificar el tipo de dato en las asignaciones
                    if new_node.symbol == 'ASIGNACION':
                        tipo_izquierdo = inferir_tipo_dato(node.children[0], lexeme, symbol_table)
                        tipo_derecho = inferir_tipo_dato(node.children[1], lexeme, symbol_table)

                        if tipo_izquierdo != tipo_derecho:
                            print(f"Error semántico: Los tipos en la asignación no coinciden ({tipo_izquierdo} y {tipo_derecho})")

  # Si la pila está vacía y la entrada también, la cadena es aceptada
  if not stack and not tokens_list:
      print("La cadena no es aceptada")
  else:
      print("La cadena es aceptada")

  # Convertir el árbol en un árbol espejo antes de imprimirlo
  root = convertir_arbol_espejo(root)

  # Imprimir el árbol sintáctico
  print_tree(root)
  print_tree_dot(root)
  print_tree_json(root)

# Función para inferir el tipo de dato de un símbolo
def inferir_tipo_dato(node, lexeme, symbol_table):
  # Implementa la lógica de inferencia de tipos según las reglas de tu lenguaje
  if node.symbol == 'PROGRAMA':
      # El símbolo 'PROGRAMA' es un símbolo especial, no tiene un tipo asociado.
      return None
  elif node.symbol == 'tipoentero':
      node.data_type = 'entero'
      return 'entero'
  elif node.symbol == 'CADENA':
      node.data_type = 'cadena'
      return 'cadena'
  elif node.symbol == 'iparen':
      node.data_type = '('
      return '('
  elif node.symbol == 'dparen':
      node.data_type = ')'
      return ')'
  elif node.symbol == 'illave':
      node.data_type = '{'
      return '{'
  elif node.symbol == 'dllave':
      node.data_type = '}'
      return '}'
  elif node.symbol == 'finsentencia':
      node.data_type = ';'
      return ';'
  elif node.symbol == 'id':
      node.data_type = symbol_table.get_symbol_type(lexeme)
      return lexeme  # Retorna el lexema en lugar de solo 'id'
  elif node.symbol == 'ASIGNACION':
      # Verificar el tipo del lado izquierdo (variable)
      tipo_izquierdo = inferir_tipo_dato(node.children[0], lexeme, symbol_table)

      # Verificar el tipo del lado derecho (expresión)
      tipo_derecho = inferir_tipo_dato(node.children[1], lexeme, symbol_table)

      # Validar la asignación de tipos
      if tipo_izquierdo != tipo_derecho:
          print(f"Error semántico: Los tipos en la asignación no coinciden ({tipo_izquierdo} y {tipo_derecho})")

      # Establecer el tipo de dato en el nodo de asignación
      node.data_type = tipo_izquierdo

      return tipo_izquierdo
  else:
      # Otros casos o símbolos no manejados, retorna el lexema si existe
      return lexeme if lexeme is not None else 'desconocido'


# Función para imprimir el árbol sintáctico
def print_tree(node, level=0):
    output = '   ' * level + f"{node.symbol} ({node.data_type})" + "\n"
    print(output, end="")
    with open("arbol_sintactico.txt", "a") as file:
        file.write(output)
    for child in node.children:
        print_tree(child, level + 1)

# Función para imprimir el árbol sintáctico en formato DOT para Graphviz
def print_tree_dot(node):
    with open("arbol_sintactico_dot.txt", "w") as file:
        file.write("digraph G {\n")
        generate_dot(node, file)
        file.write("}\n")

def print_tree_json(node):
    tree_dict = convert_tree_to_dict(node)
    with open("arbol_sintactico.json", "w") as file:
        json.dump(tree_dict, file, indent=4)

def convert_tree_to_dict(node):
    # Convierte el nodo y sus hijos a un diccionario
    node_dict = {
        "id": node.id,
        "symbol": node.symbol,
        "lexeme": node.lexeme,
        "nroline": node.nroline,
        "col": node.col,
        "data_type": node.data_type,
        "children": [convert_tree_to_dict(child) for child in node.children]
    }
    return node_dict

def sanitize_symbol(symbol):
    # Reemplazar caracteres no válidos en el nombre del símbolo DOT
    return symbol.replace("'", "_").replace('"', '_')

def get_node_color(symbol):
    # Define los colores para nodos terminales y no terminales
    terminal_color = "lightcoral"
    non_terminal_color = "lightblue"

    # Verifica si el símbolo es un no terminal (puedes ajustar esto según tu gramática)
    if symbol.isupper():
        return non_terminal_color
    else:
        return terminal_color

def generate_dot(node, file):
  # Sanitizar el símbolo antes de escribirlo en el archivo DOT
  node_symbol = sanitize_symbol(f"{node.symbol} ({node.data_type})")

  # Determinar el color del nodo actual
  node_color = get_node_color(node.symbol)

  # Escribir el nodo en el archivo DOT
  file.write(f'  "{node_symbol}{node.id}" [label="{node_symbol}", color="{node_color}", style="filled"];\n')

  # Iterar sobre los hijos
  for child in node.children:
      # Sanitizar el símbolo del hijo antes de escribirlo en el archivo DOT
      child_symbol = sanitize_symbol(f"{child.symbol} ({child.data_type})")

      # Determinar el color del nodo hijo
      child_color = get_node_color(child.symbol)

      # Escribir el nodo hijo en el archivo DOT
      file.write(f'  "{child_symbol}{child.id}" [label="{child_symbol}", color="{child_color}", style="filled"];\n')

      # Conectar el nodo actual con el nodo hijo
      file.write(f'  "{node_symbol}{node.id}" -> "{child_symbol}{child.id}";\n')

      # Llamar recursivamente a la función para los hijos del hijo
      generate_dot(child, file)
