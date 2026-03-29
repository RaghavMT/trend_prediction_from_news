# File: src/ner_pipeline/ner_pipeline.py

import spacy
from spacy.cli import download

class NERPipeline:
    """
    Extracts organization entities from text.
    """

    def __init__(self):

        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str):
        doc = self.nlp(text)

        entities = []

        # Step 1: ORG entities
        for ent in doc.ents:
            if ent.label_ == "ORG":
                entities.append(ent.text.lower().strip())

        # Step 2: fallback → keyword match (VERY IMPORTANT)
        keywords = [
            "reliance", "jio", "tcs", "infosys", "hdfc", "icici",
            "sbi", "axis", "kotak", "airtel", "itc", "maruti",
            "mahindra", "bajaj"
        ]

        text_lower = text.lower()

        for word in keywords:
            if word in text_lower:
                entities.append(word)

        return list(set(entities))