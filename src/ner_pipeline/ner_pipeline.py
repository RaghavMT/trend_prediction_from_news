# File: src/ner_pipeline/ner_pipeline.py

import spacy


class NERPipeline:
    """
    Extracts organization entities from text.
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str):
        """
        Extract ORG entities from text
        """
        doc = self.nlp(text)

        entities = []

        for ent in doc.ents:
            if ent.label_ == "ORG":
                entities.append(ent.text.lower().strip())

        return list(set(entities))