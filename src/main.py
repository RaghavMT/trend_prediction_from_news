from src.pipeline.news_pipeline import NewsPipeline

pipeline = NewsPipeline()

results = pipeline.run_live_pipeline()

print("\nFinal Results:")
for r in results:
    print(f"{r['company']} ({r['ticker']}) → {r['sentiment']} ({r['confidence']:.2f})")



    
"""while True:
    news = input("Enter headline: ")

    result = pipeline.process_headline(news)

    print("\nResult:")
    for r in result:
        print(f"{r['company']} ({r['ticker']}) → {r['sentiment']} ({r['confidence']:.2f})")
        """