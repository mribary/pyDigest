# Import regex, numpy, pandas
import re
import pandas as pd
import numpy as np

# Load Ddf_v100.csv into a pandas data frame
Ddf = pd.read_csv('./input/Ddf_v100.csv', index_col=0)
# Ddf.info()

# Remove book number from column "TextUnit_ref" and create a list: Ddf_refs
Ddf_refs = []
for i in range(0, len(Ddf['TextUnit_ref'])):
    Ddf_refs.append(re.sub('\d+\s', '', Ddf['TextUnit_ref'][i]))

# Insert a column "Work" with clean work references without book numbers
Ddf.insert(6, "Work", Ddf_refs, True)

# Insert a copy of the "Work" column
Ddf.insert(7, "BKO_key", Ddf_refs, True)

# Initialise pandas series with index corresponding with Ddf: Ddf_works
Ddf_works = Ddf['BKO_key']

# Suppress "SettingWithCopyWarning"
pd.set_option('mode.chained_assignment', None)

#################################################################################
#  Replace elements in Ddf_works which belong to a part of a multi-volume work  #
#  as identified as one item in BKO, e.g. "Paul. 1–7 ad ed."                    #
#################################################################################

# 1. "Paul ad ed."
Paul_ed_no_index = []
Paul_ed_no_list = []
Paul_ed_48_index = []
Paul_ed_48_list = []
Paul_ed_count = 0
Paul_ed_pattern = re.compile(r"(?<=Paul\.\s)(\d+)\s(ad\sed\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Paul_ed_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Paul_ed_count += 1
        Paul_ed_no = int(Paul_ed_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Paul_ed_no < 28:
            Paul_ed_no_index.append(i)
            Paul_ed_no_list.append(re.sub('\d+', '1-27', Ddf['TextUnit_ref'][i]))
        elif (Paul_ed_no > 27) & (Paul_ed_no < 48):
            Paul_ed_no_index.append(i)
            Paul_ed_no_list.append(re.sub('\d+', '28-48', Ddf['TextUnit_ref'][i]))
        elif Paul_ed_no == 49:
            Paul_ed_no_index.append(i)
            Paul_ed_no_list.append(re.sub('\d+', '48-49', Ddf['TextUnit_ref'][i]))
        elif (Paul_ed_no > 49) & (Paul_ed_no < 52):
            Paul_ed_no_index.append(i)
            Paul_ed_no_list.append(re.sub('\d+', '50-51', Ddf['TextUnit_ref'][i]))
        elif Paul_ed_no == 52:
            Paul_ed_no_index.append(i)
            Paul_ed_no_list.append(re.sub('\d+', '52', Ddf['TextUnit_ref'][i]))
        elif Paul_ed_no > 52:
            Paul_ed_no_index.append(i)
            Paul_ed_no_list.append(re.sub('\d+', '53-78', Ddf['TextUnit_ref'][i]))
        elif Paul_ed_no == 48:
            Paul_ed_48_index.append(i)
            Paul_ed_48_list.append(Ddf['TextUnit_ref'][i])
        else:
            print('Error at index ', i)
# Replace "Paul ad ed." references and check accuracy of output
for x, y in zip(Paul_ed_no_index, Paul_ed_no_list):
  Ddf_works[x] = y
# print(Paul_ed_count) # 1547
# print(len(Paul_ed_48_index)) # 36
# print(Paul_ed_count == (len(Paul_ed_no_list) + len(Paul_ed_48_list))) # True

# 2. "Paul sent."
Paul_sent_no_index = []
Paul_sent_no_list = []
Paul_sent_1_index = []
Paul_sent_1_list = []
Paul_sent_count = 0
Paul_sent_pattern = re.compile(r"(?<=Paul\.\s)(\d+)\s(sent\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Paul_sent_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Paul_sent_count += 1
        Paul_sent_no = int(Paul_sent_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Paul_sent_no == 1:
            Paul_sent_1_index.append(i)
            Paul_sent_1_list.append(Ddf['TextUnit_ref'][i])
        elif Paul_sent_no == 2:
            Paul_sent_no_index.append(i)
            Paul_sent_no_list.append(re.sub('\d+', '1-2', Ddf['TextUnit_ref'][i]))
        elif Paul_sent_no == 3:
            Paul_sent_no_index.append(i)
            Paul_sent_no_list.append(re.sub('\d+', '3', Ddf['TextUnit_ref'][i]))
        elif Paul_sent_no == 4:
            Paul_sent_no_index.append(i)
            Paul_sent_no_list.append(re.sub('\d+', '4', Ddf['TextUnit_ref'][i]))
        elif Paul_sent_no == 5:
            Paul_sent_no_index.append(i)
            Paul_sent_no_list.append(re.sub('\d+', '5', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Paul sent." references and check accuracy of output
for x, y in zip(Paul_sent_no_index, Paul_sent_no_list):
  Ddf_works[x] = y
# print(Paul_sent_count) # 260
# print(len(Paul_sent_no_index)) # 180
# print(len(Paul_sent_1_index)) # 80
# print(Paul_sent_count == (len(Paul_sent_no_list) + len(Paul_sent_1_list))) # True

# 3. "Gaius. ad ed. provinc."
Gaius_no_index = []
Gaius_no_list = []
Gaius_count = 0
Gaius_pattern = re.compile(r"(?<=Gai\.\s)(\d+)\s(ad\sed\.\sprovinc\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Gaius_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Gaius_count += 1
        Gaius_no = int(Gaius_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if (Gaius_no < 9) | (Gaius_no == 19):
            Gaius_no_index.append(i)
            Gaius_no_list.append(re.sub('\d+', '1-8, 19', Ddf['TextUnit_ref'][i]))
        elif (Gaius_no > 8) & (Gaius_no < 19):
            Gaius_no_index.append(i)
            Gaius_no_list.append(re.sub('\d+', '9-18', Ddf['TextUnit_ref'][i]))
        elif Gaius_no == 20:
            Gaius_no_index.append(i)
            Gaius_no_list.append(re.sub('\d+', '20', Ddf['TextUnit_ref'][i]))
        elif Gaius_no > 20:
            Gaius_no_index.append(i)
            Gaius_no_list.append(re.sub('\d+', '21-30', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Gai. ad ed. provinc." references and check accuracy of output
for x, y in zip(Gaius_no_index, Gaius_no_list):
  Ddf_works[x] = y
# print(Gaius_count) # 517
# print(Gaius_count == len(Gaius_no_list)) # True

# 4. "Ulp. ad ed."
Ulp_ed_no_index = []
Ulp_ed_no_list = []
Ulp_ed_55_index = []
Ulp_ed_55_list = []
Ulp_ed_count = 0
Ulp_ed_pattern = re.compile(r"(?<=Ulp\.\s)(\d+)\s(ad\sed\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Ulp_ed_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Ulp_ed_count += 1
        Ulp_ed_no = int(Ulp_ed_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Ulp_ed_no < 26:
            Ulp_ed_no_index.append(i)
            Ulp_ed_no_list.append(re.sub('\d+', '1-25', Ddf['TextUnit_ref'][i]))
        elif (Ulp_ed_no > 25) & (Ulp_ed_no < 52):
            Ulp_ed_no_index.append(i)
            Ulp_ed_no_list.append(re.sub('\d+', '26-51', Ddf['TextUnit_ref'][i]))
        elif (Ulp_ed_no > 51) & (Ulp_ed_no < 54):
            Ulp_ed_no_index.append(i)
            Ulp_ed_no_list.append(re.sub('\d+', '52-53', Ddf['TextUnit_ref'][i]))
        elif Ulp_ed_no == 54:
            Ulp_ed_no_index.append(i)
            Ulp_ed_no_list.append(re.sub('\d+', '54-55', Ddf['TextUnit_ref'][i]))
        elif Ulp_ed_no == 55:
            Ulp_ed_55_index.append(i)
            Ulp_ed_55_list.append(Ddf['TextUnit_ref'][i])
        elif Ulp_ed_no > 55:
            Ulp_ed_no_index.append(i)
            Ulp_ed_no_list.append(re.sub('\d+', '56-81', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Ulp ad ed." references and check accuracy of output
for x, y in zip(Ulp_ed_no_index, Ulp_ed_no_list):
  Ddf_works[x] = y
# print(Ulp_ed_count) # 5335
# print(len(Ulp_ed_no_index)) # 5286
# print(len(Ulp_ed_55_index)) # 49
# print(Ulp_ed_count == (len(Ulp_ed_no_list) + len(Ulp_ed_55_list))) # True

# 5. "Paul ad Plaut."
Paul_Plaut_no_index = []
Paul_Plaut_no_list = []
Paul_Plaut_count = 0
Paul_Plaut_pattern = re.compile(r"(?<=Paul\.\s)(\d+)\s(ad\sPlaut\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Paul_Plaut_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Paul_Plaut_count += 1
        Paul_Plaut_no = int(Paul_Plaut_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Paul_Plaut_no < 15:
            Paul_Plaut_no_index.append(i)
            Paul_Plaut_no_list.append(re.sub('\d+', '1-14', Ddf['TextUnit_ref'][i]))
        elif Paul_Plaut_no > 14:
            Paul_Plaut_no_index.append(i)
            Paul_Plaut_no_list.append(re.sub('\d+', '15-18', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Paul. ad Plaut." references and check accuracy of output
for x, y in zip(Paul_Plaut_no_index, Paul_Plaut_no_list):
  Ddf_works[x] = y
# print(Paul_Plaut_count) # 341
# print(Paul_Plaut_count == len(Paul_Plaut_no_list)) # True

# 6. "Marcian. reg."
Marcian_no_index = []
Marcian_no_list = []
Marcian_count = 0
Marcian_pattern = re.compile(r"(?<=Marcian\.\s)(\d+)\s(reg\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Marcian_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Marcian_count += 1
        Marcian_no = int(Marcian_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Marcian_no < 3:
            Marcian_no_index.append(i)
            Marcian_no_list.append(re.sub('\d+', '1-2', Ddf['TextUnit_ref'][i]))
        elif (Marcian_no > 2) & (Marcian_no < 5):
            Marcian_no_index.append(i)
            Marcian_no_list.append(re.sub('\d+', '3-4', Ddf['TextUnit_ref'][i]))
        elif Marcian_no == 5:
            Marcian_no_index.append(i)
            Marcian_no_list.append(re.sub('\d+', '5', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Marcian. reg." references and check accuracy of output
for x, y in zip(Marcian_no_index, Marcian_no_list):
  Ddf_works[x] = y
# print(Marcian_count) # 100
# print(Marcian_count == len(Marcian_no_list)) # True

# 7. "Paul. resp."
Paul_resp_no_index = []
Paul_resp_no_list = []
Paul_resp_count = 0
Paul_resp_pattern = re.compile(r"(?<=Paul\.\s)(\d+)\s(resp\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Paul_resp_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Paul_resp_count += 1
        Paul_resp_no = int(Paul_resp_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Paul_resp_no < 8:
            Paul_resp_no_index.append(i)
            Paul_resp_no_list.append(re.sub('\d+', '1-7', Ddf['TextUnit_ref'][i]))
        elif (Paul_resp_no > 7) & (Paul_resp_no < 16):
            Paul_resp_no_index.append(i)
            Paul_resp_no_list.append(re.sub('\d+', '8-15', Ddf['TextUnit_ref'][i]))
        elif (Paul_resp_no > 15) & (Paul_resp_no < 20):
            Paul_resp_no_index.append(i)
            Paul_resp_no_list.append(re.sub('\d+', '16-19', Ddf['TextUnit_ref'][i]))
        elif Paul_resp_no > 19:
            Paul_resp_no_index.append(i)
            Paul_resp_no_list.append(re.sub('\d+', '20-23', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Paul. resp." references and check accuracy of output
for x, y in zip(Paul_resp_no_index, Paul_resp_no_list):
  Ddf_works[x] = y
# print(Paul_resp_count) # 219
# print(Paul_resp_count == len(Paul_resp_no_list)) # True

# 8. "Scaev. resp."
Scaev_resp_no_index = []
Scaev_resp_no_list = []
Scaev_resp_count = 0
Scaev_resp_pattern = re.compile(r"(?<=Scaev\.\s)(\d+)\s(resp\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Scaev_resp_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Scaev_resp_count += 1
        Scaev_resp_no = int(Scaev_resp_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Scaev_resp_no == 1:
            Scaev_resp_no_index.append(i)
            Scaev_resp_no_list.append(re.sub('\d+', '1', Ddf['TextUnit_ref'][i]))
        elif (Scaev_resp_no > 1) & (Scaev_resp_no < 5):
            Scaev_resp_no_index.append(i)
            Scaev_resp_no_list.append(re.sub('\d+', '2-4', Ddf['TextUnit_ref'][i]))
        elif Scaev_resp_no == 5:
            Scaev_resp_no_index.append(i)
            Scaev_resp_no_list.append(re.sub('\d+', '5', Ddf['TextUnit_ref'][i]))
        elif Scaev_resp_no == 6:
            Scaev_resp_no_index.append(i)
            Scaev_resp_no_list.append(re.sub('\d+', '6', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Scaev. resp." references and check accuracy of output
for x, y in zip(Scaev_resp_no_index, Scaev_resp_no_list):
  Ddf_works[x] = y
# print(Scaev_resp_count) # 210
# print(Scaev_resp_count == len(Scaev_resp_no_list)) # True

# 9. "Ulp. fideicomm."
Ulp_fid_no_index = []
Ulp_fid_no_list = []
Ulp_fid_count = 0
Ulp_fid_pattern = re.compile(r"(?<=Ulp\.\s)(\d+)\s(fideicomm\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Ulp_fid_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Ulp_fid_count += 1
        Ulp_fid_no = int(Ulp_fid_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Ulp_fid_no < 5:
            Ulp_fid_no_index.append(i)
            Ulp_fid_no_list.append(re.sub('\d+', '1-4', Ddf['TextUnit_ref'][i]))
        elif Ulp_fid_no > 4:
            Ulp_fid_no_index.append(i)
            Ulp_fid_no_list.append(re.sub('\d+', '5-6', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Ulp. fideicomm." references and check accuracy of output
for x, y in zip(Ulp_fid_no_index, Ulp_fid_no_list):
  Ddf_works[x] = y
# print(Ulp_fid_count) # 224
# print(Ulp_fid_count == len(Ulp_fid_no_list)) # True

# 10. "Valens. fideicomm."
# Note the absence of full stop after "Valens"
Val_fid_no_index = []
Val_fid_no_list = []
Val_fid_count = 0
Val_fid_pattern = re.compile(r"(?<=Valens\s)(\d+)\s(fideicomm\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Val_fid_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Val_fid_count += 1
        Val_fid_no = int(Val_fid_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Val_fid_no < 5:
            Val_fid_no_index.append(i)
            Val_fid_no_list.append(re.sub('\d+', '1-4', Ddf['TextUnit_ref'][i]))
        elif Val_fid_no > 4:
            Val_fid_no_index.append(i)
            Val_fid_no_list.append(re.sub('\d+', '5-7', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Valens fideicomm." references and check accuracy of output
for x, y in zip(Val_fid_no_index, Val_fid_no_list):
  Ddf_works[x] = y
# print(Val_fid_count) # 24
# print(Val_fid_count == len(Val_fid_no_list)) # True

# 11. "Maec. fideicomm."
Maec_fid_no_index = []
Maec_fid_no_list = []
Maec_fid_count = 0
Maec_fid_pattern = re.compile(r"(?<=Maec\.\s)(\d+)\s(fideicomm\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Maec_fid_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Maec_fid_count += 1
        Maec_fid_no = int(Maec_fid_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Maec_fid_no < 9:
            Maec_fid_no_index.append(i)
            Maec_fid_no_list.append(re.sub('\d+', '1-8', Ddf['TextUnit_ref'][i]))
        elif Maec_fid_no > 8:
            Maec_fid_no_index.append(i)
            Maec_fid_no_list.append(re.sub('\d+', '9-16', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Maec. fideicomm." references and check accuracy of output
for x, y in zip(Maec_fid_no_index, Maec_fid_no_list):
  Ddf_works[x] = y
# print(Maec_fid_count) # 77
# print(Maec_fid_count == len(Maec_fid_no_list)) # True

# 12. "Hermog. iuris epit."
Hermog_no_index = []
Hermog_no_list = []
Hermog_count = 0
Hermog_pattern = re.compile(r"(?<=Hermog\.\s)(\d+)\s(iuris\sepit\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Hermog_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Hermog_count += 1
        Hermog_no = int(Hermog_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Hermog_no == 1:
            Hermog_no_index.append(i)
            Hermog_no_list.append(re.sub('\d+', '1', Ddf['TextUnit_ref'][i]))
        elif Hermog_no == 2:
            Hermog_no_index.append(i)
            Hermog_no_list.append(re.sub('\d+', '2', Ddf['TextUnit_ref'][i]))
        elif Hermog_no == 3:
            Hermog_no_index.append(i)
            Hermog_no_list.append(re.sub('\d+', '3', Ddf['TextUnit_ref'][i]))
        elif Hermog_no == 4:
            Hermog_no_index.append(i)
            Hermog_no_list.append(re.sub('\d+', '4', Ddf['TextUnit_ref'][i]))
        elif Hermog_no > 4:
            Hermog_no_index.append(i)
            Hermog_no_list.append(re.sub('\d+', '5-6', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Hermog. iuris epit." references and check accuracy of output
for x, y in zip(Hermog_no_index, Hermog_no_list):
  Ddf_works[x] = y
# print(Hermog_count) # 152
# print(Hermog_count == (len(Hermog_no_list))) # True

# 13. "Tryph. disp."
Tryph_no_index = []
Tryph_no_list = []
Tryph_count = 0
Tryph_pattern = re.compile(r"(?<=Tryph\.\s)(\d+)\s(disp\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Tryph_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Tryph_count += 1
        Tryph_no = int(Tryph_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Tryph_no < 13:
            Tryph_no_index.append(i)
            Tryph_no_list.append(re.sub('\d+', '1-12', Ddf['TextUnit_ref'][i]))
        elif Tryph_no > 12:
            Tryph_no_index.append(i)
            Tryph_no_list.append(re.sub('\d+', '13-21', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Tryph. disp." references and check accuracy of output
for x, y in zip(Tryph_no_index, Tryph_no_list):
  Ddf_works[x] = y
# print(Tryph_count) # 170
# print(Tryph_count == (len(Tryph_no_list))) # True

# 14. "Proc. epist."
Proc_no_index = []
Proc_no_list = []
Proc_count = 0
Proc_pattern = re.compile(r"(?<=Proc\.\s)(\d+)\s(epist\.\s?)$")
for i in range(0, len(Ddf['TextUnit_ref'])):
    if Proc_pattern.search(Ddf['TextUnit_ref'][i]) is not None:
        Proc_count += 1
        Proc_no = int(Proc_pattern.search(Ddf['TextUnit_ref'][i]).group(1))
        if Proc_no < 7:
            Proc_no_index.append(i)
            Proc_no_list.append(re.sub('\d+', '1-6', Ddf['TextUnit_ref'][i]))
        elif Proc_no > 6:
            Proc_no_index.append(i)
            Proc_no_list.append(re.sub('\d+', '7-11', Ddf['TextUnit_ref'][i]))
        else:
            print('Error at index ', i)
# Replace "Proc. epist." references and check accuracy of output
for x, y in zip(Proc_no_index, Proc_no_list):
  Ddf_works[x] = y
# print(Proc_count) # 44
# print(Proc_count == (len(Proc_no_list))) # True

# Export the new data frame as a csv file: Ddf_v101.csv
Ddf.to_csv("./output/Ddf_v101.csv")