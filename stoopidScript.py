import array
from dataclasses import replace
from sys import argv as args, exit
vars={}
file="helloWorld.stsc"
file = args[1]
forcerun="--forcerun" in args
timed= "--time" in args
#make the interpreter not exit on error (in most cases)
#WARNING: THIS IS NOT A GOOD IDEA
#i made this for reasons that i dont know myself
#use at your own risk, because this is a bad idea, and it might return unexpected results

if timed:
    import time
    startTime=time.perf_counter()


program=[]
with open(file,"r") as f:
    program=f.readlines()


if forcerun:
    print("Forcerun enabled (use with care!)")


operators= ["+","*","/","<<",">>","^","==","<=",">=","-"]

def kwDef(line,locals:dict=None):
    #print("a")
    global vars,curLin
    working=cut(line,"def")
    name=working.replace("{","").replace("}","").strip()
    type="func"
    value=curLin
    vars[name]=(type,value)
    i=curLin-1
    a=0
    b=1
    try:
        while 1:
            i+=1
            line=program[i].strip()
            for k in line:
                if k=="{":
                    a+=1
                    b=0
                if k=="}":
                    a-=1
                    b=0
                if a==0 and b==0:
                    break
            else:
                continue
            break
        curLin=i
    except Exception as e:
        errorMessage("Failed to find closing bracket!",e=e)

def kwIf(line,locals:dict=None):
    try:
        global program, curLin
        working=cut(line,"if")
        toMath=working
        if "{" in working:
            toMath=working.replace("{","")

        solved=getValue(toMath,locals)
        if solved:
            return
        else:
            i=curLin-1
            a=0
            b=1
            try:
                while 1:
                    i+=1
                    line=program[i].strip()
                    for k in line:
                        if k=="{":
                            a+=1
                            b=0
                        if k=="}":
                            a-=1
                            b=0
                        if a==0 and b==0:
                            break
                    else:
                        continue
                    break

            except Exception:
                errorMessage("Failed to find closing bracket!")
            curLin=i
    except Exception as e:
        errorMessage("error resolving if statement, ",e=e)

def kwVar(line,local=False,locals:dict=None):
    global vars
    working=cut(line,"var")
    if working.startswith("str"):
        if '"' in working:
            working=cut(working,"str")
            working=working.split('=')
            name=working[0].strip()
            type="str"
            value=working[1]
            
        else:
            working=cut(working,"str")
            working=working.split('=')
            name=working[0].strip()
            type="str"
            working="=".join(working[1:])
            value=getValue(working, locals)
            

    elif working.startswith("int"):
        working=cut(working,"int")
        working=working.split('=')
        name=working[0].strip()
        type="int"
        working="=".join(working[1:])
        value=int(float(getValue(working, locals)))
        
    elif working.startswith("float"):
        working=cut(working,"float")
        working=working.split('=')
        name=working[0].strip()
        type="float"
        working="=".join(working[1:])
        value=float(str(getValue(working, locals)))
        
    elif working.startswith("bool"):
        working=cut(working,"bool")
        working=working.split('=')
        name=working[0].strip()
        type="bool"
        working="=".join(working[1:])
        value=isTruthy(getValue(working, locals))
        
    elif working.startswith("dynamic"):
        working=cut(working,"dynamic")
        working=working.split('=')
        name=working[0].strip()
        type="dynamic"
        working="=".join(working[1:])
        value=getValue(working, locals)
        
    elif working.startswith("auto"):
        working=cut(working,"auto")
        working=working.split('=')
        name=working[0].strip()
        working="=".join(working[1:])
        value=getValue(str(working), locals)
        type=getRawType(value)
        
    elif working.startswith("label"):
        global curLin
        working=cut(working,"label")
        if "=" in working:
            working=working.split('=')
            name=working[0].strip()
            type="label"
            value=int(getValue(working[1], locals))
           
        else:
            name=working.strip()
            type="label"
            value=curLin
    if local:
        return (name,type,value)
    else:
        vars[name]=(type,value)
    
def kwOut(line,locals:dict=None):
    working=cut(line,"out")
    global vars
    working=getValue(working, locals)
    print(cleanString(str(working)))

def kwEnd(line,locals:dict=None):
    onExit()


def runFunction(line): #Feeling cute, might git reset --hard later after i break this
    try:
        locals=vars
        def localVar(line,locals):  #did it need to be like this? no. did i do this first, then change the system, and not bother to update this? yes. I mean, its not clean, but it works, so i dont care

            tmp=kwVar(line,local=True,locals=locals)

            locals[tmp[0]]=tmp[1:]

            return locals


        #we need proxies for the functions, as they are local, and arent supposed to do global stuff
        funwords={ 
        "var":localVar,
        "out":kwOut,
        "if" :kwIf,
        "end":kwEnd,
        "goto":kwGoto,
        None:None
        }
        #this is me from the past! If you are trying to understand what im trying to do here, i am sorry, i dont know either
        #anyway, good lucK!
        #this is me from the future. Past me was dumb.
        #it didnt need to be this complicated.

        funLine=line
        while funLine<len(program):
            c=program[funLine]
            kw=c.strip().split(" ")[0]
            #print(kw,len(program),funLine)
            if kw == "return":
                return getValue(cut(c,"return"),locals)
            if kw in funwords:
                funwords[kw](c,locals)
            else:
                # #yes, im lazy, and the minimum required is to make this work, and i dont care for now if its inconvenient
                 if '=' in c:
                     if c.strip().split("=")[0].strip() in vars:
                         errorMessage("Vars cant be changed in functions without using var!")
                #         setVar(c.strip().split("=")[0].strip(),c.strip().split("=")[1].strip())
            funLine+=1
        errorMessage("Function ended without return statement!")
    except Exception as e:

        errorMessage(f"Error running function in line {line}",e=e)
def kwGoto(line,locals:dict=None):
    global curLin
    dest=getValue(cut(line,"goto"), locals)
    curLin=dest-1

keywords={
    "var":kwVar,
    "out":kwOut,
    "if" :kwIf,
    "end":kwEnd,
    "goto":kwGoto,
    "def":kwDef,
    None:None
}

def isNumber(x):
    try:
        a=float(x)
        return True
    except:
        return False

def solveEquasion(equasion: str,locals:dict=None) -> float:
    """Solves the given equasion
    Args:
        equasion (str): the mathematical equasion to be solved

    Returns:
        float: solved equasion
    """

    try:

        global vars,operators
        equasion = str(equasion)
        for i in vars:
            equasion = equasion.replace(i, str(vars[i][1]))
        equasion=equasion.replace("True","1").replace("true","1").replace("yes","1").replace("False","0").replace("false","0").replace("no","0")
        orderOfOps = [["<<",">>","==","<=",">="],["+", "-"], ["*", "/"], ["%", "^"]]
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
                errorMessage("No matching bracket")
            #print(equasion[start + 1 : stop])
            tmpequasion = equasion[:start]
            tmpequasion += str(int(getValue(equasion[start + 1 : stop],locals)))
            tmpequasion += equasion[stop + 1 :]
            return getValue(tmpequasion)


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
            elif any((equasion[x:x+len(o)]==o) for o in operators):
                if (x == 0 and equasion[x] == "-") or (
                    x > 0 and not isNumber(equasion[x - 1])
                ):
                    values.append(equasion[x])
                else:
                    tmp=[(o,equasion[x:x+len(o)]==o) for o in operators]
                    for i in tmp:
                        if i[1]:
                            break
                    ops.append(str(equasion[x:x+len(i[0])]))

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
        #print(ops,values,order)
        # now we have the order in which the operators should be solved, we need to solve them
        try:
            minorder = max(order)
        except Exception as e:
            errorMessage(f"Critical error when solving math!{order}{values}{ops}")
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
            return (float(str((getValue(equasion),locals)))
            )
        elif len(ops) == 1:
            #return float(operators[ops[0]](float(values[0]), float(values[1])))
            return solveBasicMath(f"{float(values[0])}{ops[0]}{float(values[1])}")
        else:

            return int(values[0])
    except Exception as e:
            errorMessage(f"Failed to solve equasion {equasion}",e=e)

def cleanString(input : str):
    input=input.strip()
    if (input.startswith('"') or input.startswith("'")) and (input.endswith('"') or input.endswith("'")):
        return input[1:-1]
    return input

def solveBasicMath(input:str,locals:dict=None) -> int|float|bool:
    """ input: A math equasion, with two numbers or variables and one operator
        output: A solution
    """
    #print(input)
    global operators
    ops=operators
    if isIn(ops,input):
        for i in ops:
            if i in input:
                comp=i
                break
        num1,num2=input.split(comp)
        num1=getValue(num1,locals)
        num2=getValue(num2,locals)
        if comp=="+":
            out= num1+num2
        elif comp=="-":
            out= num1-num2
        elif comp=="*":
            out= num1*num2
        elif comp=="/":
            out= num1/num2
        elif comp=="<<":
            out= num1<num2
        elif comp==">>":
            out= num1>num2
        elif comp=="==":
            out=num1==num2
        elif comp=="<=":
            out=num1<=num2
        elif comp==">=":
            out=num1>=num2
        else:
            return num1**num2
        return out

    else:
        return getValue(input,locals)

def getRawType(input:any):
    return type(input).__name__

def getValue(input:str,locals:dict=None):
    if input=="":
        return 0
    if getRawType(input)=="str":
        input=input.strip()
    if locals!=None:
        try:
            if input in locals:
                return locals[input][1]
        except:
            print(input,locals)
    global vars
    if input in vars:
        if vars[input][0]=="func":
            return runFunction(vars[input][1])
        return vars[input][1]
    else:
        if isNumber(input):
            if str(input).isdigit():
                return int(input)
            else:
                return float(input)
        else:
            sep=0
            for i in str(input):
                if i in ["'",'"']:
                    sep+=1
            if isIn(operators,input):
                return solveEquasion(input)
            else:
                if (input.startswith('"') or input.startswith("'")) and (input.endswith('"') or input.endswith("'")) and sep==2:
                    return input
                else:
                    if input.lower() in ["true","false","1","0","yes","no"]:
                        return isTruthy(input)
                    if input.startswith("!"):
                        return not getValue(input[1:])
                    errorMessage(f"Unknown value type : {input}", e=Exception("Unknown type exception"))
                    #raise Exception("Unknown value type:", input)
                    return f'"{input}"'

def isTruthy(inp):
    return str(inp).lower() in [
        "true",
        "1",
        "yes",
        "Yes, do as I say!"#Felt cute, might remove my desktop environment later
        ]


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
            elif type=="dynamic":
                vars[name]=(getType(value),value)
            else:
                errorMessage(f"Cannot assign value to {name} because it is not mutable")
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

def errorMessage(message:str,e:Exception=None):
    global forcerun
    print("\033[91mError: "+message)
    if e != None:
        lineInInterpreter="\033[91mNot availablen\033[0m"
    else:
        lineInInterpreter=e.__traceback__.tb_lineno
    print(f"\033[0mError dump: \nvars: {vars}\nlineinProgram:{curLin}\nlineinInterpreter:{lineInInterpreter}\033[0m")

    if not forcerun:
        onExit()
    if forcerun:
        print("\033[0merror ignored")
        return
    if e!=None:
        raise e
    exit()

def isIn(list,string):
    for i in list:
        if i in string:
            return True
    return False

def onExit():
    global timed,startTime
    if timed:
        print(f"Execution time: {time.perf_counter()-startTime}s")
    exit()

curLin=0
while curLin<len(program):
    c=program[curLin]
    kw=c.strip().split(" ")[0]
    if kw in keywords:
        keywords[kw](c)
    else:
        if '=' in c:
            if c.strip().split("=")[0].strip() in vars:
                setVar(c.strip().split("=")[0].strip(),c.strip().split("=")[1].strip())
    curLin+=1
onExit()
