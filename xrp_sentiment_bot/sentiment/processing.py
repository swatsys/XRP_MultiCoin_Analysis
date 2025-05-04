# import time

# def process_sentiment_data(cg, reddit, news):
#     all_sentiments = []
#     cg_score = (cg["sentiment_up"] - cg["sentiment_down"]) / 100
#     all_sentiments.append({"source": "coingecko", "polarity": cg_score, "weight": 0.4})
#     avg_r = sum(x["polarity"] for x in reddit)/len(reddit) if reddit else 0
#     avg_n = sum(x["polarity"] for x in news)/len(news) if news else 0
#     all_sentiments.append({"source": "reddit", "polarity": avg_r, "weight": 0.3})
#     all_sentiments.append({"source": "news", "polarity": avg_n, "weight": 0.3})
#     composite = sum(x["polarity"] * x["weight"] for x in all_sentiments)
#     return {"individual_sentiments": all_sentiments, "composite_sentiment": composite, "timestamp": time.time()}

import time

def process_sentiment_data(cg, reddit, news):
    """
    Process and combine sentiment data from different sources.
    
    Args:
        cg (dict): CoinGecko sentiment data
        reddit (list): Reddit sentiment data
        news (list): News sentiment data
        
    Returns:
        dict: Processed sentiment data with composite score
    """
    all_sentiments = []
    
    # Process CoinGecko sentiment if available
    if cg.get("sentiment_up") is not None and cg.get("sentiment_down") is not None:
        cg_score = (cg["sentiment_up"] - cg["sentiment_down"]) / 100
        all_sentiments.append({"source": "coingecko", "polarity": cg_score, "weight": 0.4})
    else:
        # Use neutral sentiment if data not available
        all_sentiments.append({"source": "coingecko", "polarity": 0, "weight": 0.4})
    
    # Process Reddit sentiment
    if reddit and len(reddit) > 0:
        avg_r = sum(x.get("polarity", 0) for x in reddit) / len(reddit)
        all_sentiments.append({"source": "reddit", "polarity": avg_r, "weight": 0.3})
    else:
        all_sentiments.append({"source": "reddit", "polarity": 0, "weight": 0.3})
    
    # Process News sentiment
    if news and len(news) > 0:
        avg_n = sum(x.get("polarity", 0) for x in news) / len(news)
        all_sentiments.append({"source": "news", "polarity": avg_n, "weight": 0.3})
    else:
        all_sentiments.append({"source": "news", "polarity": 0, "weight": 0.3})
    
    # Calculate composite sentiment score
    composite = sum(x["polarity"] * x["weight"] for x in all_sentiments)
    
    return {
        "individual_sentiments": all_sentiments,
        "composite_sentiment": composite,
        "timestamp": time.time()
    }