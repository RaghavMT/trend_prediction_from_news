from transformers import pipeline
from finbert_model import FinBERTModel


class FinBERTSentimentEngine:

    def __init__(self):

        # Load FinBERT model class
        finbert = FinBERTModel()

        # Create HuggingFace sentiment pipeline
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=finbert.model,
            tokenizer=finbert.tokenizer
        )


    def analyze_sentiment(self, text):

        result = self.sentiment_pipeline(text)

        sentiment = result[0]["label"]
        confidence = result[0]["score"]

        return {
            "text": text,
            "sentiment": sentiment,
            "confidence": confidence
        }