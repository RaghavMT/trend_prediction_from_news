EVENT_MAP = {
    "oil": ["reliance", "ongc", "ioc"],
    "crude": ["reliance", "ongc"],
    "rbi": ["hdfc bank", "icici bank", "axis bank"],
    "interest rate": ["hdfc bank", "kotak bank", "sbi"],
    "inflation": ["fmcg", "banking"]
}

def detect_event(text):
    text = text.lower()

    for keyword in EVENT_MAP:
        if keyword in text:
            return EVENT_MAP[keyword]

    return []

