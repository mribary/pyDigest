# Import regex, pandas and numpy
import re
import pandas as pd
import numpy as np

# Read Ddf_v002.csv into a 1D dataframe: Ddf
Ddf = pd.read_csv('./input/Ddf_v003.csv', index_col=0)
Ddf.reset_index(drop=True, inplace=True)
# print(Ddf.head())

# Create 1D numpy array
Dnp = np.array(Ddf['0'])
# print(Dnp[:5])

# Regex patterns for sorting lines
section_ref_pattern = r"D\.\s(\d+,\s){2}0\sR\.\s[A-Z\s:,]+\."
heading_ref_pattern = r"D\.\s\d+,\s\d+\s?,\s(\d+[a-z]?,\s)?\d+[a-z]?\s\w+"

#########################################################
# Checking and cleaning data by removing lines from Dnp #
#########################################################

# Count number of lines in Dnp
# print(len(Dnp)) # 42553 - Number of total lines in the 1D numpy array

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
    elif re.search(heading_ref_pattern, Dnp[i - 1]) is not None:
        index_list_p.append(i + 1)
    else:
        index_list_x.append(i)  
s = len(index_list_s)
h = len(index_list_h)
p = len(index_list_p)
x = len(index_list_x)
print(s) # 432 - All section_ref lines captured
print(h) # 21061 = (42553 - 432) / 2 -> suggests correct 1:1 ration between h and p
print(p) # 21060 - Reference headings and text units should have a 1:1 correspondence
print(x) # No error lines
print(s+h+p+x) # 42553 - Sum of number of lines captured which corresponds with the total
print((s+h+p+x) == len(Dnp)) # True

# Regular expressions seem to capture all lines correctly
# Move on to creating a structured dataframe

#########################################################
# Creating structured dataframe from the 1D numpy array #
#########################################################

# Create dictionary with keys as column names
Ddict = {"Section_title":[], "Book_no": [], "Section_no": [], "Passage_no":
    [], "TextUnit_no": [], "TextUnit_ref": [], "TextUnit": []}

# Regex patterns for Ddict dictionary
section_title_pattern = re.compile(r"(?<=R\.\s)([A-Z\s]+)")
ref_pattern = re.compile(r"(?<=D\.\s)(\d+),\s(\d+),\s(\d+[a-z]?),\s(\d+[a-z]?)\s([A-Za-z][a-z].+)")
ref_alt_pattern = re.compile(r"(?<=D\.\s)(\d+),\s(\d+)\s?,\s(\d+[a-z]?)\s([A-Za-z][a-z].+)")
heading3032_pattern = r"D\.\s\d+,\s\d+\s?,\s\d+\s[A-Za-z][a-z].+"
heading_pattern = r"D\.\s\d+,\s\d+,\s\d+[a-z]?,\s\d+[a-z]?\s[A-Za-z][a-z].+"

# Feeding Ddict dictionary from Dnp
index_list_error = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_pattern, Dnp[i]) is not None:
        section_title = section_title_pattern.search(Dnp[i]).group(1)
    elif re.search(heading_ref_pattern, Dnp[i]) is not None:
        if re.search(heading3032_pattern, Dnp[i]) is not None:
            book_no = ref_alt_pattern.search(Dnp[i]).group(1)
            section_no = ref_alt_pattern.search(Dnp[i]).group(2)
            passage_no = ref_alt_pattern.search(Dnp[i]).group(3)
            textunit_no = 0
            passage_ref = ref_alt_pattern.search(Dnp[i]).group(4)
            Ddict["Section_title"].append(section_title)
            Ddict["Book_no"].append(book_no)
            Ddict["Section_no"].append(section_no)
            Ddict["Passage_no"].append(passage_no)
            Ddict["TextUnit_no"].append(paragraph_no)
            Ddict["TextUnit_ref"].append(passage_ref)
            passage = Dnp[(i + 1)]
            Ddict["TextUnit"].append(passage)
        elif re.search(heading_pattern, Dnp[i]) is not None:
            book_no = ref_pattern.search(Dnp[i]).group(1)
            section_no = ref_pattern.search(Dnp[i]).group(2)
            passage_no = ref_pattern.search(Dnp[i]).group(3)
            paragraph_no = ref_pattern.search(Dnp[i]).group(4)
            passage_ref = ref_pattern.search(Dnp[i]).group(5)
            Ddict["Section_title"].append(section_title)
            Ddict["Book_no"].append(book_no)
            Ddict["Section_no"].append(section_no)
            Ddict["Passage_no"].append(passage_no)
            Ddict["TextUnit_no"].append(paragraph_no)
            Ddict["TextUnit_ref"].append(passage_ref)
            passage = Dnp[(i + 1)]
            Ddict["TextUnit"].append(passage)
    elif re.search(heading_ref_pattern, Dnp[i - 1]) is not None:
        next
    else:
        index_list_error.append(i)

# Check whether ther is any uncaptured lines
print(len(index_list_error)) # No uncaptured lines

# Create dataframe (Ddf) from the dictionary (Ddict)
Ddf = pd.DataFrame(Ddict)
print(len(Ddf)) # 21055 text units
print(Ddf[:15])
print(Ddf.info())

# Export Ddf dataframe as "Ddf.csv"
Ddf.to_csv("./output/Ddf_v100.csv")