
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
from sin import analizador_sintactico

# r'atring' -> r significa que la cadena es tradada sin caracteres de escape, 
# es decir r'\n' seria un \ seguido de n (no se interpretaria como salto de linea) 

 # List of token names.   This is always required
reserved = {
    'NUMERO'    :  'TIPONUMERO',
    'decimal'   :  'TIPODECIMAL',
    'caracter'  :  'TIPOCARACTER',
    'cadena'    :  'TIPOCADENA',
    'booleano'  :  'TIPOBOOLEANO',
    'si'        :  'SI',
    'sino'      :  'SINO',
    'mientras'  :  'MIENTRAS',
    'para'      :  'PARA',
    'hacer'     :  'HACER',
    'desde'     :  'desde',
    'hasta'     :  'HASTA',
    'funcion'   :  'FUNCION',
    'retorno'   :  'RETORNO',
    'verdadero' :  'VERDADERO',
    'falso'     :  'FALSO',
    'principal' :  'PRINCIPAL',
    'romper'    :  'ROMPER',
    'entrada'   :  'ENTRADA',
    #'salida'    :  'SALIDA',
    'imprimir'  :  'IMPRIMIR',
    'leer'      :  'LEER',
}

tokens = [
    'NUMERO',
    'SALIDA',
    'ID',
    'CADENA',
    'CARACTER',
    'ESPACIO',
    'COMENTMULT',
    'COMENTARIO',
    'GUIONES',
    'PUNTO',
    'COMA',
    'ENTERO',
    'DECIMAL',
    'BOOLEANO',
    'suma',
    'funcion',
    'RESTA',
    'MULT',
    'DIV',
    'asignacion',
    'MENOR',
    'MAYOR',
    'MODULO',
    'MAYORIGUAL',
    'MENORIGUAL',
    'COMPARAR',
    'NEGACION',
    'DISTINTO',
    'IPAREN',
    'DPAREN',
    'ILLAVE',
    'DLLAVE',
    'finsentencia',
] + list(reserved.values())

 # Regular expression rules for simple tokens

#t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ESPACIO = r'\s+'
t_PRINCIPAL = r'principal'
t_PUNTO = r'\.'
t_COMA = r','
t_suma    = r'\+'
t_RESTA   = r'-'
t_MULT   = r'\*'
t_DIV  = r'/'
t_asignacion = r'='
t_SALIDA = r'<<'
t_ENTRADA = r'>>'
t_MENOR = r'<'
t_MAYOR = r'>'
t_MODULO = r'%'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_COMPARAR = r'=='
t_NEGACION = r'!='
t_DISTINTO = r'!'
t_IPAREN  = r'\('
t_DPAREN  = r'\)'
t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_finsentencia = r';'
#t_NUMBER  = r'\d+'

 # A regular expression rule with some action code
def find_column(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_CADENA(t):
    r'"([^"])*"'
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)  # guardamos el valor del lexema  
    #print("se reconocio el numero")
    return t

def t_ENTERO(t):
    r'[1-9][0-9]*|0'
    t.value = int(t.value)
    return t

def t_DECIMAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_TIPO_ENTERO(t):
    r'entero'
    t.type = reserved['entero']
    return t

def t_TIPO_DECIMAL(t):
    r'decimal'
    t.type = reserved.get(t.value, 'TIPO_DECIMAL')
    return t

def t_COMENTMULT(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    t.value = t.value  # Establece el tipo de token como 'COMENTMULT'
    return t

def t_COMENTARIO(t):
    r'//.*'
    t.value = t.value  # Ignorar comentarios de una sola línea
    return t

def t_CARACTER(t):
    r"'.'"
    return t

# Regla para guiones
def t_GUIONES(t):
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
      # Imprimir la lista de tokens
      for token_info in tokens_list:
          print(f'Symbol: {token_info["symbol"]}, Lexem: {token_info["lexeme"]}, Line: {token_info["nroline"]} Column: {token_info["col"]}')

  analizador_sintactico(tokens_list)

if __name__ == '__main__':
  main()
