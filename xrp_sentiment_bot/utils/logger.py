import csv
import os
from datetime import datetime

def log_sentiment_to_csv(data, signal, filepath="data/logs/sentiment_log.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file_exists = os.path.isfile(filepath)
    # Inside log_sentiment_to_csv...
    timestamp_str = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "price_usd", "price_sgd", "cg_score", "reddit_score", "news_score", "composite", "signal", "strength"])
        
        row = [
            timestamp_str,
            f"${data['coin_price']:.4f}",
            f"${data['coin_price_sgd']:.4f}",
            round(data["individual_sentiments"][0]["polarity"], 3),
            round(data["individual_sentiments"][1]["polarity"], 3),
            round(data["individual_sentiments"][2]["polarity"], 3),
            round(data["composite_sentiment"], 3),
            signal["signal"],
            round(signal["strength"], 3)
        ]
        writer.writerow(row) 

def save_output_to_txt(processed, signal, filepath="data/logs/sentiment_analysis_log.txt"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    timestamp = datetime.fromtimestamp(processed["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    price_usd = processed["coin_price"]
    price_sgd = processed["coin_price_sgd"]

    with open(filepath, "a", encoding="utf-8") as file:
        file.write("\n" + "="*40 + "\n")
        file.write("📊 SENTIMENT ANALYSIS SUMMARY\n")
        file.write("="*40 + "\n")
        file.write(f"🕒 Timestamp: {timestamp}\n\n")
        file.write("🔍 Individual Sentiments:\n")
        for s in processed["individual_sentiments"]:
            file.write(f" - {s['source'].capitalize():<10}: Polarity = {s['polarity']:.3f} (Weight: {s['weight']})\n")
        
        file.write(f"\n💰 Current XRP Price (USD): ${price_usd:.4f}\n")
        file.write(f"💱 Current XRP Price (SGD): ${price_sgd:.4f}\n")
        file.write(f"\n🧠 Composite Sentiment Score: {processed['composite_sentiment']:.3f}\n\n")
        file.write("💡 Trading Signal:\n")
        file.write(f" 👉 Action   : {signal['signal']}\n")
        file.write(f" 🔥 Strength : {signal['strength']:.3f}\n")
        file.write("="*40 + "\n")

