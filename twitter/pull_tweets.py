from pytwitter import Api
import twitter_credentials #twitter_credentials is a python file that contains the API keys but dummy ones are shown here for security reasons
import pandas as pd
from datetime import datetime, timedelta

#Have more data, do staggered times, add in stuff from before, 100 per day last 30 days, company name, date
#Initialize the API with your credentials
api = Api(
    consumer_key=twitter_credentials.CONSUMER_KEY,
    consumer_secret=twitter_credentials.CONSUMER_SECRET,
    access_token=twitter_credentials.ACCESS_TOKEN,
    access_secret=twitter_credentials.ACCESS_TOKEN_SECRET
)

#Save the stock data to a csv
def call_stock(query):
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=5)
    end_date = today - timedelta(days=1)

    columns = ['tweet', 'query', 'timestamp']
    df = pd.DataFrame(columns=columns)
    for date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
        search_params = {
            'query': query,
            'max_results': 100,
            'start_time': datetime.combine(date, datetime.min.time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'end_time': datetime.combine(date, datetime.max.time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'tweet_fields': ['created_at']
        }
        tweets = api.search_tweets(**search_params)
        for tweet in tweets.data:
            tweet_text = tweet.text
            timestamp = tweet.created_at
            df = df.append({'tweet': tweet_text, 'query': query, 'timestamp': timestamp}, ignore_index=True)
    df.to_csv('tweets.csv', index=False)

call_stock("AAPL")