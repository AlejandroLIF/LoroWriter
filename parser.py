import sys
import ply.yacc as yacc
from lexer import tokens
from procedureDirectory import procedureDirectory
from quadrupleGenerator import quadrupleGenerator
from semanticCube import getResultingType

currentDirectory = procedureDirectory("global")
functionDirectory = None
instructions = quadrupleGenerator()

variableStack = []
seenType = None
parameterCounter = 0 
FuncVarName = None

precedence =    (
                ('left', 'AND', 'OR'),
                ('left', 'PLUS', 'MINUS'),
                ('left', 'MUL', 'DIV')
                )

start = 'program'

def p_program(p):
    '''program  : PROGRAM ID vars functionDecs seen_main block END'''

def p_seen_main(p):
    '''seen_main : '''
    global instructions    
    while len(instructions.jumpStack) is not 0:
        pendingJump = instructions.popJumpStack()
        instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction) 

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
    instructions.generateQuadruple("GOTO",0,0,0)
    instructions.pushJumpStack(instructions.nextInstruction - 1)
    
def p_seen_function_id(p):
    '''seen_function_id :'''
    global currentDirectory
    functionID = p[-1]
    currentDirectory.add_directory(functionID)
    currentDirectory = currentDirectory.get_directory(functionID)

def p_params(p):
    '''params   : param
                | empty'''

def p_param(p):
    '''param    : type ID seen_param more_param'''    

def p_seen_param(p):
    '''seen_param   :'''
    global currentDirectory
    variableID = p[-1]
    currentDirectory.parameters.append(variableID)
    currentDirectory.add_variable(variableID, seenType)

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
    '''block    : LBRACE seen_address statements RBRACE'''

def p_seen_address(p):
    '''seen_address : '''
    global currentDirectory, instructions
    currentDirectory.startAddress = instructions.nextInstruction

def p_statements(p):
    '''statements   : statement SEMICOLON statements
                    | empty'''

def p_statement(p):
    '''statement    : ID seen_id_ass_or_fun assignOrFunccall
                    | instruction
                    | condition
                    | loop
                    | print'''

def p_seen_id_ass_or_fun(p):
    '''seen_id_ass_or_fun : '''
    global FuncVarName
    FuncVarName = p[-1]
   
def p_assignOrFunccall(p):
    '''assignOrFunccall : assignment
                        | functionCall'''

def p_assignment(p):
    '''assignment   : EQU seen_EQU ssuperexp'''
    global instructions, currentDirectory
    op1 = instructions.popOperand()
    result = instructions.popOperand()
    operator = instructions.popOperator()
        
    if result.Type is op1.Type:
        instructions.generateQuadruple(operator, op1, 0, result)
    else:
        raise TypeError("Cannot store {} in variable {}".format(currentDirectory.get_variable(op1.Name), currentDirectory.get_variable(result.Name)))

def p_seen_EQU(p):
    '''seen_EQU :'''
    global instructions, currentDirectory, FuncVarName
    variable = currentDirectory.get_variable(FuncVarName)

    if variable:
        instructions.pushOperand(variable)
        instructions.pushOperator(p[-1])
    else:
        p_error(p)
        #WARNING: Change error type
        raise TypeError("Variable \"{}\" undeclared!".format(FuncVarName))

def p_functionCall(p):
    '''functionCall : LPAREN seen_func_id args RPAREN'''
    global instruction, currentDirectory, functionDirectory, parameterCounter
    if len(functionDirectory.parameters) == parameterCounter:
        instructions.generateQuadruple("GOTO",0,0,functionDirectory.startAddress)
    else:
        #WARNING: Wrong number of arguments error
        raise TypeError("Sent {} arguments, expected {}".format(parameterCounter,functionDirectory.parameters.len()))
                
def p_seen_func_id(p):
    '''seen_func_id : '''
    global currentDirectory, functionDirectory, FuncVarName, parameterCounter
    functionDirectory = currentDirectory.get_directory(FuncVarName)
    parameterCounter = 0

    if not functionDirectory:
        raise TypeError("Undeclared function")

def p_args(p):
    '''args     : arg
                | empty'''

def p_arg(p):
    '''arg      : operand seen_operand more_arg'''
    
def p_seen_operand(p):
    '''seen_operand : '''
    global instructions,currentDirectory,functionDirectory,parameterCounter
    op1 = instructions.popOperand()
    nextParam = functionDirectory.parameters[parameterCounter]

    if parameterCounter <= len(functionDirectory.parameters):
        if functionDirectory.get_variable(nextParam).Type is op1.Type:
            instructions.generateQuadruple("=",op1,0,functionDirectory.get_variable(nextParam))
        else:
            raise TypeError("Incompatible types. Is {}, expected {}".format(op1.Type,functionDirectory.get_variable(nextParam)))
    else:
        raise TypeError("Sent more arguments than expected")
    parameterCounter += 1
    
def p_more_arg(p):
    '''more_arg : COMMA arg
                | empty'''

def p_instruction(p):
    '''instruction  : movementi
                    | drawi
                    | pressurei
                    | colori
                    | arci
                    | circlei
                    | squarei'''
                    
def p_movementi(p):
    '''movementi    : movement integer'''
    global instructions
    op1 = instructions.popOperand()
    operator = instructions.popOperator()
    instructions.generateQuadruple(operator, op1, 0, 0)
        
def p_drawi(p):
    '''drawi        : DRAW boolean'''
    global instructions
    #NOTE:  special scenario because boolean is a keyword and not the result of logic evaluation
    #       in this case, op1 comes from the operators.  
    op1 = instructions.popOperator()
    instructions.generateQuadruple('D', op1, 0, 0)
    
def p_pressurei(p):
    '''pressurei    : PRESSURE integer'''
    global instructions
    op1 = instructions.popOperand()
    instructions.generateQuadruple('P', op1, 0, 0)

def p_colori(p):
    '''colori       : COLOR colorConstant'''
    global instructions
    #NOTE:  special scenario because colorConstant is a keyword. In this case,
    #       op1 comes from the operators.
    op1 = instructions.popOperator()
    instructions.generateQuadruple('C', op1, 0, 0)

def p_arci(p):
    '''arci         : ARC integer integer'''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()
    instructions.generateQuadruple('A', op1, op2, 0)

def p_circlei(p):
    '''circlei      : CIRCLE integer'''
    global instructions
    op1 = instructions.popOperand()
    instructions.generateQuadruple('O', op1, 0, 0)

def p_squarei(p):
    '''squarei      : SQUARE integer integer'''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()
    instructions.generateQuadruple('S', op1, op2, 0)

def p_movement(p):
    '''movement : FORWARD
                | BACKWARD
                | RIGHT
                | LEFT'''
    global instructions
    operator = {'FORWARD' : 'F', 'BACKWARD' : 'B', 'RIGHT' : 'R', 'LEFT' : 'L'}[p[1]]
    instructions.pushOperator(operator)
    
def p_operand(p):
    '''operand  : INTEGER
                | FLOAT
                | STRING
                | ID'''
    global instructions, currentDirectory
    if type(p[1]) is str:
        if p[1][0] != "\"":
            op1 = currentDirectory.get_variable(p[1])
        else:
            varType = type(p[1])
            op1 = currentDirectory.add_const(varType, p[1])    
    else:
        varType = type(p[1])
        op1 = currentDirectory.add_const(varType, p[1])

    if op1:    
        instructions.pushOperand(op1)
    else:
        print op1, p[1], "OPERAND ERROR"
    
def p_boolean(p):
    '''boolean  : TRUE
                | FALSE'''
    global instructions
    #NOTE:  boolean is a keyword and not the result of logic evaluation; it is an operator
    instructions.pushOperator(p[1])

def p_integer(p):
    '''integer  : ID
                | INTEGER'''
    global instructions, currentDirectory
    if type(p[1]) is str:
        op1 = currentDirectory.getVariable(p[1])
    else:
        op1 = currentDirectory.add_const(int, p[1])
    
    if op1:
        instructions.pushOperand(op)
    else:
        print "INTEGER ERROR"

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
    global instructions
    #NOTE:  colorConstant is a keyword and not the result of logic evaluation; it is an operator
    instructions.pushOperator(p[1])

def p_condition(p):
    '''condition    : IF LPAREN ssuperexp RPAREN seen_condition block seen_condition_block else END'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)

def p_seen_condition(p):
    '''seen_condition   :'''
    global instructions
    condition = instructions.popOperand()
    
    if condition.Type is bool:
        instructions.generateQuadruple("GOTOF", condition, 0, 0)
        instructions.pushJumpStack(instructions.nextInstruction - 1)
    else:
        p_error(p)
        print condition
        raise TypeError("Expected type: bool")

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
    '''seen_for_ssuperexp    :'''
    global instructions
    condition = instructions.popOperandStack()
    
    if condition.Type is not bool:
        p_error(p)
        raise TypeError("Expected type: bool")
    
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
    
    if condition.Type is not bool:
        p_error(p)
        raise TypeError("Expected type: bool")
    
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

#TODO: This has not been verified
def p_printable(p):
    '''printable    : ssuperexp
                    | STRING'''
    global instructions
    op1 = instructions.popOperand()
    instructions.generateQuadruple('PRINT', op1, 0, 0);

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
    instructions.pushOperator(p[1])

def p_superexp(p):
    '''superexp   : exp compareto'''
    global instructions, currentDirectory
    if instructions.topOperatorEquals('&&') or instructions.topOperatorEquals('||') :
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()
        
        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            p_error(p)
            raise TypeError("Type operation {} {} {} is incompatible".format(op1.Name, operator, op2.Name))
    
        result = currentDirectory.add_temp(resultingType)
        
        if result:
            instructions.generateQuadruple(operator, op1, op2, result)
            instructions.pushOperand(result)
        else:
            print "SUPEREXP ERROR"
    
    
def p_compareto(p):
    '''compareto    : comparator exp seen_exp
                    | empty'''

def p_seen_exp(p):
    '''seen_exp :'''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()
    operator = instructions.popOperator()
    
    resultingType = getResultingType(operator, op1.Type, op2.Type)
    if resultingType is None:
        p_error(p)
        raise TypeError("Type operation {} {} {} is incompatible".format(op1.Name, operator, op2.Name))
    
    result = currentDirectory.add_temp(resultingType)
        
    if result:
        instructions.generateQuadruple(operator, op1, op2, result)
        instructions.pushOperand(result)
    else:
        print "SEEN_EXP ERROR"    

def p_comparator(p):
    '''comparator   : CEQ
                    | CGT 
                    | CGE
                    | CLT
                    | CLE
                    | CNE'''
    global instructions
    instructions.pushOperator(p[1])

def p_exp(p):
    '''exp      : term seen_term exp2'''

def p_seen_term(p):
    '''seen_term    :'''
    global instructions
    if instructions.topOperatorEquals('+') or instructions.topOperatorEquals('-'):
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()
        
        resultingType = getResultingType(operator, op1.Type, op2.Type)
        if resultingType is None:
            p_error(p)
            raise TypeError("Type operation {} {} {} is incompatible".format(op1.Name, operator, op2.Name))
        
        result = currentDirectory.add_temp(resultingType)
        
        if result:    
            instructions.generateQuadruple(operator, op1, op2, result)
            instructions.pushOperand(result)
        else:
            print "SEEN_TERM ERROR"        

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
    instructions.pushOperator(p[1])

def p_factor(p):
    '''factor   : LPAREN seen_LPAREN ssuperexp RPAREN seen_RPAREN
                | operand'''
    global instructions
    if instructions.topOperatorEquals('*') or instructions.topOperatorEquals('/'):
        op2 = instructions.popOperand()
        op1 = instructions.popOperand()
        operator = instructions.popOperator()
        
        resultingType = getResultingType(operator, op1.Type, op2.Type)

        if resultingType is None:
            p_error(p)
            raise TypeError("Type operation {} {} {} is incompatible".format(op1.Name, operator, op2.Name))
        
        result = currentDirectory.add_temp(resultingType)
        
        if result:    
            instructions.generateQuadruple(operator, op1, op2, result)
            instructions.pushOperand(result)
        else:
            print "FACTOR ERROR"

def p_seen_LPAREN(p):
    '''seen_LPAREN  :'''
    global instructions
    instructions.pushOperator(p[-1])
    
def p_seen_RPAREN(p):
    '''seen_RPAREN  :'''
    global instructions
    instructions.popOperand()

def p_empty(p):
    'empty :'
    pass

#   TODO
def p_error(p):
    '''error    :'''
    global instructions, currentDirectory
    print currentDirectory
    print instructions

#Test routine
if __name__ == '__main__':
    if len(sys.argv) == 2:
        f = open(sys.argv[1], 'r')
        s = f.read()
        parser = yacc.yacc()
        parser.parse(s);
        #print currentDirectory
        print instructions
    else:
        print "Usage syntax: %s filename" %sys.argv[0]

