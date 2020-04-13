import ply.lex as lex
import ply.yacc as yacc
import sys 
# Definicion de los Tokens y palabras reservadas
reserved = {
	'programa' : 'PROGRAMA',
	'principal' : 'PRINCIPAL',
	'var' : 'VAR',
	'funcion' : 'FUNCION',
	'regresa' : 'REGRESA',
	'lee' : 'LEE',
	'escribe' : 'ESCRIBE',
	'for' : 'FOR',
	'si' : 'SI',
	'entonces' : 'ENTONCES',
	'sino' : 'SINO',
	'mientras' : 'MIENTRAS',
	'haz' : 'HAZ',
	'desde' : 'DESDE',
	'hasta' : 'HASTA',
	'hacer' : 'HACER',
	'void' : 'VOID',
	'int' : 'INT',
	'float' : 'FLOAT',
	'char'	:	'CHAR'
}
tokens = [ 'NUM_I', 'NUM_F', 'ID', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAR', 'RPAR',
			'LBRA', 'RBRA', 'EQUAL', 'SCO', 'COL', 'COM', 'LT', 'MT', 'NOTEQUAL', 
			'STRING', 'ELT', 'EMT',
			'LCOR', 'RCOR'] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRA = r'\{'
t_RBRA = r'\}'
t_EQUAL = r'\='
t_SCO = r'\;'
t_COL = r'\:'
t_COM = r'\,'
t_LT = r'\<'
t_MT = r'\>'
t_NOTEQUAL = r'\<>'
t_LCOR = r'\['
t_RCOR = r'\]'
t_ELT = r'\<='
t_EMT = r'\>='

t_ignore = ' \t'

def t_NUM_F(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t
	
def t_NUM_I(t):
	r'\d+'
	t.value = int(t.value)
	return t


def t_ID(t): 
	r'[a-zA-Z_][a-zA-Z]*'
	if t.value in reserved:
		t.type = reserved[t.value]    # lista de palabras reservadas
	return t

def t_STRING(t): 
	r'"([^\\"\n]+|\\.)*"'
	t.type = 'STRING'
	return t

#Saltos de linea
def t_newLine(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

#Funcino que maneja caracteres extraÃ±os
def t_error(t):
	print("Ilegal charcater '%s'" % t.value[0])
	t.lexer.skip(1)
	
lexer = lex.lex()

lexer.input("programa prueba;")

while True:
	tok  = lexer.token()
	if not tok :
		break
	print(tok)