#Begin class quadruple
class quadruple:
    def __init__(self, operator="", op1="", op2="", result=""):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.result = result
        
    def __str__(self):
        return str(self.operator) + '\t' + str(self.op1) + '\t' + str(self.op2) + \
                '\t' + str(self.result)
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
        string = "quadruples:\n"
        
        for index, quadruple in enumerate(self.quadruples):
            string += "\t{} {}\n".format(str(index), str(quadruple))
            
        string += "operatorStack:\n{}\n".format(str(self.operatorStack))
        string += "operandStack:\n{}\n".format(str(self.operandStack))
        string += "jumpStack:\n{}\n".format(str(self.jumpStack))
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
    
    def topOperatorEquals(self, operator):
        return self.operatorStack[len(self.operatorStack)] == operator
        
    def generateQuadruple(self, operator="", op1="", op2="", result=""):
        self.quadruples.append(quadruple(operator, op1, op2, result))
        self.nextInstruction += 1
        
    def setQuadrupleResult(self, index, result):
        self.quadruples[index].result = result
#End class quadrupleGenerator

#Test routine
if __name__ == '__main__':
    instructions = quadrupleGenerator()
    instructions.generateQuadruple("+", "A", "B", "T1")
    instructions.generateQuadruple("*", "C", "T1", "T2")
    instructions.generateQuadruple("-", "X", "T2", "T3")
    print instructions
