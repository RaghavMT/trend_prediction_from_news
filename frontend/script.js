// FastAPI backend is expected to run locally via: python -m src.api.api_app
const API_BASE = "http://127.0.0.1:8000";

const statusEl = document.getElementById("status");
const headlineInput = document.getElementById("headline-input");
const analyzeBtn = document.getElementById("analyze-btn");
const analyzeResults = document.getElementById("analyze-results");
const liveBtn = document.getElementById("live-btn");
const liveResults = document.getElementById("live-results");

// pings the API root so the user knows immediately if the backend isn't running
async function checkBackend() {
  try {
    const res = await fetch(`${API_BASE}/`);
    if (!res.ok) throw new Error("bad status");
    statusEl.textContent = "Backend connected";
    statusEl.className = "status status--ok";
  } catch (err) {
    statusEl.textContent = "Backend not reachable — start it with: python -m src.api.api_app";
    statusEl.className = "status status--down";
  }
}

// renders a list of {company, ticker, sentiment, confidence} into a results container
function renderResults(container, results) {
  container.innerHTML = "";

  if (!results || results.length === 0) {
    container.innerHTML = '<p class="empty">No relevant companies found.</p>';
    return;
  }

  for (const item of results) {
    const sentimentClass = `sentiment--${(item.sentiment || "neutral").toLowerCase()}`;

    const row = document.createElement("div");
    row.className = "result-item";
    row.innerHTML = `
      <span>
        <span class="company">${item.company}</span>
        <span class="ticker">(${item.ticker})</span>
      </span>
      <span class="sentiment ${sentimentClass}">${item.sentiment} ${(item.confidence * 100).toFixed(0)}%</span>
    `;
    container.appendChild(row);
  }
}

function renderError(container, message) {
  container.innerHTML = `<p class="error">${message}</p>`;
}

// disables a button and swaps its label while an async action runs
function withLoading(button, loadingLabel, fn) {
  const originalLabel = button.textContent;
  return async (...args) => {
    button.disabled = true;
    button.textContent = loadingLabel;
    try {
      await fn(...args);
    } finally {
      button.disabled = false;
      button.textContent = originalLabel;
    }
  };
}

async function analyzeHeadline() {
  const text = headlineInput.value.trim();
  if (!text) return;

  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderResults(analyzeResults, data.results);
    statusEl.textContent = "Backend connected";
    statusEl.className = "status status--ok";
  } catch (err) {
    renderError(analyzeResults, "Could not reach the backend. Is it running on port 8000?");
    statusEl.textContent = "Backend not reachable — start it with: python -m src.api.api_app";
    statusEl.className = "status status--down";
  }
}

async function fetchLiveNews() {
  try {
    const res = await fetch(`${API_BASE}/live-news`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderResults(liveResults, data.results);
    statusEl.textContent = "Backend connected";
    statusEl.className = "status status--ok";
  } catch (err) {
    renderError(liveResults, "Could not reach the backend. Is it running on port 8000?");
    statusEl.textContent = "Backend not reachable — start it with: python -m src.api.api_app";
    statusEl.className = "status status--down";
  }
}

analyzeBtn.addEventListener("click", withLoading(analyzeBtn, "Analyzing...", analyzeHeadline));
liveBtn.addEventListener("click", withLoading(liveBtn, "Fetching...", fetchLiveNews));
headlineInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") analyzeBtn.click();
});

checkBackend();
