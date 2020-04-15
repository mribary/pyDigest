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