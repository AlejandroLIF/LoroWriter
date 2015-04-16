from procedureDirectory import Variable

#Begin class quadruple
class quadruple:
    def __init__(self, operator='', op1='', op2='', result=''):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.result = result
        
    def __str__(self):
        return str(self.operator) + '\t' + str(self.op1.Name) + '\t' + str(self.op2.Name) + \
                '\t' + str(self.result.Name)
#End class quadruple

#Begin class quadrupleGenerator
class quadrupleGenerator:
    def __init__(self):
        self.quadruples = []
        self.jumpStack = []
        self.operatorStack = []
        self.operandStack = []
        self.nextInstruction = 0
    
    def __str__(self):
        string = 'quadruples:\n'
        
        for index, quadruple in enumerate(self.quadruples):
            string += '\t{} {}\n'.format(str(index), str(quadruple))
            
        string += 'operatorStack:\n{}\n'.format(str(self.operatorStack))
        
        string += 'operandStack:\n[\n'
        for operand in self.operandStack:
            string += '{}\n'.format(operand)
        string += ']\n'
            
        string += 'jumpStack:\n{}\n'.format(str(self.jumpStack))
        return string
    
    def pushJumpStack(self, index):
        self.jumpStack.append(index)
        
    def popJumpStack(self):
        return self.jumpStack.pop()
        
    def pushOperand(self, operand):
        self.operandStack.append(operand)
        
    def popOperand(self):
        return self.operandStack.pop()
        
    def pushOperator(self, operator):
        self.operatorStack.append(operator)
        
    def popOperator(self):
        return self.operatorStack.pop()
    
    #TODO:  warning - verify that the program operates correctly when operatorStack is empty
    def topOperatorEquals(self, operator):
        index = len(self.operatorStack) - 1
        if index >= 0:
            return self.operatorStack[index] == operator
        else:
            return False
            
    #   If an integer is passed as op1, op2 or result, it is converted into a Variable type
    #TODO: properly assign a variable address to this Variable.
    def generateQuadruple(self, operator='', op1='', op2='', result=''):
        if type(op1) is int:
            op1 = Variable(str(op1))
        if type(op2) is int:
            op2 = Variable(str(op2))
        if type(result) is int:
            result = Variable(str(result))
        self.quadruples.append(quadruple(operator, op1, op2, result))
        self.nextInstruction += 1
       
    #   If an integer is passed as result, it is converted into a Variable type
    #TODO: properly assign a variable address to this Variable.
    def setQuadrupleResult(self, index, result):
        if type(result) is int:
            result = Variable(str(result))
        self.quadruples[index].result = result
#End class quadrupleGenerator

#Test routine
if __name__ == '__main__':
    instructions = quadrupleGenerator()
    instructions.generateQuadruple('+', 'A', 'B', 'T1')
    instructions.generateQuadruple('*', 'C', 'T1', 'T2')
    instructions.generateQuadruple('-', 'X', 'T2', 'T3')
    print instructions
