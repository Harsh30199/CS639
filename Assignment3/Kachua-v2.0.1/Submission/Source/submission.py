import sys
import graphviz as pgv

sys.path.insert(0, '../KachuaCore/ast')

import kachuaAST

from irgen import *

def genNode(d=None,id1=None):   ##Creates nodes for CFG
    
    global nodes
    
    if id1 not in nodes.keys():
        
        if(d!=None):
            
            nodes[id1]=d
        
        else:
            
            nodes[id1]=['Termination'] ##Last Node



def targetcalc(ir): ##Calculates targets for jump statements
    
    global t
    global tdict
    t=[]
    tdict={}
    
    for idx,item in enumerate(ir):
        
        if(item[1]!=1):
            
            t.append(idx+item[1])
            tdict[idx]=idx+item[1]

def genCFG(ir):
    
    
    targetcalc(ir) 
    
    cfg=None
    
    global nodes
    
    nodes=dict() ##Dictionary of nodes with format as node id as key and statements as value
    
    data=[]      ##List to temporarily store statements from code
    
    global edges
    edges =[]    ##List of edges of CFG
    
    global t
    
    id1=0
    
    for idx, item in enumerate(ir):
        
        if len(data)==0:   ##Condition for initial node containing non conditional statements
            
            id1=idx
            data.append(item[0])
            
            if(item[1]!=1): ##Checks if initial node contains Conditional Satements
                
                genNode(data,id1)
                edges.append([id1,idx+1]) ##Adds edge from condition node to  true statement node 
                edges.append([id1,idx+item[1]]) ##Adds edge from condition node to  false statement node
                
                data=[] ##Signifies new node
        else:
            
            if item[1]==1: ##Checks Assignment Statement or not
                
                if idx not in t: ##Checks if it is a target node then make seperate node
                    
                    data.append(item[0])
                
                else:
                    
                    genNode(data,id1)
                    edges.append([id1,idx])
                    data=[item[0]]
                    id1=idx

            else:
                
                if idx not in t: ##Checks if it is a target node then make seperate node
                    if(str(item[0])!='False'):
                        edges.append([id1,idx+1])

                    data.append(item[0])
                    genNode(data,id1)
                    edges.append([id1,idx+item[1]])
                    
                    
                else:
                    
                    genNode(data,id1)
                    edges.append([id1,idx])
                    
                    genNode([item[0]],idx)
                    if(str(item[0])!='False'):
                        edges.append([idx,idx+1])
                    edges.append([idx,idx+item[1]])
                
                data=[]
                
        

    if len(data)!=0 :
        genNode(data,id1) ##Generates penultimate node in case not generated
        edges.append([id1,len(ir)]) ##Adds edge from penultimate node to terminate node
    
    genNode(d=None,id1=len(ir)) ##Generates terminate node
    

    cfg=[nodes,edges] ##Graph like datastructure , list containign nodes and edges
    
    return cfg

def dumpCFG(cfg):
    
    dot = pgv.Digraph(comment='Control Flow Graph',format='png',strict=True) ##Defines graph type 
    
    
    for id1,data in cfg[0].items(): ##Reads nodes dictionary and adds each node and its label to the digraph
        
        label=''
        
        for d in data:
            
            label+= str(d)+'\n'
        
        dot.node(str(id1),label,shape='box')

    for e in cfg[1]: ##Reads list of edges and adds each edge to digraph
        
        dot.edge(str(e[0]),str(e[1]))
    
    print('\n\n\n------------ Dot File ----------------\n\n\n')
    
    print(dot.source)
    
    dot.render('../Submission/testcases/cfg.dot',view=True) ##Saves dot and png file



def predecessor(c,n):  ##Calculates predecessor of nodes in CFG and then filters nodes with more than 1 predecessor
    p={}
    for i in c[0]:
        p[i]= []
    for e in c[1]:
        if(e[0]!=n and e[1]!=n):
            p[e[1]].append(e[0])
    p ={k:v for k,v in p.items() if len(p[k])>1}
    
    return p

def successor(c,n): ##Calculates successor of nodes in CFG and then filters nodes with more than 1 successor
    s={}
    for i in c[0]:
        s[i]= []
    for e in c[1]:
        if(e[0]!=n and e[1]!=n):
            s[e[0]].append(e[1])
    s ={k:v for k,v in s.items() if len(s[k])>1}
    
    
    return s





def blockoptimize(ir): ##Optimizes each block in CFG independently

    genCFG(ir)
    nodes.pop(len(ir)) ##Removes Termination Node
    newidx = {} ##Dictionary to store 
    count1=0   ##No of staements from IR processed
    optidistid = None ##Id of the statement where last optimization was done
    optidir = None    ##Direction of movement optimized forward or backward
    totrot = 0    ##Angle of Kachua between two or more forward/backward instructions
   
    ir2=[]     ##Stores optimized IR

    for idx,node in nodes.items():   ##Iterates over each node in list of nodes of CFG
      
        
        ir2.append([kachuaAST.AssignmentCommand(':optidist', 0),1]) ##Initialization of variable used for optimization 
        optidistid = None
        optidir = None
        totrot = 0
        
        for idx, item in enumerate(node): ##Iterates over each statement of node
            
            
            if isinstance(item, kachuaAST.MoveCommand):
                
                
                if(str(item)[0:7] == 'forward'):
                    
                    if(optidir != 'backward'):
                        if(totrot == 0):
                            ir2.append([kachuaAST.AssignmentCommand(':optidist', ':optidist ' + "+ " + str(item)[8:]),1])
                            
                            count1+=1
                            optidistid = len(ir2)-1

                            
                        
                        else:
                            if optidistid!=None:
                                ir2[optidistid] = [kachuaAST.MoveCommand('forward' ,str(ir2[optidistid][0])[11:]),1]
                            if totrot!=0 :
                                ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
                            

                            totrot=0
                            optidistid=None
                            ir2.append([kachuaAST.AssignmentCommand(':optidist', 0),1])
                            ir2.append([kachuaAST.AssignmentCommand(':optidist', ':optidist ' + "+ " + str(item)[8:]),1])
                            
                            count1+=1
                            optidistid = len(ir2)-1
                    else:
                        if(optidistid!=None):
                            ir2[optidistid] = [kachuaAST.MoveCommand('backward' ,str(ir2[optidistid][0])[11:]),1]
                        if totrot!=0 :
                            ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
                        
                        totrot=0
                        optidistid=None
                        ir2.append([kachuaAST.AssignmentCommand(':optidist', 0),1])
                        ir2.append([kachuaAST.AssignmentCommand(':optidist', ':optidist ' + "+ " + str(item)[8:]),1])
                        
                        count1+=1
                        optidistid = len(ir2)-1

                    optidir = 'forward'
                    newidx[count1-1]=optidistid



                elif(str(item)[0:8] == 'backward'):
                    if(optidir!= 'forward'):
                        if(totrot == 0):
                           
                            ir2.append([kachuaAST.AssignmentCommand(':optidist', ':optidist ' + "+ " + str(item)[8:]),1])
                            optidistid = len(ir2)-1
                            
                            count1+=1
                            
                       
                        else:
                            if(optidistid!=None):
                                ir2[optidistid] = [kachuaAST.MoveCommand('backward' ,str(ir2[optidistid][0])[11:]),1]
                            if totrot!=0 :
                                ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
                            

                            totrot=0
                            optidistid=None
                            ir2.append([kachuaAST.AssignmentCommand(':optidist',0),1])
                            ir2.append([kachuaAST.AssignmentCommand(':optidist', ':optidist ' + "+ " + str(item)[8:]),1])
                            optidistid = len(ir2)-1
                            
                            count1+=1
                    else:
                        if(optidistid!=None):
                            ir2[optidistid] = [kachuaAST.MoveCommand('forward' ,str(ir2[optidistid][0])[11:]),1]
                        if totrot!=0 :
                            ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
                        
                        totrot=0
                        optidistid=None
                        ir2.append([kachuaAST.AssignmentCommand(':optidist', 0),1])
                        ir2.append([kachuaAST.AssignmentCommand(':optidist', ':optidist ' + "+ " + str(item)[8:]),1])
                        optidistid = len(ir2)-1
                        
                        count1+=1

                    optidir = 'backward'
                    newidx[count1-1]=optidistid

                elif(str(item)[0:5]== 'right'):
                    
                    totrot = (totrot + int(str(item)[6:]))%360
                    
                    if count1 in t:
                        newidx[count1]=len(ir2)
                    count1+=1

                    
                else:
                    
                    totrot = (totrot - int(str(item)[5:]))%360
                    
                    if count1 in t:
                        newidx[count1]=len(ir2)
                    count1+=1
                        


                

            elif isinstance(item, kachuaAST.PenCommand):
                
                if totrot!=0 :
                    ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
                    totrot = 0
                    
                if optidistid !=None :
                    ir2[optidistid] = [kachuaAST.MoveCommand(optidir ,str(ir2[optidistid][0])[11:]),1]
                    totrot=0
                    optidistid=None
                    optidir=None
            
                ir2.append([kachuaAST.PenCommand(str(item)),1])
                newidx[count1]= len(ir2)-1
                
                count1+=1
                ir2.append([kachuaAST.AssignmentCommand(':optidist', 0),1])

            elif isinstance(item, kachuaAST.GotoCommand):
                
                if totrot!=0 :
                    ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
                    totrot = 0
                    
                if optidistid !=None :
                    ir2[optidistid] = [kachuaAST.MoveCommand(optidir ,str(ir2[optidistid][0])[11:]),1]
                    totrot=0
                    optidistid=None
                    optidir=None
            
                ir2.append([item,1])
                newidx[count1]= len(ir2)-1
                
                count1+=1
                ir2.append([kachuaAST.AssignmentCommand(':optidist', 0),1])
                
            
            elif isinstance(item, kachuaAST.ConditionCommand):
                if totrot!=0 :
                    ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
                    totrot=0
                    
                if optidistid !=None :
                    
                    ir2[optidistid] = [kachuaAST.MoveCommand(optidir ,str(ir2[optidistid][0])[11:]),1]
                    totrot=0
                    optidistid=None
                    optidir=None

                    

                
                ir2.append([kachuaAST.ConditionCommand(str(item)),0])
                
                newidx[count1]= len(ir2)-1
                
                count1+=1


            else:
                if(item=='False'):
                    ir2.append([kachuaAST.ConditionCommand(str(item)),0])
                else:
                    ir2.append([item,1])
                newidx[count1]= len(ir2)-1
                
                count1+=1

            


                

        if(optidir!=None):
            ir2[optidistid]=[kachuaAST.MoveCommand(optidir ,str(ir2[optidistid][0])[11:]),1]
            

            newidx[count1]= optidistid

        if(totrot!=0):
            ir2.append([kachuaAST.MoveCommand('right',str(totrot)),1])
           
            newidx[count1-1]=len(ir2) -1


            
###Below lines of code take index of instruction from old ir and new ir and update relative jumps for required instructions.

    newidx[len(ir)]=len(ir2)
   
    
    nklist = list(newidx.keys())
    nvlist = list(newidx.values())
    for idx,item in enumerate(ir2):
        
        if(int(item[1])!=1):
            if(newidx[tdict[nklist[nvlist.index(idx)]]] != len(ir2)):
                ir2[idx] = (item[0],newidx[tdict[nklist[nvlist.index(idx)]]]-(idx)-1)
            else:
                ir2[idx] = (item[0],newidx[tdict[nklist[nvlist.index(idx)]]]-(idx))


    return ir2



def calcfacts(c,t,l):  ##Finds first and last movement statemenrts in a node and stores relevant information
    facts={}
    
    for idx in l:
        node = c[0][idx]
        totrot = 0
        optidir = None
        ids={'m':None,'r':None,'r0':[]}
        facts[idx]={'head':None,'tail':None}
        for i in range(len(node)):
            if (isinstance(node[i], kachuaAST.MoveCommand)):
                if(str(node[i])[0:8] == 'backward'):  
                    optidir = 'backward'
                    ids['m']=idx+i
                    facts[idx]['head'] = [optidir,totrot,ids]
                    break

                if(str(node[i])[0:7] == 'forward'):
                    optidir = 'forward'
                    ids['m']=idx+i
                    facts[idx]['head'] = [optidir,totrot,ids]
                    break

                if(str(node[i])[0:5]== 'right'):
                    totrot = (totrot + int(str(node[i])[6:]))%360
                    ids['r']=idx+i
                    facts[idx]['head'] = [optidir,totrot,ids]

            elif(isinstance(node[i], kachuaAST.PenCommand) or isinstance(node[i],kachuaAST.GotoCommand)):
                facts[idx]['head'] = [optidir,totrot,ids]
            elif(str(node[i]) == ':optidist = 0'):
                ids['r0'].append(idx + i) 

        totrot = 0
        optidir = None
        ids={'m':None,'r':None}

        for i in range(len(node)-1,-1,-1):
            if (isinstance(node[i], kachuaAST.MoveCommand)):
                if(str(node[i])[0:8] == 'backward'):  
                    optidir = 'backward'
                    ids['m']=idx+i
                    facts[idx]['tail'] = [optidir,totrot,ids]
                    break

                if(str(node[i])[0:7] == 'forward'):
                    optidir = 'forward'
                    ids['m']=idx+i
                    facts[idx]['tail'] = [optidir,totrot,ids]
                    break

                if(str(node[i])[0:5]== 'right'):
                    totrot = (totrot + int(str(node[i])[6:]))%360
                    ids['r']=idx+i
                    facts[idx]['tail'] = [optidir,totrot,ids]

            elif(isinstance(node[i], kachuaAST.PenCommand) or isinstance(node[i],kachuaAST.GotoCommand)):
                facts[idx]['tail'] = [optidir,totrot,ids]

    idx = t
    node = c[0][idx]
    totrot = 0
    optidir = None
    ids={'m':None,'r':None,'r0':[]}
    facts[idx]={'head':None,'tail':None}
    for i in range(len(node)):
        if (isinstance(node[i], kachuaAST.MoveCommand)):
            if(str(node[i])[0:8] == 'backward'):  
                optidir = 'backward'
                ids['m']=idx+i
                facts[idx]['head'] = [optidir,totrot,ids]
                break

            if(str(node[i])[0:7] == 'forward'):
                optidir = 'forward'
                ids['m']=idx+i
                facts[idx]['head'] = [optidir,totrot,ids]
                break

            if(str(node[i])[0:5]== 'right'):
                totrot = (totrot + int(str(node[i])[6:]))%360
                ids['r']=idx+i
                facts[idx]['head'] = [optidir,totrot,ids]

        elif(isinstance(node[i], kachuaAST.PenCommand) or isinstance(node[i],kachuaAST.GotoCommand)):
            facts[idx]['head'] = [optidir,totrot,ids]
        elif(str(node[i]) == ':optidist = 0'):
            ids['r0'].append(idx + i) 

    totrot = 0
    optidir = None
    ids={'m':None,'r':None}

    for i in range(len(node)-1,-1,-1):
        if (isinstance(node[i], kachuaAST.MoveCommand)):
            if(str(node[i])[0:8] == 'backward'):  
                optidir = 'backward'
                ids['m']=idx+i
                facts[idx]['tail'] = [optidir,totrot,ids]
                break

            if(str(node[i])[0:7] == 'forward'):
                optidir = 'forward'
                ids['m']=idx+i
                facts[idx]['tail'] = [optidir,totrot,ids]
                break

            if(str(node[i])[0:5]== 'right'):
                totrot = (totrot + int(str(node[i])[6:]))%360
                ids['r']=idx+i
                facts[idx]['tail'] = [optidir,totrot,ids]

        elif(isinstance(node[i], kachuaAST.PenCommand)or isinstance(node[i],kachuaAST.GotoCommand)):
            facts[idx]['tail'] = [optidir,totrot,ids]


    return facts







def optimize(ir):

    
    
    ir2 = blockoptimize(ir)  ##Block Level Optimization is done
    
    c = genCFG(ir2) ##Generates CFG for new IR
    
    pred = predecessor(c,len(ir2))  ##Calculates Predecessor
    succ = successor(c,len(ir2))   ##Calculates Successor

    

    
    ##Below lines optimize nodes which have multiple successors

    for t,suc in succ.items():
        facts = calcfacts(c,t,suc)
        
        flag1=False
        for s in suc:
            
            if(facts[t]['tail']!=None and  facts[s]['head']!=None):
                if(facts[t]['tail'][0] == facts[s]['head'][0]):
                    if(facts[t]['tail'][1]!=None and  facts[s]['head'][1]!=None):
                        if(((facts[t]['tail'][1]+facts[s]['head'][1]))%360 == 0):
                            
                            flag1 = True
                        else:
                            flag1=False
                            break
                    else:
                        flag1=False
                        break
                else:
                    flag1=False
                    break
            else:
                flag1 = False
                break
        
        
        if(flag1):
            
            for s in suc:
                for i in facts[s]['head'][2]['r0']:
                    removeInstruction(ir2,i)
                    ir2[i]=[ir2[i][0],1]

               
                if(facts[s]['head'][2]['r']!=None):
                    ir2[facts[s]['head'][2]['r']] = [kachuaAST.MoveCommand('right',0),1]


            if(facts[t]['tail'][2]['r']!=None):
                ir2[facts[t]['tail'][2]['r']] = [kachuaAST.MoveCommand('right',0),1]
            if(facts[t]['tail'][2]['m']!=None and facts[t]['tail'][0]=='backward'):
                ir2[facts[t]['tail'][2]['m']] = [kachuaAST.AssignmentCommand(':optidist', str(ir2[facts[t]['tail'][2]['m']][0])[8:]),1]
                    
            if(facts[t]['tail'][2]['m']!=None and facts[t]['tail'][0]=='forward'):
                ir2[facts[t]['tail'][2]['m']] = [kachuaAST.AssignmentCommand(':optidist', str(ir2[facts[t]['tail'][2]['m']][0])[7:]),1]

    
##Below lines optimize nodes with multiple predecessors
    for t,pre in pred.items():
        facts = calcfacts(c,t,pre)
        
        flag1=False
        for p in pre:
            if(facts[t]['head']!=None and  facts[p]['tail']!=None):
                if(facts[t]['head'][0] == facts[p]['tail'][0]):
                    if(facts[t]['head'][1]!=None and  facts[p]['tail'][1]!=None):
                        if(((facts[t]['head'][1]+facts[p]['tail'][1]))%360 == 0):
                            flag1 = True
                        else:
                            flag1=False
                            break
                    else:
                        flag1=False
                        break
                else:
                    flag1=False
                    break
            else:
                flag1 = False
                break

       
        if(flag1):
            for i in facts[t]['head'][2]['r0']:
                removeInstruction(ir2,i)
                ir2[i]=[ir2[i][0],1]
            for p in pre:
                if(facts[p]['tail'][2]['r']!=None):
                    ir2[facts[p]['tail'][2]['r']] = [kachuaAST.MoveCommand('right',0),1]
                if(facts[p]['tail'][2]['m']!=None and facts[p]['tail'][0]=='backward'):
                    ir2[facts[p]['tail'][2]['m']] = [kachuaAST.AssignmentCommand(':optidist', str(ir2[facts[p]['tail'][2]['m']][0])[8:]),1]
                if(facts[p]['tail'][2]['m']!=None and facts[p]['tail'][0]=='forward'):
                    ir2[facts[p]['tail'][2]['m']] = [kachuaAST.AssignmentCommand(':optidist', str(ir2[facts[p]['tail'][2]['m']][0])[7:]),1]

            if(facts[t]['head'][2]['r']!=None):
                ir2[facts[t]['head'][2]['r']] = [kachuaAST.MoveCommand('right',0),1]
            


##Prints the final Optimized IR geerated

    print('\n\n------------------------ OPTIMIZED IR -------------------------------------\n\n')
    for idx , item in enumerate(ir2):
        print(idx,str(item[0]),item[1])
   
    return ir2 ##Returns optimized IR to Kachua.py
    
