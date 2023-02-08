'''
etl.py contains functions used to download, create, and save DataFrames
'''

import sys
import json
import pandas as pd
from sklearn.model_selection import train_test_split
import csv

def get_data(data_config):

    df = pd.read_csv('{}/{}'.format(data_config['outdir_test'], data_config['test_data']), header=0, names=['sentiment', 'text'])

    return df
    # elif:
    
    
    # # dataset 1 (columns: 0(sentiment), 1(text))
    # df_1=pd.read_csv('{}/{}'.format("data/raw/", "all-data.csv"), delimiter=',', encoding='latin-1', header=0, names=['sentiment', 'text'])

    # # dataset 2 (columns: Text, Sentiment(int))
    # df_2=pd.read_csv('{}/{}'.format("data/raw/","stock_data.csv"), header=0, names=['text', 'sentiment'])

    # # dataset 3 (columns: text, sentiment(str)) with na values
    # df_3=pd.read_csv('{}/{}'.format("data/raw/","tweets_labelled_09042020_16072020.csv"), on_bad_lines='skip', delimiter=';', header=0, names=['text','sentiment'])

def save_data(data_config, data):
    train, test = train_test_split(data, test_size=0.1)
    train.to_csv('{}/{}'.format(data_config['outdir_temp'], "train.csv"), index=False)
    test.to_csv('{}/{}'.format(data_config['outdir_temp'], "test.csv"), index=False)
    # data.to_csv("data/temp/myData.csv", index=False)
    # data.to_csv('{}/{}'.format(data_config['outdir_temp'], data_config['temp_data']), index=False)
