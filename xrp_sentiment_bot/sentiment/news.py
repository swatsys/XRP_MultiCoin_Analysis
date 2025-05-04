# import requests, time
# from textblob import TextBlob

# def get_news_sentiment(coin):
#     api_key = "ba315c2499eeab33b9f037d3193db7e0f2c7ebffc17694f1acf888c5fec495e5"
#     url = f"https://min-api.cryptocompare.com/data/news/?categories=XRP&api_key={api_key}"
#     articles = requests.get(url).json()
#     results = []
#     for a in articles:
#         text = a['title'] + " " + a.get('body', "")
#         polarity = TextBlob(text).sentiment.polarity
#         results.append({"source": "news", "title": a['title'], "polarity": polarity, "timestamp": a['published_on']})
#     return results

import requests, time
from textblob import TextBlob

def get_news_sentiment(category="XRP"):
    api_key = "ba315c2499eeab33b9f037d3193db7e0f2c7ebffc17694f1acf888c5fec495e5"
    url = f"https://min-api.cryptocompare.com/data/news/?categories={category}&api_key={api_key}"

    articles = requests.get(url).json()
    results = []
    for a in articles:
        text = a['title'] + " " + a.get('body', "")
        polarity = TextBlob(text).sentiment.polarity
        results.append({"source": "news", "title": a['title'], "polarity": polarity, "timestamp": a['published_on']})
    return results
