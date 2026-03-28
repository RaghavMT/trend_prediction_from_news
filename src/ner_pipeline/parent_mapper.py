# File: src/ner_pipeline/parent_mapper.py

from typing import List, Dict
from src.ner_pipeline.company_mapper import CompanyMapper


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
            # Reliance
            "jio": "reliance industries",
            "reliance jio": "reliance industries",
            "jio platforms": "reliance industries",
            "reliance retail": "reliance industries",
            "ril" : "reliance industries",

            # TCS
            "tcs": "tata consultancy services",
            "tata consultancy": "tata consultancy services",
            "tata technologies": "tata consultancy services",

            # Infosys
            "infosys": "infosys",

            # HDFC
            "hdfc bank": "hdfc bank",
            "hdfc": "hdfc bank",
            "hdfc life": "hdfc bank",
            "hdfc asset management": "hdfc bank",

            # ICICI
            "icici": "icici bank",
            "icici bank": "icici bank",
            "icici prudential": "icici bank",
            "icici lombard": "icici bank",

            # SBI
            "sbi": "state bank of india",
            "state bank": "state bank of india",

            # Axis
            "axis": "axis bank",
            "axis bank": "axis bank",

            # Kotak
            "kotak": "kotak mahindra bank",
            "kotak bank": "kotak mahindra bank",

            # Airtel
            "airtel": "bharti airtel",
            "bharti airtel": "bharti airtel",

            # Larsen & Toubro
            "l&t": "larsen & toubro",
            "larsen and toubro": "larsen & toubro",

            # ITC
            "itc": "itc",

            # HUL
            "hul": "hindustan unilever",
            "hindustan unilever": "hindustan unilever",

            # Maruti
            "maruti": "maruti suzuki",
            "maruti suzuki": "maruti suzuki",

            # M&M
            "mahindra": "mahindra & mahindra",
            "m&m": "mahindra & mahindra",
            "mahindra and mahindra": "mahindra & mahindra",

            # Bajaj Finance
            "bajaj finance": "bajaj finance",
            "bajaj finserv": "bajaj finance"
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