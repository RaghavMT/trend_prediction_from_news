import streamlit as st
from src.pipeline.news_pipeline import NewsPipeline

st.caption("⚠️ Model loads once and may take a few seconds on first run")

st.title("News Sentiment Analyzer")

@st.cache_resource
def load_pipeline():
    return NewsPipeline()

with st.spinner("Loading model... please wait"):
    pipeline = load_pipeline()

# Manual input
st.subheader("Analyze Custom News")

user_input = st.text_input("Enter news headline:")

if st.button("Analyze"):
    if user_input:
        results = pipeline.process_headline(user_input)

        if results:
            for r in results:
                st.write(f"{r['company']} ({r['ticker']}) → {r['sentiment']} ({r['confidence']:.2f})")
        else:
            st.write("No relevant companies found")

# Live news
st.subheader("Live Market News")

if st.button("Fetch Live News"):
    results = pipeline.run_live_pipeline()

    if results:
        for r in results:
            st.write(f"{r['company']} ({r['ticker']}) → {r['sentiment']} ({r['confidence']:.2f})")
    else:
        st.write("No results")