'''
# Run the check for heading_ref lines
# Locate heading_ref lines in Dnp
index_list_h = []
for i in range(0, len(Dnp_new)):
    if re.search(heading_ref_pattern, Dnp_new[i]) is not None:
        index_list_h.append(i)
        if re.search(heading_ref_pattern, Dnp_new[i + 1]) is not None:
            print(Dnp_new[i +1])


print(len(index_list_h)) # 21083
# Dnp = np.delete(Dnp_check, index_list_h)
print(len(Dnp_new)) # 21081 = 42164 - 21083
print(len(index_list_h)) # 21083


# Passage lines
index_list_p = []
for i in range(0, len(Dnp_check)):
    if re.search(passage_pattern, Dnp_check[i]) is not None:
        index_list_p.append(i)

print(len(index_list_p)) # 21081
Dnp = np.delete(Dnp_check, index_list_p)
print(len(Dnp_check)) # 0 = 21081 - 21081

# Create dictionary with keys as column names
Ddict = {"Section_title":[], "Book_no": [], "Section_no": [], "Passage_no":
    [], "Paragraph_no": [], "Passage_ref": [], "Passage": []}

# Regex patterns for Ddict dictionary
section_title_pattern = re.compile(r"(?<=R\.\s)([A-Z\s]+)")
ref_pattern = re.compile(r"(?<=D\.\s)(\d+),\s(\d+),\s(\d+[a-z]?),\s(\d+[a-z]?)\s([A-Za-z][a-z].+)")
ref_alt_pattern = re.compile(r"(?<=D\.\s)(\d+),\s(\d+)\s?,\s(\d+[a-z]?)\s([A-Za-z][a-z].+)")
heading3032_pattern = r"D\.\s\d+,\s\d+\s?,\s\d+\s[A-Za-z][a-z].+"
heading_pattern = r"D\.\s\d+,\s\d+,\s\d+[a-z]?,\s\d+[a-z]?\s[A-Za-z][a-z].+"

# Feeding Ddict dictionary from Dnp
index_list_p = []
for i in range(0, len(Dnp)):
    if re.search(section_ref_pattern, Dnp[i]) is not None:
        section_title = section_title_pattern.search(Dnp[i]).group(1)
    elif re.search(heading_ref_pattern, Dnp[i]) is not None:
        if re.search(heading3032_pattern, Dnp[i]) is not None:
            book_no = ref_alt_pattern.search(Dnp[i]).group(1)
            section_no = ref_alt_pattern.search(Dnp[i]).group(2)
            passage_no = ref_alt_pattern.search(Dnp[i]).group(3)
            paragraph_no = 'NaN'
            passage_ref = ref_alt_pattern.search(Dnp[i]).group(4)
            Ddict["Section_title"].append(section_title)
            Ddict["Book_no"].append(book_no)
            Ddict["Section_no"].append(section_no)
            Ddict["Passage_no"].append(passage_no)
            Ddict["Paragraph_no"].append(paragraph_no)
            Ddict["Passage_ref"].append(passage_ref)
            passage = Dnp[(i + 1)]
            Ddict["Passage"].append(passage)
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
            Ddict["Paragraph_no"].append(paragraph_no)
            Ddict["Passage_ref"].append(passage_ref)
            passage = Dnp[(i + 1)]
            Ddict["Passage"].append(passage)
    elif re.search(passage_pattern, Dnp[i]) is not None:
        index_list_p.append(i)

# Create data frame (Ddf) from the dictionary (Ddict)
Ddf = pd.DataFrame(Ddict)
print(Ddf)

# Export Ddf data frame as "Ddf.csv"
Ddf.to_csv("Ddf.csv")


# Select elements from Passage_no and Paragraph_no with appended references (e.g. "4a")
# Exclude rows of Paragraph_no with NaN elements (dtype float)
a_index = []
for i in range(0, len(Ddf['Passage_no'])):
    if re.search('[a-z]', Ddf['Passage_no'][i]):
        a_index.append(i)
        print(Ddf['Passage_no'][i])
    elif pd.notna(Ddf['Paragraph_no'][i]):
        if re.search('[a-z]', Ddf['Paragraph_no'][i]):
            a_index.append(i)
            print(Ddf['Paragraph_no'][i])
print(len(a_index))
print(a_index)
# 23 appended references, highest appended letter is "d"
# [908, 1330, 2072, 2073, 2074, 2075, 2643, 2890, 2965, 2966, 2967, / 
# 2968, 3716, 7135, 9668, 13155, 13895, 15115, 16780, 16975, 18240, 19837, 20219]
# Manually change appended references to floats in Ddf.csv
# so that "4a" -> 4.2, "4b" -> 4.4, "4c" -> 4.6 and "4d" -> 4.8

# Export Ddict python dictionary as "Dpickle"
infile = open("Dpickle",'rb')
Ddict = pickle.load(infile)
infile.close()

# Check pickling by unpickling Dpickle
infile = open("Dpickle",'rb')
Ddict_check = pickle.load(infile)
print(type(Ddict_check))
print(Ddict_check == Ddict)
infile.close()

# Close Digest.txt file
str.close()
'''