import requests

def get_stock_data(symbol):
    api_key = "API KEY"
    request_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    return response.json()
