from src.pipeline.news_pipeline import NewsPipeline

pipeline = NewsPipeline()

results = pipeline.run_live_pipeline()

print("\nFinal Results:")
for r in results:
    print(f"{r['company']} ({r['ticker']}) → {r['sentiment']} ({r['confidence']:.2f})")