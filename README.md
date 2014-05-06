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
- This proportion is compared against the actual proportion of hits each page received, and the difference between them is calculated as a percentage. In our model, positive percentages correspond to larger than expected influxes of hits, while negative values represent fewer than expected hits.
- Since each successive term in the summation over transition matrices includes an additional power of the discount factor, there will be a point past which additional terms are adding only negligible amounts to the sum. With this in mind, we wrote code to let the computer decide how many iterations to run, by giving it a threshold value. If the percentage calculation for a given number of iterations varies at ANY node (page) by more than the threshold amount (in our model, we used 5%) from the previous iteration, another successive iteration is run; only once all values are within the threshold limit is the model considered sufficiently close.

###### Lucy's code part 1


###### Lucy's code part 2


##### Plans for Expansion on the Final Project
1. The actual Wikipedia data is many orders of magnitude larger than the testing data we are using for the prototype, which will require both much more efficient algorithms and adequate means of parallelism.
2. We have concerns about what level of predictive power, if any, we are able to achieve with this model since the timespan of our data (hourly) is too broad to accurately get a feel for the direction people are moving between pages. However, there may be some potential in seeing if we can use the model over several time iterations to make more accurate predictions about the true probabilities relating to page views than are obtained under the equal-distribution random surfer model. Our idea is tentatively to break up the hourly data into chinks of days/weeks and have each successive time interval make adjustments to the predicted distributions for the next interval. 



