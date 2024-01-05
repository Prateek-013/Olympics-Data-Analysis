import pandas as pd
import numpy as np

def preprocess(df, region_df):
    #filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    #Merging with region df
    df = df.merge(region_df, on='NOC', how='left')
    #dropping duplicates
    df.drop_duplicates(inplace=True)
    #one Hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df