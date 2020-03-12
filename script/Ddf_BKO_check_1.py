# Import numpy and pandas
import pandas as pd
import numpy as np

# Load filtered dataframe from Ddf.csv and remove trailing white space
Ddf = pd.read_csv('./input/Ddf_v102.csv', usecols=['BKO_key'])
Ddf.BKO_key = Ddf.BKO_key.map(lambda x: x.strip())
# print(list(Ddf.BKO_key))
BKO_unique = Ddf.BKO_key.unique()
#print(len(BKO_unique))
#print(np.count_nonzero(Ddf.BKO_key.unique()))

# Load filtered dataframe from BKO.csv and remove trailing white space
BKOdf = pd.read_csv('./input/BKO_v002.csv', usecols=['Work_ref'])
BKOdf.Work_ref = BKOdf.Work_ref.astype(str)
BKOdf.Work_ref = BKOdf.Work_ref.map(lambda x: x.strip())
# print(list(BKOdf.Work_ref))
#print(len(BKOdf.Work_ref))

# Identify anomalous reference headings in Ddf by checking against BKO
BKO_list = []
non_BKO_list = []
count1 = 0
count2 = 0
for x in list(BKO_unique):
    if x in list(BKOdf.Work_ref):
        count1 += 1
        BKO_list.append(x)
    else:
        count2 += 1
        print(x)
#print(BKO_list)
print(count1)
print(count2)    

'''
# Count number of unique values and memory usage in Key, Ref_book_title and Ref
print(sorted(Ddf.BKO_key.unique()))
print(np.count_nonzero(Ddf.BKO_key.unique())) # 403 categories
print(np.count_nonzero(Ddf.Work.unique())) # 367 categories
print(np.count_nonzero(Ddf.TextUnit_ref.unique())) # 1522 categories


# Count number of passages
a_index = []
for i in range(0, len(Ddf.BKO_key)):
    if Ddf['TextUnit_no'][i] == 0:
        a_index.append(i)
    elif pd.isna(Ddf['TextUnit_no'][i]): # Cover anomalous books 30-32
        if Ddf['Passage_no'][i] == 0:
            a_index.append(i)
# print(len(a_index)) # 9762 individual passages
# print(a_index)
'''