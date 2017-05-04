import pickle, csv
import os, numpy
import editdistance
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance


# Cluster_names_features is a dictionary

      
# cluster_name_features is a dictionary 


# Nested Dictionary : distance[test_name][train_name] = dist
global edit_distance
global cosine_distance
global euc_distance
global missing_attributes

missing_attributes = []
edit_distance = {}
cosine_distance = {}
euc_distance = {}
''' 
Test_Data      = pickle.load(open('../Feature_Vectors/DataFeatures_Match.pickle'))		#Test_Data[Attribute Name]   = feature vector
Som_clusters   = pickle.load(open('../Results/Distances/SOM_train_test_with_normal.pickle'))		        #cluster[id][attribute_name] = feature vector 
 
Test_names = []
Test_features = []
 
print  Som_clusters.keys()
for cluster_id in Som_clusters.values():

    test_names_features = {}
    train_names_features = {}
    
    for attribute in cluster_id.keys():
         if attribute in Test_Data.keys():
                test_names_features[attribute] =  cluster_id[attribute]          
         else:
                train_names_features[attribute] =  cluster_id[attribute]             
    
    calculate_edit_distance(test_names_features,train_names_features)
    cosine_euc_distance(test_names_features,train_names_features)



#Calulating Probablity for all three distances
cal_probability(edit_distance,'edit')
#cal_probability(cosine_distance,'cosine')
#cal_probability(euc_distance,'euc')

print "missing attributes" , missing_attributes      
print "done"    
    
'''    
    
    
    
    
                           
        

