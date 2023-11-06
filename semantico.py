from tabulate import tabulate

class SymbolTableEntry:
    def __init__(self, lexeme, symbol, lineno, es_funcion, tipo_dato, scope):
        self.lexeme = lexeme
        self.symbol = symbol
        self.lineno = lineno
        self.es_funcion = es_funcion
        self.tipo_dato = tipo_dato
        self.scope = scope

class SymbolTable:
    def __init__(self):
        self.entries = []

    def buscar(self, lexeme, scope):
        for entry in self.entries:
            if entry.lexeme == lexeme and entry.scope == scope:
                return entry
        return None

    def insertar(self, entry):
        if entry.symbol not in {'FUNCION', 'ID', 'asignacion', 'suma', 'NUMERO', 'ILLAVE', 'DLLAVE', 'IPAREN', 'DPAREN', 'finsentencia', ';', '{', '}', ')'}:
            return
        existing_entry = self.buscar(entry.lexeme, entry.scope)
        if existing_entry:
            return
        self.entries.append(entry)

    def imprimir_tabla(self):
        print("Tabla de símbolos:")
        print("===================")
        symbol_table_data = []
        for entry in self.entries:
            es_funcion = "función" if entry.es_funcion else "variable"
            symbol_table_data.append([entry.lexeme, entry.symbol, entry.lineno, es_funcion, entry.tipo_dato, entry.scope])

        table = tabulate(symbol_table_data, headers=["lexeme", "Símbolo", "Línea", "Es función", "Tipo de dato", "Ámbito"], tablefmt="pretty")
        print(table)
        print("===================")

class SemanticAnalyzer:
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree
        self.analyzed = False
        self.symbol_table = SymbolTable()
        self.printed_table = False
        self.current_scope = "global"

    def analyze(self):
        if not self.analyzed:
            self.traverse_tree(self.syntax_tree)
            self.analyzed = True
            self.print_symbol_table()
            print("Verificación de ámbito de variables realizada")

    def traverse_tree(self, node):
        if hasattr(node, 'lexeme') and node.lexeme is not None:
            lexeme = node.lexeme
            is_function = False
            if node.symbol == 'FUNCION':
                is_function = True
            elif node.symbol == 'ID':
                existing_entry = self.symbol_table.buscar(lexeme, self.current_scope)
                if existing_entry and existing_entry.es_funcion:
                    is_function = True
            entry = SymbolTableEntry(lexeme, node.symbol, node.lineno, is_function, node.symbol, self.current_scope)
            self.symbol_table.insertar(entry)

        if node.symbol == 'FUNCION':
            function_name = node.children[1].lexeme
            function_type = node.children[0].symbol
            entry = SymbolTableEntry(function_name, function_type, node.lineno, True, function_type, self.current_scope)
            self.symbol_table.insertar(entry)
            self.current_scope = function_name

        for child in node.children:
            if child.symbol == 'FUNCION':
                self.current_scope = child.children[1].lexeme
            elif child.symbol in {'ID', 'NUMERO'}:
                self.traverse_tree(child)
                lexeme = child.lexeme
                entry = SymbolTableEntry(lexeme, child.symbol, child.lineno, False, child.symbol, self.current_scope)
                self.symbol_table.insertar(entry)
            else:
                self.traverse_tree(child)

    def print_symbol_table(self):
        if not self.printed_table:
            self.symbol_table.imprimir_tabla()
            self.printed_table = True

if __name__ == "__main__":
  from sin import tree_espejo  # Importa el árbol espejo desde sin.py
  analyzer = SemanticAnalyzer(tree_espejo)  # Pasa el árbol espejo al analizador semántico
  analyzer.analyze()
