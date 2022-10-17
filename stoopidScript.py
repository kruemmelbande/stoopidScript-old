vars={}
file="helloWorld.stsc"
#Make this use args later
program=[]
with open(file,"r") as f:
    program=f.readlines()

def kwVar(line):
    working=cut(line,"var")
    if working.startswith("str"):
        if '"' in working:
            working=cut(working,"str")
            working=working.split('=')
            name=working[0].strip()
            type="str"
            value=working[1].split('"')[1]
            global vars
            vars[name]=(type,value)


def kwOut(line):
    working=cut(line,"out")
    global vars

    if working in vars:
        print(vars[working][1])

keywords={
    "var":kwVar,
    "out":kwOut
}

def cut(input:str,toRemove:str):
    working=input.strip()
    if working[:len(toRemove)] == toRemove:
        return working[len(toRemove):].strip()

curLin=0
while curLin<len(program):
    if program[curLin].strip().split(" ")[0] in keywords:
        keywords[program[curLin].strip().split(" ")[0]](program[curLin])
    curLin+=1