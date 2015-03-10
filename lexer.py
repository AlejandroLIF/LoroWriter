import ply.lex as lex

reserved = {
	'program'	: 'PROGRAM',
	'var'		: 'VAR',
	'if'		: 'IF',
	'else'		: 'ELSE',
	'while'		: 'WHILE',
	'for'		: 'FOR',
	'function'	: 'FUNCTION',
	'end'		: 'END',
	'print'		: 'PRINT',
	'forward'	: 'FORWARD',
	'backward'	: 'BACKWARD',
	'right'		: 'RIGHT',
	'left'		: 'LEFT',
	'color'		: 'COLOR',
	'draw'		: 'DRAW',
	'pressure'	: 'PRESSURE',
	'true'		: 'TRUE',
	'false'		: 'FALSE'
}

tokens = [	'COMMA', 'SEMICOLON', 'COLON', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LBRACE',
		'RBRACE', 'LPAREN', 'RPAREN', 'CEQ', 'CNE', 'CLT', 'CGT', 'CLE', 'CGE',
		'STRING', 'ID', 'FLOAT', 'INTEGER' ] + list(reserved.values())
		
t_ignore = ' \t\r'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_CEQ = r'\='
t_CNE = r'\<\>'
t_CLT = r'\>'
t_CGT = r'\<'
t_CLE = r'\<\='
t_CGE = r'\>\='
t_STRING = r'\"[a-zA-z0-9 ]*\"'

def t_ID(t):
	r'[a-zA-Z0-9_]+'
	t.value = str(t.value)
	t.type = reserved.get(t.value, 'ID')
	return t


def t_FLOAT(t):
	r'[0-9]+\.[0-9]+'
	t.value = float(t.value)
	return t

def t_INTEGER(t):
	r'[0-9]+'
	t.value = int(t.value)
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)
	
lex.lex() #Build the lexer
