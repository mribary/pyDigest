# Import packages
import pandas as pd
import numpy as np

# Load filtered dataframe based on Ddf.csv
load_columns = ['Section_title', 'Book_no']
df = pd.read_csv('./input/Ddf_v104.csv', usecols=load_columns)
# print(df.head())
# print(df.dtypes)
# print(df.info())

# Number thematic sections and count them
section_list = [0]
section_no = 0
for i in range(1, len(df.Book_no)):
    if (df.Section_title[i] == df.Section_title[i-1]) & (df.Book_no[i] == df.Book_no[i-1]):
            section_list.append(section_no)
    else:
            section_no += 1
            section_list.append(section_no)    
# print(len(section_list)) # 21055 matches the number of text units
# print(section_no) # 431 -> 432 thematic sections, matches manual count in the ToC of Mommsen's print edition
df['Section_id'] = section_list
df['Section_title'] = df['Section_title'].astype('category')
df = df.drop(columns=['Book_no'])

# Unique section titles
Sections1 = pd.DataFrame(df.Section_id.unique())
Sections2 = pd.merge(Sections1, df, left_on=0, right_on='Section_id')
Sections2 = Sections2.drop(columns=[0])
Sections2 = Sections2[['Section_id', 'Section_title']]
drop_rows = []
for i in range(1, len(Sections2.index)):
        if Sections2.Section_id[i] == Sections2.Section_id[i-1]:
                drop_rows.append(i)
# print(432 == (21055 - len(drop_rows))) # True
Section_IDs = Sections2.drop(drop_rows)
# print(Section_IDs.head())
# print(Section_IDs.info())

# Export dataframes: Ddf_sections.csv and Ddf_Section_IDs.csv
df.to_csv("./output/Ddf_sections.csv")
Section_IDs.to_csv("./output/Ddf_Section_IDs.csv")