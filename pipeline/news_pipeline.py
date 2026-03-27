# File: src/pipeline/news_pipeline.py

from ner_pipeline.ner_pipeline import NERPipeline
from ner_pipeline.parent_mapper import ParentCompanyMapper


class NewsPipeline:
    """
    Main pipeline to process news headlines into structured market data.
    """

    def __init__(self):
        self.ner = NERPipeline()
        self.parent_mapper = ParentCompanyMapper()

    def process_headline(self, headline: str):
        """
        Full pipeline:
        Headline → Entities → Parent Mapping → Tickers
        """

        # Step 1: Extract entities
        entities = self.ner.extract_entities(headline)

        # Step 2: Map to parent companies + tickers
        results = self.parent_mapper.map_entities(entities)

        return results