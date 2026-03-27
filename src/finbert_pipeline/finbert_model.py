from transformers import AutoTokenizer, AutoModelForSequenceClassification


class FinBERTModel:

    def __init__(self):

        self.model_name = "ProsusAI/finbert"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)


