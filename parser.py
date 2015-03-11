import ply.yacc as yacc
from lexer import tokens

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'MUL', 'DIV')
)

start = 'program'

def p_program(p):
	'''program	: PROGRAM ID vars function block END'''

def p_function(p):
	'''function	: FUNCTION ID vars block END
			| empty'''
def p_vars(p):
	'''vars		: VAR ids
			| empty'''
def p_ids(p): 	#Problem detected: Left association.
	'''ids		: id COLON type SEMICOLON
			| id COLON type SEMICOLON ids'''
def p_id(p):	#Problem detected: Left association.
	'''id		: ID
			| ID COMMA id'''

def p_type(p):
	'''type		: INT
			| FLO
			| STR'''

def p_block(p):
	'''block	: LBRACKET statements RBRACKET'''
	
def p_statements(p):
	'''statements	: empty
			| statement statements'''
	
def p_statement(p):
	'''statement	: assignment
			| ID
			| instruction
			| condition
			| loop
			| print'''
def p_assignment(p):
	'''assignment	: ID EQU expression SEMICOLON'''
	


def p_empty(p):
	'empty :'
	pass
