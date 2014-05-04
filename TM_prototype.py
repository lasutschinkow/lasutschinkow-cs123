# Michael Lasutschinkow
# CMSC 123000 Final Project with Lucy Chen
#
#

import sys
import numpy as np
import pickle
import math

# Test data for prototype

DIR = "TestData/fake_data_20140429"
HITS = DIR + "_hits.txt"
INCIDENCE = DIR + "_incidence.txt"
TRANSITIONS = DIR + "_transitions.txt"

DAMPING = 0.85

# loads pickled numpy matrix from file
def loadmatrix(fn):
    f = open(fn, "r")
    M = pickle.load(f)
    return M

# iToj : Matrix int int int -> num
# returns probability of getting from
# page i to page j within N steps
def iToj(M, i, j, N):
    Prob = 0
    Pr_mx = M
    if(N>=1):
        Prob+=Pr_mx[i,j] 
    for step in range(2,N+1):
        Pr_mx *= Pr_mx
        Prob+=Pr_mx[i,j]
    return Prob
        
# prob_N_Steps : Matrix int -> Matrix
# returns a matrix corresponding to probabilities
# of getting from page i to page j within N steps for all (i,j)
def prob_N_Steps(M, N):
    sz = len(M)
    P = M
    prob_track = [[0 for i in range(0,sz)] for j in range(0,sz)]
    if(N>=1):
        for i in range(0,sz):
            for j in range(0,sz):
                prob_track[i][j] = P[i,j]
    for x in range(2,N+1):
        P *= P
        for i in range(0,sz):
            for j in range(0,sz):
                prob_track[i][j]+=P[i,j]
    res = np.matrix(prob_track)
    return res
        

# graphLinks_i : Matrix -> array
# returns an array where every entry
# is the [# in-links, # out-links]
# for the corresponding page node
# Use with Incidence matrix for accurate results
def graphLinks_i(M):
    l = len(M)
    links = np.array([(0,0) for i in range(0,l)])
    for i in range(0,l):
        out = np.sum(M[i])
        links[i][1] = out
        for j in range(0,l):
            if((i != j) and (M[i,j] > 0)):
                (links[j][0])+=1
    return links


# linkIndexes : Matrix int -> list(int)
# returns a list of nodes with links to given index
def linkIndexes(M,j):
    l = len(M)
    indexes = []
    for i in range(0,l):
        if((j != i) and (M[i,j]>0)):
            indexes.append(i)
    return indexes


# pageRank_simple : Matrix -> array
# returns array where each element is the pageRank
# corresponding to the page at that index
# simple : does not include damping factor or weight by page traffic
def pageRank_simple(M):
    l = len(M)
    links = graphLinks_i(M)
    ranks = np.array([0.0 for x in range(0,l)])
    rk = float(1)/l # all pages have equal weight
    for i in range(0,l):
        numIn = links[i][0]
        indices = linkIndexes(M,i)
        pagerank = 0
        for index in indices:
            pagerank += (rk / float(links[index][1]))
        ranks[i]=pagerank
    return ranks
        
        
# damped_pageRank_simple : Matrix num -> array
# damped page rank, does NOT factor in weight by page traffic    
def damped_pageRank_simple(M,d):
    N = len(M)
    ranks = pageRank_simple(M)
    for i in range(0,N):
        ranks[i] = (1-d)/N + d*ranks[i]
    return ranks
    
    
# pageRank_traffic : Matrix -> array
# pages weighted by traffic (hits) rather than random
# returns array of pageranks without damping





# ========= MAIN =========

def main():
    Hits_mx = loadmatrix(HITS)
    Incidence_mx = loadmatrix(INCIDENCE)
    Transitions_mx = loadmatrix(TRANSITIONS)
    #print type(Transitions_mx)
    #print Transitions_mx
    #print(iToj(Transitions_mx,2,0,2))
    #print prob_N_Steps(Transitions_mx,3)
   # g = graphLinks_i(Incidence_mx)
   # print g
   # i = linkIndexes(Incidence_mx, 3)
   # print i
    s = pageRank_simple(Incidence_mx)
    print s
    print damped_pageRank_simple(Incidence_mx,DAMPING)


    return 0

if __name__=="__main__":
    main()
