import os,csv,pickle
import numpy

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

dataFeaturePath = '../Codes/DataFeatures.pickle'

DataFeatures = pickle.load(open(dataFeaturePath, 'rb'))

Features = []
for val in DataFeatures.values():
    Features.append(val)

k = len(Features)

silhouettes = {}


for n in range(2,k+1):

    model    = KMeans(n_clusters = n)
    clusters = model.fit_predict(Features)

    silhouettes[n] = silhouette_score(Features, clusters, sample_size = 1000)
    
#clusterfile = folder + '_scores.pkl'    
#pickle.dump(silhouettes, open(clusterfile,'wb'))

print silhouettes

n_cluster = sorted(silhouettes, key=silhouettes.__getitem__, reverse=True)[0]

print 'optimal number of clusters: ', n_cluster

model    = KMeans(n_clusters = n_cluster)
clusters = model.fit_predict(Features)
    
optimal_cluster = '../Codes/KMeans_optimal_cluster_' + str(n_cluster) + '.pkl'
pickle.dump(clusters, open(optimal_cluster,'wb'))

print clusters
