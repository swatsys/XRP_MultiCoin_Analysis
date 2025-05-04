# import requests, time

# def get_coingecko_sentiment():
#     url = "https://api.coingecko.com/api/v3/coins/ripple"
#     data = requests.get(url).json()
#     return {
#         "source": "coingecko",
#         "sentiment_up": data.get("sentiment_votes_up_percentage", 0),
#         "sentiment_down": data.get("sentiment_votes_down_percentage", 0),
#         "timestamp": time.time()
#     }



# import requests
# import time

# def get_coingecko_sentiment(coin_id):
#     url_sentiment = "https://api.coingecko.com/api/v3/coins/ripple"
#     url_price = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd,sgd"

#     sentiment_response = requests.get(url_sentiment).json()
#     price_response = requests.get(url_price).json()

#     up = sentiment_response['sentiment_votes_up_percentage']
#     down = sentiment_response['sentiment_votes_down_percentage']
#     price_usd = price_response["ripple"]["usd"]
#     price_sgd = price_response["ripple"]["sgd"]

#     return {
#         "source": "coingecko",
#         "sentiment_up": up,
#         "sentiment_down": down,
#         "price": price_usd,
#         "price_sgd": price_sgd,
#         "timestamp": time.time()
#     }


import requests
import time
import random

def get_coingecko_sentiment(coin_id="ripple"):
    """
    Get sentiment and price data from CoinGecko for a specified coin.
    Implements exponential backoff for rate limiting.
    
    Args:
        coin_id (str): CoinGecko ID for the coin (default: "ripple")
        
    Returns:
        dict: Dictionary containing sentiment and price data
    """
    # Add a random delay to avoid synchronized rate limiting
    time.sleep(random.uniform(0.5, 1.5))
    
    # Max retries for rate limiting
    max_retries = 3
    
    try:
        # API endpoints
        url_sentiment = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        url_price = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd,sgd"
        
        # Add a randomized user agent to avoid rate limiting
        headers = {
            "User-Agent": f"Crypto Sentiment Analyzer/{random.random()}",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br"
        }
        
        # Function to make request with retries
        def make_request_with_retry(url, max_attempts=max_retries):
            for attempt in range(max_attempts):
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    # If rate limited, wait and retry
                    if response.status_code == 429:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"Rate limited. Waiting {wait_time:.2f}s before retry...")
                        time.sleep(wait_time)
                        continue
                    
                    # For other errors, raise exception
                    response.raise_for_status()
                    return response.json()
                    
                except requests.exceptions.RequestException as e:
                    if attempt < max_attempts - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"Request error: {e}. Retrying in {wait_time:.2f}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"Failed after {max_attempts} attempts: {e}")
                        raise
            
            # If we get here, all retries failed
            raise Exception(f"All {max_attempts} requests failed")
        
        # Get sentiment data
        try:
            sentiment_data = make_request_with_retry(url_sentiment)
        except Exception as e:
            print(f"Error fetching sentiment data for {coin_id}: {e}")
            sentiment_data = {}
        
        # Wait between requests to avoid rate limiting
        time.sleep(random.uniform(1.0, 2.0))
        
        # Get price data
        try:
            price_data = make_request_with_retry(url_price)
        except Exception as e:
            print(f"Error fetching price data for {coin_id}: {e}")
            price_data = {}
        
        # Extract sentiment data (if available)
        up = sentiment_data.get('sentiment_votes_up_percentage')
        down = sentiment_data.get('sentiment_votes_down_percentage')
        
        # Extract price data (if available)
        price_usd = price_data.get(coin_id, {}).get("usd", 0)
        price_sgd = price_data.get(coin_id, {}).get("sgd", 0)
        
        # If we have price but not sentiment, try to get market cap and volume
        market_cap = 0
        volume = 0
        price_change_24h = 0
        
        if sentiment_data and 'market_data' in sentiment_data:
            market_data = sentiment_data['market_data']
            market_cap = market_data.get('market_cap', {}).get('usd', 0)
            volume = market_data.get('total_volume', {}).get('usd', 0)
            price_change_24h = market_data.get('price_change_percentage_24h', 0)
        
        # Return all data
        return {
            "source": "coingecko",
            "sentiment_up": up,
            "sentiment_down": down,
            "price": price_usd,
            "price_sgd": price_sgd,
            "market_cap": market_cap,
            "volume": volume,
            "price_change_24h": price_change_24h,
            "timestamp": time.time()
        }
    
    except Exception as e:
        print(f"Unexpected error in get_coingecko_sentiment for {coin_id}: {e}")
        # Return default values as fallback
        return {
            "source": "coingecko",
            "sentiment_up": None,
            "sentiment_down": None,
            "price": 0,
            "price_sgd": 0,
            "timestamp": time.time(),
            "error": str(e)
        }