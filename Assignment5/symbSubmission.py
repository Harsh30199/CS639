from z3 import *
import argparse
import json
import sys
import ast
import re
import time

sys.path.insert(0, '../KachuaCore/')
from kast.builder import astGenPass
from sExecutionInterface import *
import z3solver as zs
from irgen import *
from interpreter import *
from sExecution import *

def symbolicExecutionmod(ir, params_mod, timeLimit=10): ###Taken from sExecution.py and minor modifications are made
    """[summary]

    Args:
        ir (List): List of program IR statments
        params (dict): Mapped variables with initial assignments.
        timeLimit (float/int): Total time(sec) to run the fuzzer loop for.

    Returns:
        tuple (coverageInfo, corpus) : Return coverage information and corpus of inputs.
    """
    print(f"[Symbolic Execution] Starting symbolic execution : init args -> {params_mod}")
    
    # Initial Seed values from user.
    # temp_input = InputObject(data=params)
    start_time = time.time()
    # symbolic execution ends at this timestamp.
    endTime = time.time() + timeLimit
    flipPC = []
    s = z3Solver(ir)
    s.initProgramContext(params_mod)
    # The maximum time for symbolic execution of the
    # program must be less than end time.
    rnd1=0
    res = "sat"
    tmplist = []
    testData = {}
    while time.time() <= endTime:
        if str(res)=="sat":
            # print("Testcase: ",rnd1)
            rnd1+=1
            coverage = [] # coverage for current path
            pc = []
            pcEval = []
            output ={}
            inptr = ConcreteInterpreter(ir)
            terminated = False
            inptr.initProgramContext(params_mod)
            while time.time() <= endTime :
                coverage.append(inptr.pc)
                stmt, tgt = ir[inptr.pc]
                if isinstance(stmt, kachuaAST.ConditionCommand):
                    pc.append(inptr.pc)
                terminated = inptr.interpret()
                if isinstance(stmt, kachuaAST.ConditionCommand):
                    pcEval.append(inptr.cond_eval)
                if terminated:
                    for p in params_mod:
                        output[p.replace(':','')] = getattr(inptr.prg,p) ##Modication made here. This stores variable name and its value at the end of execution
                    break
        # print("pc coverage",pc,coverage)
        if time.time() > endTime:
            break
        flipPC += [0 for i in range(len(flipPC),len(pc))]
        # print(flipPC)
        if str(pcEval) not in tmplist:
            tmplist.append(pcEval)
        # print("Coverage: ",coverage,"\nParameters: ",params,"\n\n")
        s.initProgramContext(params_mod)
        s.resetSolver()
        pcIndex=0
        # print("testdata ",testData,pc,pcEval,coverage)
        pc, pcIndex =generateEncryption(s,pcIndex,pc,params_mod,coverage,ir,pcEval)
        if str(res)=="sat":
            data = {}
            
            data['params']=str(params_mod).replace("'",'"')
            
            data['coverage']=str(coverage)
            data['pc']=str(pc)
            data['pcEval']=str(pcEval)
            data['output'] = output ##Modification made here. Variable name and values at end of execution is added to testData dictionary
            symbEnc1={}
            symbEnc = vars(s.z3Vars)
            for k in symbEnc:
                symbEnc1[k]=str(symbEnc[k])
            data['symbEnc']=str(symbEnc1)
            data['constraints']=str(s.s.assertions())
            ##print(data)
            testData[rnd1] = data
        # print("pc before ",pc,pcEval,flipPC)
        pc, pcEval, flipPC, done = genPC(pc, pcEval, flipPC)

        if done:
            print("done break\n\n")
            break
        pcIndex=0
        s.initProgramContext(params_mod)
        s.resetSolver()
        pc, pcIndex =generateEncryption(s,pcIndex,pc,params_mod,coverage,ir,pcEval)
        res = s.s.check()
        if str(res)=="sat":
            m = s.s.model()
            print("model printing",m,type(m))
            for x in m:
                for key in params_mod:
                    if str(x) == key: ##Modification made here. ':'+ removed
                        params_mod[str(x)] = m[x].as_long()
            print(params_mod,"end")
      
    ##json_obj = json.dumps(testData,indent=4)
    
    return testData



def checker(params1,constraints2): ##Function to findout which constraint does the input paramter value match and returing sat or unsat.

    s = zs.z3Solver()
    ##print(params1)
    for p in params1.keys():
        s.addSymbVar(p)  ##Adds parameter to solver as symbolic variable

    for c in constraints2:
        for p in params1.keys():
            ##print(type(p),p)
            s.addConstraint(re.sub(r'\b[%s]\b' % str(p), str(params1[p]) ,str(c))) ##Substitutes variable name with its value in constraint

    ##print(params1,constraints2)
    ##print('aser',s.s.assertions())
    return s.s.check()  ## returns sat if constraint is satisfied and unsat if constraint not satisfied




def checkEq(args,ir):

    file1 = open("../Submission/testData.json","r+") 
    testData=json.loads(file1.read())  ##Reads testData generated from Symbolic Execution
    file1.close()
    s = zs.z3Solver()    ## Creates a object of class zs Solver
    testData = convertTestData(testData)
    print(testData)
    # output = args.output
    
    # TODO: write code to check equivalence

   ## params = list(testData['1']['symbEnc'].keys())
    

    #for c in params:
        #print(c)
        #s.addSymbVar(c.replace(':',''))
        
  
    for testno , case in testData.items(): ##For each test case in testData 

       
        p = case['params']  ## Dictionary of variable name and values 
        interest_var = list(case['symbEnc'].keys()) ## List of variable name computed in symbolic execution
        
        ##Adds variables to solver as symbloic variables by removing ':' from variable name
        for i in interest_var:
            s.addSymbVar(i.replace(':',''))

        
        ##Reoves constant parameter variables from dictionary and list
        for c in case['constparams']:
            del p[c.replace(':','')]
            del interest_var[interest_var.index(c.replace(':',''))]
            
        ##print(p,interest_var)
        
        ##Executes the Turtle Refernece Program to calculate value of output variables for input variable values specified in test case being considered
        inptr = ConcreteInterpreter(ir)
        terminated = False
        inptr.initProgramContext(p)
        context = inptr.prg
        print('\n\n\n-----------Program Execution--------------\n\n')
        while True:
            terminated = inptr.interpret()
            if terminated:
                
                print('\nVariable Values :\n')
                
                for v in interest_var:
                    try:
                        print(v , ':',getattr(context,v)) ##Prints output variable name and its value.
                        
                    except :
                        pass
                
                break
       

       ##Creates constraints to add to solver by modifying constraints from test case by replacing variable name with thier numeric values
        for lhs,rhs in case['symbEnc'].items():
            if(str(lhs) != str(rhs)):
                for v in interest_var:
                    try: 
                        
                        lhs = re.sub(r'\b[%s]\b' % v, str(getattr(context,v)) ,str(lhs))
                        rhs = re.sub(r"\b[%s]\b" % v, str(getattr(context,v)) ,str(rhs))
                    except:
                        pass
                ##print(lhs,rhs)
               
                s.addConstraint(lhs + '==' + rhs) ##Adds constarint to solver

   
    ##Performs Symbolic Execution of Reference Turtle Program by taking seed inputs fromuser

    print('\n\nEnter Seed values for Symbolic Execution of First Program or Reference Program')

    seed_1 ={}

    for a in args.output:
        seed_1 [a] = int(input('Value for %s : ' %a)) ##Takes seed input for each variable in output variable list

    testData_1 = symbolicExecutionmod(ir,seed_1) ##Performs symbolic execution and returns testData in dictionary format
    
    #testData_1 = convertTestData(testData_1)
    ##print(testData_1,'\n\n')

    ##Below Code checks for each new test case generated above from symbolic execution of Reference Turtle Program, which constraint from symbolic execution of turtle program with
    ##constant parameter is satisfied by the parameter value specified in current test case. if a constarint is found, then variable name in symbolic expressions of that test case is replaced with numeric parameter value
    ##and it is added as constraint to z3 Solver. 

    for id1 , case1 in testData_1.items():
       ## print(id1,case1,'\n\n')
        f = 0
        for id2 , case2 in testData.items():
        
            res1 = checker(json.loads(case1['params']),case2['constraints'])

            if(str(res1) == 'sat'):
                f1 = 0
                for lhs,rhs in case2['symbEnc'].items():
                    if(str(lhs) != str(rhs)):
                        for v in case1['output'].keys():
                            try: 
                        
                                lhs = re.sub(r'\b[%s]\b' % v, str(case1['output'][v]) ,str(lhs)) ##Code to replace variable name in lhs with numeric value
                                rhs = re.sub(r"\b[%s]\b" % v, str(case1['output'][v]) ,str(rhs)) ##Code to replace variable name in rhs with numeric value
                            except:
                                pass
                        ##print(lhs,rhs)
                        s.addConstraint(lhs + '==' + rhs) ##Adds constraint to solver
                        f1 = 1
                        break

                    if(f1):
                        f = 1
                        break
            if(f):
                break

    
    
    
    ##print(s.s.assertions()) ##prints list of constraints that have been added to Z3 Solver
    

    if(str(s.s.check()) == 'sat'): ##Checks if all the constraints can be satisfied or not. if satisfied then s.s.check() returns 'sat' else 'unsat'
        print('\n\n-----------------Constant Parameter Values------------------\n\n')

        ans = s.s.model() ##Generates a model with constant parameter values
        for d in ans:
            if ':'+str(d)  in testData['1']['constparams']:
                print(d,'=',ans[d])  ##Prints the computed constant parameter Values


    else:
        print('Two Programs are not Equivalent') ##Outputted when s.s.check() return something other than 'sat'

    print('\n\n')





if __name__ == '__main__':
    cmdparser = argparse.ArgumentParser(
        description='symbSubmission for assignment Program Synthesis using Symbolic Execution')
    cmdparser.add_argument('progfl')
    cmdparser.add_argument(
        '-b', '--bin', action='store_true', help='load binary IR')
    cmdparser.add_argument(
        '-e', '--output', default=list(), type=ast.literal_eval,
                               help="pass variables to kachua program in python dictionary format")
    args = cmdparser.parse_args()
    ir = loadIR(args.progfl)
    checkEq(args,ir)
    exit()
