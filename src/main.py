from src.pipeline.news_pipeline import NewsPipeline

pipeline = NewsPipeline()
test_news = [
    "Reliance rises after strong earnings",
    "HDFC falls due to weak loan growth",
    "ICICI gains market share",
    "TCS reports decline in profits",
    "Infosys sees growth in AI segment"
]

for ns in test_news:
    news = ns

    result = pipeline.process_headline(news)
    print("\nResult:")
    for r in result:
        print(f"{r['company']} ({r['ticker']}) → {r['sentiment']} ({r['confidence']:.2f})")
    

    
"""while True:
    news = input("Enter headline: ")

    result = pipeline.process_headline(news)

    print("\nResult:")
    for r in result:
        print(f"{r['company']} ({r['ticker']}) → {r['sentiment']} ({r['confidence']:.2f})")
        """