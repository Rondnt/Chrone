
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
from sin import analizador_sintactico

# r'atring' -> r significa que la cadena es tradada sin caracteres de escape, 
# es decir r'\n' seria un \ seguido de n (no se interpretaria como salto de linea) 

 # List of token names.   This is always required
reserved = {
    'entero'    :  'tipoentero',
    'decimal'   :  'TIPODECIMAL',
    'caracter'  :  'TIPOCARACTER',
    'cadena'    :  'TIPOCADENA',
    'booleano'  :  'TIPOBOOLEANO',
    'si'        :  'si',
    'sino'      :  'sino',
    'mientras'  :  'MIENTRAS',
    'para'      :  'PARA',
    'hacer'     :  'HACER',
    'desde'     :  'desde',
    'hasta'     :  'HASTA',
    'funcion'   :  'funcion',
    'retornar'   :  'retornar',
    'verdadero' :  'VERDADERO',
    'falso'     :  'FALSO',
    'principal' :  'principal',
    'romper'    :  'ROMPER',
    'entrada'   :  'ENTRADA',
    #'salida'    :  'salida',
    'imprimir'  :  'imprimir',
    'leer'      :  'LEER',
}

tokens = [
    'entero',
    'salida',
    #'retornar',
    'id',
    'cadena',
    'caracter',
    'espacio',
    'COMENTMULT',
    'COMENTARIO',
    'guiones',
    'punto',
    'coma',
    'decimal',
    'booleano',
    'suma',
    #'funcion',
    'resta',
    'mult',
    'div',
    'asignacion',
    'menor',
    'mayor',
    'MODULO',
    'mayorigual',
    'menorigual',
    'comparar',
    'NEGACION',
    'DISTINTO',
    'iparen',
    'dparen',
    'illave',
    'dllave',
    'finsentencia',
] + list(reserved.values())

 # Regular expression rules for simple tokens

#t_idENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_espacio = r'\s+'
#t_principal = r'principal'
t_punto = r'\.'
t_coma = r','
t_suma    = r'\+'
t_resta   = r'-'
t_mult   = r'\*'
t_div  = r'/'
t_asignacion = r'='
t_salida = r'<<'
t_ENTRADA = r'>>'
t_menor = r'<'
t_mayor = r'>'
t_MODULO = r'%'
t_mayorigual = r'>='
t_menorigual = r'<='
t_comparar = r'=='
t_NEGACION = r'!='
t_DISTINTO = r'!'
t_iparen  = r'\('
t_dparen  = r'\)'
t_illave = r'\{'
t_dllave = r'\}'
t_finsentencia = r';'
#t_NUMBER  = r'\d+'

 # A regular expression rule with some action code
def find_column(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'id')  # Check for reserved words
    return t

def t_cadena(t):
    r'"([^"])*"'
    return t

def t_entero(t):
    r'\d+'
    t.value = int(t.value)  # guardamos el valor del lexema  
    #print("se reconocio el entero")
    return t

def t_decimal(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_TIPODECIMAL(t):
    r'decimal'
    t.type = reserved.get(t.value, 'TIPODECIMAL')
    return t

def t_COMENTMULT(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    t.value = t.value  # Establece el tipo de token como 'COMENTMULT'
    return t

def t_COMENTARIO(t):
    r'//.*'
    t.value = t.value  # Ignorar comentarios de una sola línea
    return t

def t_caracter(t):
    r"'.'"
    return t

# Regla para guiones
def t_guiones(t):
    r'--'
    return t
 # Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

 # A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\n\r\f\v'

 # Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def main():
  tokens_list = []

  # Leer ejemplos de código fuente desde un archivo
  with open("ex1.txt", "r") as archivo:
      for linea in archivo:
          lexer.input(linea)
          while True:
              tok = lexer.token()
              if not tok:
                  break
              print(tok)  # Imprime cada token a medida que se genera
              # Agregar el token a la lista como un diccionario
              token_info = {
                  'symbol': tok.type,
                  'lexeme': tok.value,
                  'nroline': tok.lineno,
                  'col': find_column(linea, tok)
              }
              tokens_list.append(token_info)

  # Después de llenar tokens_list
  if not tokens_list:
      print("La lista de tokens está vacía.")
  else:
      print("La lista de tokens no está vacía.")
      # imprimir la lista de tokens
      for token_info in tokens_list:
          print(f'Symbol: {token_info["symbol"]}, Lexem: {token_info["lexeme"]}, Line: {token_info["nroline"]} Column: {token_info["col"]}')

  analizador_sintactico(tokens_list)


if __name__ == '__main__':
  main()
