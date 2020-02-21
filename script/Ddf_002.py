# Import regex, pandas and numpy
import re
import pandas as pd
import numpy as np

# Read Ddf_v002.csv into a 1D dataframe: Ddf
Ddf = pd.read_csv('./input/Ddf_v002.csv', index_col=0)
Ddf.reset_index(drop=True, inplace=True)
# print(Ddf.head())

# Create 1D numpy array
Dnp = np.array(Ddf['0'])
# print(Dnp[:5])

# Regex patterns for sorting lines
# section_ref_pattern to include [\^:]
# book_ref_pattern = r"D\.\s\d+,\s0,\s0\sR\."
# book_title_pattern = r"^(?!(D\.))[A-Z\s]+\."
section_ref_pattern = r"D\.\s(\d+,\s){2}0\sR\.\s[A-Z\s\^:,]+\."
heading_ref_pattern = r"D\.\s\d+,\s\d+\s?,\s(\d+[a-z]?,\s)?\d+[a-z]?\s\w+"
textunit_pattern = r"^((?!(D\.|[A-Z]{2,}))|\"(\s|[A-Za-z]))\w+"

#########################################################
# Checking and cleaning data by removing lines from Dnp #
#########################################################

# Count number of lines in Dnp
# print(len(Dnp)) # 42597

# Run the check for section_ref lines
# Locate section_ref lines in Dnp
index_list_s = []
index_list_h = []
index_list_p = []
index_list_x = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_pattern, Dnp[i]) is not None:
        index_list_s.append(i)
    elif re.search(heading_ref_pattern, Dnp[i]) is not None:
        index_list_h.append(i)
    elif re.search(textunit_pattern, Dnp[i]) is not None:
        index_list_p.append(i)
    else:
        index_list_x.append(i)  
# s = len(index_list_s)
# h = len(index_list_h)
# p = len(index_list_p)
# x = len(index_list_x)
# print(s) # 432 - All section_ref lines captured
# print(h) # 21058 - Some lines are probably missing
# print(p) # 21057 - Reference headings and text units should have a 1:1 correspondence
# print(x) # 50 - 50 lines are not captured lines
# print(s+h+p+x) # 42597 - Sum of number of lines captured which corresponds with the total
# print((s+h+p+x) == len(Dnp)) # True

# Create dictionary with non-captured anomalous lines and their Dnp indices
Dnp_index = list(index_list_x)
Text = list(Dnp[index_list_x])
d = {'Dnp_index' : Dnp_index, 'Text': Text}

# Create dataframe from dictionary
Ddf_v002x = pd.DataFrame(d)

# Export list of non-captured anomalous lines with their indices in a csv file
Ddf_v002x.to_csv('./output/Ddf_v002x.csv')