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
tokens = [ 'NUM_I', 'NUM_F', 'LETRERO', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAR', 'RPAR',
			'LBRA', 'RBRA', 'EQUAL', 'SCO', 'COM', 'LT', 'MT', 'NOTEQUAL', 
			'STRING', 'ELT', 'EMT',
			'LCOR', 'RCOR', 'CR', 'AND', 'OR', 'EEQ'] + list(reserved.values())

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
t_COM = r'\,'
t_LT = r'\<'
t_MT = r'\>'
t_NOTEQUAL = r'\<>'
t_LCOR = r'\['
t_RCOR = r'\]'
t_ELT = r'\<='
t_EMT = r'\>='
t_AND = r'\&'
t_OR = r'\|'
t_EEQ = r'\=='

t_ignore = ' \t'

def t_NUM_F(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t
	
def t_NUM_I(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_CR(t): 
	r'[a-zA-Z]\s'
	t.type = 'CR'
	return t

def t_LETRERO(t): 
	r'[a-zA-Z_][a-zA-Z]*'
	if t.value in reserved:
		t.type = reserved[t.value]    # lista de palabras reservadas
	return t

def t_STRING(t): 
	r'%%([^\\"\n]+|\\.)*'
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

#Parser (definicion de la gramatica)
def p_programa(p):
	'''programa : PROGRAMA LETRERO SCO VARIABLES FUNCIONES PRIN
				| PROGRAMA LETRERO SCO FUNCIONES PRIN
				| PROGRAMA LETRERO SCO VARIABLES PRIN
				| PROGRAMA LETRERO SCO PRIN'''
				
def p_VARIABLES(p):
	'''VARIABLES : VAR OTRA'''
				
def p_OTRA(p):
	'''OTRA : LETRERO OTRA
			| LETRERO LCOR NUM_I RCOR OTRA
			| TIPO OTRA
			| COM OTRA
			| SCO OTRA
			| empty'''
					
#vacios
def p_empty(p):
	'empty :'
	pass
			
def p_TIPO(P):
	'''TIPO : INT
			| FLOAT 
			| CHAR'''
			
def p_FUNCIONES(p):
	'''FUNCIONES : FUNCION TIPO LETRERO LPAR OTRA RPAR SCO VARIABLES LBRA ESTATUTOS REGRESA LPAR EXPRESION RPAR SCO RBRA
				| FUNCION VOID LETRERO LPAR OTRA RPAR SCO VARIABLES LBRA ESTATUTOS RBRA
				| FUNCION TIPO LETRERO LPAR OTRA RPAR SCO LBRA ESTATUTOS REGRESA LPAR EXPRESION RPAR SCO RBRA
				| FUNCION VOID LETRERO LPAR OTRA RPAR SCO LBRA ESTATUTOS RBRA'''
	
def p_PRIN(p):
	'''PRIN : PRINCIPAL LPAR RPAR LBRA ESTATUTOS RBRA'''
	
def p_ESTATUTOS(p):
	'''ESTATUTOS : EST ESTATUTOS
				| empty'''
				
def p_EST(p): 
	'''EST : ASIGNACION
			| LECTURA
			| ESCRITURA
			| DESICION
			| CONDICIONAL
			| NOCONDICIONAL
			| LLAMADA'''
			
def p_ASIGNACION(p):
	'''ASIGNACION : LETRERO LCOR EXPRESION RCOR EQUAL EXPRESION SCO
					| LETRERO EQUAL EXPRESION SCO'''
				
def p_LECTURA(p):
	'''LECTURA : LEE LPAR OTRA RPAR SCO'''
	
def p_ESCRITURA(p):
	'''ESCRITURA : ESCRIBE LPAR WRITE RPAR SCO'''
	
def p_WRITE(p):
	'''WRITE : EXPRESION WRITE
			| LETRERO WRITE 
			| COM WRITE 
			| empty'''
			
def p_DESICION1(p):
	'''DESICION : SI LPAR EXPRESION RPAR ENTONCES LBRA ESTATUTOS RBRA SINO LBRA ESTATUTOS RBRA'''
	
def p_DESICION2(p):
	'''DESICION : SI LPAR EXPRESION RPAR ENTONCES LBRA ESTATUTOS RBRA'''
				
def p_CONDICIONAL(p):
	'''CONDICIONAL : MIENTRAS LPAR EXPRESION RPAR HAZ LBRA ESTATUTOS RBRA'''
	
def p_NOCONDICIONAL(p):
	'''NOCONDICIONAL : DESDE LETRERO LCOR NUM_I RCOR EQUAL EXPRESION HASTA EXPRESION HACER LBRA ESTATUTOS RBRA'''
	
def p_LLAMADA(p): 
	'''LLAMADA : LETRERO LPAR OTRA RPAR SCO'''
	
def p_EXPRESION(p):
	'''EXPRESION : EXP SIM EXP 
				| EXP'''
				
def p_SIM(p):
	'''SIM : LT 
			| MT
			| NOTEQUAL
			| ELT
			| EMT
			| EEQ
			| AND
			| OR'''
			
def p_EXP(p):
	'''EXP : TERMINO PLUS TERMINO
			| TERMINO MINUS TERMINO
			| TERMINO'''

def p_TERMINO(p):
	'''TERMINO : FACTOR MULT FACTOR
				| FACTOR DIV FACTOR
				| FACTOR'''
				
def p_FACTOR(p):
	'''FACTOR : LETRERO LPAR EXP2 RPAR 
			| LETRERO LCOR EXP RCOR
			| LPAR EXP RPAR
			| CONSTANTE'''
			
def p_EXP2(p):
	'''EXP2 : EXP EXP2
			| COM EXP2 
			| empty'''
			
def p_CONSTANTE(p):
	'''CONSTANTE : NUM_I
				| NUM_F
				| CR'''

#Manejo de errores en el sintaxis
def p_error(p):
	if p == None:
		t = "EOF"
	else:
		t = f"{p.type}({p.value}) on line {p.lineno}"
	print(f"Syntax error: {t}")
	
parser = yacc.yacc()

with open(r'prueba.txt','r') as file:
	try:
		print("Parsing Complete")
		parser.parse(file.read())
	except:
		print("Error while reading the file")