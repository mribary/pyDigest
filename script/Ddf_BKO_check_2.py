# Import numpy and pandas
import pandas as pd
import numpy as np

# Load filtered dataframe from Ddf.csv and remove trailing white space
Ddf = pd.read_csv('./input/Ddf_v103.csv', usecols=['BKO_key'])
Ddf.BKO_key = Ddf.BKO_key.map(lambda x: x.strip())
# print(list(Ddf.BKO_key))

BKO_unique = Ddf.BKO_key.unique()
# print(len(BKO_unique)) # 397

# Load filtered dataframe from BKO.csv and remove trailing white space
BKOdf = pd.read_csv('./input/BKO_v003.csv', usecols=['Work_ref'])
BKOdf.Work_ref = BKOdf.Work_ref.astype(str)
BKOdf.Work_ref = BKOdf.Work_ref.map(lambda x: x.strip())
# print(list(BKOdf.Work_ref))
# print(len(BKOdf.Work_ref)) # 298

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