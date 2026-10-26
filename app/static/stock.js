const ticker = window.STOCK_TICKER;
const history = window.STOCK_HISTORY;
const detail = document.querySelector("#detail");
const loading = document.querySelector("#loading");
const error = document.querySelector("#error");
const notFound = document.querySelector("#not-found");
const watchButton = document.querySelector("#watch-button");

function formatNumber(value) {
  return Number(value).toFixed(2);
}

function formatSigned(value, suffix = "") {
  const sign = value > 0 ? "+" : "";
  return `${sign}${formatNumber(value)}${suffix}`;
}

function drawChart(points) {
  const width = 720;
  const height = 260;
  const padding = 18;
  const values = points.map((point) => Number(point.close));
  const minimum = Math.min(...values);
  const maximum = Math.max(...values);
  const range = maximum - minimum || 1;
  const coordinates = values.map((value, index) => {
    const x = padding + (index / (values.length - 1)) * (width - padding * 2);
    const y = height - padding - ((value - minimum) / range) * (height - padding * 2);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });
  document.querySelector("#chart").innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="60-day closing price line">
      <polyline points="${coordinates.join(" ")}" fill="none" stroke="currentColor" stroke-width="3" vector-effect="non-scaling-stroke" />
    </svg>`;
}

function renderWatchlist(items) {
  const watched = items.some((item) => item.ticker === ticker);
  watchButton.textContent = watched ? "Remove from watchlist" : "Add to watchlist";
  watchButton.dataset.watched = String(watched);
}

async function loadWatchlist() {
  const response = await fetch("/api/watchlist");
  if (!response.ok) throw new Error("watchlist request failed");
  renderWatchlist(await response.json());
}

async function toggleWatchlist() {
  const watched = watchButton.dataset.watched === "true";
  const response = await fetch(watched ? `/api/watchlist/${ticker}` : "/api/watchlist", {
    method: watched ? "DELETE" : "POST",
    headers: watched ? {} : { "Content-Type": "application/json" },
    body: watched ? undefined : JSON.stringify({ ticker }),
  });
  if (!response.ok) {
    error.hidden = false;
    return;
  }
  await loadWatchlist();
}

async function loadDetail() {
  if (!history) {
    loading.hidden = true;
    notFound.hidden = false;
    return;
  }
  try {
    const [quoteResponse, analysisResponse] = await Promise.all([
      fetch(`/api/stocks/${ticker}`),
      fetch(`/api/stocks/${ticker}/analysis`),
    ]);
    if (!quoteResponse.ok || !analysisResponse.ok) throw new Error("detail request failed");
    const quote = await quoteResponse.json();
    const analysis = await analysisResponse.json();
    const breakdown = analysis.breakdown;
    const sma20 = quote.latest_close / (1 + breakdown.position_vs_sma / 100);
    const sma5 = sma20 * (1 + breakdown.sma_trend / 100);
    document.querySelector("#company-name").textContent = quote.name;
    document.querySelector("#quote-date").textContent = `Dataset date: ${quote.data_date}`;
    document.querySelector("#latest-close").textContent = formatNumber(quote.latest_close);
    document.querySelector("#daily-change").textContent = `${formatSigned(quote.daily_change)} (${formatSigned(quote.daily_change_percent, "%")})`;
    document.querySelector("#sma5").textContent = formatNumber(sma5);
    document.querySelector("#sma20").textContent = formatNumber(sma20);
    document.querySelector("#momentum").textContent = formatSigned(breakdown.momentum, "%");
    document.querySelector("#trend").textContent = formatSigned(breakdown.sma_trend, "%");
    document.querySelector("#score").textContent = formatNumber(analysis.score);
    document.querySelector("#label").textContent = analysis.label;
    document.querySelector("#source").textContent = analysis.source;
    document.querySelector("#explanation").textContent = analysis.explanation;
    document.querySelector("#chart-range").textContent = `${history.length} dated closes`;
    document.querySelector("#breakdown").innerHTML = Object.entries(breakdown.components).map(([name, value]) => `
      <div><dt>${name.replaceAll("_", " ")}</dt><dd>${formatNumber(value)} <small>${formatNumber(breakdown.weights[name] * 100)}%</small></dd></div>
    `).join("");
    drawChart(history);
    await loadWatchlist();
    loading.hidden = true;
    detail.hidden = false;
  } catch (requestError) {
    loading.hidden = true;
    error.hidden = false;
  }
}

watchButton.addEventListener("click", toggleWatchlist);
loadDetail();