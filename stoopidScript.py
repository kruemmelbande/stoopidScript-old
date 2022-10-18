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
            if ["+","-","*","/","=","<",">","!"].__contains__(input):

                return "not yet implemented"
            else:
                if (input.startswith('"') or input.startswith("'")) and (input.endswith('"') or input.endswith("'")):
                    return input[1:-1]
                else:
                    raise Exception("Unknown value type")


def setVar(name,value):
    global vars
    if name in vars:
        type=vars[name][0]
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
