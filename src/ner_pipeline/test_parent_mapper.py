from parent_mapper import ParentCompanyMapper

mapper = ParentCompanyMapper()

test_entities = [
    "Jio",
    "Reliance Retail",
    "Reliance Industries",
    "Tata Technologies",
    "Unknown Company"
]

results = mapper.map_entities(test_entities)

for a in results:
    print(a)
    