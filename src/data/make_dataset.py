import subprocess
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import logging
from box import Box
import yaml
import os

# access config files and extract necessary parameters
with open('config/data-params.yml', 'r') as file:
    data_config = Box(yaml.full_load(file))
    
os.environ['KAGGLE_CONFIG_DIR'] = data_config.data_path # set folder path for kaggle credential
random_state = data_config.random_state
split = data_config.split
save_path = data_config.save_path
save_path_raw = data_config.save_path_raw
train_name = data_config.train_name
test_name = data_config.test_name
expand = data_config.expand
    
# datasets name
ds1 = data_config.ds1_name
ds2 = data_config.ds2_name
ds3 = data_config.ds3_name
#     ds4...

# datasets path from source
ds1_path = data_config.ds1_path
ds2_path = data_config.ds2_path
ds3_path = data_config.ds3_path
#     ds4...

# file name for reading the files in saved dataset
df1_name = data_config.df1_name
df2_name = data_config.df2_name
df3_name = data_config.df3_name

# function to pull online data from API
def download_data():
    dir = os.listdir(save_path_raw)
    logging.info('downloading datasets....')
    # commands to download dataset from Kaggle
    if ds1 not in dir: # detect if dataset 1 being downloaded
        subprocess.run('~/.local/bin/kaggle datasets download -p {} {}'.format(save_path_raw, ds1_path), shell = True, stdout = subprocess.PIPE)
    if ds2 not in dir: # detect if dataset 2 being downloaded
        subprocess.run('~/.local/bin/kaggle datasets download -p {} {}'.format(save_path_raw, ds2_path), shell = True, stdout = subprocess.PIPE)
    if ds3 not in dir: # detect if dataset 3 being downloaded
        subprocess.run('~/.local/bin/kaggle datasets download -p {} {}'.format(save_path_raw, ds3_path), shell = True, stdout = subprocess.PIPE)
    if (df1_name not in dir or df2_name not in dir ) or df3_name not in dir: # if any of the required file is not included
        subprocess.run('unzip {}/\*.zip -d {}'.format(save_path_raw, save_path_raw), shell = True, stdout = subprocess.PIPE) # unzip all the .zip files in the data raw folder
        # df4 = ... Dylan's api
    logging.info('downloading done.')

# function to generate training, validation, testing data
def generate_data():
    logging.info('loading datasets from {}....'.format(save_path_raw))
    df1 = pd.read_csv('{}/{}'.format(save_path_raw, df1_name), delimiter=',', encoding='latin-1',
                      names=['sentiment', 'text']) # read first data
    df2 = pd.read_csv('{}/{}'.format(save_path_raw, df2_name)) # read second data
    df3 = pd.read_csv('{}/{}'.format(save_path_raw, df3_name), on_bad_lines='skip', sep=';') # read third data
    # df4 = ... Dylan's api
    logging.info('datasets loaded')

    # function to convert sentiment labels to numerical values
    def convert_sentiment(sent):
        if sent == 'neutral':
            return 0
        elif sent == 'positive':
            return 1
        else:
            return -1

    logging.info('preprocessing...')
    # data preprocessing
    df1['sentiment'] = df1['sentiment'].apply(convert_sentiment)
    df1 = df1[['text', 'sentiment']]
    df2.rename(columns={'Text': 'text', 'Sentiment': 'sentiment'}, inplace=True)
    df3 = df3.dropna()[['text', 'sentiment']]
    df3['sentiment'] = df3['sentiment'].apply(convert_sentiment)
    df3.rename(columns={'Sentiment': 'sentiment', 'Text': 'text'}, inplace=True)
    if expand:                 
        # df = pd.concat([df1, df2, df3, df4], ignore_index=True, axis=0) # to concat Spacy processed data, will be implemented in Quater 2
        df = pd.concat([df1, df2, df3], ignore_index=True, axis=0)
    else:
        df = pd.concat([df1, df2, df3], ignore_index=True, axis=0)
    df.rename(columns={'sentiment': 'labels'}, inplace=True)
    logging.info('preprocessing completed.')
    return df


# function to save the processed dataset
def save_data(df):
        logging.info('train test with {} split, random state {}'.format(split, str(random_state)))
        # split the dataset into training and testing sets.
        train, test = train_test_split(df, test_size=split, random_state = random_state)
        logging.info('saving training and testing data...')
        train.to_csv(save_path + train_name, index=False) # save training data
        test.to_csv(save_path + test_name, index=False) # save testing data
        logging.info('training and testing saved at {}') 
        return
