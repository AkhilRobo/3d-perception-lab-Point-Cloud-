import numpy as np
import matplotlib.pyplot as plt
import cv2

# Define a function to generate clusters
def cluster_gen(n_clusters, pts_minmax=(10, 100), x_mult=(1, 4), y_mult=(1, 3), 
                x_off=(0, 50), y_off=(0, 50)):
    
    clusters_x = []
    clusters_y = []
    n_points = np.random.randint(pts_minmax[0], pts_minmax[1], n_clusters)
    x_multipliers = np.random.randint(x_mult[0], x_mult[1], n_clusters)
    y_multipliers = np.random.randint(y_mult[0], y_mult[1], n_clusters)
    x_offsets = np.random.randint(x_off[0], x_off[1], n_clusters)
    y_offsets = np.random.randint(y_off[0], y_off[1], n_clusters)
     
    for idx, npts in enumerate(n_points):
        
        xpts = np.random.randn(npts) * x_multipliers[idx] + x_offsets[idx]
        ypts = np.random.randn(npts) * y_multipliers[idx] + y_offsets[idx]
        clusters_x.append(xpts)
        clusters_y.append(ypts)
    
    return clusters_x, clusters_y

n_clusters = 7
clusters_x, clusters_y = cluster_gen(n_clusters)
data = np.float32((np.concatenate(clusters_x), np.concatenate(clusters_y))).transpose()


k_clusters = 7
max_iter = 10
epsilon = 1.0
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
compactness, label, center = cv2.kmeans(data, k_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

kmeans_clusters_x = []
kmeans_clusters_y = []

for idx in range (k_clusters):
    kmeans_clusters_x.append(data[label.ravel()==idx][:,0])
    kmeans_clusters_y.append(data[label.ravel()==idx][:,1])
    
#Ploting
fig = plt.figure(figsize=(12,6))
plt.subplot(121)
min_x = np.min(data[:, 0])
max_x = np.max(data[:, 0])
min_y = np.min(data[:, 1])
max_y = np.max(data[:, 1])
for idx, xpts in enumerate(clusters_x): 
    plt.plot(xpts, clusters_y[idx], 'o')
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.title('Original Clusters', fontsize=20)
plt.subplot(122)
for idx, xpts in enumerate(kmeans_clusters_x):
    plt.plot(xpts, kmeans_clusters_y[idx], 'x')
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.title('k-means Clusters', fontsize=20)
fig.tight_layout()
plt.subplots_adjust(left=0.03, right=0.98, top=0.9, bottom=0.05)
