# Code source: Gaël Varoquaux
# Modified for documentation by Jaques Grobler
# License: BSD 3 clause

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from sklearn.decomposition import PCA
from collections import defaultdict
from math import sqrt
import numpy as np
import random

result = []
centroids = []

def Euclidean__distance(p, c):
    return sqrt(sum((e1-e2)**2 for e1, e2 in zip(p,c)))

def k_means_algorithm(data):
    result_list = []
    distance_p_to_c = []
    p1, p2, p3 = random.sample(range(0, len(data)), 3)
    centroids.append(data[p1])
    centroids.append(data[p2])
    centroids.append(data[p3])
    
    while True:
        for p in data:
            curr = []
            for c in centroids:
                Euclidean_dis = Euclidean__distance(p,c)
                #print(Euclidean_dis)
                curr.append(Euclidean_dis)
            distance_p_to_c.append(curr)
        
        new_result_list = []

        for p in distance_p_to_c:
            #print(distance_p_to_c[p])
            new_result_list.append(np.argmin(p))

        if  new_result_list == result_list:
            return result_list
        else:
            result_list = new_result_list
            distance_p_to_c = []

        for i in range(len(centroids)):
            point_set = []
            for index, p in enumerate(result_list):
                if p == i:
                    point_set.append(data[index])
            
            centroids[i] = np.mean(point_set,axis = 0)
            #print("centroids[i]: ", centroids[i])

# import some data to play with
iris = datasets.load_iris()
#print(iris)

data = iris.data[:, :4]  # we only take the first two features.
y = iris.target

x_min, x_max = data[:, 0].min() - 0.5, data[:, 0].max() + 0.5
y_min, y_max = data[:, 1].min() - 0.5, data[:, 1].max() + 0.5
result = k_means_algorithm(data)

plt.figure(2, figsize=(8, 6))
plt.clf()

# Plot the training points
print(type(centroids))
print(type(data[:4]))
arr = np.array(centroids)
plt.scatter(data[:, 0], data[:, 1], c=result, cmap=plt.cm.Set1, edgecolor="k")
plt.scatter(arr[:, 0], arr[:, 1], cmap=plt.cm.Set1, edgecolor="k")

plt.xlabel("Sepal length")
plt.ylabel("Sepal width")
plt.title("3-means Clustering")

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())

# To getter a better understanding of interaction of the dimensions
# plot the first three PCA dimensions
fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
X_reduced = PCA(n_components=3).fit_transform(iris.data)
ax.scatter(
    X_reduced[:, 0],
    X_reduced[:, 1],
    X_reduced[:, 2],
    c=y,
    cmap=plt.cm.Set1,
    edgecolor="k",
    s=40,
)
ax.set_title("First three PCA directions")
ax.set_xlabel("1st eigenvector")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("2nd eigenvector")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("3rd eigenvector")
ax.w_zaxis.set_ticklabels([])

plt.show()