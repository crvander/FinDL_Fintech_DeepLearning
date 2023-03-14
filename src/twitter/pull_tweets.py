from pytwitter import Api
import pandas as pd
from datetime import datetime, timedelta
import yaml
from box import Box

#Have more data, do staggered times, add in stuff from before, 100 per day last 30 days, company name, date
#Initialize the API with your credentials

with open('config/twitter_credentials.yml', 'r') as file:
    twitter_config = Box(yaml.full_load(file))

api = Api(
    consumer_key=twitter_config.CONSUMER_KEY,
    consumer_secret=twitter_config.CONSUMER_SECRET,
    access_token=twitter_config.ACCESS_TOKEN,
    access_secret=twitter_config.ACCESS_TOKEN_SECRET
)

# access config files and extract necessary parameters
with open('config/data-params.yml', 'r') as file:
    data_config = Box(yaml.full_load(file))
    
save_path = data_config.save_path_raw # the save path for raw tweets data
ds_name = data_config.ds4_name # the file name for raw tweets data

#Save the stock data to a csv
def call_stock(query, time_window, max_results, ds_name = ds_name, save_path = save_path):
    """
    Function to retrieve and save tweets from Twitter API. This function will call from 
    pytwitter to retrieve specific tweets from Twitter and then save them to a user defined
    destination. Default destination is data/raw. This function allows users to define the 
    companies, time interval and number of tweets they want to search for.

    Return None.

    Parameters:
        query: str, NASDAQ code for companies.
        time_window: int, the length of the time interval in terms of days.
        max_results: int, the number of tweets to retrieve.
        ds_name: str, the name of the dataset generated
        save_path: str, the destination to save the generated dataset.
    """
    today = datetime.utcnow().date() # today's date
    start_date = today - timedelta(days=time_window) # the earlist date for tweets
    end_date = today - timedelta(days=1) # the last date for tweets

    columns = ['tweet', 'query', 'timestamp']
    df = pd.DataFrame(columns=columns)
    for date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
        search_params = {
            'query': query,
            'max_results': max_results,
            'start_time': datetime.combine(date, datetime.min.time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'end_time': datetime.combine(date, datetime.max.time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'tweet_fields': ['created_at']
        }
        tweets = api.search_tweets(**search_params)
        for tweet in tweets.data:
            tweet_text = tweet.text
            timestamp = tweet.created_at
            df = df.append({'tweet': tweet_text, 'query': query, 'timestamp': timestamp}, ignore_index=True)
    df.to_csv(save_path + '/' + ds_name, index=False)