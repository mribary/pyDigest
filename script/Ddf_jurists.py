# Import packages
import pandas as pd
import numpy as np

# Load BKO.csv into a pandas data frame
load_columns = ['Jurist_name']
df = pd.read_csv('./dump/BKO_v004.csv', usecols=load_columns)
df.Jurist_name = df.Jurist_name.str.strip()

# Unique Jurists in df
Jurists = pd.DataFrame(sorted(df.Jurist_name.unique()))
Jurists[1] = range(len(Jurists))
Jurists.rename(columns={0: 'Jurist', 1: 'Jurist_id'}, inplace=True)
Jurists['Jurist'] = Jurists['Jurist'].astype('category')
Jurists = Jurists[['Jurist_id', 'Jurist']]
print(Jurists.head())
print(len(Jurists)) # 38

# Export Jurists dataframe: Jurists_v001.csv
Jurists.to_csv("./dump/Jurists_v001.csv")