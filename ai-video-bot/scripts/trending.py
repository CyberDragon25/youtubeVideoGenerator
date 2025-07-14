# scripts/trending.py

import feedparser

def get_trending_topic_from_rss():
    # Google Trends RSS feed for trending searches (US daily)
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    feed = feedparser.parse(url)

    if feed.entries:
        # Get the title of the first trending topic
        return feed.entries[0].title
    else:
        return "AI news"

if __name__ == "__main__":
    topic = get_trending_topic_from_rss()
    print(f"Trending topic: {topic}")
