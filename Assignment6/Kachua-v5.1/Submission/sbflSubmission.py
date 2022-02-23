#!/usr/bin/env python3

import argparse
import sys
import numpy as np
sys.path.insert(0,'../KachuaCore/')
from irgen import *
from kast.builder import astGenPass
from sbfl import *
import csv
import time
def fitnessScore(IndividualObject):
    """
    Parameters
    ----------
    IndividualObject : Individual (definition of this class is in KachuaCore/sbfl.py)
        This is a object of class Individual. The Object has 3 elements
        1. IndividualObject.individual : activity matrix.
                                    type : list, row implies a test
                                    and element of rows are components.
        2. IndividualObject.fitness : fitness of activity matix.
                                    type : float
        3. Indivisual.fitness_valid : a flag used by Genetic Algorithm.
                                    type : boolean
    Returns
    -------
    fitness_score : flaot
        returns the fitness-score of the activity matrix.
        Note : No need to set/change fitness and fitness_valid attributes.
    """
    #Design the fitness function
    fitness_score = 0
    activity_mat = np.array(IndividualObject.individual,dtype='int');
    activity_mat = activity_mat[:,:activity_mat.shape[1]-1]
    #Use 'activity_mat' to compute fitness of it.
    #ToDo : Write your code here to compute fitness of test-suite

    
    
    fitness_score = ddumetric(activity_mat)
   
    return fitness_score

def ddumetric(activity_mat):
    fscore = 0
    nrows = activity_mat.shape[0]
    ncols = activity_mat.shape[1]
   
    
    if nrows == 0:
        return 0

    density = np.sum(activity_mat) / (nrows*ncols)

    uniqtest_dict={}
  
    for i in activity_mat:
        if str(i) not in uniqtest_dict.keys():
            uniqtest_dict[str(i)] = 1
        else:
            uniqtest_dict[str(i)]+=1
    if nrows>1:
        diversity = 1 - np.sum([x*(x-1) for x in uniqtest_dict.values()])/((nrows-1)*nrows)
    else:
        diversity = 1
    uniqcomp_dict = {}
    for i in range(ncols):
        if str(activity_mat[:,i]) not in uniqcomp_dict.keys():
            uniqcomp_dict[str(activity_mat[:,i])] = 1
        else:
            uniqcomp_dict[str(activity_mat[:,i])]+=1

    
    uniqueness = len(uniqcomp_dict.keys())/ ncols

    fscore = diversity * uniqueness * (1-np.abs(1-2*density))

    for i in range(ncols):
        if np.sum(activity_mat[:,i])==0:
            fscore-=1
   
    return -1*fscore


def ulysis(activity_mat):
    ncols = activity_mat.shape[1]
    sum1 = 0
    for i in range(ncols):
        count = 0
      
        if (sum(activity_mat[:,i]) != 0):
            for j in range(ncols):
                if(str(activity_mat[:,i]) == str(activity_mat[:,j])):
                   count+=1
        
            sum1 += (count-1)/(ncols-1)
        else:
            sum1 += ncols
            
    sum1 /= ncols

    return (sum1)



    
#This class takes a spectrum and generates ranks of each components.
#finish implementation of this class.
class SpectrumBugs():
    def __init__(self,spectrum):
        self.spectrum = np.array(spectrum,dtype='int')        
        self.comps = self.spectrum.shape[1] - 1
        self.tests = self.spectrum.shape[0]
        self.activity_mat = self.spectrum[:,:self.comps]
        self.errorVec = self.spectrum[:,-1]

    def getActivity(self,comp_index):
        '''
        get activity of component 'comp_index'
        Parameters
        ----------
        comp_index : int
        '''
        return self.activity_mat[:,comp_index]

    def suspiciousness(self,comp_index):
        '''
        Parameters
        ----------
        comp_index : int
            component number/index of which you want to compute how suspicious
            the component is. assumption: if a program has 3 components then
            they are denoted as c0,c1,c2 i.e 0,1,2
        Returns
        -------
        sus_score : float
            suspiciousness value/score of component 'comp_index'
        '''
        sus_score = 0
        #ToDo : implement the suspiciousness score function.
      

        Cf = Cp = Nf  = Np =0
        activity_pattern = self.getActivity(comp_index)
        
        for i in range(self.tests):
            if(self.errorVec[i] == 1 and activity_pattern[i]==1):
                Cf+=1
            elif(self.errorVec[i] == 0 and activity_pattern[i]==1):
                Cp+=1
            elif(self.errorVec[i] == 1 and activity_pattern[i]==0):
                Nf+=1
            else:
                Np+=1

        ##print(Cf,Cp,Nf,Np)
        if(Cf==0):
            return 0
        sus_score = (Cf)/np.sqrt((Cf+Nf)*(Cp+Cf))
                


        
        return sus_score
    def getRankList(self):
        '''
        find ranks of each components according to their suspeciousness score.
        
        Returns
        -------
        rankList : list
            ranList will contain data in this format:
                suppose c1,c2,c3,c4 are components and their ranks are
                1,2,3,4 then rankList will be :
                    [[c1,1],
                     [c2,2],
                     [c3,3],
                     [c4,4]]
        '''
        rankList = []
        print('\n\n--------------------------------Spectrum---------------------------------\n\n')
        print(self.spectrum)
        susp_score = []
        for i in range (self.comps):
            susp_score.append([self.suspiciousness(i),i])

      
        sort_susp_score = sorted(susp_score,reverse = True)
        print('\n\n--------------------------------Sorted Suspiciousness Score---------------------------------\n\n')
        for i in range(self.comps):
            print('Component',sort_susp_score[i][1],':',sort_susp_score[i][0])
        for i in range(self.comps):
            rankList.append(['c'+str(i),sort_susp_score.index(susp_score[i])+1])
        print('\n\n--------------------------------Rank List---------------------------------\n\n')   
        for i in range(self.comps):
            print('Component',rankList[i][0],':',rankList[i][1])
        
        return rankList

#do not modify this function.
def computeRanks(spectrum,outfilename):
    '''
    Parameters
    ----------
    spectrum : list
        spectrum
    outfilename : str
        components and their ranks.
    '''
    S = SpectrumBugs(spectrum)
    rankList = S.getRankList();
    with open(outfilename,"w") as file:
        writer = csv.writer(file)
        writer.writerows(rankList) 
