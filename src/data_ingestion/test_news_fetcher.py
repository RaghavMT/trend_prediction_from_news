from src.data_ingestion.news_fetcher import NewsFetcher

API_KEY = "feb1ceb153984d179fb60e1108f1d90c"

fetcher = NewsFetcher(API_KEY)

news = fetcher.fetch_market_news()

for article in news:
    print(article)