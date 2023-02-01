'''
etl.py contains functions used to download, create, and save DataFrames
'''

# create and save data
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import csv
# from sklearn.model_selection import train_test_split


# def get_data(data_config):

#     df = pd.read_csv(data_config[outdir_test] + "/test_data.csv", delimeter=',', encoding='latin-1', names=['label', 'text'])

#     return df


# def save_data(data_config, data):
#     train, test = train_test_split(data, test_size=0.1)
#     train.to_csv('../data/temp/train.csv', index=False)
#     test.to_csv('../data/temp/test.csv', index=False)
#     return


# #============ my changes ================

def get_data(data_config):
    df = pd.read_csv(data_config[outdir_test]/test_load.csv, delimeter=',', encoding='latin-1', names=['label', 'text'])

    return df

# def save_data():

#     return