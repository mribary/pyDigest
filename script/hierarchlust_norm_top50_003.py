# Import packages
import pandas as pd 
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()

# Load normalized dataframes
df = pd.read_csv('/home/mribary/Dropbox/pyDigest/dump/D_lemmatized_norm.csv', index_col=0)
cf = pd.read_csv('/home/mribary/Dropbox/pyDigest/dump/hierarchlust_norm_top50.csv', index_col=0)
cf1 = cf
cf2 = cf

# Generate keywords for clusters at cuts
cuts = ['3.5', '3.0', '2.5', '2.0', '1.75', '1.5', '1.375']
for x in cuts:
    # test vectorizing for one cut
    corpus = []
    for j in set(cf[x]):
        ids = list(cf.index[cf[x] == j])
        doc = ' '.join(df.doc[ids].values)
        corpus.append(doc)

    # Vectorize
    X = vectorizer.fit_transform(corpus)            
    scores = X.toarray().transpose()                
    feature_names = vectorizer.get_feature_names()
    # Create dictionary with lemmas as keys and Tfidf scores in section titles as values
    feature_scores = dict(zip(feature_names, scores))
    # Create and export dataframe for lemmas and their Tfidf scores
    tfidf = pd.DataFrame(feature_scores)

    top10_terms_scores = []
    top10_terms_only = []
    for j in set(cf[x]):
        top10_1 = dict(tfidf.iloc[j-1].sort_values(ascending=False).head(10))       
        top10_2 = list(tfidf.iloc[j-1].sort_values(ascending=False).head(10).index)   
        for i in range(len(cf.index[cf[x] == j])):
            top10_terms_scores.append(top10_1)
            top10_terms_only.append(top10_2)

    # Insert into a column
    cf[str(x) + '_top10_terms_scores'] = top10_terms_scores
    cf[str(x) + '_top10_terms_only'] = top10_terms_only

    # Keep track of computation
    print('|', end= '')
print('complete')

cf.to_csv('/home/mribary/Dropbox/pyDigest/dump/hierarchlust_terms_norm_top50.csv')