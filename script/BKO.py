# Import regex and pandas
import re
import pandas as pd
import numpy as np

# Read BK_Ordo.txt into a string
str = open('./input/BKO_v002.txt', 'r')
file = str.read()

# Remove empty lines, string -> list object at \n, remove copyright notice
list_file = file.splitlines()
BKO_list = [x for x in list_file if x]

# Create regular expression pattern to extract information
BKO_pattern = re.compile(r"(\d+)\.\s(bis\.)?\s?([A-Z][a-z]+\s?([A-Z][a-z]+)?)\s(\d+)\s(.+)")

# Create an empty python dictionary with keys as column labels
BKO_dict = {'BKO_no':[], 'bis':[], 'Jurist_name':[], 'Number_of_books':[], 'Work_title':[]}

# Extract and feed data into BKO_dict
count = 0
for i in range(0, len(BKO_list)):
    if re.search(BKO_pattern, BKO_list[i]) is not None:
        count += 1
        BKO_dict['BKO_no'].append(BKO_pattern.search(BKO_list[i]).group(1))
        BKO_dict['bis'].append(BKO_pattern.search(BKO_list[i]).group(2))
        BKO_dict['Jurist_name'].append(BKO_pattern.search(BKO_list[i]).group(3))
        BKO_dict['Number_of_books'].append(BKO_pattern.search(BKO_list[i]).group(5))
        BKO_dict['Work_title'].append(BKO_pattern.search(BKO_list[i]).group(6))
print(count)

# Create dataframe BKO_df from the dictionary BKO_dict
BKO_df = pd.DataFrame(BKO_dict)

# Export BKO_df dataframe as "BKO_df_v001.csv"
BKO_df.to_csv("./output/BKO_v001.csv")

# Close BK_Ordo.txt file
str.close()