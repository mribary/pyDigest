# Import basic packages
import pandas as pd
import re
import numpy as np

# Import packages and models from cltk and initialize tools
from cltk.corpus.utils.importer import CorpusImporter
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
corpus_importer = CorpusImporter('latin')                           # Initialize cltk's CorpusImporter
corpus_importer.import_corpus('latin_models_cltk')                  # Import the latin_models_cltk corpus for lemmatization
lemmatizer = BackoffLatinLemmatizer()                               # Initialize Latin lemmatizer

# Import and initialize TfidfVecotirizer with custom stoplist
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()

# Load dataframes from GitHub repo
file_path_df = './dump/Ddf_v105.csv'
file_path_s = './dump/Ddf_sections_v001.csv'
file_path_sID = './dump/Ddf_Section_IDs_v001.csv'
file_path_stoplist = './dump/D_stoplist_001.txt'
df = pd.read_csv(file_path_df, index_col=0)     # text units (21055)
s = pd.read_csv(file_path_s, index_col=0)       # text unitts with section IDs (21055)
sID = pd.read_csv(file_path_sID, index_col=0)   # sections with section IDs (432)
D_stoplist = list(pd.read_csv(file_path_stoplist, header=None)[0])  # 57 custom stopwords

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

##########################
# Tokenize and lemmatize #
##########################

# Create a column with tuples of (token, lemma)
lemmas_list = []
for x in sID.Section_id:
    tokens = sID.loc[sID.Section_id == x,'bow'].values[0]           # Load tokens from the bow column
    lemmas = lemmatizer.lemmatize(tokens)                           # Lemmatize tokens
    lemmas_list.append(lemmas)                                      # Load lemmas into a list
sID['lemmas'] = lemmas_list                                         # Insert lemmas in a new column

# Remove stopwords and create a list of "documents" from lemmas for vectorization: doc
doc = []
for x in sID.Section_id:
    lemmas = sID.loc[sID.Section_id == x,'lemmas'].values[0]    # Load tokens from the bow column
    l = []                                                      # Create empty list for lemmas in one row
    for y in range(len(lemmas)):
       l.append(lemmas[y][1])                                   # Load the lemma to the list
    l_string = ' '.join([str(word) for word in l \
        if word not in D_stoplist])                             # Drop stopwords and create a string from the list: "document"
    doc.append(l_string)                                        # Add the "document" to a list
sID['doc'] = doc                                                # Insert stopword-free lemma list into a new column

# Transform section titles to all lower case
section_titles_lower = []
for x in sID.Section_id:
    text = sID.loc[sID.Section_id == x,'Section_title'].values[0]   # Load upper-case section titles
    text_lower = text.lower()                                       # Transform to lower case
    section_titles_lower.append(text_lower)                         # Add the lower case title to a list
sID['Title'] = section_titles_lower                                 # Insert list of lower-case titles in a new column

# Streamline dataframe
sections = sID[['Section_id', 'Title', 'doc']]
sections.set_index('Section_id', inplace=True)

#############
# Vectorize #
#############

# Vectorize section titles based on a corpus of 432 documents including the 432 section titles
corpus = doc                                    # Define corpus as set of "documents" from section titles
X = vectorizer.fit_transform(corpus)            # Vectorize: dtype: matrix, shape: (432, 10875)
scores = X.toarray().transpose()                # Create and transpose array: dtype: numpy array, shape: (10875, 432)
feature_names = vectorizer.get_feature_names()  # Extract the feature names for the Tfidf dictionary: dtype: list, len: 10875

# Create dictionary with lemmas as keys and Tfidf scores in section titles as values
feature_scores = dict(zip(feature_names, scores))

# Create dataframe for lemmas and their Tfidf scores
df_fs = pd.DataFrame(feature_scores)

# Export data
df_fs.to_csv('./dump/D_tfidf_sections_001.csv')
sections.to_csv('./dump/D_doc_sections_001.csv')