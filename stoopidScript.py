import operator
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
            value=working[1]
            vars[name]=(type,value)
        else:
            working=cut(working,"str")
            working=working.split('=')
            name=working[0].strip()
            type="str"
            value=str(getValue(working[1]))
            vars[name]=(type,value)
    elif working.startswith("int"):
        working=cut(working,"int")
        working=working.split('=')
        name=working[0].strip()
        type="int"
        value=int(float(getValue(working[1])))
        vars[name]=(type,value)
    elif working.startswith("float"):
        working=cut(working,"float")
        working=working.split('=')
        name=working[0].strip()
        type="float"
        value=float(getValue(working[1]))
        vars[name]=(type,value)
    elif working.startswith("bool"):
        working=cut(working,"bool")
        working=working.split('=')
        name=working[0].strip()
        type="bool"
        value=bool(getValue(working[1]))
        vars[name]=(type,value)
    elif working.startswith("dynamic"):
        working=cut(working,"dynamic")
        working=working.split('=')
        name=working[0].strip()
        type="dynamic"
        value=getValue(working[1])
        vars[name]=(type,value)
    elif working.startswith("auto"):
        working=cut(working,"auto")
        working=working.split('=')
        name=working[0].strip()
        value=getValue(working[1])
        type=getType(value)
        vars[name]=(type,value)


def kwOut(line):
    working=cut(line,"out")
    global vars
    working=getValue(working)
    print(cleanString(str(working)))



keywords={
    "var":kwVar,
    "out":kwOut
}

def isNumber(x):
    try:
        a=float(x)
        return True
    except:
        return False

def solveEquasion(equasion: str) -> float:
    """Solves the given equasion

    Args:
        equasion (str): the mathematical equasion to be solved

    Returns:
        float: solved equasion
    """

    global vars
    orderOfOps = [["<",">"],["+", "-"], ["*", "/"], ["%", "^"]]
    operators=["+","-","*","/","<",">","^"]
    equasion = equasion.replace(" ", "")
    if "(" in equasion:
        start,end,stop=0,0,0
        for k in range(len(equasion)):
            if equasion[k] == "(":
                start = k
        end=1
        for j in range(start+1, len(equasion)):


            if equasion[j] == "(":
                end +=1
            if equasion[j] == ")":
                end -=1
            if end==0 :
                stop=j
                break
        else:
            print("No matching bracket")

        tmpequasion = equasion[:start]
        tmpequasion += str(int(solveEquasion(equasion[start + 1 : stop])))
        tmpequasion += equasion[stop + 1 :]
        return solveEquasion(tmpequasion)
    equasion = str(equasion)
    for i in vars:
        equasion = equasion.replace(i, str(vars[i][1]))
    equasion=equasion.replace("True","1").replace("true","1").replace("yes","1").replace("False","0").replace("false","0").replace("no","0")

    ops = []
    values = []

    x = 0
    while x < len(equasion):
        if isNumber(equasion[x]):
            if x > 0 and (
                isNumber(equasion[x - 1])
                or values[len(values) - 1][len(values[len(values) - 1]) - 1]
                in ["-", "."]
            ):
                values[len(values) - 1] += equasion[x]
            else:
                values.append(str(equasion[x]))
        elif equasion[x] in [o for o in operators]:
            if (x == 0 and equasion[x] == "-") or (
                x > 0 and not isNumber(equasion[x - 1])
            ):
                values.append(equasion[x])
            else:
                ops.append(str(equasion[x]))
        elif equasion[x] == ".":
            if x > 0 and isNumber(equasion[x - 1]):
                values[len(values) - 1] += "."
            else:
                values.append("0.")
        x += 1

    # now we have the values and the operators, find the order in which they should be solved
    order = []
    for i in range(len(ops)):
        for k in range(len(orderOfOps)):
            if ops[i] in orderOfOps[k]:
                order.append(k)

    # now we have the order in which the operators should be solved, we need to solve them
    minorder = max(order)
    for i in range(len(ops)):
        if order[i] == minorder:
            values[i]=solveBasicMath(f"{float(values[i])}{ops[i]}{float(values[i + 1])}")

            values.pop(i + 1)
            ops.pop(i)

            order.pop(i)
            break
    # after we have solved the first operator, we need to solve the rest
    if len(ops) > 1:
        # recreate the equation
        equasion = ""
        for i in range(len(ops)):
            equasion += str(values[i]) + str((ops[i]))
        equasion += str(values[-1])
        return (float(str((solveEquasion(equasion))))
        )
    elif len(ops) == 1:
        #return float(operators[ops[0]](float(values[0]), float(values[1])))
        return solveBasicMath(f"{float(values[0])}{ops[0]}{float(values[1])}")
    else:

        return int(values[0])

def cleanString(input : str):
    input=input.strip()
    if (input.startswith('"') or input.startswith("'")) and (input.endswith('"') or input.endswith("'")):
        return input[1:-1]
    return input

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
            out= num1+num2
        elif comp=="-":
            out= num1-num2
        elif comp=="*":
            out= num1*num2
        elif comp=="/":
            out= num1/num2
        elif comp=="<":
            out= num1<num2
        elif comp==">":
            out= num1>num2
        else:
            return num1**num2
        return out

    else:
        return getValue(input)

def getRawType(input:any):
    return type(input).__name__

def getValue(input:str):
    if getRawType(input)=="str":
        input=input.strip()
    global vars
    if input in vars:
        return vars[input][1]
    else:
        if isNumber(input):
            if str(input).isdigit():
                return int(input)
            else:
                return float(input)
        else:
            if isIn(["+","-","*","/","<",">","^"],input):
                return solveEquasion(input)
            else:
                if (input.startswith('"') or input.startswith("'")) and (input.endswith('"') or input.endswith("'")):
                    return input
                else:
                    if input.lower() in ["true","false","1","0","yes","no"]:
                        return isTruthy(input)
                    errorMessage(f"Unknown value type : {input}", e=Exception("Unknown type exception"))
                    #raise Exception("Unknown value type:", input)
                    return f'"{input}"'

def isTruthy(str):
    return str.lower() in ["true","1","yes"]


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

def toString(input: any):
    return f'"{cleanString(str(input))}"'

def getType(input:any):
    input=getValue(input)
    return type(input).__name__

def cut(input:str,toRemove:str):
    working=input.strip()
    if working[:len(toRemove)] == toRemove:
        return working[len(toRemove):].strip()
def errorMessage(message:str,e=None):
    global forcerun
    print("Error: "+message)
    if forcerun:
        print("error ignored")
        return
    if e!=None:
        raise e
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
