"""from company_mapper import CompanyMapper

mapper = CompanyMapper()
entities = [
    "RIL",
    "Reliance",
    "Bharti Airtel Ltd.",
    "TCS"
]
enty = [
    "Reliance",
    "Jio",
    "Tata Tech"
]

result = mapper.map_entities_to_ticker(entities)
abc = mapper.map_entities_to_ticker(enty)

print(result)
print(abc)"""

from ner_pipeline import NERPipeline

ner = NERPipeline()

print(ner.extract_entities("Reliance Industries plans expansion"))