from sys import argv as args, exit
vars={}
file="helloWorld.stsc"
file = args[1]
forcerun="--forcerun" in args
#make the interpreter not exit on error (in most cases)
#WARNING: THIS IS NOT A GOOD IDEA
#i made this for reasons that i dont know myself
#use at your own risk, because this is a bad idea, and it might return unexpected results



program=[]
with open(file,"r") as f:
    program=f.readlines()


if forcerun:
    print("Forcerun enabled (use with care!)")

def kwVar(line):
    global vars
    working=cut(line,"var")
    if working.startswith("str"):
        if '"' in working:
            working=cut(working,"str")
            working=working.split('=')
            name=working[0].strip()
            type="str"
            value=working[1].split('"')[1]
            vars[name]=(type,value)
    elif working.startswith("int"):
        working=cut(working,"int")
        working=working.split('=')
        name=working[0].strip()
        type="int"
        value=int(float(working[1]))
        vars[name]=(type,value)
    elif working.startswith("float"):
        working=cut(working,"float")
        working=working.split('=')
        name=working[0].strip()
        type="float"
        value=float(working[1])
        vars[name]=(type,value)
    elif working.startswith("bool"):
        working=cut(working,"bool")
        working=working.split('=')
        name=working[0].strip()
        type="bool"
        value=bool(working[1])
        vars[name]=(type,value)
    elif working.startswith("dynamic"):
        working=cut(working,"dynamic")
        working=working.split('=')
        name=working[0].strip()
        type="dynamic"
        value=working[1]
        vars[name]=(type,value)
    elif working.startswith("auto"):
        working=cut(working,"dynamic")
        working=working.split('=')
        name=working[0].strip()
        value=working[1]
        type=getType(value)
        vars[name]=(type,value)


def kwOut(line):
    working=cut(line,"out")
    global vars

    print(getValue(working))

keywords={
    "var":kwVar,
    "out":kwOut
}
def solveComplexMath(input:str):
    ops=[]
    vars=[]
    working=input.replace(" ","")
    if isIn(["+","-","*","/","<",">","^"],input):
        for i in ["+","-","*","/","<",">","^"]:
            if i in input:
                vars.append(working.split(i)[0])
                working=cut(working,i)
                ops.append(i)
    if "(" in working:
        start,end,stop=0,0,0
        for k in range(len(working)):
            if working[k] == "(":
                start = k
        end=1
        for j in range(start+1, len(working)):


            if working[j] == "(":
                end +=1
            if working[j] == ")":
                end -=1
            if end==0 :
                stop=j
                break
        else:
            print("No matching bracket")

        tmpworking = working[:start]
        tmpworking += str(int(solveComplexMath(working[start + 1 : stop])))
        tmpworking += working[stop + 1 :]
        return solveComplexMath(tmpworking)

def solveBasicMath(input:str) -> int|float|bool:
    """ input: A math equasion, with two numbers or variables and one operator
        output: A solution
    """
    if isIn(["+","-","*","/","<",">","^"],input):
        for i in ["+","-","*","/","<",">","^"]:
            if i in input:
                comp=i
                break
        num1,num2=input.split(comp)
        num1=getValue(num1)
        num2=getValue(num2)
        if comp=="+":
            return num1+num2
        elif comp=="-":
            return num1-num2
        elif comp=="*":
            return num1*num2
        elif comp=="/":
            return num1/num2
        elif comp=="<":
            return num1<num2
        elif comp==">":
            return num1>num2
        else:
            return num1**num2
    else:
        return getValue(input)

def getValue(input:str):
    global vars
    if input in vars:
        return vars[input][1]
    else:
        if str(input).isnumeric():
            if str(input).isdigit():
                return int(input)
            else:
                return float(input)
        else:
            if isIn(["+","-","*","/","<",">","^"],input):
                return solveBasicMath(input)
            else:
                if (input.startswith('"') or input.startswith("'")) and (input.endswith('"') or input.endswith("'")):
                    return input[1:-1]
                else:
                    raise Exception("Unknown value type")


def setVar(name,value):
    global vars
    if name in vars:
        type=vars[name][0]
        value=getValue(value)
        try:
            if type=="str":
                vars[name]=(type,str(value))
            elif type=="int":
                vars[name]=(type,int(value))
            elif type=="float":
                vars[name]=(type,float(value))
            elif type=="bool":
                vars[name]=(type,bool(value))
            else:
                vars[name]=(getType(value),value)
        except:
            errorMessage(f"Cannot convert {value} (type : {getType(value)}) to {type}")
    else:
        errorMessage("Variable "+name+" not found")

def getType(input:any):
    input=getValue(input)
    return type(input).__name__

def cut(input:str,toRemove:str):
    working=input.strip()
    if working[:len(toRemove)] == toRemove:
        return working[len(toRemove):].strip()
def errorMessage(message:str):
    global forcerun
    print("Error: "+message)
    if forcerun:
        print("error ignored")
        return
    exit()

def isIn(list,string):
    for i in list:
        if i in string:
            return True
    return False

curLin=0
while curLin<len(program):
    c=program[curLin]
    if c.strip().split(" ")[0] in keywords:
        keywords[c.strip().split(" ")[0]](c)
    else:
        if '=' in c:
            if c.strip().split("=")[0].strip() in vars:
                setVar(c.strip().split("=")[0].strip(),c.strip().split("=")[1].strip())
    curLin+=1
