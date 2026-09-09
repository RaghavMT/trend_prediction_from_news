# 📊 AI-Powered Stock Sentiment Analyzer

# ⚠️⚠️⚠️⚠️This is only for the top 15 stocks of nifty 50 which are as follows:
    RELIANCE
    TCS
    INFY
    HDFCBANK
    ICICIBANK
    SBIN
    AXISBANK
    KOTAKBANK
    BHARTIARTL
    LT
    ITC
    HINDUNILVR
    MARUTI
    M&M
    BAJFINANCE

# As this project takes manual mapping of multiple different sectors and keywords it's quit challenging to do it for all 6000+ stocks listed only on the indian market,

## 🚀 Overview
This project is an NLP-based pipeline that analyzes financial news headlines to identify affected companies and determine sentiment.

It extracts company entities, maps them to listed stocks, and uses a financial sentiment model to classify sentiment.

---

## ⚙️ Features

- 🔍 Named Entity Recognition (NER) for company detection  
- 🔗 Company → Parent stock mapping  
- 🧠 Sentiment analysis using FinBERT  
- ⚡ Multi-company sentiment handling  
- 🧩 Rule + ML hybrid approach  

---

## 🏗️ Pipeline Architecture

News Headline  
↓  
NER (Entity Extraction)  
↓  
Company Mapping  
↓  
Parent Mapping (Ticker)  
↓  
Context Extraction  
↓  
FinBERT Sentiment  
↓  
Final Output  

---

## 📌 Example

Input:  
Reliance rises but HDFC falls after market pressure  

Output:  
Reliance (RELIANCE) → Positive  
HDFC Bank (HDFCBANK) → Negative  

---

## 🛠️ Tech Stack

- Python  
- HuggingFace Transformers  
- FinBERT  
- Custom NLP pipeline  

---

## ▶️ How to Run

Command line:

```bash
python -m src.main
```

Streamlit app:

```bash
streamlit run app.py
```

HTML/CSS/JS frontend + API (run both, then open `frontend/index.html` in your browser):

```bash
python -m src.api.api_app
```

---

## 📁 Project Structure

```
src/
├── ner_pipeline/
├── finbert_pipeline/
├── pipeline/
├── api/
├── main.py
frontend/
mappings/
```

---

## 🎯 Future Improvements
- Event-based stock impact detection
- Better context extraction
- Real-time news API integration

---

## 💼 Author

Raghav Tibra
