import requests


class NewsFetcher:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

        self.domains = [
            "reuters.com",
            "bloomberg.com",
            "economictimes.indiatimes.com",
            "moneycontrol.com",
            "cnbc.com"
        ]

    def fetch_market_news(self):

        params = {
            "q": "stock OR market OR company OR earnings OR economy",
            "domains": ",".join(self.domains),
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 20,
            "apiKey": self.api_key
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            raise Exception(f"NewsAPI HTTP Error: {response.status_code}")

        data = response.json()

        if data["status"] != "ok":
            raise Exception(f"NewsAPI Error: {data}")

        articles = []

        for article in data["articles"]:

            title = article["title"]

            if not title:
                continue

            news_item = {
                "title": title.strip(),
                "source": article["source"]["name"],
                "published_at": article["publishedAt"]
            }

            articles.append(news_item)

        return articles

if __name__ == "__main__":

    API_KEY = "feb1ceb153984d179fb60e1108f1d90c"

    fetcher = NewsFetcher(API_KEY)

    news = fetcher.fetch_market_news()

    for article in news:
        print(article)