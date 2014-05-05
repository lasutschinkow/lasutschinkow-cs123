# Michael Lasutschinkow
# CMSC 123000 Final Project with Lucy Chen
#
# PageRank_prototype.py
#
#

import sys
import numpy as np
import pickle
import math
import make_visual

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

def sum_over_column(mat,col):
    return np.sum(mat[:,col])



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



# sumTM : Matrix int num -> Matrix
# returns the matrix sum of (damp * M)^i
# for i between 1 and N
def sumTM(M,N,damp):
    l = len(M)
    sum_arr = np.array([[0.0 for i in range(0,l)] for j in range(0,l)])
    sum_mx = np.matrix(sum_arr)
    for n in range(1,N+1):
        TM = prob_N_Steps((damp*M),n)
        sum_mx += TM
    return sum_mx

# hitsMx : (listof list) -> matrix
# Turns the initial hits list into an Nx1 matrix
def hitsMx(hits_list):
    l = len(hits_list)
    arr = np.array([[0] for x in range(0,l)])
    for i in range(0,l):
        m = len(hits_list[i])
        for j in range(1,m):
            arr[i]+=hits_list[i][j]
    return np.matrix(arr)

# numHits : sums over the list of hits, returns total
def numHits(hits_list):
    l = len(hits_list)
    count = 0
    for i in range(0,l):
        m = len(hits_list[i])
        for j in range(1,m):
            count+=hits_list[i][j]
    return count

# sum_vec : sums over 1-dimensional vector of numbers
def sum_vec(v):
    num = 0.0
    l = len(v)
    for i in range(0,l):
        num+=v[i]
    return num


# diff_vec : Matrix Matrix -> Vector
# Takes in a summed transition matrix and hits matrix
# Calculates the percent difference between expected hits (by model)
# and actual hits (by data), returns a vector of the values
def diff_vec(TM_sum, hits_mx):
    l = len(TM_sum)
    total_real_hits = sum_vec(hits_mx).tolist()[0][0]
    proj_hits = np.array([[0] for i in range(0,l)])
    for i in range(0,l):
        proj_hits[i]+=sum_over_column(TM_sum,i)
    difference_vector = np.array([[0.0] for i in range(0,l)])
    total_proj_hits = sum_vec(proj_hits).tolist()[0]
    for i in range(0,l):
        proj = float(proj_hits[i][0])/total_proj_hits
        actual = float(hits_mx[i].tolist()[0][0])/total_real_hits
        x = proj if (proj != 0) else 1
        diff = float(actual-proj)/x
        difference_vector[i]+=diff
    return difference_vector
        


# Compare difference vectors
# used by find_optimal_k
def compare_vec(dvec1, dvec2):
    diff = 0
    l = len(dvec1)
    for i in range(0,l):
        v1 = dvec1[i].tolist()[0]
        v2 = dvec2[i].tolist()[0]
        d = abs(v2-v1)
        if(d > diff):
            diff = d
    return diff



# Attempt to let the computer find optimal number of iterations
# want : the difference vector has no entries changing by more than .001 between iterations
def find_optimal_k(transMx,hitsMx,damping):
    k = 2
    within = .05
    # WARNING : do not set within smaller than .05 in this current setup
    # I tried .01 and it took 70 iterations and about 5 minutes

    sum1 = sumTM(transMx,1,damping)
    sum2 = sumTM(transMx,2,damping)
    dv1 = diff_vec(sum1,hitsMx)
    dv2 = diff_vec(sum2,hitsMx)

    while(compare_vec(dv1,dv2)>=within):
        k+=1
        sum1 = sum2
        dv1 = dv2
        sum2 = sumTM(transMx,k,damping)
        dv2 = diff_vec(sum2,hitsMx)



        # There is a hell of a lot of room for optimization in this code

    s = "The optimum number of iterations to get variation of less than %f is K = %d" %(within,k)
    return (dv2,sum2,s) # Diff Vec, Final Transition Matrix sum after k iterations, string
        
    








# ========= MAIN =========

def main():
    Hits_list = loadmatrix(HITS)
    Incidence_mx = loadmatrix(INCIDENCE)
    Transitions_mx = loadmatrix(TRANSITIONS)
    H = hitsMx(Hits_list)
    n = numHits(Hits_list)
    # print " "
    opt = find_optimal_k(Transitions_mx,H,DAMPING)
    dv = opt[0]
    tmSum = opt[1]
    kstr = opt[2]
    print " "
    print kstr
    print " "



    # read to file
    FN = "TestData/"
    f = open(FN + "diff_vec.txt", "w")
    pickle.dump(opt[0],f)
    f.close()
    f = open(FN + "tmSum.txt", "w")
    pickle.dump(opt[1],f)
    f.close()
    
    
    # make graph
    d = {}
    for i in range(0,50):
        d[str(i)] = i
    nodelist = []
    for i in range(0,50):
        nodelist.append([str(i)])


    # print nodelist
    # print " "
    # print d


    make_visual.do_makezoomgraph(20,50,nodelist,d,dv,tmSum,"Model_Results/graph2.png","")
    






    return 0

if __name__=="__main__":
    main()
