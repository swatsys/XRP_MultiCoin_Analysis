# from utils.logger import save_output_to_txt
# from utils.logger import log_sentiment_to_csv
# from sentiment.coingecko import get_coingecko_sentiment
# from sentiment.reddit import analyze_reddit_sentiment
# from sentiment.news import get_news_sentiment
# from sentiment.processing import process_sentiment_data
# from signals.generator import generate_trading_signals
# import time

# def run_sentiment_analysis():
#     try:
#         print("=== Starting sentiment analysis ===")
#         cg = get_coingecko_sentiment()
#         print("✅ CoinGecko data collected.")

#         reddit = analyze_reddit_sentiment()
#         print("✅ Reddit data collected.")

#         news = get_news_sentiment()
#         print("✅ News data collected.")

#         processed = process_sentiment_data(cg, reddit, news)
#         processed["coin_price"] = cg["price"]
#         processed["coin_price_sgd"] = cg["price_sgd"]  # Add SGD price to processed data

#         signal = generate_trading_signals(processed)
#         log_sentiment_to_csv(processed, signal)

#         # Fancy output
#         print("\n" + "="*40)
#         print("📊 SENTIMENT ANALYSIS SUMMARY")
#         print("="*40)
#         print(f"🕒 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(processed['timestamp']))}")

#         print("\n🔍 Individual Sentiments:")
#         for s in processed['individual_sentiments']:
#             print(f" - {s['source'].capitalize():<10}: Polarity = {s['polarity']:.3f} (Weight: {s['weight']})")
        
#         print(f"\n💰 Current XRP Price (USD): ${cg['price']:.4f}")
#         print(f"💱 Current XRP Price (SGD): ${cg['price_sgd']:.4f}")
#         print(f"\n🧠 Composite Sentiment Score: {processed['composite_sentiment']:.3f}")
       
#         print("\n💡 Trading Signal:")
#         print(f" 👉 Action   : {signal['signal']}")
#         print(f" 🔥 Strength : {signal['strength']:.3f}")
#         print("="*40 + "\n")
        
#         # Save to sentiment_analysis_log.txt
#         save_output_to_txt(processed, signal)

#     except Exception as e:
#         print(f"❌ Error occurred: {e}")

# if __name__ == "__main__":
#     while True:
#         run_sentiment_analysis()
#         print("⏳ Waiting for 10 minutes before next analysis...\n")
#         time.sleep(600)  # 600 seconds = 10 minutes

# import time
# import os
# import csv
# from datetime import datetime
# from sentiment.coingecko import get_coingecko_sentiment
# from sentiment.reddit import analyze_reddit_sentiment
# from sentiment.news import get_news_sentiment
# from sentiment.processing import process_sentiment_data
# from signals.generator import generate_trading_signals

# # Define supported coins with their configuration
# COINS = {
#     "XRP":  {"id": "ripple",      "subreddit": "Ripple",      "news_cat": "XRP"},
#     "ETH":  {"id": "ethereum",    "subreddit": "ethereum",    "news_cat": "ETH"},
#     "BTC":  {"id": "bitcoin",     "subreddit": "Bitcoin",     "news_cat": "BTC"},
#     "BNB":  {"id": "binancecoin", "subreddit": "binance",     "news_cat": "BNB"},
#     "DOGE": {"id": "dogecoin",    "subreddit": "dogecoin",    "news_cat": "DOGE"},
#     "ADA":  {"id": "cardano",     "subreddit": "cardano",     "news_cat": "ADA"},
#     "TRX":  {"id": "tron",        "subreddit": "Tronix",      "news_cat": "TRX"},
#     "SUI":  {"id": "sui",         "subreddit": "SuiNetwork",  "news_cat": "SUI"},
# }

# # Ensure log directories exist
# def ensure_log_dirs():
#     if not os.path.exists("data/logs"):
#         os.makedirs("data/logs")
#     for coin in COINS.keys():
#         if not os.path.exists(f"data/logs/{coin}"):
#             os.makedirs(f"data/logs/{coin}")

# # Log data to CSV file
# def log_to_csv(coin, data, signal):
#     filepath = f"data/logs/{coin}/sentiment_log.csv"
#     file_exists = os.path.isfile(filepath)
#     timestamp_str = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    
#     with open(filepath, mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         if not file_exists:
#             writer.writerow([
#                 "timestamp", "price_usd", "price_sgd", "cg_score", 
#                 "reddit_score", "news_score", "composite", "signal", "strength"
#             ])
        
#         # Get sentiment scores
#         cg_score = data["individual_sentiments"][0]["polarity"] if len(data["individual_sentiments"]) > 0 else 0
#         reddit_score = data["individual_sentiments"][1]["polarity"] if len(data["individual_sentiments"]) > 1 else 0
#         news_score = data["individual_sentiments"][2]["polarity"] if len(data["individual_sentiments"]) > 2 else 0
        
#         row = [
#             timestamp_str,
#             f"${data.get('coin_price', 0):.4f}",
#             f"${data.get('coin_price_sgd', 0):.4f}",
#             round(cg_score, 3),
#             round(reddit_score, 3),
#             round(news_score, 3),
#             round(data["composite_sentiment"], 3),
#             signal["signal"],
#             round(signal["strength"], 3)
#         ]
#         writer.writerow(row)

# # Save detailed analysis to text file
# def save_to_txt(coin, cg, processed, signal):
#     filepath = f"data/logs/{coin}/analysis_log.txt"
#     timestamp = datetime.fromtimestamp(processed["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    
#     with open(filepath, "a", encoding="utf-8") as file:
#         file.write("\n" + "="*50 + "\n")
#         file.write(f"📊 {coin} SENTIMENT ANALYSIS\n")
#         file.write("="*50 + "\n")
#         file.write(f"🕒 Timestamp: {timestamp}\n\n")
        
#         file.write("💰 Market Data:\n")
#         file.write(f" - Price (USD): ${cg.get('price', 0):.4f}\n")
#         file.write(f" - Price (SGD): ${cg.get('price_sgd', 0):.4f}\n")
        
#         file.write("\n🔍 Sentiment Breakdown:\n")
#         for s in processed['individual_sentiments']:
#             file.write(f" - {s['source'].capitalize():<10}: Polarity = {s['polarity']:.3f} (Weight: {s['weight']})\n")
        
#         file.write(f"\n🧠 Composite Sentiment Score: {processed['composite_sentiment']:.3f}\n\n")
        
#         file.write("💡 Trading Signal:\n")
#         file.write(f" 👉 Action   : {signal['signal']}\n")
#         file.write(f" 🔥 Strength : {signal['strength']:.3f}\n")
#         file.write("="*50 + "\n")

# # Print XRP summary to console
# def print_xrp_summary(cg, processed, signal):
#     print(f"\n--------------- XRP ---------------")
#     print(f"💰 Price (USD): ${cg.get('price', 0):.4f} | SGD: ${cg.get('price_sgd', 0):.4f}")
#     print("🔍 Sentiment Breakdown:")
#     for s in processed['individual_sentiments']:
#         print(f" - {s['source'].capitalize():9}: {s['polarity']:.3f} (Weight: {s['weight']})")
#     print(f"🧠 Composite Score: {processed['composite_sentiment']:.3f}")
#     print(f"💡 Signal: {signal['signal']} (Strength: {signal['strength']:.3f})")

# # Print summary table of all coins
# def print_table(rows):
#     print("\n-----------------------------------------------")
#     print("COIN   |   USD      |  SGD     | Score  | Signal | Strength")
#     print("-----------------------------------------------")
#     for r in rows:
#         price_usd = r.get('usd', 0)
#         price_sgd = r.get('sgd', 0)
#         score = r.get('score', 'N/A')
#         signal = r.get('signal', 'N/A')
#         strength = r.get('strength', 'N/A')
        
#         print(f"{r['coin']:<6} | ${price_usd:<8.4f} | ${price_sgd:<7.4f} | {score:<6} | {signal:^6} | {strength:<7}")
#     print("-----------------------------------------------")

# # Process a single coin with rate limiting
# def process_coin(coin, meta, delay=1.0):
#     try:
#         # Add delay to avoid rate limiting
#         print(f"Processing {coin}...")
#         time.sleep(delay)
        
#         # Get CoinGecko data
#         cg = get_coingecko_sentiment(meta["id"])
#         print(f"✅ CoinGecko data collected for {coin}.")
        
#         # Check if we have valid sentiment data
#         if cg.get("sentiment_up") is not None and cg.get("sentiment_down") is not None:
#             # Get Reddit data with delay
#             time.sleep(delay)
#             try:
#                 reddit = analyze_reddit_sentiment(meta["subreddit"])
#                 print(f"✅ Reddit data collected for {coin}.")
#             except Exception as e:
#                 print(f"⚠️ Error collecting Reddit data for {coin}: {e}")
#                 reddit = []
            
#             # Get News data with delay
#             time.sleep(delay)
#             try:
#                 news = get_news_sentiment(meta["news_cat"])
#                 print(f"✅ News data collected for {coin}.")
#             except Exception as e:
#                 print(f"⚠️ Error collecting news data for {coin}: {e}")
#                 news = []
            
#             # Process sentiment data
#             processed = process_sentiment_data(cg, reddit, news)
#             processed["coin_price"] = cg.get("price", 0)
#             processed["coin_price_sgd"] = cg.get("price_sgd", 0)
            
#             # Generate trading signal
#             signal = generate_trading_signals(processed)
            
#             # Log data
#             log_to_csv(coin, processed, signal)
#             save_to_txt(coin, cg, processed, signal)
            
#             return {
#                 "coin": coin,
#                 "usd": cg.get("price", 0),
#                 "sgd": cg.get("price_sgd", 0),
#                 "score": f"{processed['composite_sentiment']:.3f}",
#                 "signal": signal["signal"],
#                 "strength": f"{signal['strength']:.3f}",
#                 "processed": processed,
#                 "signal_data": signal,
#                 "cg_data": cg
#             }
#         else:
#             print(f"⚠️ No sentiment data available for {coin}")
#             return {
#                 "coin": coin,
#                 "usd": cg.get("price", 0) or 0,
#                 "sgd": cg.get("price_sgd", 0) or 0,
#                 "score": "N/A",
#                 "signal": "N/A",
#                 "strength": "N/A"
#             }
#     except Exception as e:
#         print(f"❌ Error processing {coin}: {e}")
#         return {
#             "coin": coin,
#             "usd": 0,
#             "sgd": 0,
#             "score": "Error",
#             "signal": "Error",
#             "strength": "Error"
#         }

# # Main analysis function
# def run_sentiment_analysis():
#     print("=== Starting multi-coin sentiment analysis ===")
#     ensure_log_dirs()
    
#     # Process only a subset of coins to avoid rate limiting
#     # Start with the most important ones: XRP, BTC, ETH
#     primary_coins = ["XRP", "BTC", "ETH"]
#     secondary_coins = ["BNB", "DOGE", "ADA", "TRX", "SUI"]
    
#     # Calculate an appropriate delay based on coin count
#     delay = 2.0  # Base delay in seconds
    
#     # Process primary coins first
#     primary_results = []
#     xrp_result = None
    
#     for coin in primary_coins:
#         result = process_coin(coin, COINS[coin], delay)
#         if coin == "XRP":
#             xrp_result = result
#         else:
#             primary_results.append(result)
        
#         # Increase delay between requests to avoid rate limiting
#         time.sleep(delay * 2)
    
#     # If XRP has valid data, print summary
#     if xrp_result and "processed" in xrp_result:
#         print_xrp_summary(xrp_result["cg_data"], xrp_result["processed"], xrp_result["signal_data"])
    
#     # Process secondary coins with a longer delay
#     secondary_results = []
#     for coin in secondary_coins:
#         result = process_coin(coin, COINS[coin], delay * 2)
#         secondary_results.append(result)
#         # Add a longer delay between secondary coins
#         time.sleep(delay * 3)
    
#     # Combine results and print summary table
#     all_results = primary_results + secondary_results
#     print_table(all_results)
#     print("\n========================================")

# # Main loop
# if __name__ == "__main__":
#     while True:
#         try:
#             run_sentiment_analysis()
#             # Wait longer between full analysis runs
#             wait_time = 15 * 60  # 15 minutes
#             print(f"⏳ Waiting for {wait_time//60} minutes before next analysis...")
#             time.sleep(wait_time)
#         except KeyboardInterrupt:
#             print("\n🛑 Analysis stopped by user")
#             break
#         except Exception as e:
#             print(f"❌ Error in main loop: {e}")
#             print("⏳ Retrying in 2 minutes...")
#             time.sleep(120)

import time
import os
import csv
from datetime import datetime
from sentiment.coingecko import get_coingecko_sentiment
from sentiment.reddit import analyze_reddit_sentiment
from sentiment.news import get_news_sentiment
from sentiment.processing import process_sentiment_data
from signals.generator import generate_trading_signals

# Define supported coins with their configuration
COINS = {
    "XRP":  {"id": "ripple",      "subreddit": "Ripple",      "news_cat": "XRP"},
    "ETH":  {"id": "ethereum",    "subreddit": "ethereum",    "news_cat": "ETH"},
    "BTC":  {"id": "bitcoin",     "subreddit": "Bitcoin",     "news_cat": "BTC"},
    "BNB":  {"id": "binancecoin", "subreddit": "binance",     "news_cat": "BNB"},
    "DOGE": {"id": "dogecoin",    "subreddit": "dogecoin",    "news_cat": "DOGE"},
    "ADA":  {"id": "cardano",     "subreddit": "cardano",     "news_cat": "ADA"},
    "TRX":  {"id": "tron",        "subreddit": "Tronix",      "news_cat": "TRX"},
    "SUI":  {"id": "sui",         "subreddit": "SuiNetwork",  "news_cat": "SUI"},
}

# Ensure log directories exist
def ensure_log_dirs():
    if not os.path.exists("data/logs"):
        os.makedirs("data/logs")
    for coin in COINS.keys():
        if not os.path.exists(f"data/logs/{coin}"):
            os.makedirs(f"data/logs/{coin}")

# Log data to CSV file
def log_to_csv(coin, data, signal):
    filepath = f"data/logs/{coin}/sentiment_log.csv"
    file_exists = os.path.isfile(filepath)
    timestamp_str = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "timestamp", "price_usd", "price_sgd", "cg_score", 
                "reddit_score", "news_score", "composite", "signal", "strength"
            ])
        
        # Get sentiment scores
        cg_score = data["individual_sentiments"][0]["polarity"] if len(data["individual_sentiments"]) > 0 else 0
        reddit_score = data["individual_sentiments"][1]["polarity"] if len(data["individual_sentiments"]) > 1 else 0
        news_score = data["individual_sentiments"][2]["polarity"] if len(data["individual_sentiments"]) > 2 else 0
        
        row = [
            timestamp_str,
            f"${data.get('coin_price', 0):.4f}",
            f"${data.get('coin_price_sgd', 0):.4f}",
            round(cg_score, 3),
            round(reddit_score, 3),
            round(news_score, 3),
            round(data["composite_sentiment"], 3),
            signal["signal"],
            round(signal["strength"], 3)
        ]
        writer.writerow(row)

# Save detailed analysis to text file
def save_to_txt(coin, cg, processed, signal):
    filepath = f"data/logs/{coin}/analysis_log.txt"
    timestamp = datetime.fromtimestamp(processed["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    
    with open(filepath, "a", encoding="utf-8") as file:
        file.write("\n" + "="*50 + "\n")
        file.write(f"📊 {coin} SENTIMENT ANALYSIS\n")
        file.write("="*50 + "\n")
        file.write(f"🕒 Timestamp: {timestamp}\n\n")
        
        file.write("💰 Market Data:\n")
        file.write(f" - Price (USD): ${cg.get('price', 0):.4f}\n")
        file.write(f" - Price (SGD): ${cg.get('price_sgd', 0):.4f}\n")
        
        file.write("\n🔍 Sentiment Breakdown:\n")
        for s in processed['individual_sentiments']:
            file.write(f" - {s['source'].capitalize():<10}: Polarity = {s['polarity']:.3f} (Weight: {s['weight']})\n")
        
        file.write(f"\n🧠 Composite Sentiment Score: {processed['composite_sentiment']:.3f}\n\n")
        
        file.write("💡 Trading Signal:\n")
        file.write(f" 👉 Action   : {signal['signal']}\n")
        file.write(f" 🔥 Strength : {signal['strength']:.3f}\n")
        file.write("="*50 + "\n")

# Print XRP summary to console
# Print XRP summary to console - modified to prevent duplication
def print_xrp_summary(cg, processed, signal):
    print(f"--------------- XRP ---------------")
    print(f"💰 Price (USD): ${cg.get('price', 0):.4f} | SGD: ${cg.get('price_sgd', 0):.4f}")
    print("🔍 Sentiment Breakdown:")
    for s in processed['individual_sentiments']:
        print(f" - {s['source'].capitalize():9}: {s['polarity']:.3f} (Weight: {s['weight']})")
    print(f"🧠 Composite Score: {processed['composite_sentiment']:.3f}")
    print(f"💡 Signal: {signal['signal']} (Strength: {signal['strength']:.3f})")
    print("------------------------------")
# Print summary table of all coins
def print_table(rows):
    print("\n-----------------------------------------------")
    print("COIN   |   USD      |  SGD     | Score  | Signal | Strength")
    print("-----------------------------------------------")
    for r in rows:
        price_usd = r.get('usd', 0)
        price_sgd = r.get('sgd', 0)
        score = r.get('score', 'N/A')
        signal = r.get('signal', 'N/A')
        strength = r.get('strength', 'N/A')
        
        print(f"{r['coin']:<6} | ${price_usd:<8.4f} | ${price_sgd:<7.4f} | {score:<6} | {signal:^6} | {strength:<7}")
    print("-----------------------------------------------")

# Process a single coin with rate limiting
# Process a single coin with rate limiting
def process_coin(coin, meta, delay=1.0, max_retries=5):
    try:
        # Add delay to avoid rate limiting
        print(f"Processing {coin}...")
        time.sleep(delay)
        
        # Get CoinGecko data with improved retry logic
        retry_count = 0
        cg = None
        
        while retry_count < max_retries:
            try:
                cg = get_coingecko_sentiment(meta["id"])
                print(f"✅ CoinGecko data collected for {coin}.")
                break
            except Exception as e:
                retry_count += 1
                wait_time = retry_count * 2
                print(f"⚠️ Attempt {retry_count}/{max_retries} failed: {e}")
                if retry_count < max_retries:
                    print(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Failed to get CoinGecko data for {coin} after {max_retries} attempts")
                    return {
                        "coin": coin,
                        "usd": 0,
                        "sgd": 0,
                        "score": "Error",
                        "signal": "Error",
                        "strength": "Error"
                    }
        
        # If we still don't have data, exit early
        if not cg:
            return {
                "coin": coin,
                "usd": 0,
                "sgd": 0,
                "score": "Error",
                "signal": "Error",
                "strength": "Error"
            }
        
        # Check if we have valid sentiment data
        if cg.get("sentiment_up") is not None and cg.get("sentiment_down") is not None:
            # Get Reddit data with delay and retry
            time.sleep(delay)
            reddit = []
            retry_count = 0
            
            while retry_count < 3:
                try:
                    reddit = analyze_reddit_sentiment(meta["subreddit"])
                    print(f"✅ Reddit data collected for {coin}.")
                    break
                except Exception as e:
                    retry_count += 1
                    wait_time = retry_count * 2
                    if retry_count < 3:
                        print(f"⚠️ Reddit attempt {retry_count}/3 failed. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"⚠️ Error collecting Reddit data for {coin}: {e}")
            
            # Get News data with delay and retry
            time.sleep(delay)
            news = []
            retry_count = 0
            
            while retry_count < 3:
                try:
                    news = get_news_sentiment(meta["news_cat"])
                    print(f"✅ News data collected for {coin}.")
                    break
                except Exception as e:
                    retry_count += 1
                    wait_time = retry_count * 2
                    if retry_count < 3:
                        print(f"⚠️ News attempt {retry_count}/3 failed. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"⚠️ Error collecting news data for {coin}: {e}")
            
            # Check if we have valid price data
            if cg.get("price", 0) <= 0:
                print(f"⚠️ Warning: Invalid price (${cg.get('price', 0)}) for {coin}. Using fallback method.")
                # You could implement a fallback price fetching method here
            
            # Process sentiment data
            processed = process_sentiment_data(cg, reddit, news)
            processed["coin_price"] = cg.get("price", 0)
            processed["coin_price_sgd"] = cg.get("price_sgd", 0)
            
            # Generate trading signal
            signal = generate_trading_signals(processed)
            
            # Log data
            log_to_csv(coin, processed, signal)
            save_to_txt(coin, cg, processed, signal)
            
            return {
                "coin": coin,
                "usd": cg.get("price", 0),
                "sgd": cg.get("price_sgd", 0),
                "score": f"{processed['composite_sentiment']:.3f}",
                "signal": signal["signal"],
                "strength": f"{signal['strength']:.3f}",
                "processed": processed,
                "signal_data": signal,
                "cg_data": cg
            }
        else:
            print(f"⚠️ No sentiment data available for {coin}")
            return {
                "coin": coin,
                "usd": cg.get("price", 0) or 0,
                "sgd": cg.get("price_sgd", 0) or 0,
                "score": "N/A",
                "signal": "N/A",
                "strength": "N/A"
            }
    except Exception as e:
        print(f"❌ Error processing {coin}: {e}")
        return {
            "coin": coin,
            "usd": 0,
            "sgd": 0,
            "score": "Error",
            "signal": "Error", 
            "strength": "Error"
        }

# Main analysis function
# Main analysis function
def run_sentiment_analysis():
    print("=== Starting multi-coin sentiment analysis ===")
    ensure_log_dirs()
    
    # Process only a subset of coins to avoid rate limiting
    # Start with the most important ones: XRP, BTC, ETH
    primary_coins = ["XRP", "BTC", "ETH"]
    secondary_coins = ["BNB", "DOGE", "ADA", "TRX", "SUI"]
    
    # Calculate an appropriate delay based on coin count
    delay = 3.0  # Increased base delay in seconds
    
    # Process primary coins first
    primary_results = []
    
    for coin in primary_coins:
        result = process_coin(coin, COINS[coin], delay, max_retries=5)
        
        # Print XRP summary immediately after processing XRP
        if coin == "XRP" and "processed" in result:
            print_xrp_summary(result["cg_data"], result["processed"], result["signal_data"])
            print("-" * 30)
        
        if coin != "XRP":  # Only add non-XRP results to the list
            primary_results.append(result)
        
        # Increase delay between requests to avoid rate limiting
        time.sleep(delay * 2)
    
    # Process secondary coins with a longer delay
    secondary_results = []
    for coin in secondary_coins:
        result = process_coin(coin, COINS[coin], delay * 2, max_retries=5)
        secondary_results.append(result)
        # Add a longer delay between secondary coins
        time.sleep(delay * 3)
    
    # Combine results and print summary table
    all_results = primary_results + secondary_results
    
    # Filter out coins with errors or zero prices
    valid_results = []
    for r in all_results:
        price = r.get('usd', 0)
        if price > 0 and r.get('score') != 'Error' and r.get('score') != 'N/A':
            valid_results.append(r)
        else:
            # Try to use fallback display for coins with issues
            if r.get('score') == 'Error' or r.get('score') == 'N/A':
                r['score'] = 'N/A'
                r['signal'] = 'N/A'
                r['strength'] = 'N/A'
            valid_results.append(r)
    
    print_table(valid_results)
    print("\n========================================")

# Main loop
if __name__ == "__main__":
    while True:
        try:
            run_sentiment_analysis()
            # Wait longer between full analysis runs
            wait_time = 15 * 60  # 15 minutes
            print(f"⏳ Waiting for {wait_time//60} minutes before next analysis...")
            time.sleep(wait_time)
        except KeyboardInterrupt:
            print("\n🛑 Analysis stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            print("⏳ Retrying in 2 minutes...")
            time.sleep(120)