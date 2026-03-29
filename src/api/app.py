from fastapi import FastAPI
from pydantic import BaseModel

from src.pipeline.news_pipeline import NewsPipeline

app = FastAPI()

pipeline = NewsPipeline()


class NewsInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "News Sentiment API running"}


@app.get("/live-news")
def get_live_news():
    results = pipeline.run_live_pipeline()
    return {"results": results}


@app.post("/analyze")
def analyze_news(input: NewsInput):
    result = pipeline.process_headline(input.text)
    return {"results": result}