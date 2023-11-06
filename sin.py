import pandas as pd

class NodeStack:
      def __init__(self, symbol, lexeme):
          global count
          self.symbol = symbol
          self.lexeme = lexeme
          self.id = count + 1
          count += 1

class NodeTree:
      def __init__(self, id, symbol, lexeme):
          self.id = id
          self.symbol = symbol
          self.lexeme = lexeme
          self.children = []
          self.father = None

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
      root = NodeTree(symbol_E.id, symbol_E.symbol, symbol_E.lexeme)

      # Analizador sintáctico LL(1)
      while stack and tokens_list:  # Asegurarse de que tokens_list no esté vacío
          # Obtener el símbolo superior de la pila y el símbolo de entrada actual
          top_of_stack = stack[-1]
          current_input = tokens_list[0]

          if top_of_stack.symbol == current_input["symbol"]:
              # Coincidencia, avanzar en la pila y la entrada
              stack.pop()
              tokens_list.pop(0)
          else:
              try:
                  # Obtener la producción desde la tabla de análisis sintáctico

                  production = tabla.loc[top_of_stack.symbol, current_input["symbol"]]
              except KeyError:
                  print(f"Error sintáctico: No se encontró una regla para {top_of_stack.symbol} y {current_input['symbol']}")
                  return

              if pd.isna(production):  # Detectar producción no definida
                  print(f"Error sintáctico: No se encontró una producción para {top_of_stack.symbol} y {current_input['symbol']}")
                  return

              # Reemplazar la producción en la pila
              stack.pop()
              if production != '': 
                production_symbols = production.split()
                production_symbols.reverse()
                for symbol in production_symbols:
                    if symbol != 'e':
                        new_node = NodeStack(symbol, current_input["lexeme"])
                        stack.append(new_node)

                        # Crear el nodo en el árbol sintáctico
                        new_node_tree = NodeTree(new_node.id, new_node.symbol, new_node.lexeme)
                        father = buscar_node(top_of_stack.id, root)
                        father.children.append(new_node_tree)
                        new_node_tree.father = father

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

  # Función para imprimir el árbol sintáctico
def print_tree(node, level=0):
      output = '   ' * level + node.symbol + "\n"
      print(output, end="")
      with open("arbol_sintactico.txt", "a") as file:
          file.write(output)
      for child in node.children:
          print_tree(child, level+1)

  # Función para imprimir el árbol sintáctico en formato DOT para Graphviz
def print_tree_dot(node):
      with open("arbol_sintactico_dot.txt", "w") as file:
          file.write("digraph G {\n")
          generate_dot(node, file)
          file.write("}\n")

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
  for child in node.children:
      # Sanitizar los símbolos antes de escribirlos en el archivo DOT
      node_symbol = sanitize_symbol(node.symbol)
      child_symbol = sanitize_symbol(child.symbol)

      # Determinar el color del nodo actual y del nodo hijo
      node_color = get_node_color(node.symbol)
      child_color = get_node_color(child.symbol)

      file.write(f'  {node_symbol}{node.id} [label="{node_symbol}", color="{node_color}", style="filled"];\n')
      file.write(f'  {child_symbol}{child.id} [label="{child_symbol}", color="{child_color}", style="filled"];\n')
      file.write(f'  {node_symbol}{node.id} -> {child_symbol}{child.id};\n')

      generate_dot(child, file)
