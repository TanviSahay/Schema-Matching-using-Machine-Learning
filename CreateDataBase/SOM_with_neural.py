import os, numpy, csv
from minisom import MiniSom
import pickle
from sklearn.neural_network import MLPClassifier

dataFeaturePath = '../Codes/DataFeatures.pickle'
DataFeatures = pickle.load(open(dataFeaturePath, 'rb'))

testFeaturesPath = '../Codes/DataFeatures_Match.pickle'
TestFeatures = pickle.load(open(testFeaturesPath,'rb'))

# Extracting Training features for SOM

Features = []
for val in DataFeatures.values():
    Features.append(val)

# Extracting Testing features for SOM

Y_test = []
Y_name = []

for key in TestFeatures.keys():
    Y_test.append(TestFeatures[key])
    Y_name.append(key)

x = 7
y = 7

# Training and extracting weights from SOM

som = MiniSom(x,y,17,sigma=0.3, learning_rate=0.5)
print "Training..."
weights = som.train_random(Features, 100) # trains the SOM with 100 iterations
print "...ready!"

feature_map = {}

k = 0

# Making a feature map for mapping Cluster ID's

for i in range(x):
    for j in range(y):
        feature_map[(i,j)] = k
        k += 1
             
out_file_path = '../Codes/AttributeCluster_'+ str(x*y) +'.csv'
out_file = open(out_file_path,'w')
output_file = csv.writer(out_file, delimiter = ',')
output_file.writerow(["Attribute", "Cluster ID"])

len_f = len(Features)

i = 0

final_weights = {}

# Storing Training test attributes and its assigned cluster ID to a file

for k in DataFeatures.keys():
    for f in Features:
        if DataFeatures[k] == f:
            attribute_cluster = [k, feature_map[som.winner(f)]]
            if feature_map[som.winner(f)] not in final_weights:
                 final_weights[feature_map[som.winner(f)]] = weights[som.winner(f)].tolist()
            output_file.writerow(attribute_cluster)
            
n_clusters = len(final_weights)            
print "weights : " , len(final_weights[0])

out_file.close()


########################################### Neural network ##############################################################################

X_train = []
Y_train = []
for key in final_weights.keys():
    Y = [0]*(x*y)
    X_train.append(final_weights[key])
    Y[key] = 1
    Y_train.append(Y)
#N_neurons_hidden = ( 17 + n_clusters )/ 2 
N_neurons_hidden = 10

clf = MLPClassifier(solver='sgd', alpha=1e-5,hidden_layer_sizes=(N_neurons_hidden,), random_state=1,verbose = True, max_iter = 1000000)   

print "Training done"
clf.fit(X_train, Y_train)
      
Output_class = clf.predict(Y_test)

print Y_name[0] , Output_class


    

