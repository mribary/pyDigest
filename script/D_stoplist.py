# Import basic packages
import pandas as pd
import re
import numpy as np

# Load dataframes from GitHub repo
file_path_df = './dump/Ddf_v106.csv'
file_path_s = './dump/Ddf_sections_v001.csv'
file_path_sID = './dump/Ddf_Section_IDs_v001.csv'
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

# Create a list of lemmas: lem_only
lem_only = []
for x in sID.Section_id:
    lemmas = sID.loc[sID.Section_id == x,'lemmas'].values[0]        # Load tokens from the bow column
    l = []                                                          # Create empty list for lemmas in one row
    for y in range(len(lemmas)):
        l.append(lemmas[y][1])                                      # Load the lemma (and drop the token) to the list
    l_string = ' '.join([str(word) for word in l])                  # Create a string from the list: "document"
    lem_only.append(l_string)                                       # Add the "document" to a list

##################################
# Construct stoplist: D_stoplist #
##################################

# Import cltk's Stop module
from cltk.stop.latin import CorpusStoplist  # Import the Latin stop module
S = CorpusStoplist()                        # Initialize cltk's Latin stop module

# Generate Latin stoplist with cltk based on frequency
D_stoplist_initial = S.build_stoplist(lem_only, basis='frequency', size=150, inc_values=True, sort_words=False)

# List of words from initial stoplist to be exluded from stoplist
stop_from_stoplist = ['accipio', 'actio', 'actium', 'ago', 'bonus', 'causa', 'condicio', 'creditor', \
    'dies', 'dominus', 'emo', 'familia', 'fideicommitto', 'filius', 'fundus', 'hereditas', \
    'heres', 'iudicium', 'ius', 'legatus', 'lex', 'liber', 'libertas', 'locus', 'meus', 'mulier', \
    'multus', 'nomen', 'pars', 'paruus', 'pater', 'pecunia', 'pertineo', 'peto', 'possessio', 'praesto', \
    'praetor', 'quaero', 'ratio', 'relinquo', 'res', 'respondeo', 'restituo', 'scribo', 'servus', \
    'solvo', 'stipulo', 'tempus', 'teneo', 'testamentum', 'utor', 'verus']

# Adjusted stoplist (frequency values dropped)
D_stoplist = S.build_stoplist(lem_only, basis='frequency', size=120, inc_values=False, \
    sort_words=False, exclude=stop_from_stoplist)

# Export stoplist into a text file
with open('./dump/D_stoplist_001.txt', "w") as output:
    string = '\n'.join([str(word) for word in D_stoplist])
    output.write(str(string))