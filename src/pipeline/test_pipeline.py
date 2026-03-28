from src.pipeline.news_pipeline import NewsPipeline

pipeline = NewsPipeline()

news = "Reliance does nothing"

result = pipeline.process_headline(news)

print(result)