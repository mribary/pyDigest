import pandas as pd 

# Load dataframes
path_BKO = '/home/mribary/Dropbox/pyDigest/dump/BKO_v006.csv'
BKO = pd.read_csv(path_BKO, index_col=0)
path_BKO_ids = '/home/mribary/Dropbox/pyDigest/dump/Ddf_BKO_IDs_v003.csv'
BKO_ids = pd.read_csv(path_BKO_ids, index_col=0)

# Align BKO and BKO_IDs and load BKO_id to the BKO
BKO_id_list = []
for i in BKO.index:
    if BKO_ids.BKO_id[BKO_ids.BKO_label == BKO.Work_ref[i]].size:       # Check if array is not empty
        BKO_id = int(BKO_ids.BKO_id[BKO_ids.BKO_label == BKO.Work_ref[i]].values)
    else:                                                               # If array is empty
        BKO_id = None
    BKO_id_list.append(BKO_id)
BKO.insert(loc=3, column='BKO_id', value=BKO_id_list)

BKO.to_csv('/home/mribary/Dropbox/pyDigest/dump/BKO_v007.csv')