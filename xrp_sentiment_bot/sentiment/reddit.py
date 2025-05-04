import praw
from textblob import TextBlob
import time

reddit = praw.Reddit(
    client_id="F6z17Qm7QkY8-lSUcqLxNg",
    client_secret="x36e1H5zHn4McnAZOJHuVizrsy6jAw",
    user_agent="script:xrp_sentiment_bot:1.0 (by /u/Apprehensive_Dog3290)"
)

def analyze_reddit_sentiment(subreddit="Ripple", post_limit=10):
    posts = reddit.subreddit(subreddit).hot(limit=post_limit)
    results = []

    for post in posts:
        title = post.title
        polarity = TextBlob(title).sentiment.polarity
        results.append({
            "source": "reddit",
            "text": title,
            "polarity": polarity,
            "timestamp": post.created_utc
        })

    return results

