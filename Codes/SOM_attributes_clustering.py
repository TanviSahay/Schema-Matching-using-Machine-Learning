import warnings
warnings.filterwarnings("ignore")
import os, numpy, csv
from minisom import MiniSom
import pickle
from scipy.spatial import distance
from sklearn.metrics import silhouette_score
import editdistance
from sklearn.metrics.pairwise import cosine_similarity


def calculate_edit_distance(test_name , train_names_features):
    # Calculating edit distance of a test attribute from all train attributes.
        edit_distance[test_name] = {} 
        for name in train_names_features:
                edit_distance[test_name][name] = editdistance.eval(test_name, name)  
                

def cosine_euc_distance(test_name,test_feature, train_name_features):
    # Calculating cosine and euclidean distance of a test attribute from all train attributes. 
         
          cosine_distance[test_name] = {}
          euc_distance[test_name] = {}
          for name in train_name_features.keys():
              cosine_distance[test_name][name] = cosine_similarity(test_feature, train_name_features[name])[0][0]
              euc_distance[test_name][name] = distance.euclidean(test_feature, train_name_features[name])
                                  

def cal_probability(distance_dic,name):
     file_path = open('../Results/Distances/All_distances/centroid_' + name + '.csv','w')
     Out = csv.writer(file_path,delimiter=',')
     
     new_row = ['test_attribute' , 'train_attribute' , 'distance', 'probability']
     Out.writerow(new_row)
     for test_attribute in edit_distance.keys():
           total = sum(edit_distance[test_attribute].values())
           
           for train_attribute in edit_distance[test_attribute].keys():
                prob = 1 - (edit_distance[test_attribute][train_attribute]/float(total))
                new_row = [test_attribute,train_attribute,edit_distance[test_attribute][train_attribute] ,prob]       
                Out.writerow(new_row)
     file_path.close()
     
     


global edit_distance
global cosine_distance
global euc_distance

edit_distance = {}
cosine_distance = {}
euc_distance = {}   

 
#Training Data
dataFeaturePath = '../Feature_Vectors/normalised_features_train.pickle'
DataFeatures = pickle.load(open(dataFeaturePath, 'rb'))

#Test Data
testFeaturesPath = '../Feature_Vectors/normalised_features_match.pickle'
TestFeatures = pickle.load(open(testFeaturesPath,'rb'))

#List of all features in training data
Features = []
for val in DataFeatures.values():
    Features.append(val)


#(x,y) -- size of output grid for SOM
x = 5
y = 5
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
             

#Open a csv file to write the attribute name and its corresponding cluster id
#print 'attribute			Spatial Position'
out_file_path = '../Results/Centroid_Clustering_Result/final_AttributeCluster_centroid_'+ str(x*y) + '_itr' + str(iteration) + '.csv'
out_file = open(out_file_path,'w')
output_file = csv.writer(out_file, delimiter = ',')
output_file.writerow(["Attribute", "Cluster ID"])

#print "number of rows to be written: ", len(Features)

# Write the attribute name and its corresponding id. DataFeatures is the dictionary (attribute, feature). 
# Attribute_cluster is the dictionary (attribute, cluster_id). 
# If the feature being mapped is same as the feature in the dictionary, save its winner ID in the dictionary.

attribute_cluster = {}

for k in DataFeatures.keys():
    for f in Features:
        if DataFeatures[k] == f:
            attribute_cluster[k] = feature_map[som.winner(f)]
            output_file.writerow([k, feature_map[som.winner(f)]])

out_file.close()

#Open the output file for test data clusters
out_file_path_test = '../Results/Centroid_Clustering_Result/final_CentroidDistance_20_'+ str(x*y) + '_itr' + str(iteration) +'.csv'
out_file = open(out_file_path_test,'w')
output_file = csv.writer(out_file, delimiter = ',')
output_file.writerow(["Attribute", "Cluster ID"])

#Find out the cluster center of each unique cluster id. Cluster Center = average of feature vectors belonging to that cluster.
cluster_center = {}

#print 'number of unique clusters: ', numpy.unique(attribute_cluster.values())

for element in numpy.unique(attribute_cluster.values()):
    center = []
    i = 0
    for k in attribute_cluster.keys():
        if attribute_cluster[k] == element:
            i += 1
            center.append(DataFeatures[k])
    centerSum = [sum(j) for j in zip(*center)]

    cluster_center[element] = [centerElem / i for centerElem in centerSum]


#List of all cluster_centers
list_of_cluster_centers = []

for val in cluster_center.values(): 
   list_of_cluster_centers.append(val)

    
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

labels = []
for f in Features:
    labels.append(feature_map[som.winner(f)])

silhouetteScore = silhouette_score(Features, labels)

print silhouetteScore


for key, value in test_cluster.items():
    output_file.writerow([key,value])
    

for key,val in test_cluster.items():
   
      train_names = []
      train_name_features = {}
      for k, v in attribute_cluster.items():
          if val == v:
             train_names.append(k)
             train_name_features[k] = DataFeatures[k] 
             
      calculate_edit_distance(key,train_names)
      cosine_euc_distance(key,TestFeatures[key],train_name_features)


cal_probability(edit_distance,'edit_' + str(x*y))
cal_probability(cosine_distance,'cosine_' + str(x*y))
cal_probability(euc_distance,'euc_' + str(x*y))

print silhouetteScore

