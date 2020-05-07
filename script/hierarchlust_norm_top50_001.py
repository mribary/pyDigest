# Import packages
import pandas as pd 
from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import linear_kernel       # cosine_similarity as linear_kernel#
from scipy.cluster.hierarchy import dendrogram, linkage
# import pyDigest

# Load normalized dataframes
df = pd.read_csv('./dump/D_lemmatized_norm.csv', index_col=0)
sf = pd.read_csv('./dump/tfidf_sections_norm_top50.csv', index_col=0)
tf = pd.read_csv('./dump/tfidf_titles_norm.csv', index_col=0)

# Extract matrix from dataframe
X = np.array(sf.values)         # Tfidf matrix of shape 339 (sections) x 3868 (terms)
section_IDs = list(sf.index)    # List for section_IDs
print(X.shape)

# Run method-metric linkage combinations and print cophenetic correlation coefficient (CCC-score)
# mmdf = pyDigest.linkage_for_clustering(X, threshold=0.1)
# mmdf.head(20)
# Display the CCC-score for the ward/euclidean method-metric pair
# print(mmdf[mmdf.method == 'ward'])

# Create denrdogram for hierarchical clustering based on Ward's method
linkage_matrix = linkage(X, method='ward', metric='euclidean')
fig, ax = plt.subplots(figsize=(22.5, 30)) # Set plot size
ax = dendrogram(linkage_matrix, orientation="right", labels=section_IDs)

plt.tick_params(    
    axis= 'x',         # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout

plt.title("Dendrogram of thematic sections of the Digest based on Ward's method")
plt.xlabel("Euclidean distance between clusters")
plt.ylabel("ID of thematic sections")

# Save plot
plt.savefig('./images/norm_top50_ward_euc_clusters.png', dpi=200) #save figure as ward_clusters

# Save tfidf matrix and linkage matrix in a numpy binary file
with open('./dump/norm_top50_ward_euc_clusters.npy', 'wb') as f:
    np.save(f, X)
    np.save(f, linkage_matrix)

'''
# Load matrices from the numpy binary file
with open('./dump/norm_top50_ward_euc_clusters.npy', 'rb') as f:
    tfidf_matrix = np.load(f)
    linkage_matrix = np.load(f)
'''