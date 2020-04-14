# Import basic packages
import pandas as pd
import re
import numpy as np

# Load dataframes from GitHub repo
file_path_df = 'https://raw.githubusercontent.com/mribary/pyDigest/master/input/Ddf_v105.csv'
file_path_s = 'https://raw.githubusercontent.com/mribary/pyDigest/master/input/Ddf_sections_v001.csv'
file_path_sID = 'https://raw.githubusercontent.com/mribary/pyDigest/master/input/Ddf_Section_IDs_v001.csv'
df = pd.read_csv(file_path_df, index_col=0)     # text units (21055)
s = pd.read_csv(file_path_s, index_col=0)       # text unitts with section IDs (21055)
sID = pd.read_csv(file_path_sID, index_col=0)   # sections with section IDs (432)
# Merge dataframes and keep only necessary columns
df_1 = df.TextUnit
s_1 = s.Section_id
s_df = pd.merge(s_1, df_1, left_index=True, right_index=True)

# Bag of words from thematic sections with preprocessing
punctuation = r"[\"#$%&\'()*+,-/:;<=>@[\]^_`{|}~.?!«»]"             # Punctuation pattern
bow_sections = []
for i in range(len(s_df.Section_id.unique())):
    text = str(list(s_df.TextUnit[s_df.Section_id == i]))           # Load all text units from a thematic unit
    text_no_punct = re.sub(punctuation, '', text)                   # Remove punctuation
    text_one_white_space = re.sub(r"\s{2,}", ' ', text_no_punct)    # Leave only one white space between words
    text_lower = text_one_white_space.lower()                       # Transform to all lower case
    text_split = text_lower.split(' ')                              # Split to a list of tokens
    bow_sections.append(text_split)                                 # Load word tokens into a list
sID['bow'] = bow_sections                                           # Insert bow in a new column in sID

# Import packages and models from cltk and initialize tools
from cltk.corpus.utils.importer import CorpusImporter
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
corpus_importer = CorpusImporter('latin')                           # Initialize cltk's CorpusImporter
corpus_importer.import_corpus('latin_models_cltk')                  # Import the latin_models_cltk corpus for lemmatization
lemmatizer = BackoffLatinLemmatizer()                               # Initialize Latin lemmatizer

# Create a column with tuples of (token, lemma)
lemmas_list = []
for x in sID.Section_id:
    tokens = sID.loc[sID.Section_id == x,'bow'].values[0]           # Load tokens from the bow column
    lemmas = lemmatizer.lemmatize(tokens)                           # Lemmatize tokens
    lemmas_list.append(lemmas)                                      # Load lemmas into a list
sID['lemmas'] = lemmas_list                                         # Insert lemmas in a new column

# Create a list of "documents" from lemmas for vectorization
lem_doc = []
for x in sID.Section_id:
    lemmas = sID.loc[sID.Section_id == x,'lemmas'].values[0]        # Load tokens from the bow column
    l = []                                                          # Create empty list for lemmas in one row
    for y in range(len(lemmas)):
        l.append(lemmas[y][1])                                      # Load the lemma (and drop the token) to the list
    l_string = ' '.join([str(word) for word in l])                  # Create a string from the list: "document"
    lem_doc.append(l_string)                                        # Add the "document" to a list
sID['lem_doc'] = lem_doc                                            # Insert list of "documents" in a new column

# Import and initialize TfidfVecotirizer with custom stoplist
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
# Vectorize section titles based on a corpus of 432 documents including the 432 section titles
corpus = lem_doc                                # Define corpus as set of "documents" from section titles
X = vectorizer.fit_transform(corpus)            # Vectorize: dtype: matrix, shape: (432, 10925)
scores = X.toarray().transpose()                # Create and transpose array: dtype: numpy array, shape: (10925, 432)
feature_names = vectorizer.get_feature_names()  # Extract the feature names for the Tfidf dictionary: dtype: list, len: 10925

# Create dictionary with lemmas as keys and Tfidf scores in section titles as values
feature_scores = dict(zip(feature_names, scores))

# Create dataframe for lemmas and their Tfidf scores
df_fs = pd.DataFrame(feature_scores)

# Get the first 20 lemmas with the highest Tfidf scores in thematic section id "0"
# dict(df_fs.loc[0].transpose().sort_values(ascending=False).head(20))

# Create recommender for 10 most similar thematic sections based on cosine similarity
from sklearn.metrics.pairwise import linear_kernel                     # Import cosine_similarity (as linear_kernel)
corpus = lem_doc                                # Define corpus as set of "documents" from section titles
X = vectorizer.fit_transform(corpus)            # Generate Tfidf matrix: X
cosine_sim = linear_kernel(X, X)                # Generate cosine similarity matrix: cosine_sim
def similar(id, cosine_sim):
    # Sort thematic sections based on the similarity scores
    sim_scores = list(enumerate(cosine_sim[id]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores for 10 most similar thematic sections
    sim_scores = sim_scores[1:11]
    return sim_scores

def similar_sections(id):
    similar_to_id = similar(id, cosine_sim)
    similar_dict_id = {'Section_id':[], 'Book_no':[], 'Section_no':[], 'Section_title':[], 'Similarity_score':[]}
    for i in range(10):
        section_id = similar_to_id[i][0]
        text_unit_id = sID.loc[sID.Section_id == section_id].index[0]
        book_no = df.loc[df.index == text_unit_id,'Book_no'].values[0]
        section_no = df.loc[df.index == text_unit_id,'Section_no'].values[0]
        section_title = df.loc[df.index == text_unit_id,'Section_title'].values[0]
        similarity_score = similar_to_id[i][1]
        similar_dict_id['Section_id'].append(section_id)
        similar_dict_id['Book_no'].append(book_no)
        similar_dict_id['Section_no'].append(section_no)
        similar_dict_id['Section_title'].append(section_title)
        similar_dict_id['Similarity_score'].append(similarity_score)
    similar_df_id = pd.DataFrame(similar_dict_id)
    return similar_df_id

# df_59 = similar_sections(59)
# df_59.to_csv('/home/mribary/Desktop/df_59.csv')