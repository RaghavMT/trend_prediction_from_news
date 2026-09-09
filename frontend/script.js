// The FastAPI backend must be running locally: python -m src.api.api_app
const API_BASE = "http://127.0.0.1:8000";

// grab all the HTML elements we need
const statusEl = document.getElementById("status");
const headlineInput = document.getElementById("headline-input");
const analyzeBtn = document.getElementById("analyze-btn");
const analyzeResults = document.getElementById("analyze-results");
const liveBtn = document.getElementById("live-btn");
const liveResults = document.getElementById("live-results");

// checks if the backend is running and updates the status pill at the top
async function checkBackend() {
  try {
    const response = await fetch(API_BASE + "/");
    if (!response.ok) {
      throw new Error("backend returned an error");
    }
    statusEl.textContent = "Backend connected";
    statusEl.className = "status status--ok";
  } catch (error) {
    statusEl.textContent = "Backend not reachable — start it with: python -m src.api.api_app";
    statusEl.className = "status status--down";
  }
}

// builds the little colored badge, e.g. "positive 92%"
function buildSentimentBadge(sentiment, confidence) {
  const sentimentLower = sentiment.toLowerCase();
  const confidencePercent = Math.round(confidence * 100);
  return `<span class="sentiment sentiment--${sentimentLower}">${sentiment} ${confidencePercent}%</span>`;
}

// shows a list of results in the page. Each result includes the headline
// it came from, the company name, ticker, and sentiment.
function showResults(container, results) {
  container.innerHTML = "";

  if (!results || results.length === 0) {
    container.innerHTML = '<p class="empty">No relevant companies found.</p>';
    return;
  }

  for (const item of results) {
    const badge = buildSentimentBadge(item.sentiment, item.confidence);

    const resultCard = document.createElement("div");
    resultCard.className = "result-item";
    resultCard.innerHTML = `
      <p class="headline-text">"${item.headline}"</p>
      <div class="result-row">
        <span>
          <span class="company">${item.company}</span>
          <span class="ticker">(${item.ticker})</span>
        </span>
        ${badge}
      </div>
    `;
    container.appendChild(resultCard);
  }
}

function showError(container, message) {
  container.innerHTML = `<p class="error">${message}</p>`;
}

// runs when the user clicks "Analyze"
async function handleAnalyzeClick() {
  const headline = headlineInput.value.trim();
  if (headline === "") {
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  try {
    const response = await fetch(API_BASE + "/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: headline })
    });

    const data = await response.json();
    showResults(analyzeResults, data.results);
  } catch (error) {
    showError(analyzeResults, "Could not reach the backend. Is it running on port 8000?");
  }

  analyzeBtn.disabled = false;
  analyzeBtn.textContent = "Analyze";
}

// runs when the user clicks "Fetch Live News"
async function handleLiveNewsClick() {
  liveBtn.disabled = true;
  liveBtn.textContent = "Fetching...";

  try {
    const response = await fetch(API_BASE + "/live-news");
    const data = await response.json();
    showResults(liveResults, data.results);
  } catch (error) {
    showError(liveResults, "Could not reach the backend. Is it running on port 8000?");
  }

  liveBtn.disabled = false;
  liveBtn.textContent = "Fetch Live News";
}

analyzeBtn.addEventListener("click", handleAnalyzeClick);
liveBtn.addEventListener("click", handleLiveNewsClick);

// let the user press Enter in the input box instead of clicking the button
headlineInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    handleAnalyzeClick();
  }
});

checkBackend();
