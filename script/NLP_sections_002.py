# Import basic packages
import pandas as pd 
import numpy as np

# Load dataframes
path_doc = './dump/D_lemmatized.csv'
path_tfidf_sections = './dump/tfidf_sections.csv'
path_tfidf_titles = './dump/tfidf_titles.csv'
df = pd.read_csv(path_doc, index_col=0)     # Sections with documents inlcuding lemmas from text
sf = pd.read_csv(path_tfidf_sections, index_col=0)   # Original tfidf matrix for sections
tf = pd.read_csv(path_tfidf_titles, index_col=0)   # Original tfidf matrix for titles

# Identify the cell in the doc column which is interpreted as dtype float
for i in range(len(df.doc)):
    if type(df.doc[i]) is not str:
        print(str(i) + ' ' + str(df.doc[i]) + ' - ' + str(type(df.doc[i]))) # 308 nan - <class 'float'>
# Overwrite nan value and check type
df.doc[308] = ''
# print(type(df.doc[308])) # Thematic section with id 308 had Greek characters only which were removed

# Count number of lemmas and unique lemmas in thematic sections
df['length'] = df.doc.apply(str.split).apply(len)                   # Count lemmas in section
df['length_unique'] = df.doc.apply(str.split).apply(set).apply(len) # Count unique lemmas in section
df.sort_values(by=['length_unique'], inplace=True)                  # Sort by the number of unique lemmas

# Check output, mean and median of length
# print(df.length_unique.mean())        # Average length: 347.34 lemmas
# print(df.length_unique.median())      # Median length: 270 lemmas
# print(df.head())

# Explore length at percentiles
percentiles = {'percentile':[], 'length':[]}
for x in range(100):
    length = np.percentile(df['length_unique'], x)
    percentiles['percentile'].append(x)
    percentiles['length'].append(length)
ps = pd.DataFrame(percentiles)
# print(ps.head(30))                           # Length reaches the 100-word mark between 21% and 22%

# Create list of IDs of thematic sections which are shorter than 100 unique lemmas
drop_short = df.index[df.length_unique <= 100]
# print(len(drop_short))                       # 92 thematic sections below the 100-word mark

# Remove short thematic sections from the dataframes
dataframes = [df, sf, tf]
for x in dataframes:
    x.drop(labels=drop_short, inplace=True)

# Align dataframes, rename their indexes to 'Section_id'
df.sort_values(by=['Section_id'], inplace=True)
sf.index.name = 'Section_id'
tf.index.name = 'Section_id'

# Create list of unique terms which appear in the top 50 tfidf of sections
top_terms = []
for i in sf.index:
    t = list(sf.loc[i].sort_values(ascending=False)[0:50].index)
    top_terms.extend(t)
top_terms = list(set(top_terms))    # 4029 unique terms
# print(len(top_terms))

# Keep top terms in the tfidf matrix
sf = sf[top_terms]                  # 4029 columns (unique terms) and 339 rows (thematic sections)
# print(sf.info())

# Export normalized dataframes
df.to_csv('./dump/D_lemmatized_norm.csv')
sf.to_csv('./dump/tfidf_sections_norm_top50.csv')
tf.to_csv('./dump/tfidf_titles_norm.csv')