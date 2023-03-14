import subprocess
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import logging
from box import Box
import yaml
import os
from src.twitter.pull_tweets import call_stock

# access config files and extract necessary parameters
with open('config/data-params.yml', 'r') as file:
    data_config = Box(yaml.full_load(file))
    
os.environ['KAGGLE_CONFIG_DIR'] = data_config.data_path # set folder path for kaggle credential
random_state = data_config.random_state # random state for train test split
split = data_config.split # ratio of train test split
save_path = data_config.save_path # save path for processed dataset
save_path_raw = data_config.save_path_raw # save path for raw dataset
train_name = data_config.train_name # file name for proccesed training dataset
test_name = data_config.test_name # file name for proccesed training dataset
expand = data_config.expand # whether to expand dataset from Spacy polarization
    
# datasets name
ds1 = data_config.ds1_name
ds2 = data_config.ds2_name
ds3 = data_config.ds3_name

# datasets path from source
ds1_path = data_config.ds1_path
ds2_path = data_config.ds2_path
ds3_path = data_config.ds3_path

# file name for reading the files in saved dataset
df1_name = data_config.df1_name
df2_name = data_config.df2_name
df3_name = data_config.df3_name
df4_name = data_config.df4_name # file for processed tweets dataset

query = data_config.query # stock code to be fetch
time_window = data_config.time_window # days to be fetch
max_results = data_config.max_results # max number of tweets to be fetch per day

def download_data():
    """
    Function to gather training dataset from different sources. This function will download
    datasets from Kaggle API and save them to the data/raw folder. If the dataset already exists,
    ignore and continue to next dataset.

    Return None.

    No additional arguments required for this function.
    """
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
    """
    Function to preprocess raw data downloaded by download_data(). The function will return
    a preprocessed dataset ready for model training.

    Preprocess:
        1. convert categorical sentiment representations to numerical values.
        2. sync feature names for each datasets in order to join them in the future.
        3. join all preprocessed datasets and perform renaming as necessary. 

    Return pd.dataframe

    No additional arguments required for this function.
    """
    logging.info('loading datasets from {}....'.format(save_path_raw))
    df1 = pd.read_csv('{}/{}'.format(save_path_raw, df1_name), delimiter=',', encoding='latin-1',
                      names=['sentiment', 'text']) # read first data
    df2 = pd.read_csv('{}/{}'.format(save_path_raw, df2_name)) # read second data
    df3 = pd.read_csv('{}/{}'.format(save_path_raw, df3_name), on_bad_lines='skip', sep=';') # read third data
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
        # df = pd.concat([df1, df2, df3, df4], ignore_index=True, axis=0) # to concat Spacy processed data
        df = pd.concat([df1, df2, df3], ignore_index=True, axis=0)
    else:
        df = pd.concat([df1, df2, df3], ignore_index=True, axis=0)
    df.rename(columns={'sentiment': 'labels'}, inplace=True)
    logging.info('preprocessing completed.')
    return df


# function to save the processed dataset
def save_data(df):
    """
    Function to split and save the preprocessed dataset to appropriate destinations.

    Split:
        split the preprocessed data into training and testing portions based on customized
        training size.
    Save:
        The training and testing dataset will be saved at user desired destination.
        Default destination is data/temp.

    Return None.

    Parameters:
        df: pd.dataframe, dataset that is in need of splitting and saving.
    """
    logging.info('train test with {} split, random state {}'.format(split, str(random_state)))
    # split the dataset into training and testing sets.
    train, test = train_test_split(df, test_size=split, random_state = random_state)
    logging.info('saving training and testing data...')
    train.to_csv(save_path + train_name, index=False) # save training data
    test.to_csv(save_path + test_name, index=False) # save testing data
    logging.info('training and testing saved at {}') 
    return

# function to fetch, process and save tweets data
def generate_tweet(query = query, time_window = time_window, max_results = max_results):
    """
    Function to fetch, process and save data from Twitter API. 

    Fetch:
        This function will fetch data from the Twitter API in a user preferred time interval.
        It also allows users to choose how many tweets they want and what companies they want 
        the tweets to be about.
    Process:
        Perform preprocessing for the retrieved tweets including filtering and renaming. Tweets
        will then be ready for model training.
    Save:
        Save the dataset at user desired destinations. Default destination is data/temp.

    Return None

    Parameters:
        query: str, NASDAQ codes for companies that users need to search for.
        time_window: int, defines how large is the time interval in terms of days.
        max_results: int, defines how many tweets are generated.
    """
    logging.info('calling tweets api...')
    call_stock(query, time_window, max_results) # fetch tweets and save raw tweets data
    logging.info('reading tweets raw data and process...')
    df4 = pd.read_csv('{}/{}'.format(save_path_raw, ds4_name)) # read tweets raw data
    df4 = df4.drop(["query"], axis = 1) # drop stock code
    df4['timestamp'] = df4['timestamp'].str[:10] # clean the date in yyyy-mm-dd
    logging.info('saving proccesed tweets data...')
    df4.to_csv(save_path + df4_name, index=False) # save in data/temp
    