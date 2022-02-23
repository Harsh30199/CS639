import json
import sys
from ast import parse
from ast2json import ast2json

## Three lists to store different operations
assign=[]
loop=[]
condition=[]

def generators(generators): ##Returns generators used in different kinds of Comprehensions
    s=''
    for g in generators:
        m=" for "+typechecker(g['target'])+ ' in ' + typechecker(g['iter'])
        loop.append(m.lstrip(" for "))
        s+=m
        for f in g['ifs']:
            c=typechecker(f)
            condition.append(c)
            s+=' if '+c
    return s

def booloperator(o): ##Defines a Dictionary of Boolean Operators and returns a Boolean Operator
    op={'And':'and','Or':'or' }
    return op[o]

def operator(o): ##Defines a Dictionary of Operators and returns a Operator
    op={'Add':'+','Sub':'-','Mult':'*','Div':'/','FloorDiv':'//','Mod':'%','Pow':'**','Eq':'==','NotEq':'!=','Lt':'<','LtE':'<=','Gt':'>','GtE':'>=','Is':' is ','IsNot':' is not ','In':' in ','NotIn':' not in ','LShift':'<<','RShift':'>>','BitOr':'|','BitXor':'^','BitAnd':'&'}
    return op[o]

def typechecker(t):
    if(t!=None):
        
        if (t['_type']=='Name'): ##Returns variable names
            return t['id']
        
        elif(t['_type']=='NameConstant'): ##Returns keyword constant like True, False
            return str(t['value'])
        
        elif(t['_type']=='Constant'): ##Returns Constant values in Python 3.9
            if(type(t['value'])==str):
               return repr(t['value'])
            return str(t['value'])
        
        elif(t['_type']=='Num'):  ##Returns numeric constants in Python 3.7
            return str(t['n'])
        
        elif(t['_type']=='Str'):   ##Returns string or character type constant in Python 3.7
            return "'"+t['s']+"'"
        
        elif(t['_type']=='Subscript'): ##Returns Scriptable variables like X[5]
            s=typechecker(t['value'])+'['+typechecker(t['slice'])+']'
            return s
        
        elif(t['_type']=="Index"): ##Returns the index in Python 3.7
            return typechecker(t['value'])
        
        elif(t['_type']=='Slice'): ##Returns the Slice values
            s=typechecker(t['lower'])+':'+typechecker(t['upper'])
            if(t['step']!=None):
                s=s+":"+typechecker(t['step'])
            return s
        
        elif(t['_type']=='BinOp'): ##Returns Binary Expressions
            left= typechecker(t['left'])
            right=typechecker(t['right'])    
            return '('+left + operator(t['op']['_type'])+right+')'
        
        elif(t['_type']=='List'): ##Returns List Definitions
            s='['
            for e in t['elts'] :
                s=s+typechecker(e)+','
            return s.rstrip(',')+']'
        
        elif(t['_type']=='Dict'): ##Returns Dictionary Definitions
            s='{'
            i=0
            for k in t['keys']:
                s=s+typechecker(k)+":"+typechecker(t['values'][i])+','
                i+=1
            return s.rstrip(',')+'}'
        
        elif(t['_type']=='Tuple'): ##Returns Tuple Definitions
            s='('
            for e in t['elts'] :
                s=s+typechecker(e)+','
            return s.rstrip(',')+')'
        
        elif(t['_type']=='Set'):  ##Returns Set Definitions
            s='{'
            for e in t['elts'] :
                s=s+typechecker(e)+','
            return s.rstrip(',')+'}'
        
        elif(t['_type']=='Compare'): ##Returns Condition expressions
            s= typechecker(t['left'])
            for i in range(len(t['ops'])):
                s+=operator(t['ops'][i]['_type'])
                s+=typechecker(t['comparators'][i])
            return s
        
        elif(t['_type']=='BoolOp'): ##Returns Boolean operator (like and ,or) containig expressions
            s=''
            s=typechecker(t['values'][0])
            for v in range(1,len(t['values'])):
                s=s+" "+booloperator(t['op']['_type'])+" "+typechecker(t['values'][v])
            return s
        
        elif(t['_type']=='UnaryOp'): ##Returns Unary operator (like UnaryMinus) for expressions
            if(t['op']['_type']=='USub'):
                return '-'+typechecker(t['operand'])
            elif(t['op']['_type']=='Not'):
                return 'not('+typechecker(t['operand'])+')'
            elif(t['op']['_type']=='Invert'):
                return '~'+typechecker(t['operand'])
            elif(t['op']['_type']=='UAdd'):
                return '+'+typechecker(t['operand'])
            
        elif(t['_type']=='Call'):  ##Returns function Call statements
            s = typechecker(t['func'])+'('
            if(not(len(t['args']))):
                return s+')'
            for a in t['args']:
                s=s+typechecker(a)+','
            return s[0:-1]+')'
        
        elif(t['_type']=='Attribute'): ##Returns In-built Attributes (Ex: dict.items()) 
            return typechecker(t['value'])+"."+t['attr']
        
        elif(t['_type']=="ListComp"): ##Returns List Comprehension Expression
            return '['+typechecker(t['elt'])+generators(t['generators'])+']'
        
        elif(t['_type']=='arg'): ##Returns Function Arguments
            return t['arg']
        
        elif(t['_type']=='DictComp'): ##Returns Dictionary Comprehension Expression
            s='{'+typechecker(t['key'])
            s+=':'+typechecker(t['value'])
            return s+generators(t['generators'])+'}'
        
        elif(t['_type']=="SetComp"): ##Returns Set Comprehension Expression
            return '{'+typechecker(t['elt'])+generators(t['generators'])+'}'
        
        elif(t['_type']=='Lambda'): ##Returns Lambda Function Definition
            s='lambda '
            for a in t['args']['args']:
                s+=typechecker(a)
            s+=':'+typechecker(t['body'])
            return s
            
        else:    ##Returns In case a new type is found for which return statement is not provided
            return ""
    else:        ##Returns in case parameter passed to function is of None Type
        return ""

def checker(body):
    
    for a in body:
        
        if(a['_type']=="Assign"):
            s=''
            for t in a['targets']:
                s+=typechecker(t)+"="                
            assign.append(s+typechecker(a['value']))
            
        elif(a['_type']=="AugAssign"): ##Checks for Assignments like x-=y
            assign.append(typechecker(a['target'])+operator(a['op']['_type'])+"="+typechecker(a['value']))
            
        elif(a['_type']=='If'):
            condition.append(typechecker(a['test']))
            checker(a['body']) ##Checks the If Statement Block
            checker(a['orelse'])##Checks the Else Statement Block
            
        elif(a['_type']=='While'):
            loop.append(typechecker(a['test']))
            checker(a['body']) ##Checks While Statement Block
            
        elif(a['_type']=='For'):
            loop.append(typechecker(a['target'])+" in "+typechecker(a['iter']))
            checker(a['body'])##Checks For Statement Block
            checker(a['orelse'])##Checks Else Statement Block of For Loop
            
        elif(a['_type']=='FunctionDef'):
            b=a['args']
            j=len(b['args'])-len(b['defaults']) 
            for i in range(len(b['defaults'])):
                assign.append(typechecker(b['args'][j+i])+"="+typechecker(b['defaults'][i]))   ##Processes Default type Arguments of a function
            checker(a['body'])##Checks Function Block

        elif(a['_type']=='ClassDef'):
            checker(a['body'])
               
path = sys.argv[1]   ##Takes path of python file to be checked as input from run.sh
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
