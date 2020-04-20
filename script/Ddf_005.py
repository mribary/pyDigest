# Import pandas
import pandas as pd

# Load dataframes
path_002 = '/home/mribary/Dropbox/pyDigest/dump/Ddf_v102.csv'
path_005 = '/home/mribary/Dropbox/pyDigest/dump/Ddf_v105.csv'
df2 = pd.read_csv(path_002, index_col=0)
df5 = pd.read_csv(path_005, index_col=0)

# Keep Digest reference columns in df5: df6
df6 = df5[['Book_no', 'Section_no', 'Passage_no', 'TextUnit_no']]

# Insert 'TextUnit' column from df2 where Greek script is displayed correctly
df6['TextUnit'] = df2['TextUnit']

# Export dataframe: Ddf_v106.csv
df6.to_csv('/home/mribary/Dropbox/pyDigest/dump/Ddf_v106.csv')