# Lucy Chen
# For CMSC12300 Final Project with Michael Lasutschinkow
#
# * * * To use this:
# first import this file.
# then call the function:
#   do_makegraph(threshold between 0 and 1 [0 to graph all, 1 to graph only greatest deviating nodes], number of nodes, array of links (or some other array with node IDs), dictionary of node IDs to keywords, the difference vector, any transition matrix, filename for saving the image, non-empty filename to save a pickle under that filename)
#
# Or in short,
# do_makegraph(threshold, number_nodes, link_array, keyword_dictionary, diff_vector, transition_mtx, save_to_image_filename, save_to_pickle_filename)
#
# That will create a graph image containing all nodes with a scaled deviation beyond the threshold value.
#
# Alternatively, you can "zoom in" on a node and view that node and all its
# immediate neighbors:
#
# do_makezoomgraph(node_to_focus_on, number_nodes, link_array, keyword_dictionary, diff_vector, transition_mtx, save_to_image_filename, save_to_pickle_filename)
#
# Notice that the syntax is the same except for the first parameter.
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

# makes an object that holds everything you need to make a graph
class graphobj:
    def __init__(self, graph, nodes_ordered, nodeweights, edgeweights, vmin, vmax):
        self.graph = graph #this is a networkx graph object
        self.nodes_ordered = nodes_ordered #necessary to fix order of nodes (to match with nodeweights)
        self.nodeweights = nodeweights
        self.edgeweights = edgeweights #probably unnecessary, keeping it here just in case
        self.vmax = vmax
        self.vmin = vmin

# adapted from http://matplotlib.org/examples/pylab_examples/custom_cmap.html
# sets up a dictionary object to be converted into a colormap
def makecolormap():
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

# gets the min and max values for a vector and tests to ensure non-degeneracy
def getminmax(diff_vector):
    vmax = max(diff_vector)
    vmin = min(diff_vector)
    #make nodeweights from diff_vector (nodeweights has values from 0 to 1)
    #we want to do a linear mapping, vmin -> 0, 0 -> 1/2, vmax -> 1

    # Since the difference vector is all about deviation from an expectation,
    # and the expected and actual have the same average, it's literally impossible
    # not for the difference vector to be all positive or all negative. The only
    # possible case degenerate case is all 0's, which isn't
    # going to happen. Still, I have this test here just in case something
    # goes wrong in these early test stages.
    if vmin > 0:
        print "Impossible! vmin > 0!"
        sys.exit()
    if vmax < 0:
        print "Impossible! vmax < 0!"
        sys.exit()
    #else nondegenerate
    return (vmax, vmin)

# scales a value in the difference vector down to a value between 0 and 1,
# with 1/2 representing the original 0,
# so that it can correspond with our intuitive red-green color scheme
def scalevalue(unscaled, vmin, vmax):
    if unscaled < 0:
        magnitude = (float(unscaled) / vmin)
        scaled = 0.5 - 0.5 * magnitude
    else: #unscaled nonnegative
        magnitude = (float(unscaled) / vmax)
        scaled = 0.5 + 0.5 * magnitude
    return (magnitude, scaled)

# make a graph with all nodes that deviate beyond a certain threshold
def makegraph(threshold, num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx):
    #the ordering of keywords is preserved: first row in linkarray is the first node... etc.
    #keyword_dict maps linkarray serial numbers to human readable names

    #for now just using a graph instead of digraph, for the sake of cleanness
#    G = nx.DiGraph() #initializes empty graph 
    G = nx.Graph()

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

        if rv[0] > threshold: #rv[0] is magnitude
            nodeweights.append(rv[1]) #rv[1] is scaled value
            nodes_to_show.append(label)
            G.add_node(label, index=i, diff=diff_vector[i])

    included_nodes = set(nodes_to_show) #restrict edges to nodes we've chosen to include
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

# make a graph with one node and all its neighbors
def makezoomgraph(num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx, focused_node):
    #initialize some stuff, handle our node in focus
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


    for j in range(0, num_nodes):
        label2 = keyword_dict[linkarray[j][SERIAL_INDEX]]
        p_from_i_to_j = transition_mtx[i,j]
        p_from_j_to_i = transition_mtx[j,i]
        if (p_from_i_to_j > 0) or (p_from_j_to_i > 0): #if this node is a neighbor
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

# given a graph object, handle the minutiae of drawing
def drawgraph(graphobj, filename):
    mycolormap = makecolormap()
    plt.register_cmap(name='BlueRed', data=mycolormap)
    plt.rcParams['image.cmap'] = 'BlueRed'

    # I've kept these in for the syntax: they're different ways to auto-arrange the nodes.
#    position = nx.graphviz_layout(graphobj.graph,prog='neato')
#    position = nx.spectral_layout(graphobj.graph)
    position = nx.spring_layout(graphobj.graph, weight='weight') #I like this best. It positions nodes closer based on the strength of their connections.

    nx.draw_networkx(graphobj.graph, pos=position, nodelist=graphobj.nodes_ordered, node_color=graphobj.nodeweights, cmap='BlueRed')
    #forget about edge colorings for now, they don't look very good. may worry about those later.
    plt.savefig(filename)
    plt.close()

# --------------------------------------------- Call this to make a graph -------------------------------------------

# wrapper for full graph with threshold (use threshold = 0 to get the whole entire graph)
def do_makegraph(threshold, num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx, filename, picklename):
    newgraph = makegraph(threshold, num_nodes, linkarray, keyword_dict, diff_vector, transition_mtx)
    if picklename != "":
        f = open(picklename, "w")
        pickle.dump(newgraph, f)
        f.close()       
    drawgraph(newgraph, filename)
    return

# wrapper for one node and neighbors graph
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



