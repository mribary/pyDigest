# Import packages
import pandas as pd 
import numpy as np
import re
punctuation = r"[\"#$%&\'()*+,-/:;<=>@[\]^_`{|}~.?!«»]" 

# Load dataframe
path = '/home/mribary/Dropbox/pyDigest/dump/hierarchlust_terms_norm_top50.csv'
df = pd.read_csv(path, index_col=0)

# Write cluster terms at cuts into individual text files
cuts = ['3.5', '3.0', '2.5', '2.0', '1.75', '1.5', '1.375']
for cut in cuts:
    path = '/home/mribary/Dropbox/pyDigest/dump/' + str(cut) + '_cut_terms.txt'
    with open(path, "a") as f:
        for y in set(df[cut].values):
            print(len(df[cut][df[cut] == y]), file=f)
            terms = df[str(cut) + '_top10_terms_only'][min(df.index[df[cut] == y])]
            new_terms = re.sub(punctuation, '', terms)
            terms_list = new_terms.split(' ')
            for x in terms_list:
                print(x, file=f)
            print('\n', file=f)