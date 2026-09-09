# src/ner_pipeline/company_mapper.py

class CompanyMapper:
    def __init__(self):
        """
        Dictionary mapping company names → stock tickers
        """
        self.alias_to_company = {
            "ril": "reliance industries",
            "reliance": "reliance industries",

            "tcs": "tata consultancy services",

            "infosys ltd": "infosys",

            "hdfc": "hdfc bank",

            "icici": "icici bank",

            "airtel": "bharti airtel",

            "sbi": "state bank of india",

            "lt": "larsen & toubro",

            "itc ltd": "itc"
        }

        self.company_to_ticker = {
            "reliance industries": "RELIANCE",
            "tata consultancy services": "TCS",
            "infosys": "INFY",
            "hdfc bank": "HDFCBANK",
            "icici bank": "ICICIBANK",
            "bharti airtel": "BHARTIARTL",
            "state bank of india": "SBIN",
            "axis bank": "AXISBANK",
            "kotak mahindra bank": "KOTAKBANK",
            "itc": "ITC",
            "maruti suzuki": "MARUTI",
            "wipro": "WIPRO",
            "mahindra & mahindra": "M&M",
            "bajaj finance": "BAJFINANCE",
            "hindustan unilever": "HINDUNILVR",
            "larsen & toubro": "LT"
        }

    def map_entities_to_ticker(self, entities):
        
        """
        Convert NER output → ticker

        Args:
            entities (list): List of company names from NER

        Returns:
            list: List of mapped tickers
        """
        
        tickers = []

        for entity in entities:
            cleaned_entity = self.clean_company_name(entity)

            # ✅ Step 1: Check direct match
            if cleaned_entity in self.company_to_ticker:
                tickers.append(self.company_to_ticker[cleaned_entity])
                continue

            # ✅ Step 2: Check alias match
            if cleaned_entity in self.alias_to_company:
                actual_company = self.alias_to_company[cleaned_entity]

                ticker = self.company_to_ticker.get(actual_company)
                if ticker:
                    tickers.append(ticker)
                continue

        return list(set(tickers))
    
    def clean_company_name(self, name):
        name = name.lower().strip()
        name = name.replace(".", "")

        words = name.split()
        # remove only exact suffix words
        suffixes = {"ltd", "limited", "inc", "corp", "corporation"}

        cleaned_words = [word for word in words if word not in suffixes]

        return " ".join(cleaned_words)

    #this becomes useless now, because we are not currently using rapidfuzz      
    """def fuzzy_match_company(self, cleaned_entity):
        best_match = None
        highest_score = 0

        for company_name in self.company_to_ticker.keys():
            score = fuzz.ratio(cleaned_entity, company_name)

            if score > highest_score:
                highest_score = score
                best_match = company_name

        # threshold (important)
        if highest_score > 80:
            return best_match

        return None"""
        
    def map_company_to_ticker(self, company_name: str):
        """
        Maps a single company name → ticker
        """
        cleaned_entity = self.clean_company_name(company_name)

        # Step 1: Direct match
        if cleaned_entity in self.company_to_ticker:
            return self.company_to_ticker[cleaned_entity]

        # Step 2: Alias match
        if cleaned_entity in self.alias_to_company:
            actual_company = self.alias_to_company[cleaned_entity]
            return self.company_to_ticker.get(actual_company)

        return None