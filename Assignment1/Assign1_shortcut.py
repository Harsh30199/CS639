import json
import sys
from ast import parse
from ast2json import ast2json

## Three lists to store different operations
assign=[]
loop=[]
condition=[]

def checker(body):
    for a in body:
        if(a['_type']in ["Assign","AugAssign"]):
            assign.append(lines[a['lineno']-1].strip())
        elif(a['_type']=='If'):
            if(lines[a['lineno']-1].strip()[0]=="i"):
                condition.append("If: "+lines[a['lineno']-1].strip()[2:-1].strip())
            else:
                condition.append("Elif: "+lines[a['lineno']-1].strip()[4:-1].strip())
            checker(a['body']) ##Checks the If Statement Block
            checker(a['orelse'])##Checks the Else Statement Block
        elif(a['_type']=='While'):
            loop.append("While: "+lines[a['lineno']-1].strip()[5:-1].strip())
            checker(a['body']) ##Checks While Statement Block
        elif(a['_type']=='For'):
            loop.append("For: "+lines[a['lineno']-1].strip()[3:-1].strip())
            checker(a['body'])##Checks For Statement Block
        elif(a['_type']=='FunctionDef'):
            checker(a['body'])##Checks Function Block
           

    
path = sys.argv[1]   ##Takes path of python file to be checked as input
code=open(path)               ##Opens the file at the specified path
lines=code.readlines()        ##Reads each line and stores in  list
ast=ast2json(parse(open(path).read())) ##Reads test file , makes ast and then converts to json type data

##print(json.dumps(ast,indent=4)) ##Prints the json data
checker(ast['body'])          ##checker is the function that reads the json data and identifies type of operation


if len(assign):
    print("\nAssignments Statements:")
    for a in assign:
        print(a)
if len(loop):    
    print("\nLoop Conditions:")
    for a in loop:
        print(a)
if len(condition):
    print("\nBranch Conditions:")
    for a in condition:
        print(a)
