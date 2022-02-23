import sys
import graphviz as pgv

sys.path.insert(0,'./ast')
import kachuaAST

def genNode(d=None,id1=None):   ##Creates nodes for CFG
	
	global nodes
	
	if id1 not in nodes.keys():
		
		if(d!=None):
			
			nodes[id1]=d
		
		else:
			
			nodes[id1]=['Termination'] ##Last Node


def targetcalc(ir): ##Calculates targets for jump statements
	
	global t
	t=[]
	
	for idx,item in enumerate(ir):
		
		if(item[1]!=1):
			
			t.append(idx+item[1])

def genCFG(ir):
	
	targetcalc(ir) 
	
	cfg=None
	
	global nodes
	
	nodes=dict() ##Dictionary of nodes with format as node id as key and statements as value
	
	data=[]      ##List to temporarily store statements from code
	
	edges =[]    ##List of edges of CFG
	
	global t
	
	id1=0
	
	for idx, item in enumerate(ir):
		
		if len(data)==0:   ##Condition for initial node containing non conditional statements
			
			id1=idx
			data.append(str(item[0]))
			
			if(item[1]!=1): ##Checks if initial node contains Conditional Satements
				
				genNode(data,id1)
				edges.append([id1,idx+1]) ##Adds edge from condition node to  true statement node 
				edges.append([id1,idx+item[1]]) ##Adds edge from condition node to  false statement node
				
				data=[] ##Signifies new node
		else:
			
			if item[1]==1: ##Checks Assignment Statement or not
				
				if idx not in t: ##Checks if it is a target node then make seperate node
					
					data.append('\n'+str(item[0]))
				
				else:
					
					genNode(data,id1)
					edges.append([id1,idx])
					data=[str(item[0])]
					id1=idx

			else:
				
				if idx not in t: ##Checks if it is a target node then make seperate node
					if(str(item[0])!='False'):
						edges.append([id1,idx+1])

					data.append('\n'+str(item[0]))
					genNode(data,id1)
					edges.append([id1,idx+item[1]])
					
					
				else:
					
					genNode(data,id1)
					edges.append([id1,idx])
					
					genNode([str(item[0])],idx)
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
			
			label+=d
		
		dot.node(str(id1),label,shape='box')

	for e in cfg[1]: ##Reads list of edges and adds each edge to digraph
		
		dot.edge(str(e[0]),str(e[1]))
	
	print('\n\n\n------------ Dot File ----------------\n\n\n')
	
	print(dot.source)
	
	dot.render('../Submission/testcases/cfg.dot',view=True) ##Saves dot and png file
