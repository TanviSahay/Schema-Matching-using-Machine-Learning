import pickle, csv
import os, numpy
from sklearn.neighbors import KNeighborsClassifier

Train_Data  = pickle.load(open('../Feature_Vectors/normalised_features_train.pickle'))		#Train_Data[Attribute Name] = feature vector
Test_Data   = pickle.load(open('../Feature_Vectors/normalised_features_match.pickle'))		#Test_Data[Attribute Name] = feature vector

#Attribute Name, Cluster ID
Train_Data_Clusters = csv.reader(open('../Results/Centroid_Clustering_Result/AttributeCluster_centroid_49_itr1000.csv','r'))		

#The input to KNN will be (X,Y) where X is a list of lists, with each internal list = a feature vector and Y is a list with each value = cluster id of the corresponding input vector.
Train_Input_X = []
Train_Input_Y = []
Test_Input_X  = []
Test_Input_attribute = []

#Prepare Training Input
for row in Train_Data_Clusters:
    if row[0] != 'Attribute':
        Train_Input_X.append(Train_Data[row[0]])
        Train_Input_Y.append(row[1])

#Prepare Testing Input
for key,value in Test_Data.items():
    Test_Input_attribute.append(key)
    Test_Input_X.append(value)


#Prepare a KNN classifier that uses BallTree algorithm and takes number of neighbors as input from the user.
a = raw_input('use default number of neighbors(10) y or n: ')

if a == 'y':
    neighbors = 10
elif a == 'n':
    val = input('enter number of neigbors to be considered: ')
    neighbors = val
else:
    print 'invalid input entry, using default neighbors'
    neighbors = 10


knn_classifier = KNeighborsClassifier(n_neighbors = neighbors)
knn_classifier.fit(Train_Input_X,Train_Input_Y)

#Dump the trained tree into the current directory
pickle.dump(knn_classifier,open('trained_tree_n' + str(neighbors),'wr'))

predictions = knn_classifier.predict(Test_Input_X)

#Write predictions into a csv file 
Out_File_Path = open('../Results/KNN_Result/KNNClusteringResult_' + str(neighbors) + '.csv','w')
Test_Out = csv.writer(Out_File_Path,delimiter=',')

for pred in range(len(predictions)):
    new_row = [Test_Input_attribute[pred],predictions[pred]]
    Test_Out.writerow(new_row)

Out_File_Path.close()
