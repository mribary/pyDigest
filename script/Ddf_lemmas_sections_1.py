# Import packages
import pandas as pd
from cltk.corpus.utils.importer import CorpusImporter
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer

# Load latin_models_cltk corpus and initialize lemmatizer
corpus_importer = CorpusImporter('latin')
corpus_importer.import_corpus('latin_models_cltk')
lemmatizer = BackoffLatinLemmatizer()

# Load Sections dataframe
Sections = pd.read_csv('./input/Ddf_Section_IDs_v001.csv', index_col=0)

# Create a bag-of-words ("bow") columns with tokens from section titles
bow_list = []
for x in Sections.Section_id:
    title = Sections.loc[Sections.Section_id == x,'Section_title'].values[0]
    lower_title = title.lower()
    split_title = lower_title.split(' ')
    bow_list.append(split_title)
Sections['bow'] = bow_list

# Create a lemmas column with a list of tuples based on tokens in bow
lemmas_list = []
for x in Sections.Section_id:
    tokens = Sections.loc[Sections.Section_id == x,'bow'].values[0]
    lemmas = lemmatizer.lemmatize(tokens)
    lemmas_list.append(lemmas)
Sections['lemmas'] = lemmas_list

# Export streamlined dataframe
Sections.drop(columns=['Section_title'], inplace=True)
Sections.set_index('Section_id', inplace=True)
Sections.to_csv('./output/Ddf_Section_lemmas_v001.csv')