# Import numpy and pandas
import pandas as pd
import numpy as np

# Load dataframes frdom csv files
BKO_IDs = pd.read_csv('./input/Ddf_BKO_IDs_v002.csv')
# Book_IDs = pd.read_csv('./input/Ddf_Book_IDs_v002.csv')
# Work_IDs = pd.read_csv('./input/Ddf_Work_IDs_v002.csv')
Ddf_IDs = pd.read_csv('./input/Ddf_IDs_v002.csv')
BKO = pd.read_csv('./input/BKO_v004.csv')
Jurists = pd.read_csv('./input/Jurists_v002.csv', index_col=None)

# Merge BKO with Jurists
BKO1 = pd.merge(BKO, Jurists, left_on='Jurist_name', right_on='Jurist')
BKO = BKO1[['Jurist_id', 'Jurist', 'Mid_date', 'Work_ref', 'BK_mass', 'BK_Ordo_no', 'BK_Ordo_no_rev', \
    'Honore_group_type', 'Honore_group_no', 'Honore_group_name', 'Work_title', 'Number_of_books', 'Note_x']]
# print(BKO.head())
# print(len(BKO)) # 300

# Merge BKO_IDs with Jurists
BKO_IDs.BKO_label = BKO_IDs.BKO_label.str.strip()
BKO.Work_ref = BKO.Work_ref.str.strip()
BKO_IDs1 = pd.merge(BKO_IDs, BKO, left_on='BKO_label', right_on='Work_ref')
BKO_IDs = BKO_IDs1[['BKO_id', 'BKO_label', 'Jurist_id', 'Mid_date']]
# print(BKO_IDs.head())
# print(len(BKO_IDs)) # 293

# Merge Ddf_IDs with Jurists
Ddf_IDs1 = pd.merge(Ddf_IDs, BKO_IDs, on='BKO_id')
Ddf_IDs = Ddf_IDs1[['BKO_id', 'Jurist_id', 'Mid_date', 'BKO_key', 'Work_id', 'Work', 'Book_id', 'TextUnit_ref']]
# print(Ddf_IDs.head())
# print(len(Ddf_IDs)) # 21055

# Update Work_IDs
Work_IDs1 = Ddf_IDs[['Work_id', 'Work', 'Jurist_id', 'Mid_date']]
Work_IDs1.rename(columns={'Work': 'Work_label'}, inplace=True)
Work_IDs2 = Work_IDs1.drop_duplicates('Work_id')
Work_IDs = Work_IDs2.sort_values(by=['Work_id'])
Work_IDs.reset_index(level=0, inplace=True)
Work_IDs.drop(columns=['index'], inplace=True)
# print(Work_IDs.head())
# print(len(Work_IDs)) # 250

# Update Book_IDs
Book_IDs1 = Ddf_IDs[['Book_id', 'TextUnit_ref', 'Jurist_id', 'Mid_date']]
Book_IDs1.rename(columns={'TextUnit_ref': 'Book_label'}, inplace=True)
Book_IDs2 = Book_IDs1.drop_duplicates('Book_id')
Book_IDs = Book_IDs2.sort_values(by=['Book_id'])
Book_IDs.reset_index(level=0, inplace=True)
Book_IDs.drop(columns=['index'], inplace=True)
# print(Book_IDs.head())
# print(len(Book_IDs)) # 1381

# Export BKO and ID dataframes
BKO.to_csv("./output/BKO_v005.csv")
Ddf_IDs.to_csv("./output/Ddf_IDs_v003.csv")
BKO_IDs.to_csv("./output/Ddf_BKO_IDs_v003.csv")
Work_IDs.to_csv("./output/Ddf_Work_IDs_v003.csv")
Book_IDs.to_csv("./output/Ddf_Book_IDs_v003.csv")