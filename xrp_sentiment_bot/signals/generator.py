# def generate_trading_signals(data, threshold_positive=0.3, threshold_negative=-0.3):
#     score = data["composite_sentiment"]
#     if score > threshold_positive: signal = "BUY"
#     elif score < threshold_negative: signal = "SELL"
#     else: signal = "HOLD"
#     return {"signal": signal, "strength": abs(score), "sentiment_score": score, "timestamp": data["timestamp"]}

# def generate_trading_signals(data, threshold_positive=0.3, threshold_negative=-0.3):
#     score = data["composite_sentiment"]
#     if score > threshold_positive: signal = "BUY"
#     elif score < threshold_negative: signal = "SELL"
#     else: signal = "HOLD"
#     return {"signal": signal, "strength": abs(score), "sentiment_score": score, "timestamp": data["timestamp"]}

import time

def generate_trading_signals(data):
    score = data["composite_sentiment"]
    price = data["coin_price"]

    if score > 0.3:
        signal = "BUY"
        strength = round(score - 0.3, 3)

    elif score < 0.1:
        signal = "SELL"
        strength = round(0.1 - score, 3)

    else:
        signal = "HOLD"
        strength = round(0.3 - abs(score - 0.2), 3)

    return {
        "signal": signal,
        "sentiment_score": score,
        "strength": strength,
        "timestamp": time.time()
    }

