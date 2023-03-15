# 8. Documentation

data/make_dataset.py

## `download_data()`:

    Function to gather training dataset from different sources. This function will download
    datasets from Kaggle API and save them to the data/raw folder. If the dataset already exists,
    ignore and continue to the next dataset.

    Return None.

    No additional arguments required for this function.


data/make_dataset.py

## `save_data(df)`:
    
    Function to split and save the preprocessed dataset to appropriate destinations.

    Split:
        - split the preprocessed data into training and testing portions based on customized
          training size.

    Save:
        - The training and testing dataset will be saved at user desired destination.
        - Default destination is data/temp.

    Return None.

    Parameters:
        - df: pd.dataframe, dataset that is in need of splitting and saving.


data/make_dataset.py

## `generate_data()`:
   
    Function to preprocess raw data downloaded by download_data(). The function will return
    a preprocessed dataset ready for model training.

    Preprocess:
        1. convert categorical sentiment representations to numerical values.
        2. sync feature names for each dataset in order to join them in the future.
        3. join all preprocessed datasets and perform renaming as necessary.

    Return pd.dataframe

    No additional arguments required for this function.
   
data/make_dataset.py  

## `generate_tweet(query=query, time_window=time_window, max_results=max_results)`:
    
    Function to fetch, process and save data from Twitter API.

    Fetch:
        - This function will fetch data from the Twitter API in a user-preferred time interval.
        - It also allows users to choose how many tweets they want and what companies they want
          the tweets to be about.

    Process:
        - Perform preprocessing for the retrieved tweets including filtering and renaming. Tweets
          will then be ready for model training.

    Save:
        - Save the dataset at user desired destinations. Default destination is data/temp.

    Return None

    Parameters:
        - query: str, NASDAQ codes for companies that users need to search for.
        - time_window: int, defines how large the time interval is in terms of days.
        - max_results: int, defines how many tweets are generated.
        

models/train.py

## `train()`:

[`train()`](https://github.com/crvander/capstoneproj2023/blob/14b75f083c2bc08f166ec30d2a941047951afcaf/src/models/train.py#L28) is a function to train models. This function will try to perform the training on GPUs if possible.
This is a generic function to train user preferred models. Users can choose what models and hyperparameters they prefer when training. Users can make changes to the configuration files to update their preferences.

The function will also save the trained model to user preferred destinations. Default destination is results/model_name.

**Return:** str, the name of the model.


No arguments required for this function.


models/test.py

## `test()`

[`test()`](https://github.com/crvander/capstoneproj2023/blob/14b75f083c2bc08f166ec30d2a941047951afcaf/src/models/test.py#L23) is a function to test the trained model on testing data. This function will try to perform the testing on GPUs if possible. The function will fetch the finetuned model from `results/model_name`, then fetch the testing data and perform predictions. The predictions will be saved at user preferred destinations. Default destination is `data/out`.

**Return:** None.

**Parameters:**
- `test_target`: str, this argument defines what testing data to use. Default `'test'`.
- `test_lines`: int, this argument defines how many predictions to make. Default `3`.


models/test.py:

## `prediction()`

[`prediction()`](https://github.com/crvander/capstoneproj2023/blob/14b75f083c2bc08f166ec30d2a941047951afcaf/src/models/test.py#L79) is a function to make predictions on real-time tweets. This function will try to perform the testing on GPUs if possible. This function will fetch finetuned models from `results/model_name`. The function will make predictions for each day on tweets generated from Twitter API for a specific company, then average the sentiments and save the results in a user-defined destination. Default destination is `data/out`.

**Return:** None.

**No arguments required for this function.**


twitter/pull_tweets.py

## `call_stock(query, time_window, max_results, ds_name = ds_name, save_path = save_path)`

[`call_stock()`](https://github.com/crvander/capstoneproj2023/blob/14b75f083c2bc08f166ec30d2a941047951afcaf/src/twitter/pull_tweets.py#L28) is a function to retrieve and save tweets from Twitter API. This function will call from pytwitter to retrieve specific tweets from Twitter and then save them to a user-defined destination. Default destination is `data/raw`. This function allows users to define the companies, time interval, and number of tweets they want to search for.

**Return:** None.

**Parameters:**
- `query`: str, NASDAQ code for companies.
- `time_window`: int, the length of the time interval in terms of days.
- `max_results`: int, the number of tweets to retrieve.
- `ds_name`: str, the name of the dataset generated.
- `save_path`: str, the destination to save the generated dataset.
