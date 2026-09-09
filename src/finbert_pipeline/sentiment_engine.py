from transformers import pipeline
from src.finbert_pipeline.finbert_model import FinBERTModel


class FinBERTSentimentEngine:

    def __init__(self):
        print("Loading FinBERT model...")

        finbert = FinBERTModel()

        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=finbert.model,
            tokenizer=finbert.tokenizer
        )

        print("FinBERT model loaded")

    def analyze_sentiment(self, text):
        if not text or len(text.strip()) == 0:
            return None

        try:
            result = self.sentiment_pipeline(text)

            return {
                "text": text,
                "sentiment": result[0]["label"],
                "confidence": result[0]["score"]
            }

        except Exception as e:
            print("FinBERT error:", str(e))
            return None