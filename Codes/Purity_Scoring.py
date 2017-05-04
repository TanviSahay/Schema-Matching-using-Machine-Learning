#Scoring using Intersection/ Union
import numpy as np
from collections import defaultdict
import collections
import csv, os

def ExtractCSVtoDICT(data):
    reader = csv.reader(open(data))
    Manual_Clusters=defaultdict(list)
    keys=[] 
    Values=[]
    for row in reader:
        keys.append(row[0])
        Values.append(row[1])
    i=0
    for i in range(0,len(keys)-1):
        k=keys[i]
        if(keys[i]==keys[i+1]):
            Manual_Clusters[k.lower()].append(Values[i])
        else:
            Manual_Clusters[k.lower()].append(Values[i])
            
    return Manual_Clusters

def scoring(c1,c2):
    c1_keys = [int(k) for k in c1.keys()]
    c2_keys = [int(k) for k in c2.keys()]
    #print c2.keys()
    n2=max(c2_keys)
    n1=max(c1_keys)
    #print n1, n2
    Score_Matrix=np.arange((n2+1)*(n1+1))
    Score_Matrix = np.zeros((n2+1, n1+1))
    for keys in c2.keys():
        #print keys
        value2=c2[keys]
        for key in c1.keys():
            value1=c1[key]
            #print key
            intersected=set(value1).intersection(value2)
            score= len(intersected)
            #print score
            Score_Matrix[int(keys)][int(key)]=round(score,3)
    return Score_Matrix

def printMatrix2(testMatrix):
    f = open(path+'matrix_output.txt', 'w')
    print ' ',
    for i in range(len(testMatrix[1])):
        print i,
    print
    for i, element in enumerate(testMatrix):
       saved_this=str(i), ' '.join(str(element))
       f.write(str(saved_this))  
       f.write("\n")

def column(matrix, i):
    return [row[i-1] for row in matrix]  
          
path=os.getcwd()
data1='../Results/manual_clusters_combined.csv'  
Manual_Cluster=ExtractCSVtoDICT(data1)
N = len(Manual_Cluster)

print '---Number of samples: ', N, '---'

#for r in range(29,60): 
data_path = '../Results/Distances/All_distances_combined/Clusters_combined'
data_list = os.listdir(data_path)
#data_list = ['30_review_manualClusters_w2vrandInit.csv','31_review_manualClusters_w2vrandInit.csv','32_review_manualClusters_w2vrandInit.csv','33_review_manualClusters_w2vpreInit.csv','34_review_manualClusters_w2vpreInit.csv','35_review_manualClusters_w2vpreInit.csv','36_review_manualClusters_w2vpreInit.csv']
#data_list = ['review_manualClusters_w2vrandomInit_30.csv','review_manualClusters_w2vrandomInit_31.csv','review_manualClusters_w2vrandomInit_32.csv','review_manualClusters_w2vrandomInit_33.csv','review_manualClusters_w2vrandomInit_34.csv','review_manualClusters_w2vrandomInit_35.csv','review_manualClusters_w2vrandomInit_36.csv','review_manualClusters_w2vrandomInit_37.csv','review_manualClusters_w2vrandomInit_38.csv','review_manualClusters_w2vrandomInit_39.csv','review_manualClusters_w2vrandomInit_40.csv','review_manualClusters_w2vrandomInit_41.csv','review_manualClusters_w2vrandomInit_42.csv','review_manualClusters_w2vrandomInit_43.csv','review_manualClusters_w2vrandomInit_44.csv','review_manualClusters_w2vrandomInit_45.csv','review_manualClusters_w2vrandomInit_46.csv','review_manualClusters_w2vrandomInit_47.csv','review_manualClusters_w2vrandomInit_48.csv','review_manualClusters_w2vrandomInit_49.csv']
#data_list=['g_concat_23.csv']
for data in data_list:
#data2='../Review_Phrases/review_manualClusters_w2vrandomInit_39.csv'
    #data3=os.path.join(path, "KmeansResults.csv")
    if data.endswith('.csv'):
        data2 = os.path.join(data_path, data)
        Gaussian_Cluster=ExtractCSVtoDICT(data2)
    #KMeans_Cluster=ExtractCSVtoDICT(data3)
#printMatrix2(scoring(Manual_Cluster,Gaussian_Cluster))
        scores1=scoring(Manual_Cluster,Gaussian_Cluster)
    #scores2=scoring(Manual_Cluster,KMeans_Cluster)

        Max_Scores = {}

        i = 0
        for row in scores1:
            scores = [float(score) for score in row]
            Max_Scores[i] = max(scores[:])
            i += 1

        purity_sum = 0
    #print Max_Scores
        for val in Max_Scores.values():
            purity_sum += val

            purity_score = float(purity_sum) / 391
    

        print "purity for gaussian clustering for file %s: %f" % (data2, purity_score)

        output_file = open('../Results/Distances/All_distances_combined/purity_' + data,'wb')
        output_csv = csv.writer(output_file)
        output_csv.writerow([data, purity_score])

output_file.close()        

#np.savetxt(path+"/purity_input_w2vrandomInit.csv", scores1, delimiter=",")

#np.savetxt(path+"/purity_KMeans.csv", scores2, delimiter=",")




        
