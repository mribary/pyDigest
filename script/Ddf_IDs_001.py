# Import packages
import pandas as pd
import numpy as np

# Load Ddf.csv into a pandas data frame
load_columns = ['BKO_key', 'Work', 'TextUnit_ref']
df = pd.read_csv('./dump/Ddf_v104.csv', usecols=load_columns)
# print(type(df))
# print(df.head())
# print(df.info())

# Strip whitespace in "BKO_key" column
df.BKO_key = df.BKO_key.str.strip()
df.Work = df.Work.str.strip()
df.TextUnit_ref = df.TextUnit_ref.str.strip()

# Load BKO_v004.csv into a pandas data frame
load_columns = ['Work_ref']
BKOdf = pd.read_csv('./dump/BKO_v004.csv', usecols=load_columns)
# print(type(BKOdf))
# print(BKOdf.head())
# BKOdf.info()

# Strip whitespace in "Work_ref" column
BKOdf.Work_ref = BKOdf.Work_ref.str.strip()

#######################################
# Create dataframes for reference IDs #
#######################################

# Unique BKO_keys in df
BKO_keys = pd.DataFrame(sorted(df.BKO_key.unique()))
BKO_keys[1] = range(len(BKO_keys))
BKO_keys.rename(columns={0: 'BKO_label', 1: 'BKO_id'}, inplace=True)
BKO_keys['BKO_label'] = BKO_keys['BKO_label'].astype('category')
BKO_keys = BKO_keys[['BKO_id', 'BKO_label']]
# print(BKO_keys.head())
# print(len(BKO_keys)) # 294

# Unique works in df
Works = pd.DataFrame(sorted(df.Work.unique()))
Works[1] = range(len(Works))
Works.rename(columns={0: 'Work_label', 1: 'Work_id'}, inplace=True)
Works['Work_label'] = Works['Work_label'].astype('category')
Works = Works[['Work_id', 'Work_label']]
# print(Works.head())
# print(len(Works)) # 251

# Unique libri in df
Books = pd.DataFrame(sorted(df.TextUnit_ref.unique()))
Books[1] = range(len(Books))
Books.rename(columns={0: 'Book_label', 1: 'Book_id'}, inplace=True)
Books['Book_label'] = Books['Book_label'].astype('category')
Books = Books[['Book_id', 'Book_label']]
# print(Books.head())
# print(len(Books)) # 1382

###################################################
# Link reference IDs to the indices of text units #
###################################################

# Merge df with BKO_keys: ID1
ID1 = pd.merge(df, BKO_keys, left_on='BKO_key', right_on='BKO_label')
# print(ID1.tail(10))
# print(len(ID1))

# Merge df with Works: ID2
ID2 = pd.merge(ID1, Works, left_on='Work', right_on='Work_label')
# print(ID2.tail(10))
# print(len(ID2))

# Merge IDs with BKO_keys: ID3
ID3 = pd.merge(ID2, Books, left_on='TextUnit_ref', right_on='Book_label')
# print(ID3.tail(10))
# print(len(ID3))

# Streamline ID3 for output
ID3.drop(columns=['BKO_label', 'Work_label', 'Book_label'], inplace=True)
IDs = ID3[['BKO_id', 'BKO_key', 'Work_id', 'Work', 'Book_id', 'TextUnit_ref']]
for col in ['BKO_key', 'Work', 'TextUnit_ref']:
    IDs[col] = IDs[col].astype('category')
# print(IDs.tail(10))

# Export ID dataframes: Ddf_IDs.csv, Ddf_BKO_IDs.csv, Ddf_Work_IDs.csv, Ddf_Book_IDs.csv
IDs.to_csv("./dump/Ddf_IDs_v001.csv")
BKO_keys.to_csv("./dump/Ddf_BKO_IDs_v001.csv")
Works.to_csv("./dump/Ddf_Work_IDs_v001.csv")
Books.to_csv("./dump/Ddf_Book_IDs_v001.csv")