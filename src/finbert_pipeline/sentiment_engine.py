from transformers import pipeline
from src.finbert_pipeline.finbert_model import FinBERTModel


class FinBERTSentimentEngine:

    def __init__(self):

        print("🚀 Initializing FinBERT...")

        finbert = FinBERTModel()

        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=finbert.model,
            tokenizer=finbert.tokenizer
        )

        print("✅ FinBERT Loaded Successfully")


    def analyze_sentiment(self, text):

        # 🔥 HARD DEBUG (VERY IMPORTANT)
        if not text or len(text.strip()) == 0:
            print("❌ Empty text received in FinBERT")
            return None

        print(f"🔥 FinBERT INPUT: {text}")

        try:
            result = self.sentiment_pipeline(text)

            print("🔥 RAW OUTPUT:", result)

            sentiment = result[0]["label"]
            confidence = result[0]["score"]

            return {
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence
            }

        except Exception as e:
            print("❌ FinBERT ERROR:", str(e))
            return None