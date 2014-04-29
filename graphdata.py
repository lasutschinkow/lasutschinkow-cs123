# Lucy Chen
# CMSC 123000
# Final Project with Daniel Tracht and Michael Lasutschinkow
# Functions for graphing data.


import matplotlib
import pylab
import math

#column names; values are placeholders, change later
KEYWORD = 0
YESTERDAY = 1 #wiki hit counts
TODAY = 2
TOMORROW = 3
#this controls the size of the points (which vary by avg hit counts). bigger means smaller points
SCALEFACTOR = 0.1

class GraphData:
    def __init__(self, x, y, colors, sizes):
        self.x = x
        self.y = y
        self.colors = colors
        self.sizes = sizes

# --------------------------------- UTILITIES -------------------------------------


#take in day, before-day and produce the number expressing their relationship that we want to use for our graph
#measures how much attention your article brought in (theoretically)
def produce_x(yesterday, today, tomorrow): #yesterday may not be literally yesterday, but the average of several days before (or something)
    divisor = float(yesterday + today + tomorrow) / 3 #may not be the best divisor for this idea. store lifetime average?
    x = float((today - yesterday)) / divisor
    return x

#measures how much lasting effect your article had? sort of? it's the other side of the spike, whatever that means.
def produce_y(yesterday, today, tomorrow):
    divisor = float(yesterday + today + tomorrow) / 3 #may not be the best divisor for this idea. store lifetime average?
    y = float((tomorrow - today)) / float(divisor)
    return y

def figure_color(keyword):
    #track some points with colors to test hypotheses
    #may generalize this later if we want to put in complex conditions
    if "DEATH" in keyword:
        color = "r" #red
    elif "ELECTION" in keyword:
        color = "b" #blue
    else: #not something we're tracking
        color = "k"
        #could potentially give it a grayscale value, where a float corresponds to darkness,
        #to encode some sort of meaningful continuous information
    return color

# --------------------------------- MAKE GRAPH -----------------------------------

def convert_to_graphdata(data_array):
    x_data = []
    y_data = []
    colors = []
    sizes = []
    #assumes data_array has rows for each entry and columns for each data spec
    for row in data_array: #2d array is just list of lists (rows)
        xpoint = produce_x(row[YESTERDAY], row[TODAY], row[TOMORROW])
        ypoint = produce_y(row[YESTERDAY], row[TODAY], row[TOMORROW])
        x_data.append(xpoint)
        y_data.append(ypoint)
        upperword = row[KEYWORD].upper()
        color = figure_color(upperword)
        colors.append(color)
        sizes.append(float(math.sqrt(row[YESTERDAY])) / SCALEFACTOR)
    data = GraphData(x_data, y_data, colors, sizes)
    return data

def makeplot(graphdata):
    #plot points
    matplotlib.pyplot.scatter(graphdata.x, graphdata.y, c=graphdata.colors, s=graphdata.sizes, alpha=0.8)
    #alpha is the translucency of each point bubble

    #make the axes through the origin
    matplotlib.pyplot.axhline(y=0, xmin=0, xmax=1, c='k', lw='1') #'k' is black, lw is linewidth
    matplotlib.pyplot.axvline(x=0, ymin=0, ymax=1, c='k', lw='1')

    #stick labels on things
    x_label = "Proportional Hit Gain on Day Published"
    y_label = "Proportional Hit Gain after Day Published"
    matplotlib.pyplot.xlabel(x_label)
    matplotlib.pyplot.ylabel(y_label)
    matplotlib.pyplot.title("Change in Wikipedia Hits of Relevant Pages after News Exposure")
    #the placement of these are currently manually set. figure out a better solution later, if necessary.
    matplotlib.pyplot.text(1,-1.3,"spike of interest", size="x-small")
    matplotlib.pyplot.text(1,0.5,"increasing interest", size="x-small")
    matplotlib.pyplot.text(-0.9,-1.3,"progressive disinterest", size="x-small")
    matplotlib.pyplot.text(-0.9,0.5,"crevice of disinterest", size="x-small")

    #fake legend?
#    box = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
#    matplotlib.pyplot.text(2.0, -0.5, "blah", bbox=box)

#    matplotlib.pyplot.legend() #not actually using legend right now, would requiring separating data into different lists and passing them in, sounds like a pain.

    matplotlib.pyplot.show()

# ----------------------------- SAVE/LOAD --------------------------------
#it could be expensive to make the graph data when you have a big dataset
#and maybe you just want to tinker around with text labels or something else aesthetic
#so maybe you want the GraphData object for later!

def savegraphdata(graphdata, filename):
    f = open(filename, "w")
    pickle.dump(graphdata, f)
    f.close()
    return

def loadgraphdata(filename):
    f = open(filename, "r")
    graphdata = pickle.load(f)
    f.close()
    return graphdata

# -------------------------------- TESTS ---------------------------------

def load_to_data(sourceinfo, data):
    length = len(sourceinfo)
    for row_index in range(0, length):
        data[row_index][KEYWORD] = sourceinfo[row_index][0]
        data[row_index][YESTERDAY] = sourceinfo[row_index][1]
        data[row_index][TODAY] = sourceinfo[row_index][2]
        data[row_index][TOMORROW] = sourceinfo[row_index][3]
    return data #not strictly necessary (lol pointers) but seems like good style

#this file is its own test
#running this file produces a sample graph
if __name__=="__main__":
    SCALEFACTOR = 0.1
    somefakedata = [[0 for i in range(0,10)] for j in range(0,4)] #oversized array so we can easily adjust indices
    sourceinfo = [["cats", 5, 15, 8],
                  ["dogs", 9, 12, 8],
                  ["bunnies", 14, 16, 18],
                  ["cthulu", 18, 14, 10],
                  ["the death of poor mr. pouncealot", 3, 18, 5],
                  ["the election of charlotte the spider to the senate", 15, 17, 19],
                  ["rat race elections", 14, 16, 34],
                  ["sad horrible deaths beyond comprehension", 1, 23, 3],
                  ["novels", 12, 13, 12],
                  ["anarchists", 19, 16, 25],
                  ["your best friend's mom", 18, 30, 19],
                  ["that feeling you get when stuff happens", 2, 3, 1],
                  ["sarcastic witty keyword", 26, 16, 2],
                  ["death at a funeral", 92, 100, 84],
                  ["when the water's never the right temperature in the shower", 70, 42, 90]]
#    load_to_data(sourceinfo, somefakedata) #use this in the future, but for now...
    somefakedata = sourceinfo #with default indices we don't need to convert


    data = convert_to_graphdata(somefakedata)
    makeplot(data)
    matplotlib.pyplot.close()






