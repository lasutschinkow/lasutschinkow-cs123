# Lucy Chen
# For CMSC12300 Final Project with Michael Lasutschinkow
#
# * * * To use this:
# first import this file.
# then call the function:
#   do_makegraph(number of nodes, array of links (or some other array with node IDs), dictionary of node IDs to keywords, the difference vector, any transition matrix, filename for saving the image, non-empty filename to save a pickle under that filename)
#
# To avoid remaking the graph data, you can load a previously created pickle and call drawgraph(unpickled graph object, filename for saving the image).
#
# * * *


import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
import numpy as np
import sys
import pickle

# ------------------------------------- Pieces used to make Graph ---------------------------------------------

SERIAL_INDEX = 0 #index of the page's ID in the linkarray array.

class graphobj:
    def __init__(self, graph, nodes_ordered, nodeweights, edgeweights, vmin, vmax):
        self.graph = graph
        self.nodes_ordered = nodes_ordered
        self.nodeweights = nodeweights
        self.edgeweights = edgeweights
        self.vmax = vmax
        self.vmin = vmin

def makecolormap():
# adapted from http://matplotlib.org/examples/pylab_examples/custom_cmap.html

    cdict = {'red':  ((0.0, 1.0, 1.0),
                       (0.5, 1.0, 1.0),
                       (1.0, 0.0, 0.0)),

             'green': ((0.0, 0.0, 0.0),
                       (0.5, 1.0, 1.0),
                       (1.0, 1.0, 1.0)),

             'blue':  ((0.0, 0.0, 0.0),
                       (0.5, 1.0, 1.0),
                       (1.0, 0.0, 0.0))
            }

    return cdict


def makegraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx):
    #the ordering of keywords is preserved: first row in linkarray is the first node... etc.
    #keyword_dict maps linkarray serial numbers to human readable names

    G = nx.DiGraph() #initializes empty graph
    #I think I need to keep labels in separate vectors
    edgeweights = []
    nodes_ordered = []

    #grow nodes
    for i in range(0, num_nodes):
        #with each node, associate the human-readable name, and the calculated difference value
        label = keyword_dict[linkarray[i][SERIAL_INDEX]]
        G.add_node(label, index=i, diff=diff_vector[i])
        nodes_ordered.append(label) #this is important to keep nodes in a canonical order so we can color them correctly later
    #grow edges
    for i in range(0, num_nodes):
        for j in range(0, num_nodes):
            p_from_i_to_j = transition_mtx[i,j]                
            if p_from_i_to_j > 0:
                label1 = keyword_dict[linkarray[i][SERIAL_INDEX]]
                label2 = keyword_dict[linkarray[j][SERIAL_INDEX]]
                G.add_edge(label1,label2, weight=p_from_i_to_j)
                edgeweights.append(p_from_i_to_j)
    vmax = max(diff_vector)
    vmin = min(diff_vector)
    #make nodeweights from diff_vector (nodeweights has values from 0 to 1)
    #we want to do a linear mapping, vmin -> 0, 0 -> 1/2, vmax -> 1
    if vmin > 0:
        print "Impossible! vmin > 0!"
        sys.exit()
    if vmax < 0:
        print "Impossible! vmax < 0!"
        sys.exit()
    #else nondegenerate
    nodeweights = list(diff_vector)
    for i in range(0, num_nodes):
        unscaled = nodeweights[i]
        if unscaled < 0:
            scaled = 0.5 - 0.5 * (float(unscaled) / vmin)
        else: #unscaled nonnegative
            scaled = 0.5 + 0.5 * (float(unscaled) / vmax)
        nodeweights[i] = scaled
    newgraph = graphobj(G, nodes_ordered, nodeweights, edgeweights, vmin, vmax)

    return newgraph


def drawgraph(graphobj, filename):
    mycolormap = makecolormap()
    plt.register_cmap(name='BlueRed', data=mycolormap)
    plt.rcParams['image.cmap'] = 'BlueRed'

#    Normalize(vmax=graphobj.vmax, vmin=graphobj.vmin)

#    nx.draw_networkx(graphobj.graph, with_labels=True, node_color=graphobj.nodeweights, edge_color=graphobj.edgeweights, cmap='BlueRed')
    nx.draw_networkx(graphobj.graph, nodelist=graphobj.nodes_ordered, with_labels=True, node_color=graphobj.nodeweights, cmap='BlueRed') #forget about edge colorings for now, they don't look very good
    plt.savefig(filename)


# --------------------------------------------- Call this to make a graph -------------------------------------------

def do_makegraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx, filename, picklename):
    newgraph = makegraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx)
    if picklename != "":
        f = open(picklename, "w")
        pickle.dump(newgraph, f)
        f.close()       
    drawgraph(newgraph, filename)
    return

# ------------------------------------------------------ Test ------------------------------------------------------



if __name__=="__main__":
    #run a test

    #make BS data
    keyword_dict = {'A01':'one', 'A02':'two', 'A03':'three', 'A04':'four', 'A05':'five'}
    linkarray = [['A01'],['A02'],['A03'],['A04'],['A05']]
    diff_vector = [-10, -4, -0, 8, 20]
    transitions = [[0.5, 0.5,   0,   0,   0],
                   [  0, .23, .27, .33, .17],
                   [  0,   0,   0,   0,   1],
                   [0.2, 0.2, 0.2, 0.2, 0.2],
                   [0.33, 0.33, 0.33, 0,  0]]
    transition_mtx = np.matrix(transitions)

    #make graph
    newgraph = makegraph(5, linkarray, keyword_dict, diff_vector, transition_mtx)
    drawgraph(newgraph)



