import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from src.ner_pipeline.ner_pipeline import NERPipeline
from src.ner_pipeline.parent_mapper import ParentCompanyMapper
from src.finbert_pipeline.sentiment_engine import FinBERTSentimentEngine
from mappings.event_mapper import detect_event

def split_by_contrast(text):
        keywords = ["but", "however", "while", "although", "despite"]
        
        for word in keywords:
            if word in text.lower():
                parts = text.lower().split(word)
                return [p.strip() for p in parts]
        
        return [text]
def process_news_batch(self, headlines: list):

    results = []

    for headline in headlines:
        output = self.process_headline(headline)

        for item in output:
            results.append(item)

    return results

class NewsPipeline:
    """
    Complete pipeline:
    Headline → Entities → Parent Mapping → Dedup → Sentiment → Final Output
    """

    def __init__(self):
        self.ner = NERPipeline()
        self.parent_mapper = ParentCompanyMapper()
        self.sentiment_engine = FinBERTSentimentEngine()

    
    def process_headline(self, headline: str):
        """
        Process a single news headline into structured output
        """

        # Step 1: Extract entities
        entities = self.ner.extract_entities(headline)

        if not entities:
            # 🔥 NEW LOGIC
            entities = detect_event(headline)
        
        # Step 2: Map to parent + ticker
        mapped_results = self.parent_mapper.map_entities(entities)

        # Step 3: Deduplicate (VERY IMPORTANT)
        seen = set()
        unique_results = []

        for item in mapped_results:
            ticker = item.get("ticker")

            if ticker and ticker not in seen:
                seen.add(ticker)
                unique_results.append(item)

        # ✅ FIX 1: Handle empty results (moved OUTSIDE loop)
        if not unique_results:
            print("⚠️ No companies found")
            return []

        final_output = []

        for item in unique_results:

            company_name = item["mapped_company"]

            # 🔥 Focused input
            parts = split_by_contrast(headline)

            company_text = headline  # fallback

            for part in parts:
                if company_name.lower() in part:
                    company_text = part
                    break

            sentiment = self.sentiment_engine.analyze_sentiment(company_text)

            # ✅ FIX 2: sentiment handling INSIDE loop
            if sentiment is not None:
                label = sentiment.get("sentiment", "neutral")
                score = sentiment.get("confidence", 0.0)
            else:
                label = "neutral"
                score = 0.0

            if score < 0.6:
                continue

            final_output.append({
                "entity": item["entity"],
                "company": company_name,
                "ticker": item["ticker"],
                "sentiment": label,
                "confidence": score
            })

        return final_output