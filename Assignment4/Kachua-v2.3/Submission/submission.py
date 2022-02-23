
import sys
sys.path.insert(0, "KachuaCore/interfaces/")
from interfaces.fuzzerInterface import *
import numpy as np
import time
import random
import matplotlib.pyplot as plt 


plt.rcParams["figure.figsize"] = (20,10) ##Sets Graph Size

# make sure dot or xdot works and grapviz is installed.
# Uncomment for Assignment-2
# sys.path.append("KachuaCore/kast")
# import kast.kachuaAST
# import graphviz

class CustomCoverageMetric(CoverageMetricBase):
    # Statements covered is used for 
    # coverage information.
    counter = 0 ##Keeps track of no of iterations

    len_totmet = {0:0} ## Tracks length of total_metric at each iteration
    
    def __init__(self):
        super().__init__()

    # TODO : Implement this
    def compareCoverage(self, curr_metric, total_metric):
        # must compare curr_metric and total_metric
        # True if Improved Coverage else False
        self.counter+=1

        print("Coverage Percent after execution of Mutation :",(max(0,(len(curr_metric)-1))/irlen)*100)  ##Prints Coverage Percent after executing Mutation

        ##Checks for every item in curr_metric if not present in total_metric then coverage improved

        for metric in curr_metric:
            if metric not in total_metric:
                return True
        
        self.len_totmet[self.counter] = len(total_metric)-1

        self.graphplotter()
        
        return False

    # TODO : Implement this
    def updateTotalCoverage(self, curr_metric, total_metric):
        # Compute the total_metric coverage and return it (list)
        # this changes if new coverage is seen for a 
        # given input.
        
         ##Checks for every item in curr_metric if not present in total_metric then appends it to total_metric

        for metric in curr_metric:
            if metric not in total_metric:
                total_metric.append(metric)

        self.len_totmet[self.counter] = len(total_metric)-1 ##Updates len_totmet when there is improvement at some iteration

        print("Total Coverage Percent after execution of Mutation :",(max(0,(len(total_metric)-1))/irlen)*100)  ##Prints Total Coverage Percent after executing  Mutation

        self.graphplotter()

        return total_metric

    
    ## Plots a line graph depicting Length of total_metric V/S Iteration no

    def graphplotter(self):

        fig , ax = plt.subplots(1)

        values = list(self.len_totmet.values())

        keys = list(self.len_totmet.keys())

        
        ax.plot(keys,values)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Length of Total Metric")
        ax.set_title('Length of Total Metric V/S Iteration')
        fig.savefig('../Submission/graph.png', bbox_inches='tight')

class CustomMutator(MutatorBase):
    
    one_time = 0 ##To keep print IR just once
   
    def __init__(self):
        pass

    # TODO : Implement this
    def mutate(self, input_data, coverageInfo, irList):
        # Mutate the input data and return it
        # coverageInfo is of type CoverageMetricBase
        # Don't mutate coverageInfo
        # irList : List of IR Statments (Don't Modify)
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.
        
        global irlen

        irlen = len(irList)       
        
        if(self.one_time==0):
            
            print("\n\n\n-------------- IR--------------\n\n\n")
            
            for idx,item in enumerate(irList):
                print(idx,str(item[0]),str(item[1]))
            print('\n\n\n')
            self.one_time+=1

        ##for idx,item in input_data.data.items():
            
            ##print('entryinputdata',idx,item)



        for idx,val in input_data.data.items():
            np.random.seed()
            
            bin_val = bin(val) ##Converts integer base 10 into binary format
            mod_val,bin_val = bin_val.split('b')
            mod_val+='b'
            
            if(val in [0,1,-1]):
              bin_val = '0000000' + bin_val 
                
            
            a = np.random.randint(0,1000) % 10
                    
            if a in [0,3,4,5,6,7,8,9]:
               
                b = np.random.randint(1,len(bin_val))
                index = random.sample([x for x in range(len(bin_val))],b)

                for i in range (0,len(bin_val)):
                    
                    mod_val+= bin_val[i] if i not in index else '1' if bin_val[i] == '0' else '0'
                    

            elif a ==1:

                a = np.random.randint(0,100) % 4

                if a==0:
                    input_data.data[idx] = 300
                    
                elif a==1:
                    input_data.data[idx]= -300
                
                elif a==2:
                    input_data.data[idx]= 0
                
                elif a==3:
                    input_data.data[idx]= 1
                    

                continue

            elif a==2:
                
                input_data.data[idx] = -1 * int(bin_val,2)
                continue

            input_data.data[idx]=int(mod_val,2)  ##Converts binary to back to integer base 10



       

        return input_data



# Reuse code and imports from 
# earlier submissions (if any).
def genCFG(ir):
    # your code here
    cfg = None
    return cfg

def dumpCFG(cfg):
    # dump CFG to a dot file
    pass

def optimize(ir):
    # create optimized ir in ir2
    ir2 = ir # currently no oprimization is enabled
    return ir2
