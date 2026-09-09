import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from src.data_ingestion.news_fetcher import NewsFetcher
from src.ner_pipeline.ner_pipeline import NERPipeline
from src.ner_pipeline.parent_mapper import ParentCompanyMapper
from src.finbert_pipeline.sentiment_engine import FinBERTSentimentEngine
from mappings.event_mapper import detect_event


def split_by_contrast(text):
    # if the headline has a contrast word ("but", "however", ...), split it into
    # two halves so we can match each company to the half of the sentence about it
    contrast_words = ["but", "however", "while", "although", "despite"]

    for word in contrast_words:
        if word in text.lower():
            parts = text.lower().split(word)
            return [p.strip() for p in parts]

    return [text]


class NewsPipeline:
    """
    Complete pipeline:
    Headline -> Entities -> Parent Mapping -> Dedup -> Sentiment -> Final Output
    """

    def __init__(self):
        self.ner = NERPipeline()
        self.parent_mapper = ParentCompanyMapper()
        self.sentiment_engine = FinBERTSentimentEngine()
        self.news_fetcher = NewsFetcher(api_key="feb1ceb153984d179fb60e1108f1d90c")

    def process_headline(self, headline: str):
        """
        Process a single news headline into structured output
        """

        # Step 1: find company names in the headline
        entities = self.ner.extract_entities(headline)

        if not entities:
            entities = detect_event(headline)

        if not entities:
            # fallback: guess a broad sector from a few common keywords
            text = headline.lower()

            if "oil" in text:
                entities = ["oil"]
            elif "tech" in text:
                entities = ["tech"]
            elif "bank" in text or "fed" in text:
                entities = ["banking"]

        # Step 2: turn each entity into a company + stock ticker
        mapped_results = self.parent_mapper.map_entities(entities)

        # Step 3: remove duplicate tickers
        seen_tickers = set()
        unique_results = []

        for item in mapped_results:
            ticker = item.get("ticker")

            if ticker and ticker not in seen_tickers:
                seen_tickers.add(ticker)
                unique_results.append(item)

        if not unique_results:
            return []

        final_output = []

        for item in unique_results:
            company_name = item["mapped_company"]

            # use only the half of the headline that talks about this company,
            # so "X rises but Y falls" scores X and Y separately
            parts = split_by_contrast(headline)
            company_text = headline

            for part in parts:
                if company_name.lower() in part:
                    company_text = part
                    break

            sentiment = self.sentiment_engine.analyze_sentiment(company_text)

            if sentiment is not None:
                label = sentiment.get("sentiment", "neutral")
                score = sentiment.get("confidence", 0.0)
            else:
                label = "neutral"
                score = 0.0

            # skip low-confidence results
            if score < 0.6:
                continue

            final_output.append({
                "headline": headline,
                "entity": item["entity"],
                "company": company_name,
                "ticker": item["ticker"],
                "sentiment": label,
                "confidence": score
            })

        return final_output

    def run_live_pipeline(self):
        news_articles = self.news_fetcher.fetch_market_news()
        headlines = [article["title"] for article in news_articles]

        results = []

        for headline in headlines:
            output = self.process_headline(headline)
            results.extend(output)

        return results


if __name__ == "__main__":
    pipeline = NewsPipeline()
    results = pipeline.run_live_pipeline()

    for r in results:
        print(r)
