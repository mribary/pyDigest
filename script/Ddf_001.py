# Import regex, pandas and numpy
import re
import pandas as pd
import numpy as np

# Read Digest.txt into a string
str = open('./input/Digest.txt', 'r')
file = str.read()
# print(file)

# Remove empty lines, string -> list object at \n, remove copyright notice
list_file = file.splitlines()
Dlist = [x for x in list_file if x]
del Dlist[0:2]
# print(len(Dlist)) # 42681

# Regex patterns for sorting lines
section_ref_pattern = r"D\.\s(\d+,\s){2}0\sR\.\s[A-Z\s]+\."
heading_ref_pattern = r"D\.\s\d+,\s\d+\s?,\s(\d+[a-z]?,\s)?\d+[a-z]?\s\w+"

# Remove introductory lines of the Digest
del Dlist[0:2]  
# print(len(Dlist)) # 42679 lines remain

# Delete the LIBER SEPTIMUS line by index
for i in range(len(Dlist)):
    if re.search('LIBER\sSEPTIMUS', Dlist[i]) is not None:
        l7i = i
# print(Dlist[l7i])
del Dlist[l7i] # 42768 lines remain
# print(Dlist[l7i])

#########################################################
# Checking and cleaning data by removing lines from Dnp #
#########################################################

# Create a NumPy array from Dlist to check data: Dnp
Dnp = np.array(Dlist)

# Phase 1
# Locate section_ref lines from Dnf
index_list_s = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_pattern, Dnp[i]) is not None:
        index_list_s.append(i)
# print(len(index_list_s)) # 337 - it should be 432
# print(Dnp[index_list_s]) # 95 section_ref lines not captured, e.g. "D. 1, 3,"
# Explore manually in Digest.txt why 95 section_ref lines are not captured
# In "D. 1, 3," section title is in new line with an accidental line break
# In "D. 1, 7,", section title is broken into two lines with an accidental line break
# Create alternative pattern to capture hanging full capital lines
full_capital_pattern = r"^[A-Z]{2,}"
# section_ref_x_pattern = r"D\.\s(\d+,\s){2}0\sR\.^(?!\.)"
index_list_full_capital = []
for i in range(0, len(Dnp)):
    if re.search(full_capital_pattern, Dnp[i]) is not None:
        index_list_full_capital.append(i)
# print(Dnp[index_list_full_capital])
# print(len(Dnp[index_list_full_capital])) # captures 54 - 41 remain
# Check lines before hanging full capital lines
index_list_previous_lines = [x -1 for x in index_list_full_capital]
# print(Dnp[index_list_previous_lines])
# print(len(Dnp[index_list_previous_lines]))
# Append hanging full capital lines to previous line
# Add indices of superfluous lines to a delete list: index_list_delete
index_list_delete = []
for x in index_list_full_capital:
    Dnp[x -1] = Dnp[x -1] + Dnp[x]
    index_list_delete.append(x)
# print(Dnp[index_list_previous_lines])
# print(len(Dnp[index_list_previous_lines]))
# print(len(index_list_delete)) # 54

# Phase 2
# Run the check for section_ref lines again
# Locate section_ref lines from Dnp
index_list_s = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_pattern, Dnp[i]) is not None:
        index_list_s.append(i)
# print(len(index_list_s)) # 376 - it should be 432
# print(Dnp[index_list_s]) # 56 section_ref lines not captured, e.g. "D. 1, 17,"
# Explore manually in Digest.txt why 56 section_ref lines are still not captured
# "D. 1, 17, 0 r. " includes lower case "r" and an accidental line break
# Identify section_ref lines including lower case "r"
# Create alternative pattern to capture lower case "r" lines
# section_ref_pattern = r"D\.\s(\d+,\s){2}0\sR\.\s[A-Z\s]+\."
section_ref_r_pattern = r"D\.\s(\d+,\s){2}0\sr\.\s$"
index_list_r = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_r_pattern, Dnp[i]) is not None:
        index_list_r.append(i)
# print(Dnp[index_list_r])
# print(len(Dnp[index_list_r])) # captures 27 - 29 remain
# Check lines after lower case "r" section_ref lines
index_list_following_lines = [x + 1 for x in index_list_r]
# print(Dnp[index_list_following_lines])
# print(len(Dnp[index_list_following_lines]))
# Append title lines to lower case "r" section_ref lines
# Add superfluous lines to index_list_delete
for x in index_list_r:
    Dnp[x] = Dnp[x] + Dnp[x + 1]
    index_list_delete.append(x + 1)
# Turn updated lower case "r" section_ref lines full capital
Dnp[index_list_r] = np.char.upper(Dnp[index_list_r])
# print(Dnp[index_list_r])
# print(len(Dnp[index_list_r])) # 27
# print(len(index_list_delete)) # 81

# Phase 3
# Run the check for section_ref lines again
# Locate section_ref lines from Dnp
index_list_s = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_pattern, Dnp[i]) is not None:
        index_list_s.append(i)
# print(len(index_list_s)) # 402 - it should be 432
# print(Dnp[index_list_s]) # 30 section_ref lines still not captured, e.g. "D. 1, 21,"
# Explore manually in Digest.txt why 30 section_ref lines are still not captured
# "D. 1, 21, 0 R." includes a comma
# Update section_ref_pattern to include comma in the title
section_ref_pattern = r"D\.\s(\d+,\s){2}0\sR\.\s[A-Z\s,]+\."

# Phase 4
# Run the check for section_ref lines with updated pattern
# Locate section_ref lines from Dnp
index_list_s = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_pattern, Dnp[i]) is not None:
        index_list_s.append(i)
# print(len(index_list_s)) # 423 - it should be 432
# print(Dnp[index_list_s]) # 9 section_ref lines still not captured
# Explore manually in Digest.txt why 9 section_ref lines are still not captured
# Note the 9 anomalous section titles for manual editing in output file: Ddf_v001.csv
# D. 4, 8, 0 R
# D. 5, 1, 0 R
# D. 7, 7, 0 R
# D. 14, 2, 0 R
# D. 18, 7, 0 R
# D. 29, 5, 0 R
# D. 30, 0 R
# D. 33, 9, 0 R
# D. 43, 12, 0 R

# Delete superfluous lines from Dnp
# print(len(Dnp)) # 42678
Dnp_new = np.delete(Dnp, index_list_delete)
# print(len(Dnp_new)) # 42597, difference of 81

# Export Dnp as a 1D dataframe stored in csv: Ddf_v001.csv
Ddf_v001 = pd.DataFrame(Dnp_new)
print(Ddf_v001.info())
Ddf_v001.to_csv('./output/Ddf_v001.csv')

# Close Digest.txt file
str.close()