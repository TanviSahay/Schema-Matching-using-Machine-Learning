import pickle, csv
import os, numpy
import editdistance
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance


# Cluster_names_features is a dictionary
def calculate_edit_distance(test_names_features , train_names_features):
    
# Calculating edit distance of a test attribute from all train attributes.
    for test_name in test_names_features.keys():
         edit_distance[test_name] = {}   
         for name in train_names_features:
              edit_distance[test_name][name] = editdistance.eval(test_name, name)
          

# cluster_name_features is a dictionary 
def cosine_euc_distance(test_names_features , train_name_features):
    

# Calculating cosine and euclidean distance of a test attribute from all train attributes. 
    
    for test_name in test_names_features.keys():
         cosine_distance[test_name] = {}
         euc_distance[test_name] = {}
         
         for name in train_names_features.keys():
              cosine_distance[test_name][name] = cosine_similarity(test_names_features[test_name], train_names_features[name])[0][0]
              euc_distance[test_name][name] = distance.euclidean(test_names_features[test_name], train_names_features[name])
          


def cal_probability(distance_dic,name):
     file_path = open('../Results/distances/' + name + '.csv','w')
     Out = csv.writer(file_path,delimiter=',')
     
     new_row = ['test_attribute' , 'train_attribute' , 'distance', 'probability']
     Out.writerow(new_row)
     for test_attribute in distance_dic.keys():
           total = sum(distance_dic[test_attribute].values())
           
           for train_attribute in distance_dic[test_attribute].keys():
                prob = 1 - (distance_dic[test_attribute][train_attribute]/float(total))
                new_row = [test_attribute,train_attribute,distance_dic[test_attribute][train_attribute] ,prob]       
                Out.writerow(new_row)
     file_path.close()      
     

# Nested Dictionary : distance[test_name][train_name] = dist
global edit_distance
global cosine_distance
global euc_distance

edit_distance = {}
cosine_distance = {}
euc_distance = {}
 
Test_Data      = pickle.load(open('../Feature_Vectors/normalised_features_match.pickle'))		#Test_Data[Attribute Name]   = feature vector
Som_clusters   = pickle.load(open('../Results/Distances/SOM_train_test.pickle'))		        #cluster[id][attribute_name] = feature vector 
 
Test_names = []
Test_features = []
  
for cluster_id in Som_clusters.values():

    print cluster_id
    test_names_features = {}
    train_names_features = {}
    
    for attribute in cluster_id.keys():
         print attribute
         if attribute in Test_Data.keys():
                test_names_features[attribute] =  cluster_id[attribute]          
         else:
                train_names_features[attribute] =  cluster_id[attribute]             
    
    calculate_edit_distance(test_names_features,train_names_features)
    cosine_euc_distance(test_names_features,train_names_features)


#Calulating Probablity for all three distances
cal_probability(edit_distance,'edit')
cal_probability(cosine_distance,'cosine')
cal_probability(euc_distance,'euc')
  
print "done"    
    
    
    
    
    
    
                           
        

