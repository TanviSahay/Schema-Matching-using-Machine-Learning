import os, numpy, csv
import pickle
import numpy as np
from sklearn.decomposition import PCA

dataFeaturePath = '../Codes/DataFeatures.pickle'
DataFeatures = pickle.load(open(dataFeaturePath, 'rb'))

Cluster_id_path = '../FeatureVectorResults/AttributeCluster_centroid_49_itr1000.csv'

dic_name_id = {}

with open(Cluster_id_path,'rb') as f:
    reader = csv.reader(f) 
    for row in reader:
        dic_name_id[row[0]] = row[1]

print dic_name_id

X = []
X_name = []
for key in DataFeatures.keys():
    X.append(DataFeatures[key])
    X_name.append(key)
    
pca = PCA(n_components=2)
X_new = pca.fit_transform(X)

print X_new[0][0] , X_new[0][1]

out_file_path = '../Codes/Training_vis_processed_49.csv'
out_file = open(out_file_path,'w')
output_file = csv.writer(out_file, delimiter = ',')
output_file.writerow(["Cluster ID","Attribute","Dim_x","Dim_Y", ])

for i in range (0,len(X)):
     output_file.writerow([dic_name_id[X_name[i]], X_name[i], X_new[i][0],X_new[i][1]])
      
