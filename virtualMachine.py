from turtle import *

Writer = Screen()
Writer.setup(400,200)
loro = Turtle()
loro.pendown() 

instructionMemory = {}
#dataMemory = range(0,4050700)
dataMemory = range(0,30) #for debugging
fields = []
PC = 0
operator = ""
op1 = ""
op2 = ""
result = ""
line = ""

def ADD():
    try:
        dataMemory[int(result)] = int(dataMemory[int(op1)]) + int(dataMemory[int(op2)])
    except:
        try:
            dataMemory[int(result)] = float(dataMemory[int(op1)]) + float(dataMemory[int(op2)])
        except:
            try:
                dataMemory[int(result)] = str(dataMemory[int(op1)]) + str(dataMemory[int(op2)])
            except:
                raise TypeError("Operation invalid for specified operand types")

def SUB():
    try:
        dataMemory[int(result)] = int(dataMemory[int(op1)]) - int(dataMemory[int(op2)])
    except:
        try:
            dataMemory[int(result)] = float(dataMemory[int(op1)]) - float(dataMemory[int(op2)])
        except:
            raise TypeError("Operation invalid for specified operand types")

def MUL():
    try:
        dataMemory[int(result)] = int(dataMemory[int(op1)]) * int(dataMemory[int(op2)])
    except:
        try:
            dataMemory[int(result)] = float(dataMemory[int(op1)]) * float(dataMemory[int(op2)])
        except:
            raise TypeError("Operation invalid for specified operand types")

def DIV():
    if op2 == 0:
        raise ValueError("Attempting to divide by 0")
    else:
        try:
            dataMemory[int(result)] = int(dataMemory[int(op1)]) / int(dataMemory[int(op2)])
        except:
            try:
                dataMemory[int(result)] = float(dataMemory[int(op1)]) / float(dataMemory[int(op2)])
            except:
                raise TypeError("Operation invalid for specified operand types")

def EQU():
    try:
        dataMemory[int(result)] = dataMemory[int(op1)]
    except:
        raise TypeError("Operation invalid for specified operand type")

def CEQ():
    try:
        if float(dataMemory[int(op1)]) == float(dataMemory[int(op2)]):
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        try:
            if str(dataMemory[int(op1)]) == str(dataMemory[int(op2)]):
                dataMemory[int(result)] = "TRUE"
            else:
                dataMemory[int(result)] = "FALSE"
        except:        
            raise TypeError("Operation invalid for specified operand types")

def CNE():
    try:
        if float(dataMemory[int(op1)]) != float(dataMemory[int(op2)]):
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        try:
            if str(dataMemory[int(op1)]) != str(dataMemory[int(op2)]):
                dataMemory[int(result)] = "TRUE"
            else:
                dataMemory[int(result)] = "FALSE"
        except:        
            raise TypeError("Operation invalid for specified operand types")

def CLT():
    try:
        if float(dataMemory[int(op1)]) < float(dataMemory[int(op2)]):
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        raise TypeError("Operation invalid for specified operand types")

def CGT():
    try:
        if float(dataMemory[int(op1)]) > float(dataMemory[int(op2)]):
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        raise TypeError("Operation invalid for specified operand types")

def CLE():
    try:
        if float(dataMemory[int(op1)]) <= float(dataMemory[int(op2)]):
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        raise TypeError("Operation invalid for specified operand types")

def CGE():
    try:
        if float(dataMemory[int(op1)]) >= float(dataMemory[int(op2)]):
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        raise TypeError("Operation invalid for specified operand types")

def AND():
    try:
        if str(dataMemory[int(op1)]) == "TRUE" and str(dataMemory[int(op2)]) == "TRUE":
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        raise TypeError("Operation invalid for specified operand types")

def ORR():
    try:
        if str(dataMemory[int(op1)]) == "TRUE" or str(dataMemory[int(op2)]) == "TRUE":
            dataMemory[int(result)] = "TRUE"
        else:
            dataMemory[int(result)] = "FALSE"
    except:
        raise TypeError("Operation invalid for specified operand types")

def PRT():
    try:
        print str(dataMemory[int(op1)])
    except:
        raise TypeError("Operation invalid for specified operand type")

#TODO: checar que ajustes seran necesarios una vez que queden las constantes dentro del archivo cuadruplos (offset?)
def GTO():
    global PC
    PC = int(result)-1
    

#TODO: checar que ajustes seran necesarios una vez que queden las constantes dentro del archivo de cuadruplos (offset?)
def GTF():
    global PC
    try:
        if str(dataMemory[int(op1)]) == "FALSE":
            PC = int(result)-1
    except:
        raise TypeError("Type mismatch, expected boolean")

#No se que se hace con los era, call y ret
def ERA():
    print "wede"
def CAL():
    print "wede"
def RET():
    print "wede"

def DRW():
    try:
        if str(dataMemory[int(op1)]) == "TRUE":
            loro.pendown()
        elif str(dataMemory[int(op1)]) == "FALSE":
            loro.penup()
    except: 
        raise TypeError("Type mismatch, expected boolean")

def ARC():
    try:
        loro.circle(int(dataMemory[int(op1)]), int(dataMemory[int(op1)]))
    except:
        raise TypeError("Type mismatch, expected integer values")
        
def CIR():
    try:
        loro.circle(int(dataMemory[int(op1)]))
    except:
        raise TypeError("Type mismatch, expected an integer value")
    
#Assuming first line of the square starts being drawn from starting orientation and position of the turtle
def SQR():
    try:   
        #save previous state
        speed=loro.speed()
        pen=str(loro.isdown())
        
        #paint 
        loro.speed(0)
        loro.pendown()
        loro.forward(int(dataMemory[int(op1)]))
        loro.right(90)
        loro.forward(int(dataMemory[int(op2)]))
        loro.right(90)
        loro.forward(int(dataMemory[int(op1)]))
        loro.right(90)
        loro.forward(int(dataMemory[int(op2)]))
        loro.right(90)

        #restore previous state
        loro.speed(speed)
        if pen == "False":
            loro.penup
    except:
        raise TypeError("Type mismatch, expected integer values")
    
#no supe bien que se supone que hace el pressure. yo supondria que es si se presiona la pluma o no (si dibuja o no)
#pero eso es lo que hace el draw (que tiene boolean como parametro)
#este tiene integer como argumento, por ahora lo puse como el ancho de la pluma
def PRS():
    try:
        loro.pensize(int(dataMemory[int(op1)]))
    except:
        raise ValueError("Invalid colors")

def COL():
    try:
        loro.color(str(dataMemory[int(op1)]),str(dataMemory[int(op1)]))
    except:
        raise ValueError("Invalid colors")

def RHT():
    try:
        loro.right(int(dataMemory[int(op1)]))
    except: 
        raise TypeError("Type mismatch, expected an integer value")

def LFT():
    try:
        loro.right(int(dataMemory[int(op1)]))
    except: 
        raise TypeError("Type mismatch, expected an integer value")

def FWD():
    try:
        loro.forward(int(dataMemory[int(op1)]))
    except: 
        raise TypeError("Type mismatch, expected an integer value")

def BWD():
    try:
        loro.backward(int(dataMemory[int(op1)]))
    except: 
        raise TypeError("Type mismatch, expected an integer value")


operations = {
    "ADD" : ADD,
    "SUB" : SUB, 
    "MUL" : MUL, 
    "DIV" : DIV, 
    "EQU" : EQU, 
    "CEQ" : CEQ, 
    "CNE" : CNE, 
    "CLT" : CLT, 
    "CGT" : CGT, 
    "CLE" : CLE, 
    "CGE" : CGE, 
    "AND" : AND, 
    "ORR" : ORR, 
    "PRT" : PRT, 
    "DRW" : DRW, 
    "ARC" : ARC, 
    "CIR" : CIR, 
    "SQR" : SQR, 
    "PRS" : PRS, 
    "COL" : COL, 
    "RHT" : RHT, 
    "LFT" : LFT, 
    "FWD" : FWD, 
    "BWD" : BWD, 
    "GTO" : GTO, 
    "GTF" : GTF, 
    "ERA" : ERA, 
    "CAL" : CAL, 
    "RET" : RET 
}

with open("sampleQuadruples.txt",'r') as code:
    instructionMemory = code.readlines()

for constants in range(0,len(instructionMemory)):
    line = instructionMemory[constants]    
    fields = line.split()
    PC = constants
    
    if fields[0] == "EQU":
        dataMemory[int(fields[3])] = fields[1]
    else:
        break

while PC < len(instructionMemory):
    line = instructionMemory[PC]  
    fields = line.split()
    operator = fields[0]
    op1 = fields[1]
    op2 = fields[2]
    result = fields[3]
    operations[operator]()
    PC+=1

print dataMemory #for debugging















