## Graphing Wikipedia

##### CS 123 Project

###### Lucy Chen
###### Michael Lasutschinkow


##### How to Run the Code
1. To generate random data for the prototype : python TestData/generatedataset.py :: This generates the data being used by the rest of the project. This part has already been done and the data is in the TestData directory.
2. To run the simulation and generate the graphs : python PageRank_prototype.py :: This reads in the data from TestData and constructs a model for expected page hits (using a random-surfer model with equal-probability weighting). It then compares this with the actual hits over the same  time period and calculates the differences between them. It then calls make _visual.py to create graphs corresponding to the data. 
3. The graphs, as well as some of the pickled data structures, are found in the Model_Results directory


##### Code Breakdown and Explanation

###### PageRank_prototype.py
- A Transition Matrix (TM) is a matrix of probabilities, where each entry (i,j) represents the probability of starting at node i and ending at node j in one step (in our context, one page click)
- By multiplying this TM by itself N times, you obtain a matrix where each entry (i,j) represents the probability of starting at node i and ending at node j after exactly N steps. 
- To simulate the fact that users have an "attention span" and will eventually get bored and click away, there is a discount factor added in to the multiplication. This has the effect of weighting earlier clicks more heavily than later ones, as the discount factor raised to high powers approaches zero. 
- By summing over all of these Transition Matrices for indexes 1 to K, you can obtain the proportion of hits that each page is expected to receive using the probability distribution that you started with (in our model, we are using the Random Surfer model and so our probability distribution is equally-weighted based on the number of out-links each page has).
- This proportion is compared against the actual proportion of hits each page received, and the difference between them is calculated as a percentage. In our model, positive percentages correspond to larger than expected influxes of hits, while negative values represent fewer than expected hits. For example, a value of "1" in coordinate "i" in the difference vector indicates that node i has twice as many actual hits as predicted hits (that is, 100% more) while a value of "-0.5" means that the node has half as many hits as predicted.
- Since each successive term in the summation over transition matrices includes an additional power of the discount factor, there will be a point past which additional terms are adding only negligible amounts to the sum. With this in mind, we wrote code to let the computer decide how many iterations to run, by giving it a threshold value. If the percentage calculation for a given number of iterations varies at ANY node (page) by more than the threshold amount (in our model, we used 5%) from the previous iteration, another successive iteration is run; only once all values are within the threshold limit is the model considered sufficiently close.

###### make_visual.py
- This file uses the networkx package to make and draw a graph that shows the information we've processed earlier. (The networkx package is included in our GitHub repository.)
- It takes in a bunch of information about the nodes and the actual-expected difference we calculated earlier, and outputs a graph where the nodes are colored more red if there are fewer hits than expected, and more green if there are more hits than expected.
- There are two major functions included: one which draws all nodes in the graph whose calculated difference exceeds some threshold, and one that draws one node and all its neighbors. 
    * The first function does not draw the direction of edges due to issues of visual clutter. In fact, the threshold system was implemented to begin with because having more than ten or so nodes makes the graph nigh unreadable. (See Model_Results/graph_show_all_nodes.png for the unreadability of a graph with even 50 nodes!) 
    * For the second function, the thick black boxes denote that the edge is going *into* that side. Boxes at both ends of an edge mean that there are edges going both ways.

##### Sample Results
- Running PageRank_prototype.py will display the optimum number of iterations before there is no significant improvement. It will also display the difference vector between actual and expected hits, and create three graphs.
- Model_Results/graph_show_all_nodes.png is a graph generated with all the nodes involved. Notice that with fifty hits it is already practically unreadable, and unless we build some sort of dynamic and interactive model, it is likely that showing all nodes is simply a bad idea.
- Model_Results/graph_show_most_deviant_nodes.png is a graph generated with a threshold of 0.5, showing only those nodes that deviate more than half as much as the most deviant node does. This is relatively expensive to make and perhaps not any more useful than a list of the greatest deviants, so this may not be useful for the final product.
- Model_Results/graph_zoom_node20.png is a graph generated with the node-and-its-neighbors function. There is nothing special about node 20, and since our data is all fake and mostly generated at random this is not particularly illuminating. However, on the actual data, this should provide a way of investigating whether one node's abnormal deviation is reflected in its neighbors.

##### Plans for Expansion on the Final Project
1. The actual Wikipedia data is many orders of magnitude larger than the testing data we are using for the prototype, which will require both much more efficient algorithms and adequate means of parallelism.
2. We have concerns about what level of predictive power, if any, we are able to achieve with this model since the timespan of our data (hourly) is too broad to accurately get a feel for the direction people are moving between pages. However, there may be some potential in seeing if we can use the model over several time iterations to make more accurate predictions about the true probabilities relating to page views than are obtained under the equal-distribution random surfer model. Our idea is tentatively to break up the hourly data into chinks of days/weeks and have each successive time interval make adjustments to the predicted distributions for the next interval. 
3. Since the tasks in the project can largely be done independently of each other, we can use several different techniques--perhaps even in different languages--to handle each subtask. For example, we might handle the initial construction of the matrix from the data with mapreduce, and matrix multiplication with mpi4py.

##### The Sad Tale of Deterministic Solutions That Don't Make Sense
At one point, we considered that there might be a way to perfectly find the probabilities of starting at each node.
To make a very long story short, you could solve for the initial vector in the equation:
[a matrix representing the sum of transition matrices, producing total expected hits] * [initial] = scalar*[actual]
... by using some linear algebra (multiplying by the inverse matrix).

Theoretically, this is pretty exciting, as it gives an algorithmic way to compute the probabilities of starting on each page, thereby also separating the case where lots of people start on a popular node and fan out, vs the case where lots of people start on a bunch of nodes and gravitate toward a node.

However, this produces precisely one solution completely deterministically... and that solution may involve negative numbers.
Of course, a negative value in the initial probabilities vector is nonsense: it says not that someone starts there *less often*, but to subtract the hits resulting from people wandering out from that node. 
(To see the difference: Suppose that it's impossible to start from C, there's a positive chance to start from A, and there's a "negative" chance to start from B. I start from page A, and I have to go through page B to get to page C. So I go A->B->C, giving A, B, and C one hit each. Now let's say I start from page B before leaving wikipedia, taking away one hit from B. Now A and C each have one hit, even though it should be impossible for C to get a hit without B getting a hit, and you see that this is quite different from B being less popular.)

We considered somehow excluding negative values, but because the math is so deterministic, the only way we could think of doing that would be to run this calculation on many different [actual] vectors with slightly different values within an error of margin. However this seems both incredibly expensive and unlikely to yield an all-positive vector, simply due to the number of coordinates involved.

That's why we decided to stick to descriptions of the result instead.
