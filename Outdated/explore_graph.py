# Lucy Chen
# CMSC 123000 Final Project with Michael Lasutschinkow
# Tool for human exploration of graphs
#
# syntax:
# python explore_graph.py [graph's transition matrix pickle object filename]
#
#
#

import sys
import numpy as np
import pickle
import random


def loadgraph(filename):
    f = open(filename, "r")
    graph = pickle.load(f)
    return graph

def printmessage(in_from, out_to, prob):
    print "from " + str(in_from) + " to " + str(out_to) + ": " + str(prob)

def print_ins(graph, node):
    print "Probability of incoming edges:"
    total = 0
    for i in range(0, graph[0].size):    
        prob = graph[i,node]
        if prob != 0:
            printmessage(i, node, prob)
            total += prob
        #else move on
    print "Sum = " + str(total) + "\n"

def print_outs(graph, node):
    print "Probability of outgoing edges:"
    total = 0
    for i in range(0, graph[0].size):
        prob = graph[node,i]
        if prob != 0:
            printmessage(node, i, prob)
            total += prob
        #else move on
    print "Sum = " + str(total) + "\n"

def about_node(graph):
    while(True):
        node = raw_input("Enter the index of the node you'd like to know about. (enter non-integer to quit)\n")
        try:
            node = int(node)
        except:
            sys.exit()
        print_ins(graph, node)
        print_outs(graph, node)
    return

def walker(graph):
    foo = 0
    while(foo == 0):
        num_steps = raw_input("How many steps?\n")
        try:
            num_steps = int(num_steps)
            foo = 1
        except:
            foo = 0

    dim = graph[0].size
    atnode = random.randint(0, dim)
    print "started at " + str(atnode)
    for i in range(0, num_steps):
        newnode = randomInterval(graph[atnode].tolist()[0])
        prob = graph[atnode,newnode]
        print "moved to " + str(newnode) + " with probability " + str(prob)
        atnode = newnode
    print "finished walking"
    option = raw_input("Walk again? (y to re-walk, anything else to go back to menu)\n")
    if option == "y":
        walker(graph)
    return

def randomInterval(prob_list):
    random.seed()
    rand = random.random()
    right_edge = 0
    for index in range(len(prob_list)):
        right_edge += prob_list[index]
        if rand < right_edge:
            return index
    #If we got here, there's a problem!
    if rand > numpy.longdouble(0.9999999999999999): #due to some kind of accumulated error
        return randomInterval(prob_list)
    else: #not due to rounding error
        print("The probabilities in the list provided to randomInterval do not add up to 1.")
        sys.exit(0)



# ------------------------- MENU LOGIC --------------------------

def menu(graph):
    while(True):
        option = raw_input("Enter 'about' to examine single nodes, 'walker' to launch a walker, 'exit' to exit.\n")
        if option == "exit":
            sys.exit()
        if option == "about":
            about_node(graph)
        if option == "walker":
            walker(graph)


if __name__=="__main__":
    graph = loadgraph(sys.argv[1])
    try:
        graph = loadgraph(sys.argv[1])
    except:
        print "Please enter a valid pickled matrix."
        sys.exit()
    print "There are " + str(graph[0].size) + " nodes in this graph."
    menu(graph)



