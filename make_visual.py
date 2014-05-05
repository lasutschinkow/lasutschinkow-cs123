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
THRESHOLD = 0.3 #minimum magnitude necessary to make it on the plot. put between 0 (show all) and 1 (show only max)

class graphobj:
    def __init__(self, graph, nodes_ordered, nodeweights, edgeweights, vmin, vmax):
        self.graph = graph
        self.nodes_ordered = nodes_ordered #also determines which we plot at all
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

def getminmax(diff_vector):
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
    return (vmax, vmin)

def scalevalue(unscaled, vmin, vmax):
    if unscaled < 0:
        magnitude = (float(unscaled) / vmin)
        scaled = 0.5 - 0.5 * magnitude
    else: #unscaled nonnegative
        magnitude = (float(unscaled) / vmax)
        scaled = 0.5 + 0.5 * magnitude
    return (magnitude, scaled)


def makegraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx):
    #the ordering of keywords is preserved: first row in linkarray is the first node... etc.
    #keyword_dict maps linkarray serial numbers to human readable names

    #for now just using a graph instead of digraph, for the sake of cleanness
#    G = nx.DiGraph() #initializes empty graph 
    G = nx.Graph()

    #I think I need to keep labels in separate vectors
    edgeweights = []

    rv = getminmax(diff_vector)
    vmax = rv[0]
    vmin = rv[1]
    nodeweights = []
    nodes_to_show = []

    # grow nodes while calculating adjusted weights
    for i in range(0, num_nodes):
        #calculate new magnitude, and add it only if it's significant enough
        unscaled = diff_vector[i]
        label = keyword_dict[linkarray[i][SERIAL_INDEX]] #label nodes with human-readable name

        rv = scalevalue(unscaled, vmin, vmax)

        if rv[0] > THRESHOLD: #rv[0] is magnitude
            nodeweights.append(rv[1]) #rv[1] is scaled value
            nodes_to_show.append(label)
            G.add_node(label, index=i, diff=diff_vector[i])

    included_nodes = set(nodes_to_show)
    #grow edges
    for i in range(0, num_nodes):
        label1 = keyword_dict[linkarray[i][SERIAL_INDEX]]
        if label1 in included_nodes:
            for j in range(0, num_nodes):
                label2 = keyword_dict[linkarray[j][SERIAL_INDEX]]
                if label2 in included_nodes:
                    p_from_i_to_j = transition_mtx[i,j]
                    if p_from_i_to_j > 0:
                        G.add_edge(label1,label2, weight=p_from_i_to_j)
                        edgeweights.append(p_from_i_to_j)
    newgraph = graphobj(G, nodes_to_show, nodeweights, edgeweights, vmin, vmax)

    return newgraph

def makezoomgraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx, focused_node):
    G = nx.DiGraph()

    i = focused_node
    label1 = keyword_dict[linkarray[i][SERIAL_INDEX]]
    nodes_to_show = [label1]
    rv = getminmax(diff_vector)
    vmax = rv[0]
    vmin = rv[1]
    rv = scalevalue(diff_vector[i], vmin, vmax)

    nodeweights = [rv[1]]

    G.add_node(label1, index=i, diff=diff_vector[i])

    #make edges first, as we'll figure out neighbors along the way
    for j in range(0, num_nodes):
        label2 = keyword_dict[linkarray[j][SERIAL_INDEX]]
        p_from_i_to_j = transition_mtx[i,j]
        p_from_j_to_i = transition_mtx[j,i]
        if (p_from_i_to_j > 0) or (p_from_j_to_i > 0):
            #add node
            G.add_node(label2, index=j, diff=diff_vector[j])
            nodes_to_show.append(label2)
            rv = scalevalue(diff_vector[j], vmin, vmax)
            nodeweights.append(rv[1])
            #add edge
            if p_from_i_to_j > 0:
                G.add_edge(label1,label2, weight=p_from_i_to_j)
            if p_from_j_to_i > 0:
                G.add_edge(label2, label1, weight=p_from_j_to_i)

    newgraph = graphobj(G, nodes_to_show, nodeweights, [], vmin, vmax)
    return newgraph


def drawgraph(graphobj, filename):
    mycolormap = makecolormap()
    plt.register_cmap(name='BlueRed', data=mycolormap)
    plt.rcParams['image.cmap'] = 'BlueRed'

#    Normalize(vmax=graphobj.vmax, vmin=graphobj.vmin)

#    nx.draw_networkx(graphobj.graph, with_labels=True, node_color=graphobj.nodeweights, edge_color=graphobj.edgeweights, cmap='BlueRed')

#    position = nx.graphviz_layout(graphobj.graph,prog='neato')
#    position = nx.spectral_layout(graphobj.graph)
    position = nx.spring_layout(graphobj.graph, weight='weight')
    nx.draw_networkx(graphobj.graph, pos=position, nodelist=graphobj.nodes_ordered, node_color=graphobj.nodeweights, cmap='BlueRed') #forget about edge colorings for now, they don't look very good
    plt.savefig(filename)
    plt.show()
    plt.close()


# --------------------------------------------- Call this to make a graph -------------------------------------------

def do_makegraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx, filename, picklename):
    newgraph = makegraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx)
    if picklename != "":
        f = open(picklename, "w")
        pickle.dump(newgraph, f)
        f.close()       
    drawgraph(newgraph, filename)
    return

def do_makezoomgraph(focus_node, num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx, filename, picklename):
    newgraph = makezoomgraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx, focus_node)
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
                   [  0,  .1,  .8,  .1,  .0],
                   [  0,   0,   0,   0,   1],
                   [0.2, 0.2, 0.2, 0.2, 0.2],
                   [0.33, 0.33, 0.33, 0,  0]]
    transition_mtx = np.matrix(transitions)

    #make graph
    newgraph = makezoomgraph(5, linkarray, keyword_dict, diff_vector, transition_mtx, 2)
    drawgraph(newgraph, "graph.png")



