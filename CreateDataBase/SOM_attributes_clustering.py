import os, numpy, csv
from minisom import MiniSom
import pickle
from scipy.spatial import distance

#Training Data
dataFeaturePath = '../FeatureVectorResults/DataFeatures_Train.pickle'
DataFeatures = pickle.load(open(dataFeaturePath, 'rb'))

#Test Data
testFeaturesPath = '../FeatureVectorResults/DataFeatures_Match.pickle'
TestFeatures = pickle.load(open(testFeaturesPath,'rb'))

#List of all features in training data
Features = []
for val in DataFeatures.values():
    Features.append(val)


#List of all features in test data
testFeatures = []
for val in TestFeatures.values():
    testFeatures.append(val)

#(x,y) -- size of output grid for SOM
x = 5
y = 2
#Number of iterations to run
iteration = input("Input number of iterations: ")

#Create a SOM
som = MiniSom(x,y,17,sigma=0.3, learning_rate=0.5)
print "Training..."
som.train_random(Features, iteration) # trains the SOM with 100 iterations
print "...ready!"

#Map the output neuron position to a unique cluster id. (0,0) --> 0, (0,1) --> 1 and so on.
feature_map = {}
k = 0

for i in range(x):
    for j in range(y):
        feature_map[(i,j)] = k
        k += 1
             

#Open a csv file to write the attribute name and its corresponding cluster id
#print 'attribute			Spatial Position'
out_file_path = '../FeatureVectorResults/AttributeCluster_centroid_'+ str(x*y) + '_itr' + str(iteration) + '.csv'
out_file = open(out_file_path,'w')
output_file = csv.writer(out_file, delimiter = ',')
output_file.writerow(["Attribute", "Cluster ID"])

print "number of rows to be written: ", len(Features)

#Write the attribute name and its corresponding id. DataFeatures is the dictionary (attribute, feature). attribute_cluster is the dictionary (attribute, cluster_id). If the feature being mapped is same as the feature in the dictionary, save its winner ID in the dictionary.

attribute_cluster = {}

for k in DataFeatures.keys():
    for f in Features:
        if DataFeatures[k] == f:
            attribute_cluster[k] = feature_map[som.winner(f)]
            output_file.writerow([k, feature_map[som.winner(f)]])

out_file.close()

#Open the output file for test data clusters
out_file_path_test = '../FeatureVectorResults/TestCluster_centroid_'+ str(x*y) + '_itr' + str(iteration) +'.csv'
out_file = open(out_file_path_test,'w')
output_file = csv.writer(out_file, delimiter = ',')
output_file.writerow(["Attribute", "Cluster ID"])

#Find out the cluster center of each unique cluster id. Cluster Center = average of feature vectors belonging to that cluster.
cluster_center = {}

print 'number of unique clusters: ', numpy.unique(attribute_cluster.values())

for element in numpy.unique(attribute_cluster.values()):
    center = []
    i = 0
    for k in attribute_cluster.keys():
        if attribute_cluster[k] == element:
            i += 1
            center.append(DataFeatures[k])
    centerSum = [sum(j) for j in zip(*center)]

    cluster_center[element] = [centerElem / i for centerElem in centerSum]

#print cluster_center
#List of all cluster_centers
list_of_cluster_centers = []
for val in cluster_center.values(): list_of_cluster_centers.append(val)

#Find out which feature in test data in closest to which cluster_center
test_cluster = {}
for key, value in TestFeatures.items():
    eudistance = []
    min_dist = 9000000
    for centerID, center in cluster_center.items():        
        eudistance.append(distance.euclidean(value, center))
        min_d = min(eudistance)
        if min_d < min_dist: 
            min_center = center
            min_dist = min_d
    
            test_cluster[key] = centerID
     
for key, value in test_cluster.items():
    output_file.writerow([key,value])












#Testing feature vectors
print "Feature vector of ---s_hbips_7_measure_description---"
print TestFeatures['s_hbips_7_measure_description']

print "\n"
print "Feature vector of ---imm_2_denominator---"
print DataFeatures['imm_2_denominator']
