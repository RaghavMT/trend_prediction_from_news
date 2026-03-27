# File: src/ner_pipeline/parent_mapper.py

from typing import List, Dict
from company_mapper import CompanyMapper


class ParentCompanyMapper:
    """
    Maps subsidiaries/brands to their parent company
    and returns the corresponding stock ticker.
    """

    def __init__(self):
        # Initialize existing company mapper
        self.company_mapper = CompanyMapper()

        # Subsidiary → Parent mapping (lowercase, cleaned)
        self.subsidiary_map = {
            "jio": "reliance industries",
            "reliance retail": "reliance industries",
            "tata technologies": "tata consultancy services",
            "amazon web services": "amazon"
        }

    def map_entity(self, entity: str) -> Dict:
        """
        Maps a single entity to parent company and ticker.
        """
        entity = entity.lower().strip()

        # Step 1: Resolve parent
        parent = self.subsidiary_map.get(entity, entity)

        # Step 2: Get ticker using existing mapper
        ticker = self.company_mapper.map_company_to_ticker(parent)

        # Step 3: Return structured output
        return {
            "entity": entity,
            "mapped_company": parent,
            "ticker": ticker
        }

    def map_entities(self, entities: List[str]) -> List[Dict]:
        """
        Maps a list of entities.
        """
        results = []

        for entity in entities:
            result = self.map_entity(entity)
            results.append(result)

        return results