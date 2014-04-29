import pickle
import random
import numpy as np

#settings (too lazy to code a nice sys.args thing)
FILENAME = "fake_data_20140429" #output file prefix

NUMBER_NODES = 50
APPX_SINKS = 4
APPX_SOURCES = 7
DENSITY = 2 #1 in [density] chance of spawning an edge. doesn't consider the influence of also creating sinks/sources.
BIAS_FACTOR = 2 #adds an additional 1/2 chance of having an edge. eg for density = 2, bias = 2, sinks will have about 1/4 of all possible out-vectors, sources will have a bit more than 3/4 of all possible out-vectors.
MAX_HIT = 100
MIN_HIT = 0


#column indices
TIME_RANGE_START = 50 #determines where the "week" we want starts (diff is number of hours)
TIME_RANGE_END = 60 


def makehits(array): #pass in array full of zeroes
#    random.seed()
    numrows = len(array)
    rowrange = range(TIME_RANGE_START, TIME_RANGE_END)
    for row_i in range(0, NUMBER_NODES):
        row = array[row_i]
        row[0] = "node number " + str(row_i)
        for j in rowrange:
            row[j] = random.randint(MIN_HIT, MAX_HIT)
    return array #not necessary but good style

def makegraph(): #creates an INCIDENCE MATRIX for a graph
    matrix = np.matrix([[0 for i in range(0, NUMBER_NODES)] for j in range(0, NUMBER_NODES)])
    all_nodes = range(0, NUMBER_NODES)
    specialnodes = random.sample(all_nodes, APPX_SINKS + APPX_SOURCES)
    sinks = specialnodes[:APPX_SINKS]
    sources = specialnodes[APPX_SINKS:]
    for node_from in all_nodes:
        for node_to in all_nodes:
            rolldie = random.randint(0, DENSITY)
            if rolldie == 0: #create edge
                matrix[node_from,node_to] = 1
        #we have an incidence vector for out-edges
    #sloppily create sinks and sources
    for node in sinks:
        for node_to in all_nodes:
            rolldie = random.randint(0, BIAS_FACTOR)
            if rolldie == 0: #delete edge
                matrix[node,node_to] = 0
    for node in sources:
        for node_to in all_nodes:
            rolldie = random.randint(0, BIAS_FACTOR)
            if rolldie == 0: #add edge
                matrix[node,node_to] = 1
    return matrix

def maketransitions(incidence): #takes in incidence matrix, returns equalized transitions
    nodes = range(0, NUMBER_NODES)
    transitions = [[0 for i in range(0, NUMBER_NODES)] for j in range(0, NUMBER_NODES)]
    for node in nodes:
        total_edges = np.sum(incidence[node])
        transitions[node] = (incidence[node] / float(total_edges)).tolist()[0]
    transitions = np.matrix(transitions)
    return transitions


if __name__=="__main__":
    array = [[0 for i in range(0,TIME_RANGE_END)] for j in range(0, NUMBER_NODES)]
    makehits(array)
    incidence = makegraph()
    transition = maketransitions(incidence)    
    f = open(FILENAME + "_hits.txt", "w")
    pickle.dump(array, f)
    f.close()
    f = open(FILENAME + "_incidence.txt", "w")
    pickle.dump(incidence, f)
    f.close()
    f = open(FILENAME + "_transitions.txt", "w")
    pickle.dump(transition, f)
    f.close()


