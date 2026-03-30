import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from fastapi import FastAPI
from pydantic import BaseModel

import streamlit as st
from src.data_ingestion.news_fetcher import NewsFetcher
from src.finbert_pipeline.sentiment_engine import SentimentEngine
from src.ner_pipeline.company_mapper import CompanyMapper
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