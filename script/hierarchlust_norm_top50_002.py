# Import packages
import pandas as pd 
import numpy as np
from scipy.cluster.hierarchy import fcluster

# Load normalized dataframe including 340 sections and lemmas
path_norm_df = './dump/D_lemmatized_norm.csv'
df = pd.read_csv(path_norm_df, index_col=0)             

# Load dataframes to get section titles
path_sections = './dump/Ddf_Section_IDs_v001.csv'
sections = pd.read_csv(path_sections, index_col=0)      # sections with section IDs (432)
sections.set_index('Section_id', inplace=True)          # Set Section_id as index
ids = df.index.tolist()                                 # IDs of sections included in df, sf and tf
s = sections.iloc[ids]                                  # Trim dataframe to 339 sections
s.Section_title = s.Section_title.apply(str.lower)      # Transform titles to all lower case

# Load matrices from the numpy binary file
with open('./dump/norm_top50_ward_euc_clusters.npy', 'rb') as f:
    tfidf_matrix = np.load(f)
    linkage_matrix = np.load(f)

# Cut the dendrogram at specific threshold values and get cluster assignments
threshold = [3.5, 3.0, 2.5, 2.0, 1.75, 1.5, 1.375]
assignments = []
for x in threshold:
    a = fcluster(linkage_matrix,x,'distance')     
    assignments.append(a)
    print(len(set(a)))
clustering = pd.DataFrame(dict(zip(threshold, assignments)), index=s.index.tolist())

# Sort by all cluster assigments
for i in range(len(clustering.columns)):
    clustering.sort_values(by=[clustering.columns[i]], inplace=True)

# Add section titles to the dataframe
ids = clustering.index.tolist()
titles = s.Section_title[ids]
clustering.insert(0, 'title', titles)
clustering.index.name = 'id'

# Export dataframe
clustering.to_csv('./dump/hierarchlust_norm_top50.csv')