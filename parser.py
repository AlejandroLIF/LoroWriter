import sys
import ply.yacc as yacc
from lexer import tokens
from procedureDirectory import procedureDirectory, Variable
from quadrupleGenerator import quadrupleGenerator
from semanticCube import getResultingType

currentDirectory = procedureDirectory("global")
functionDirectory = None
instructions = quadrupleGenerator()

variableStack = []
seenType = None
parameterCounter = 0 
Function_Or_Var_Name = None
functionCall = False

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
    '''functionDec  : type FUNCTION ID seen_function_id LPAREN params RPAREN vars seen_vars block END'''
    global currentDirectory        
    instructions.generateQuadruple("RETURN",0,0,0)
    currentDirectory = currentDirectory.parent
    #instructions.pushJumpStack(instructions.nextInstruction - 1)
    
def p_seen_vars(p):
    '''seen_vars    :'''
    global currentDirectory, instructions
    currentDirectory.startAddress = instructions.nextInstruction

def p_seen_function_id(p):
    '''seen_function_id :'''
    global currentDirectory
    functionID = p[-1]
    currentDirectory.add_directory(functionID)
    currentDirectory = currentDirectory.get_directory(functionID)
    currentDirectory.Type = seenType

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
    '''block    : LBRACE statements RBRACE'''

def p_statements(p):
    '''statements   : statement SEMICOLON statements
                    | empty'''

def p_statement(p):
    '''statement    : ID seen_id_assign_or_func assignOrFunccall
                    | instruction
                    | condition
                    | loop
                    | print
                    | return'''
    global functionCall
    functionCall = False
    
def p_return(p):
    '''return       : RETURN operand'''
    global currentDirectory, instructions
    var = instructions.popOperand()
    compatibleType = getResultingType("=", currentDirectory.Type, var.Type)
    
    if compatibleType:
        instructions.generateQuadruple("RETURN",var,0,0)
    else:
        print "ERROR: incompatible return types! Received {}, expected {}!".format(var.Type, currentDirectory.Type)
        raise SystemExit

def p_seen_id_assign_or_func(p):
    '''seen_id_assign_or_func : '''
    global Function_Or_Var_Name
    Function_Or_Var_Name = p[-1]
   
   
def p_assignOrFunccall(p):
    '''assignOrFunccall : assignment
                        | functionCall'''

def p_assignment(p):
    '''assignment   : EQU seen_EQU ssuperexp'''
    global instructions, currentDirectory
    
    op1 = instructions.popOperand()
    result = instructions.popOperand()
    operator = instructions.popOperator()
   
    validType = getResultingType(operator, result.Type, op1.Type)
    if validType:
        instructions.generateQuadruple(operator, op1, 0, result)
    else:
        print "ERROR: Invalid types! Variable \"{}\" cannot store \"{}\"!".format(currentDirectory.get_variable(result.Name), currentDirectory.get_variable(op1.Name))
        raise SystemExit

def p_seen_EQU(p):
    '''seen_EQU :'''
    global instructions, currentDirectory, Function_Or_Var_Name
    variable = currentDirectory.get_variable(Function_Or_Var_Name)

    if variable:
        instructions.pushOperand(variable)
        instructions.pushOperator(p[-1])
    else:
        print "ERROR: Variable \"{}\" undeclared!".format(Function_Or_Var_Name)
        raise SystemExit

def p_functionCall(p):
    '''functionCall : seen_func_id LPAREN args RPAREN'''
    global instruction, currentDirectory, functionDirectory, parameterCounter, functionCall
    if len(functionDirectory.parameters) == parameterCounter:
        instructions.generateQuadruple("CALL",0,0,functionDirectory.startAddress)
    else:
        print "ERROR: Function \"{}\" received {} arguments, expected {}!".format(functionDirectory.identifier, parameterCounter,len(functionDirectory.parameters))
        raise SystemExit
    functionCall = True
                
def p_seen_func_id(p):
    '''seen_func_id : '''
    global currentDirectory, functionDirectory, Function_Or_Var_Name, parameterCounter
    
    #Function call as an operator
    functionDirectory = currentDirectory.get_directory(p[-1])
    
    if not functionDirectory:
        #Function call as a statement
        functionDirectory = currentDirectory.get_directory(Function_Or_Var_Name)
    
    if not functionDirectory:
        #TODO: feedback line number
        print "ERROR: Undeclared function: \"{}\" in line #line number#".format(Function_Or_Var_Name)
        raise SystemExit
        
    parameterCounter = 0
    instructions.generateQuadruple("ERA", len(currentDirectory.variables), 0, 0);
    
def p_args(p):
    '''args     : arg
                | empty'''

def p_arg(p):
    '''arg      : exp seen_arg more_arg'''
    
def p_seen_arg(p):
    '''seen_arg : '''
    global instructions,currentDirectory,functionDirectory,parameterCounter
    op1 = instructions.popOperand()

    if parameterCounter < len(functionDirectory.parameters):
        nextParam = functionDirectory.parameters[parameterCounter]    
        variable = functionDirectory.get_variable(nextParam)
        compatibleType = getResultingType("=", variable.Type, op1.Type)
        if variable.Type is compatibleType:
            #TODO: find a more elegant solution for the + 7000 magic number
            instructions.generateQuadruple("=", op1, 0, Variable("Param{}".format(parameterCounter), variable.Type, parameterCounter + 7000))
        else:
            print "ERROR: Incompatible arguments. Received \"{}\", expected \"{}\"!".format(op1.Type,functionDirectory.get_variable(nextParam))
            raise SystemExit
    else:
        print "ERROR: Function \"{}\" received more arguments than expected!".format(functionDirectory.identifier)
        raise SystemExit
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
    operator = {'forward' : 'FWD', 'backward' : 'BWD', 'right' : 'RHT', 'left' : 'LFT'}[p[1]]
    instructions.pushOperator(operator)
    
def p_operand(p):
    '''operand  : INTEGER
                | FLOAT
                | STRING
                | ID id_or_func'''
    global instructions, currentDirectory
    
    op1 = None
    
    if type(p[1]) is str:
        if p[1][0] == "\"":
            op1 = currentDirectory.add_const(str, p[1])
    else:
        varType = type(p[1])
        op1 = currentDirectory.add_const(varType, p[1])
        
    if op1:
        instructions.pushOperand(op1)
    #else:
    #    print op1, p[1], "OPERAND ERROR"
    
def p_id_or_func(p):
    '''id_or_func   : functionCall
                    | empty'''
    global instructions
    if functionCall:
        variable = currentDirectory.get_directory(p[-1]).getReturnVariable()
    else:
        variable = currentDirectory.get_variable(p[-1])
    instructions.pushOperand(variable)
    
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
        instructions.pushOperand(op1)
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
        print "ERROR: Expected conditional, but found {}!".format(condition.Type)
        raise SystemExit

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
    #Begin loop condition evaluation

def p_seen_for_ssuperexp(p):
    '''seen_for_ssuperexp    :'''
    global instructions
    condition = instructions.popOperand()
    
    if condition.Type is bool:
        pendingJump = instructions.popJumpStack()
        instructions.generateQuadruple("GOTOF", condition, 0, 0)
        instructions.pushJumpStack(instructions.nextInstruction - 1)
        #Pending: exit jump address
        
        instructions.generateQuadruple("GOTO", 0, 0, 0)
        instructions.pushJumpStack(instructions.nextInstruction)
        instructions.pushJumpStack(instructions.nextInstruction - 1)
        #Pending: loop start jump address
        
        instructions.pushJumpStack(pendingJump)

    else:
        print "ERROR: Expected type: bool!"
        raise SystemExit
    
def p_seen_assignments2(p):
    '''seen_assignments2    :'''
    global instructions
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GOTO", 0, 0, pendingJump)
    #After assigning, jump to condition evaluation
    
    pendingJump = instructions.popJumpStack()
    instructions.setQuadrupleResult(pendingJump, instructions.nextInstruction)
    #Loop start jump address is right after assigning, where the loop header ends.

def p_seen_while_LPAREN(p):
    '''seen_while_LPAREN    :'''
    global instructions
    instructions.pushJumpStack(instructions.nextInstruction)

def p_seen_while_ssuperexp(p):
    '''seen_while_ssuperexp :'''
    global instructions
    condition = instructions.popOperand()
    
    if condition.Type is not bool:
        print "ERROR: Expected type: bool!"
        raise SystemExit
    
    pendingJump = instructions.popJumpStack()
    instructions.generateQuadruple("GOTOF", condition, 0, 0)
    instructions.pushJumpStack(instructions.nextInstruction - 1)
    instructions.pushJumpStack(pendingJump)

def p_assignments(p):
    '''assignments  : ID seen_id_assign_or_func assignment more_assignments'''

def p_more_assignments(p):
    '''more_assignments : COMMA assignments
                        | empty'''

def p_print(p):
    '''print    : PRINT LPAREN printables RPAREN'''

def p_printables(p):
    '''printables   : printable more_printables'''

def p_printable(p):
    '''printable    : ssuperexp'''
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
            print "ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name)
            raise SystemExit
    
        result = currentDirectory.add_temp(resultingType)
        
        if result:
            instructions.generateQuadruple(operator, op1, op2, result)
            instructions.pushOperand(result)
        else:
            print "SUPEREXP ERROR"
    
    
def p_compareto(p):
    '''compareto    : comparator exp seen_comparison
                    | empty'''

def p_seen_comparison(p):
    '''seen_comparison     :'''
    global instructions
    op2 = instructions.popOperand()
    op1 = instructions.popOperand()
    operator = instructions.popOperator()
    
    resultingType = getResultingType(operator, op1.Type, op2.Type)
    if resultingType is None:
        print "ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name)
        raise SystemExit
    
    result = currentDirectory.add_temp(resultingType)
        
    if result:
        instructions.generateQuadruple(operator, op1, op2, result)
        instructions.pushOperand(result)
    else:
        print "SEEN_COMPARISON ERROR"    

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
            print "ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name)
            raise SystemExit
        
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
            print "ERROR: Operation {} {} {} has incompatible types".format(op1.Name, operator, op2.Name)
            raise SystemExit
        
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
    instructions.popOperator()

def p_empty(p):
    'empty :'
    pass


#   TODO:
#def p_error(p):
#    '''error    :'''
#    global instructions, currentDirectory
#    #print currentDirectory
#    #print instructions

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

