import sys
import ply.yacc as yacc
from lexer import tokens
from procedureDirectory import procedureDirectory
from quadrupleGenerator import quadrupleGenerator

currentDirectory = procedureDirectory("global")
instructions = quadrupleGenerator()

variableStack = []
seenType = None

precedence =    (
                ('left', 'AND', 'OR'),
                ('left', 'PLUS', 'MINUS'),
                ('left', 'MUL', 'DIV')
                )

start = 'program'

def p_program(p):
    '''program  : PROGRAM ID vars functionDecs block END'''

def p_vars(p):
    '''vars     : VAR var 
                | empty '''

def p_var(p):
    '''var      : ids COLON type seen_type SEMICOLON more_var'''
    
def p_seen_type(p):
    '''seen_type :'''
    global currentDirectory
    while variableStack:
        currentDirectory.add_variable(variableStack.pop(), seenType)

def p_more_var(p):
    '''more_var : var
                | empty'''

def p_functionDecs(p):
    '''functionDecs : functionDec functionDecs
                    | empty'''


def p_functionDec(p):
    '''functionDec  : FUNCTION ID seen_function_id LPAREN params RPAREN vars block END'''
    global currentDirectory
    currentDirectory = currentDirectory.parent
    
def p_seen_function_id(p):
    '''seen_function_id :'''
    global currentDirectory
    currentDirectory.add_directory(p[-1])
    currentDirectory = currentDirectory.get_directory(p[-1])

def p_params(p):
    '''params   : param
                | empty'''

def p_param(p):
    '''param    : type ID seen_param more_param'''    

def p_seen_param(p):
    '''seen_param   :'''
    global currentDirectory
    currentDirectory.add_variable(p[-1], seenType)

def p_more_param(p):
    '''more_param   : COMMA param
                    | empty'''

def p_ids(p):
    '''ids      : ID seen_ID more_ids '''

def p_seen_ID(p):
    '''seen_ID  :'''
    global variableStack
    variableStack.append(p[-1])

def p_more_ids(p):
    '''more_ids : COMMA ids
                | empty'''

def p_type(p):
    '''type     : INT
                | FLO
                | STR'''
    global seenType
    variableTypes = { 'int' : int, 'float' : float, 'string' : str }
    seenType = variableTypes[p[1]]

def p_block(p):
    '''block    : LBRACE statements RBRACE'''

def p_statements(p):
    '''statements   : statement SEMICOLON statements
                    | empty'''

def p_statement(p):
    '''statement    : ID seen_id_statement assignOrFunccall
                    | instruction
                    | condition
                    | loop
                    | print'''
                    
def p_seen_id_statement(p):
    '''seen_id_statement    :'''
    global curentDirectory, instructions
    variable = currentDirectory.get_variable(p[-1])
    instructions.pushOperand(variable)

def p_assignOrFunccall(p):
    '''assignOrFunccall : assignment
                        | functionCall'''

#Warning: there is currently no way to assign a string value to a variable.
def p_assignment(p):
    '''assignment   : EQU seen_EQU ssuperexp'''

def p_seen_EQU(p):
    '''seen_EQU :'''
    global instructions
    instructions.pushOperator(p[-1])

def p_functionCall(p):
    '''functionCall : LPAREN args RPAREN'''

def p_args(p):
    '''args     : arg
                | empty'''

def p_arg(p):
    '''arg      : number more_arg'''

def p_more_arg(p):
    '''more_arg : COMMA arg
                | empty'''

def p_instruction(p):
    '''instruction  : movement number
                    | DRAW boolean
                    | PRESSURE integer
                    | COLOR colorConstant
                    | ARC integer integer
                    | CIRCLE integer
                    | SQUARE integer integer'''

def p_movement(p):
    '''movement : FORWARD
                | BACKWARD
                | RIGHT
                | LEFT'''

def p_number(p):
    '''number   : integer
                | FLOAT'''

def p_boolean(p):
    '''boolean  : TRUE
                | FALSE'''

def p_integer(p):
    '''integer  : ID
                | INTEGER'''

def p_colorConstant(p):
    '''colorConstant    : RED
                        | ORANGE
                        | YELLOW
                        | GREEN
                        | BLUE
                        | CYAN
                        | PURPLE
                        | WHITE
                        | BLACK'''

def p_condition(p):
    '''condition    : IF LPAREN ssuperexp RPAREN seen_condition block seen_condition_block else END'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

def p_seen_condition(p):
    '''seen_condition   :'''
    global instructions
    condition = instructions.PopOperand()
    #TEST IF type(condition) == bool
    instructions.generateQuadruple("GOTOF", condition, 0, 0)
    instructions.pushJumpStack(instructions.nextInstruction - 1)

def p_seen_condition_block(p):
    '''seen_condition_block :'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GOTO", 0, 0, 0)
    instructions.pushJumpStack(instructions.nextInstruction -1)
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

def p_else(p):
    '''else     : ELSE block
                | empty '''
    
def p_loop(p):
    '''loop     : loophead block seen_loop_block END'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)
    
    
def p_seen_loop_block(p):
    '''seen_loop_block  :'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GOTO", 0, 0, pendingJump)

def p_loophead(p):
    '''loophead : FOR LPAREN assignments seen_assignments1 SEMICOLON ssuperexp seen_for_ssuperexp SEMICOLON assignments seen_assignments2 RPAREN
                | WHILE LPAREN seen_while_LPAREN ssuperexp seen_while_ssuperexp RPAREN'''

def p_seen_assignments1(p):
    '''seen_assignments1    :'''
    global instructions
    instructions.pushJumpStack(instructions.nextInstruction)

def p_seen_for_ssuperexp(p):
    '''seen_for_ssuperexp(p):'''
    global instructions
    condition = instructions.popOperandStack()
    #TEST IF type(condition) == bool
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GOTOF", condition, 0, 0)
    instructions.pushJumpStack(instructions.nextInstruction - 1)
    instructions.pushJumpStack(instructions.nextInstruction + 1)
    instructions.generateQuadruple("GOTO", 0, 0, 0)
    instructions.pushJumpStack(instructions.nextInstruction - 1)
    instructions.pushJumpStack(pendingJump)

def p_seen_assignments2(p):
    '''seen_assignments2    :'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GOTO", 0, 0, pendingJump)
    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

def p_seen_while_LPAREN(p):
    '''seen_while_LPAREN    :'''
    global instructions
    instructions.pushJumpStack(instructions.nextInstruction)

def p_seen_while_ssuperexp(p):
    '''seen_while_ssuperexp :'''
    global instructions
    condition = instructions.popOperandStack()
    #TEST IF type(condition) == bool
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GOTOF", 0, 0, 0)
    instructions.pushJumpStack(instructions.nextInstruction - 1)
    instructions.pushJumpStack(pendingJump)

def p_assignments(p):
    '''assignments  : ID assignment more_assignments'''

def p_more_assignments(p):
    '''more_assignments : COMMA assignments
                        | empty'''

def p_print(p):
    '''print    : PRINT LPAREN printables RPAREN'''

def p_printables(p):
    '''printables   : printable more_printables'''

#Possible error detected: printing a "string variable"?
def p_printable(p):
    '''printable    : ssuperexp
                    | STRING'''

def p_more_printables(p):
    '''more_printables  : COMMA printables
                        | empty'''

def p_ssuperexp(p):
    '''ssuperexp    : superexp ssuperexp2'''

def p_ssuperexp2(p):
    '''ssuperexp2   : andor ssuperexp
                    | empty'''
                    
def p_andor(p):
    '''andor        : AND
                    | OR'''
    global instructions
    instructions.pushOperator(p[-1])

def p_superexp(p):
    '''superexp   : exp compareto'''
    global instructions
    if instructions.topOperatorEquals('&&') or instructions.topOperatorEquals('||') :
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()
        result = "TEMPORARY" #ADD TEMPORARY VARIABLE HERE
        instructions.generateQuadruple(operator, op1, op2, result)
        instructions.pushOperand(result)
    
    
def p_compareto(p):
    '''compareto    : comparator exp seen_exp
                    | empty'''

def p_seen_exp(p):
    '''seen_exp :'''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()
    operator = instructions.popOperator()
    result = "TEPMORARY" #ADD TEMPORARY VARIABLE HERE
    instructions.generateQuadruple(operator, op1, op2, result)
    instructions.pushOperand(result)

def p_comparator(p):
    '''comparator   : CEQ
                    | CGT 
                    | CGE
                    | CLT
                    | CLE
                    | CNE'''
    global instructions
    instructions.pushOperator(p[-1])

def p_exp(p):
    '''exp      : term seen_term exp2'''

def p_seen_term(p):
    '''seen_term    :'''
    global instructions
    if instructions.topOperatorEquals('+') or instructions.topOperatorEquals('-'):
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()
        result = "TEPMORARY" #ADD TEMPORARY VARIABLE HERE
        instructions.generateQuadruple(operator, op1, op2, result)
        instructions.pushOperand(result)

def p_exp2(p):
    '''exp2     : sumsub exp
                | empty'''

def p_sumsub(p):
    '''sumsub   : PLUS
                | MINUS'''
    global instructions
    instructions.pushOperator(p[1])

def p_term(p):
    '''term     : factor term2'''

def p_term2(p):
    '''term2    : muldiv term
                | empty'''

def p_muldiv(p):
    '''muldiv   : MUL
                | DIV'''
    global instructions
    instructions.pushOperator(p[-1])

def p_factor(p):
    '''factor   : LPAREN seen_LPAREN ssuperexp RPAREN seen_RPAREN
                | number seen_number'''
    global instructions
    if instructions.topOperatorEquals('*') or instructions.topOperatorEquals('/'):
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()
        result = "TEPMORARY" #ADD TEMPORARY VARIABLE HERE
        instructions.generateQuadruple(operator, op1, op2, result)
        instructions.pushOperand(result)

def p_seen_LPAREN(p):
    '''seen_LPAREN  :'''
    global instructions
    instructions.pushOperand(p[-1])
    
def p_seen_RPAREN(p):
    '''seen_RPAREN  :'''
    global instructions
    instructions.popOperand()

def seen_number(p):
    '''seen_number  :'''
    global instructions
    instructions.pushOperand(p[-1])

def p_empty(p):
    'empty :'
    pass

#Test routine
if __name__ == '__main__':
    if len(sys.argv) == 2:
        f = open(sys.argv[1], 'r')
        s = f.read()
        parser = yacc.yacc()
        parser.parse(s);
    else:
        print "Usage syntax: %s filename" %sys.argv[0]

