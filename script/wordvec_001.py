# Import packages
import pandas as pd 
import numpy as np
import fasttext
from pyDigest import latin_lemma_text

# Load dataframes
file_path_df = '/home/mribary/Dropbox/pyDigest/dump/Ddf_v106.csv'
df = pd.read_csv(file_path_df, index_col=0)     # text units (21055)
digest_list_of_texts = list(df.TextUnit)
path_stoplist = '/home/mribary/Dropbox/pyDigest/dump/D_stoplist_001.txt'
digest_stoplist = list(pd.read_csv(path_stoplist, header=None)[0])  # 57 custom stopwords

# Create text files for fasttext - text units in new lines in one continuous string
digest_lemma_text_stop = latin_lemma_text(digest_list_of_texts, stopwords=digest_stoplist)
path = '/home/mribary/Dropbox/pyDigest/dump/dtext_stop.txt'
with open(path, "w") as f:
    text = '\n'.join([str(textunit) for textunit in digest_lemma_text_stop])        
    print(text, file=f)

digest_lemma_text_nostop = latin_lemma_text(digest_list_of_texts)
path = '/home/mribary/Dropbox/pyDigest/dump/dtext_nostop.txt'
with open(path, "w") as f:
    text = '\n'.join([str(textunit) for textunit in digest_lemma_text_nostop])
    print(text, file=f)

