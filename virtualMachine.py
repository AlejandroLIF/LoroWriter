import sys
import shlex
from turtle import *

#Writer = Screen()
#Writer.setup(400,200)
loro = Turtle()
loro.pendown() 

instructionMemory = []
jumpStack = []
stackPointer = 0
segmentLength = 4500
returnStack = []



dataMemory = range(0,4050700)
PC = 0

passingParameters = False

#   BEGIN ASSIGNMENT
def EQU(op1, op2, result):
    dataMemory[result] = op1
#   END ASSIGNMENT

#   BEGIN ARITHMETIC OPERATIONS
def ADD(op1, op2, result):
    try:
        dataMemory[result] = op1 + op2
    except:
        try:
            dataMemory[result] = str(op1) + str(op2)
        except:
            raise TypeError("Operation invalid for specified operand types")

def SUB(op1, op2, result):
    try:
        dataMemory[result] = op1 - op2
    except:
        raise TypeError("Operation invalid for specified operand types")

def MUL(op1, op2, result):
    try:
        dataMemory[result] = op1 * op2
    except:
        raise TypeError("Operation invalid for specified operand types")

def DIV(op1, op2, result):
    if op2 == 0:
        raise ValueError("Attempting to divide by 0")
    else:
        try:    
            dataMemory[result] = op1 / op2
        except:
            raise TypeError("Operation invalid for specified operand types: {} = {} / {}".format(result, op1, op2))
#END ARITHMETIC OPERATIONS

#BEGIN LOGICAL COMPARISONS
def CEQ(op1, op2, result):
    try:
        if op1 == op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:        
        raise TypeError("Operation invalid for specified operand types")

def CNE(op1, op2, result):
    try:
        if op1 != op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:        
        raise TypeError("Operation invalid for specified operand types")

def CLT(op1, op2, result):
    try:
        if op1 < op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def CGT(op1, op2, result):
    try:
        if op1 > op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def CLE(op1, op2, result):
    try:
        if op1 <= op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def CGE(op1, op2, result):
    try:
        if op1 >= op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")
#   END LOGICAL COMPARISONS

#   BEGIN BOOLEAN OPERATIONS
def AND(op1, op2, result):
    try:
        if op1 and op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")

def ORR(op1, op2, result):
    try:
        if op1 or op2:
            dataMemory[result] = True
        else:
            dataMemory[result] = False
    except:
        raise TypeError("Operation invalid for specified operand types")
#   END BOOLEAN OPERATIONS

#   BEGIN JUMP AND FUNCTION OPERATIONS
def GTO(op1, op2, result):
    global PC
    PC = result - 1
    
def GTF(op1, op2, result):
    global PC
    try:
        if not op1:
            PC = result - 1
    except:
        raise TypeError("Type mismatch, expected boolean")

def ERA(op1, op2, result):
    global passingParameters, stackPointer
    stackPointer+=1
    #print stackPointer
    passingParameters = True


def CAL(op1, op2, result):
    global passingParameters
    jumpStack.append(PC)
    GTO(op1, op2, result + 1)
    passingParameters = False
   # print


def RET(op1, op2, result):
    global stackPointer
    #print op1 
    stackPointer-=1
    returnStack.append(op1)
    result = jumpStack.pop()
    GTO(op1, op2, result+1)
#   END JUMP AND FUNCTION OPERATIONS

#   BEGIN LANGUAGE-SPECIFIC OPERATIONS
def PRT(op1, op2, result):
    try:
        print op1
    except:
        raise TypeError("Operation invalid for specified operand type")

def DRW(op1, op2, result):
    try:
        if op1:
            loro.pendown()
        else:
            loro.penup()
    except: 
        raise TypeError("Type mismatch, expected boolean")

def ARC(op1, op2, result):
    try:
        loro.circle(op1, op2)
    except:
        raise TypeError("Type mismatch, expected integer values")
        
def CIR(op1, op2, result):
    try:
        loro.circle(op1)
    except:
        raise TypeError("Type mismatch, expected an integer value")
    
#Assuming first line of the square starts being drawn from starting orientation and position of the turtle
def SQR(op1, op2, result):
    try:   
        #save previous state
        speed=loro.speed()
        pen=loro.isdown()
        
        #paint
        loro.speed(0)
        loro.pendown()
        loro.forward(op1)
        loro.right(90)
        loro.forward(op2)
        loro.right(90)
        loro.forward(op1)
        loro.right(90)
        loro.forward(op2)
        loro.right(90)

        #restore previous state
        loro.speed(speed)
        if not pen:
            loro.penup()
    except:
        raise TypeError("Type mismatch, expected integer values")
    
def PRS(op1, op2, result):
    try:
        loro.pensize(op1)
    except:
        raise ValueError("Invalid width")

def COL(op1, op2, result):
    try:
        loro.color(op1)
    except:
        raise ValueError("Invalid colors")

def RHT(op1, op2, result):
    try:
        loro.right(op1)
    except: 
        raise TypeError("Type mismatch, expected an integer value")

def LFT(op1, op2, result):
    try:
        loro.left(op1)
    except: 
        raise TypeError("Type mismatch, expected an integer value")

def FWD(op1, op2, result):
    try:
        loro.forward(op1)
    except: 
        raise TypeError("Type mismatch, expected an integer value")

def BWD(op1, op2, result):
    try:
        loro.backward(op1)
    except: 
        raise TypeError("Type mismatch, expected an integer value")
#   END LANGUAGE-SPECIFIC OPERATIONS

def runVM():
    global PC, operator, op1, op2, result
    PC = 0
    methods = globals().copy()
    methods.update(locals())
    
    
    while PC < len(instructionMemory):
        op1Return = False
        op2Return = False
        #Read quadruple
        operator, op1, op2, result = instructionMemory[PC]
        result = int(result)
        #Translate addresses
        if operator not in ["DRW", "COL"]:
            if passingParameters:
                if operator not in ["GTO", "GTF", "CAL", "RET"]:
                    if result > 7000 and result < 7500:
                        result += 49
                        if stackPointer:
                            result += segmentLength*(stackPointer-1)
                    else:
                        if stackPointer:
                            result += segmentLength*(stackPointer-2)
                
                op2 = int(op2)
                if op2 > 7000:
                    op2 += segmentLength*(stackPointer-2)
                    #print "OP2: ", op2
                    op2 = dataMemory[op2]
                elif op2 < 7000:
                    #print "OP2: ", op2
                    op2 = dataMemory[op2]
                else:
                    op2 = returnStack.pop()
                    
                op1 = int(op1)
                if op1 > 7000:
                    op1 += segmentLength*(stackPointer-2)
                    #print "OP1: ", op1
                    op1 = dataMemory[op1]
                elif op1 < 7000:
                    op1 = dataMemory[op1]
                    #print "OP1: ", op1
                else:
                    op1 = returnStack.pop()
                    
            else:
                #print "Not passing parameters"
                if operator not in ["GTO", "GTF", "CAL", "RET"]:
                    if stackPointer:
                        result += segmentLength*(stackPointer-1)
                
                #print "Result: ", result
                
                op2 = int(op2)
                if op2 > 7000:
                    op2 += segmentLength*(stackPointer-1)
                    #print "OP2: ", op2
                    op2 = dataMemory[op2]
                elif op2 < 7000:
                    #print "OP2: ", op2
                    op2 = dataMemory[op2]
                else:
                    op2 = returnStack.pop()
                    
                op1 = int(op1)
                if op1 > 7000:
                    op1 += segmentLength*(stackPointer-1)
                    #print "OP1: ", op1
                    op1 = dataMemory[op1]
                elif op1 < 7000:
                    #print "OP1: ", op1
                    op1 = dataMemory[op1]
                else:
                    op1 = returnStack.pop()
                    
        #print "PC: ", PC
        #print [operator, op1, op2, result]
        #Execute quadruple
        method = methods.get(str(operator))
        if not method:
            raise Exception("Method \"{}\" not implemented!".format(str(operator)))
        method(op1, op2, result)
        
        #raw_input("Press enter to continue...")
        #Increment PC to execute next instruction
        PC += 1
    raw_input("Press enter to exit...")
   #Debugging code
    '''
    for i,n in enumerate(instructionMemory):
        print "{}\t{}\t{}\t{}\t{}\n".format(i, n[0], n[1], n[2], n[3])
    raise SystemExit
    '''
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        #Load code to the VM
        with open(sys.argv[1],'r') as code:
            line = code.readline()
            fields = shlex.split(line)
            while fields[0] == "CNT":
                try:
                    op1 = int(fields[1])
                except:
                    try:
                        op1 = float(fields[1])
                    except:
                        op1 = str(fields[1])
                        
                dataMemory[int(fields[3])] = op1
                    
                line = code.readline()
                fields = shlex.split(line)
            
            instructionMemory.append(fields)
            for line in code.readlines():
                instructionMemory.append(line.split())
        #Done loading code. Execute.
        runVM()
    else:
        print "Usage syntax: %s filename" %sys.argv[0]
