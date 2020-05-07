# Import packages
import pandas as pd 
from sklearn import cluster
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt

# Load normalized dataframes
df = pd.read_csv('./dump/D_lemmatized_norm.csv', index_col=0)
sf = pd.read_csv('./dump/tfidf_sections_norm_top50.csv', index_col=0)
tf = pd.read_csv('./dump/tfidf_titles_norm.csv', index_col=0)

# Extract matrix from dataframe
X = np.array(sf.values)         # Tfidf matrix of shape xxx (sections) x xxx (terms)
section_IDs = list(sf.index)    # List for section_IDs
print(X.shape)

# Generate silhouette scores for the range between 2 and 75 clusters
NumberOfClusters=range(2,75)
silhouette_score_values=list()
for i in NumberOfClusters:
    classifier=cluster.KMeans(i,init='k-means++', n_init=10, max_iter=300, \
        tol=0.0001, verbose=0, random_state=None, copy_x=True)
    classifier.fit(X)
    labels = classifier.predict(X)
    score = silhouette_score(X, labels, metric='euclidean', sample_size=None, random_state=None)
    silhouette_score_values.append(score)
    print('|', end= '')

# Pickle silhouette scores into a binary file
import pickle
with open('./dump/silhouette_scores_norm_top50.txt', 'wb') as fp:
    pickle.dump(silhouette_score_values, fp)

# Unpickle from the binary file
with open('./dump/silhouette_scores_norm_top50.txt', 'rb') as fp:   
    silhouette_score_values = pickle.load(fp)

# Calculate the optimal number of clusters and its silhouette score
optimal = NumberOfClusters[silhouette_score_values.index(max(silhouette_score_values))]
print('Optimal number of components: ' + str(optimal) + '\n' + \
        'Silhouette score: ' + str(max(silhouette_score_values)))

# Plot silhouette scores
plt.plot(NumberOfClusters, silhouette_score_values)
plt.title('Silhouette score values' + '\n' +     'based on a normalized Tfidf matrix of the top 50 lemmas (tfidf) retained from' + '\n' +     'the 340 thematic sections exceeding 100 unique lemmas in the Digest')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette score')
plt.legend(['Optimal number of components: ' + str(optimal) + '\n' +     'Silhouette score: ' + str(max(silhouette_score_values))], loc=8)
plt.tick_params(    
    axis= 'both',       # changes apply to the x-axis
    which='both',       # both major and minor ticks are affected
    direction='in'      # ticks inside the axis
    )
plt.axvline(x=optimal, color='r', alpha=0.5, linestyle=':')
plt.axhline(y=max(silhouette_score_values), color='r', alpha=0.5, linestyle=':')
plt.show()
# Save plot
plt.savefig('./images/norm_top50_silhouette_2to75.png', dpi=300)
plt.close()