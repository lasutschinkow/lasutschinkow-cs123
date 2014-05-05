## Graphing Wikipedia

##### CS 123 Project

###### Lucy Chen
###### Michael Lasutschinkow


##### How to Run the Code
1. To generate random data for the prototype : python TestData/generatedataset.py :: This generates the data being used by the rest of the project. This part has already been done and the data is in the TestData directory.
2. To run the simulation and generate the graphs : python PageRank_prototype.py :: This reads in the data from TestData and constructs a model for expected page hits (based on equal-probability weighting). It then compares this with the actual hits over the same  time period and calculates the differences between them. It then calls make _visual.py to create graphs corresponding to the data. 
3. The graphs, as well as some of the pickled data structures, are found in the Model_Results directory
