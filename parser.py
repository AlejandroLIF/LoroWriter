import ply.yacc as yacc
from lexer import tokens

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'MUL', 'DIV')
)

start = 'program'

def p_program(p):
	'''program	: PROGRAM ID program2'''
	
def p_program2(p):
	'''program2	: vars function block END
			| empty	'''

def p_function(p):
	'''function	: FUNCTION ID LPAREN parameters RPAREN vars block END
			| empty'''
def p_vars(p):
	'''vars		: VAR id1 
			| empty '''
def p_id1(p): 	
	'''id1		: ID id2 COLON type SEMICOLON id3'''
def p_id2(p):	
	'''id2		: COMMA ID id2
			| '''
def p_id3(p):	
	'''id3		: id1
			| '''
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
	'''statement	: ID paraass
			| instruction
			| condition
			| loop
			| print'''
			
def p_paraass(p):
	'''paraass	: LPAREN parameters RPAREN
			| assignment'''
			
def p_assignment(p):
	'''assignment	: CEQ expression SEMICOLON'''
	
def p_parameters(p):
	'''parameters	: type ID parameters2'''
	
def p_parameters2(p):
	'''parameters2	: COMMA parameters
			| empty'''
def p_condition(p):
	'''condition	: IF LPAREN expression RPAREN block cond2 SEMICOLON'''
	
def p_cond2(p):
	'''cond2	: ELSE block
			| empty '''
def p_instruction(p):
	'''instruction	: movement number
			| DRAW boolean
			| PRESSURE integer
			| COLOR colorconstant'''
def p_movement(p):
	'''movement	: FORWARD
			| BACKWARD
			| RIGHT
			| LEFT'''
def p_number(p):
	'''number	: integer
			| FLOAT'''
			
def p_boolean(p):
	'''boolean	: TRUE
			| FALSE'''

def p_integer(p):
	'''integer	: ID
			| INTEGER'''
			
def p_colorconstant(p):
	'''colorconstant: RED
			| GREEN
			| BLUE
			| BLACK'''

def p_loop(p):
	'''loop		: loophead block END SEMICOLON'''
	
def p_loophead(p):
	'''loophead	: FOR LPAREN assignments SEMICOLON expression SEMICOLON ASSIGNMENTS RPAREN
			| WHILE LPAREN expression RPAREN'''
			
def p_assignments(p):
	'''assignments	: assignment assignments2'''
	
def p_assignments2(p):
	'''assignments2 : COMMA assignments
			| empty'''
			
def p_print(p):
	'''print	: PRINT LPAREN printables RPAREN SEMICOLON'''
	
def p_printables(p):
	'''printables	: printable printable2'''
	
def p_printable2(p):
	'''printable2	: COMMA printables
			| empty'''
			
def p_printable(p):
	'''printable	: expression
			| STRING'''
			
def p_expression(p):
	'''expression	: exp expression2'''
	
def p_expression2(p):
	'''expression2	: comparator exp
			| empty'''
			
def p_comparator(p):
	'''comparator	: EQU
			| CGT 
			| CGE
			| CLT
			| CLE
			| CNE
			| AND
			| OR'''
			
def p_exp(p):
	'''exp		: term term2'''
	
def p_term2(p):
	'''term2	: sumsub exp
			| empty'''
			
def p_sumsub(p):
	'''sumsub	: PLUS
			| MINUS'''
			
def p_term(p):
	'''term		: factor term2'''
	
def p_term2(p):
	'''term2	: muldiv term'''
	
def p_muldiv(p):
	'''muldiv	: MUL
			| DIV'''
			
def p_factor(p):
	'''factor	: LPAREN expression RPAREN
			| number
			| sumsub number'''
			
def p_empty(p):
	'empty :'
	pass
