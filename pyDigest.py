def similar(id, corpus, size=10):
    '''The function returns the most similar documents to the one passed into based on cosine similarity
    calculated on the Tfidf matrix of a given corpus
    id: the index of the "document" in the corpus queried for its most similar documents
    corpus: a list of plain word strings ("documents"), the position of the "document" in the list is the
    id where indexing runs from 0 until len(corpus)-1
    size: the number of documents returned, default value is set to 10.'''
    # Handle errors
    valid_id = range(len(corpus))
    if id not in valid_id:
        raise ValueError("id must be in the range of len(corpus) which is between 0 and %r." % len(corpus))
    if type(corpus) != list:
        raise TypeError("corpus must be a plain list of word strings.")
    if type(size) != int:
        raise TypeError("size must be an integer")
    valid_size = range(1, (len(corpus)-1))
    if size not in valid_size:
        raise ValueError("size must be between 1 and %r." % (len(corpus)-1))
    # Import modules and initilaize models
    from sklearn.metrics.pairwise import linear_kernel              
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    # Calculate Tfidf matrix (X) and cosine similarity matrix (cosine_sim)
    X = vectorizer.fit_transform(corpus)
    cosine_sim = linear_kernel(X, X)
    # Calculate most similar documents
    sim_scores = list(enumerate(cosine_sim[id]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:(size + 1)]
    return sim_scores

def similar_sections(id, size=10):
    '''Returns a dataframe with the most similar thematic sections
    id: thematic section's id
    size: number of similar thematic sections returned
    '''
    import pandas as pd
    path_sID = 'https://raw.githubusercontent.com/mribary/pyDigest/master/input/Ddf_Section_IDs_v001.csv'
    path_doc = 'https://raw.githubusercontent.com/mribary/pyDigest/master/input/D_doc_sections_001.csv'
    path_df = 'https://raw.githubusercontent.com/mribary/pyDigest/master/input/Ddf_v105.csv'
    sID = pd.read_csv(path_sID, index_col=0)        # sections with section IDs (432)
    doc_df = pd.read_csv(path_doc, index_col=0)
    df = pd.read_csv(path_df, index_col=0)          # text units (21055)
    corpus = list(doc_df.doc)
    similar_to_id = similar(id, corpus, size)
    similar_dict_id = {'Section_id':[], 'Book_no':[], 'Section_no':[], 'Section_title':[], 'Similarity_score':[]}
    for i in range(size):
        section_id = similar_to_id[i][0]
        text_unit_id = sID.loc[sID.Section_id == section_id].index[0]
        book_no = df.loc[df.index == text_unit_id,'Book_no'].values[0]
        section_no = df.loc[df.index == text_unit_id,'Section_no'].values[0]
        section_title = df.loc[df.index == text_unit_id,'Section_title'].values[0]
        similarity_score = similar_to_id[i][1]
        similar_dict_id['Section_id'].append(section_id)
        similar_dict_id['Book_no'].append(book_no)
        similar_dict_id['Section_no'].append(section_no)
        similar_dict_id['Section_title'].append(section_title.lower())
        similar_dict_id['Similarity_score'].append(similarity_score)
    similar_df_id = pd.DataFrame(similar_dict_id)
    title = doc_df.Title[id]
    print("Thematic sections most similar to thematic section %r:" %id)
    print("%r" %title)
    return similar_df_id

def linkage_for_clustering(X, threshold=0):
    ''' The function takes a matrix X with observations stored in rows and features stored in columns.
    It returns a dataframe with linkage combinations of method and metric used for hierarchical
    clustering sorted by reverse order based on the absolute value of the cophenetic correlation
    coefficient (CCC). The CCC score ranges between -1 and 1 and measures how how faithfully a
    dendrogram preserves the pairwise distances between the original unmodeled data points.
    The cophenetic correlation is expected to be positive if the original distances are compared
    to cophenetic distances (or similarities to similarities) and negative if distances are
    compared to similarities.
    It needs to be noted that CCC is calculated for the whole dendrogram. Ideally, one should
    calculate CCC at the specific cut point where the dendrogram's output is used to identify the
    clusters. It is recommended to calculate CCC at the specific cut level yielding k clusters to
    confirm that the correct method-metric combination has been used for hierarchical clustering.
    The 'average' method generally produces the best CCC score especially with matrices with high
    dimensionality. Instead of relying exclusively on the CCC score, one also needs to consider 
    what method-metric combination suits the particular dataset on which hierarchical clustering 
    is performed by scipy's linkage function.
    '''
    import numpy as np
    # Handle errors
    if isinstance(X, np.ndarray) is not True:
        raise TypeError("X must be a matrix with samples in rows and observations in columns")
    if type(threshold) != float:
        raise TypeError("threshold must be a float")
    if abs(threshold) > 1:
        raise ValueError("threshold must be between -1 and 1")
    # Import basic packages
    import pandas as pd
    from scipy.cluster.hierarchy import linkage
    # List of 7 methods for the linkage function
    methods = ['ward', 'single', 'complete', 'average', 'weighted', 'centroid', 'median']
    # List of 22 metrics for the linkage function
    metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', \
        'dice',  'euclidean', 'hamming', 'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis', \
        'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', \
        'sokalsneath', 'sqeuclidean', 'yule']
    # Create list of dictioanries for the 154 method-metric combinations
    dicts = []
    for x in methods:
        for y in metrics:
            d = {'method':x, 'metric':y}
            dicts.append(d)
    # Load combinations into a dataframe
    linkages = {'method':[], 'metric': []}
    for i in range(len(dicts)):
        linkages['method'].append(dicts[i]['method'])
        linkages['metric'].append(dicts[i]['metric'])
    l = pd.DataFrame(linkages, columns=['method', 'metric'])
    # Calculate linkage matrices (Z) from X
    Z_matrices = []
    valid_mms = []
    count = 0
    for i in range(len(dicts)):
        try:
            Z = linkage(X, method=dicts[i]['method'], metric=dicts[i]['metric'])
            Z_matrices.append(Z)
            valid_mms.append(True)
            print(str(count) + ' ' + str(dicts[i]['method']) + ' & ' + (dicts[i]['metric']) + ' - matrix ready')
            count = count + 1
        except:
            valid_mms.append(False)
            pass
    # Drop invald combinations and reindex
    l = l.loc[valid_mms]
    l.reset_index(drop=True)
    # Calculate Cophenetic Correlation Coefficient for valid linkage combinations
    from scipy.cluster.hierarchy import cophenet
    from scipy.spatial.distance import pdist
    valid_scores = []
    CCC_scores = []
    for Z in Z_matrices:
        try:
            c, coph_dists = cophenet(Z, pdist(X))
            if np.isnan(c):
                valid_scores.append(False)
                CCC_scores.append(None)
                print('no score')
            else:
                valid_scores.append(True)
                CCC_scores.append(c)
                print(c)
        except RuntimeWarning:
            valid_scores.append(False)
            print('no score')
            pass
    # Insert scores, drop no values and reset index
    l['CCC_score'] = CCC_scores
    l['CCC_abs_score'] = [abs(number) if number is not None else number for number in CCC_scores]
    l = l.loc[valid_scores]
    l.reset_index(drop=True)
    # Sort method-metric pairs according to CCC score
    l.sort_values(by=['CCC_score', 'method', 'metric'], ascending=False, inplace=True)
    return l[l.CCC_score > threshold]