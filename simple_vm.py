#!/usr/bin/python

code = []
pc = 0
stack = []

labels = {} #map between labels and the next position

#reg0 is temp and return value, it is not saved during a call
#reg1,2 & 3 are used to pass parameters, they are also saved on the stack
regs = [0]*10


def restore_regs():
    regs[1:] = stack[-9:]
    del stack[-9:]


def save_regs():
    stack.extend(regs[1:])


def addInstruction(opcode, p1=0, p2=0, p3=0):
    code.append( (opcode, p1, p2, p3) )

def addLabel(label_name):
    labels[label_name] = len(code) #the label refers to the next instruction

def exec_next():
    global pc
    opcode, p1, p2, p3 = code[pc]
    #print "pc: %d code: %s" % (pc, str(code[pc]))
    #print "regs: ", regs
    if opcode == "LOADK":
        regs[p1] = p2

    if opcode == "ADD":
        regs[p1] = regs[p1] + regs[p2]
    
    if opcode == "DEC":
        regs[p1] = regs[p1]-1
    
    if opcode == "MOV":
        regs[p1] = regs[p2]
    
    if opcode == "MULT":
        regs[p1] = regs[p1] * regs[p2]

    if opcode == "JMPNZ":
        if regs[p1] != 0:
            pc = labels[p2] #jump based on the label
            return
    
    if opcode == "RET":
        pc = stack.pop()
        restore_regs()
        return

    if opcode == "CALL":
        save_regs()
        stack.append(pc+1)
        pc = labels[p1]
        return
    
    if opcode == "END":
        pc = len(code) #past the end of the program

    pc += 1

def main():
    global pc
    ai = addInstruction
    
    
    
    #Let's try a factorial so we can test recursion
    # if n=0, ret 1
    # else recur(n-1)*n

    #Factorial function
    '''
    int fact(int n)
        if n==0
            return 1
        return fact(n-1)*n;
    '''
    
    addLabel("main")
    ai("LOADK", 1, 5) #load 5 into reg1
    ai("CALL", "factorial") #and call the function!
    ai("END") #quit when we return


    addLabel("factorial") #add a label to jump to, instead of actual instruction addresses
    ai("JMPNZ", 1, "fact_else") #is param1 not 0?
    ai("LOADK", 0, 1) #so param1==0, set the return register to 1
    ai("RET")
    addLabel("fact_else")
    ai("MOV", 4, 1) #copy the param1 (only param) into a "safe" register so we can use it later (reg4)
    ai("DEC", 1) #decrement the incoming param so we can pass it to the next call
    ai("CALL", "factorial") #call factorial with n-1, value is returned in reg0
    ai("MULT", 0, 4) # reg0 = reg0 * reg4
    ai("RET") 


    while pc < len(code):
        exec_next()

    print regs #we expect reg1 to still have 5 in it, and the result (120) should be in reg0

if __name__ == '__main__':
    main()
