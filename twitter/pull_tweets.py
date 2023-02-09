from pytwitter import Api
import twitter_credentials #twitter_credentials is a python file that contains the API keys but dummy ones are shown here for security reasons
import pandas as pd

#Initialize the API with your credentials
api = Api(
    consumer_key=twitter_credentials.CONSUMER_KEY,
    consumer_secret=twitter_credentials.CONSUMER_SECRET,
    access_token=twitter_credentials.ACCESS_TOKEN,
    access_secret=twitter_credentials.ACCESS_TOKEN_SECRET,
)

#Save the stock data to a csv
def call_stock(stock_name):
    tweets = api.search_tweets(query=stock_name, max_results=100).data
    data = pd.Series([x.text for x in tweets])
    data.to_csv("data/raw/data.csv", index=False)
