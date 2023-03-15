# 8. Documentation

download_data():
    Function to gather training dataset from different sources. This function will download
    datasets from Kaggle API and save them to the data/raw folder. If the dataset already exists,
    ignore and continue to the next dataset.

    Return None.

    No additional arguments required for this function.

save_data(df):
    """
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
    """

generate_data():
    """
    Function to preprocess raw data downloaded by download_data(). The function will return
    a preprocessed dataset ready for model training.

    Preprocess:
        1. convert categorical sentiment representations to numerical values.
        2. sync feature names for each dataset in order to join them in the future.
        3. join all preprocessed datasets and perform renaming as necessary.

    Return pd.dataframe

    No additional arguments required for this function.
    """

generate_tweet(query=query, time_window=time_window, max_results=max_results):
    """
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
    """
