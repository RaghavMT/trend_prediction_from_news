import sys
import os

# force UTF-8 stdout/stderr so the pipeline's emoji print statements don't crash
# with UnicodeEncodeError on Windows, where the console defaults to cp1252
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# api_app.py lives in src/api, so go up two levels to reach the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.pipeline.news_pipeline import NewsPipeline

app = FastAPI()

# allow the local static frontend (served from a different origin/port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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


if __name__ == "__main__":
    # lets you start the API with `python -m src.api.api_app` instead of typing the uvicorn command
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)