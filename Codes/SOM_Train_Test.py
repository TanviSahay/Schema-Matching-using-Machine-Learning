import os, numpy, csv
from minisom import MiniSom
import pickle, numpy
from scipy.spatial import distance
from collections import defaultdict
import dill
from sklearn.metrics import silhouette_score
from normalise import Normalise

#Training Data
dataFeaturePath = '../Feature_Vectors/normalised_features_train.pickle'
DataFeatures = pickle.load(open(dataFeaturePath, 'rb'))

#Test Data
testFeaturesPath = '../Feature_Vectors/normalised_features_match.pickle'
TestFeatures = pickle.load(open(testFeaturesPath,'rb'))

#List of all features in training and testing data
InitFeatures = []
for val in DataFeatures.values():
    InitFeatures.append(val)
for val in TestFeatures.values():
    InitFeatures.append(val)

c_features = Normalise(numpy.array(InitFeatures))

Features = []
for i in range(0,len(c_features[0])):
     #column = c_features[:][i]
     column = [row[i] for row in c_features]
     Features.append(column)

#print len(Features)
#print len(InitFeatures)

#Features = N_Features

#(x,y) -- size of output grid for SOM


x = 5
y = 6
#Number of iterations to run

iteration = input("Input number of iterations: ")

#Create a SOM
som = MiniSom(x,y,20,sigma=0.3, learning_rate=0.5)
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
        
print feature_map, '\n'


      
#Write the attribute name and its corresponding id. DataFeatures is the dictionary (attribute, feature). attribute_cluster is the dictionary (attribute, cluster_id). If the feature being mapped is same as the feature in the dictionary, save its winner ID in the dictionary.

attribute_cluster = defaultdict(lambda:defaultdict())
for k in DataFeatures.keys():
    for f in Features:
        if DataFeatures[k] == f:
            print feature_map[som.winner(f)]
            attribute_cluster[feature_map[som.winner(f)]][k] = f
#print attribute_cluster
for k in TestFeatures.keys():
    for f in Features:
        if TestFeatures[k] == f:
            attribute_cluster[feature_map[som.winner(f)]][k] = f


#print attribute_cluster[]

pickle.dump(attribute_cluster,open('../Results/SOM_train_test_with_normal.pickle','w'))


#Open the output file for test data clusters
out_file_path_test = '../Results/Distances/SOM_with_normal_'+ str(x*y) + '_itr' + str(iteration) +'.csv'
out_file = open(out_file_path_test,'w')
output_file = csv.writer(out_file, delimiter = ',')
output_file.writerow(["Attribute", "Cluster ID"])            

for key1,value in attribute_cluster.items():
    for key2 in value.keys():
        new_row = [key1, key2]
        output_file.writerow(new_row)

out_file.close()

labels = []
for f in Features:
    labels.append(feature_map[som.winner(f)])

silhouetteScore = silhouette_score(Features, labels)

print silhouetteScore

print 'Train Data: ', DataFeatures['tr_state']
print 'Test Data: ', TestFeatures['ts_state']

