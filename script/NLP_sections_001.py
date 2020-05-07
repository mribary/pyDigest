# Import basic packages
import pandas as pd
import re
import numpy as np

# Import packages and models from cltk and initialize tools
from cltk.corpus.utils.importer import CorpusImporter
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
corpus_importer = CorpusImporter('latin')                           # Initialize cltk's CorpusImporter
corpus_importer.import_corpus('latin_models_cltk')                  # Import the latin_models_cltk corpus
lemmatizer = BackoffLatinLemmatizer()                               # Initialize Latin lemmatizer
from cltk.stem.latin.j_v import JVReplacer

# Import and initialize TfidfVecotirizer with custom stoplist
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()

# Load dataframes
file_path_df = '/home/mribary/Dropbox/pyDigest/dump/Ddf_v106.csv'
file_path_s = '/home/mribary/Dropbox/pyDigest/dump/Ddf_sections_v001.csv'
file_path_sID = '/home/mribary/Dropbox/pyDigest/dump/Ddf_Section_IDs_v001.csv'
file_path_stoplist = '/home/mribary/Dropbox/pyDigest/dump/D_stoplist_001.txt'
df = pd.read_csv(file_path_df, index_col=0)     # text units (21055)
s = pd.read_csv(file_path_s, index_col=0)       # text unitts with section IDs (21055)
sID = pd.read_csv(file_path_sID, index_col=0)   # sections with section IDs (432)
D_stoplist = list(pd.read_csv(file_path_stoplist, header=None)[0])  # 57 custom stopwords
punctuation = r"[\"#$%&\'()*+,-/:;<=>@[\]^_`{|}~.?!«»]"             # Punctuation pattern

# Merge dataframes and keep only necessary columns
df_1 = df.TextUnit
s_1 = s.Section_id
s_df = pd.merge(s_1, df_1, left_index=True, right_index=True)

# Pre-process, tokenize, lemmatize text of thematic sections
docs = []
for i in range(len(s_df.Section_id.unique())):
    text = str(list(s_df.TextUnit[s_df.Section_id == i]))           # Load all text units from a thematic unit
    new_text = ''.join(["" if ord(i) < 32 or ord(i) > 126 else i for i in text])
                                                                    # Remove Greek (non-ASCII) characters
    text_no_punct = re.sub(punctuation, '', new_text)               # Remove punctuation
    text_one_white_space = re.sub(r"\s{2,}", ' ', text_no_punct)    # Leave only one white space b/w words
    text_no_trailing_space = text_one_white_space.strip()           # Remove trailing white space
    text_lower = text_no_trailing_space.lower()                     # Transform to all lower case
    text_split = text_lower.split(' ')                              # Split to a list of tokens
    lemmas = lemmatizer.lemmatize(text_split)                       # Lemmatize
    l = []                                                          # Create empty list for lemmas
    for y in range(len(lemmas)):
        if lemmas[y][1] not in D_stoplist:
            l.append(lemmas[y][1])                      # Load the lemma to the list
    l_string = ' '.join([str(word) for word in l])      # Drop stopwords and create a string
    docs.append(l_string)                               # Add the "document" to a list
sID['doc'] = docs                                       # Insert stopword-free lemma list into a new column

# Pre-process, tokenize and lemmatize section titles
section_titles = []
for x in sID.Section_id:    
    text = sID.loc[sID.Section_id == x,'Section_title'].values[0]   # Load upper-case section titles
    new_text = ''.join(["" if ord(i) < 32 or ord(i) > 126 else i for i in text])
                                                                    # Remove Greek (non-ASCII) characters
    text_no_punct = re.sub(punctuation, '', new_text)               # Remove punctuation
    text_one_white_space = re.sub(r"\s{2,}", ' ', text_no_punct)    # Leave only one white space between words
    text_no_trailing_space = text_one_white_space.strip()           # Remove trailing white space
    text_lower = text_no_trailing_space.lower()                     # Transform to all lower case
    text_split = text_lower.split(' ')
    lemmas = lemmatizer.lemmatize(text_split)
    l =[]
    for y in range(len(lemmas)):
        if lemmas[y][1] not in D_stoplist:
            l.append(lemmas[y][1])                           # Load the lemma to the list
    l_string = ' '.join([str(word) for word in l])
    section_titles.append(l_string)
sID['title'] = section_titles

# Streamline and export dataframe
sections = sID[['Section_id', 'title', 'doc']]
sections.set_index('Section_id', inplace=True)
sections.to_csv('./dump/D_lemmatized.csv')

#############
# Vectorize #
#############

# Vectorize the titles of the 432 thematic sections
corpus = section_titles                         # Define corpus as set of "documents" from section titles
X = vectorizer.fit_transform(corpus)            # Vectorize: dtype: matrix, shape: (432, 641)
# print(X.shape)
scores = X.toarray().transpose()                # Create and transpose array: dtype: numpy array, shape: (641, 432)
feature_names = vectorizer.get_feature_names()  # Extract the feature names for the Tfidf dictionary: dtype: list, len: 641

# Create dictionary with lemmas as keys and Tfidf scores in section titles as values
feature_scores = dict(zip(feature_names, scores))

# Create and export dataframe for lemmas and their Tfidf scores
tfidf_titles = pd.DataFrame(feature_scores)
tfidf_titles.to_csv('./dump/tfidf_titles.csv')

# Vectorize the text of the 432 thematic sections
corpus = docs                                   # Define corpus as set of "documents" from section titles
X = vectorizer.fit_transform(corpus)            # Vectorize: dtype: matrix, shape: (432, 10865)
# print(X.shape)
scores = X.toarray().transpose()                # Create and transpose array: dtype: numpy array, shape: (10865, 432)
feature_names = vectorizer.get_feature_names()  # Extract the feature names for the Tfidf dictionary: dtype: list, len: 10865

# Create dictionary with lemmas as keys and Tfidf scores in section titles as values
feature_scores = dict(zip(feature_names, scores))

# Create dataframe for lemmas and their Tfidf scores
tfidf_sections = pd.DataFrame(feature_scores)
tfidf_sections.to_csv('./dump/tfidf_sections.csv')