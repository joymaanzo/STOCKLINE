const state = {
  stocks: [],
  watchlist: new Set(),
};

const elements = {
  search: document.querySelector("#search"),
  stocks: document.querySelector("#stocks"),
  loading: document.querySelector("#loading"),
  error: document.querySelector("#error"),
  empty: document.querySelector("#empty"),
  datasetDate: document.querySelector("#dataset-date"),
};

function formatChange(value) {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}`;
}

function formatPercent(value) {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function render() {
  const query = elements.search.value.trim().toLowerCase();
  const matches = state.stocks.filter((stock) =>
    stock.ticker.toLowerCase().includes(query) || stock.name.toLowerCase().includes(query),
  );
  elements.stocks.replaceChildren();
  elements.empty.hidden = matches.length > 0;

  for (const stock of matches) {
    const row = document.createElement("tr");
    const changeClass = stock.daily_change >= 0 ? "positive" : "negative";
    const watched = state.watchlist.has(stock.ticker);
    row.innerHTML = `
      <th scope="row"><a href="/stock/${stock.ticker}"><strong>${stock.ticker}</strong><span>${stock.name}</span></a></th>
      <td><strong>${stock.latest_close.toFixed(2)}</strong><span>${stock.data_date}</span></td>
      <td class="${changeClass}"><strong>${formatChange(stock.daily_change)}</strong><span>${formatPercent(stock.daily_change_percent)}</span></td>
      <td><button class="watch-button" data-ticker="${stock.ticker}" type="button">${watched ? "Remove" : "Add"}</button></td>
    `;
    elements.stocks.append(row);
  }
  document.querySelectorAll(".watch-button").forEach((button) => {
    button.addEventListener("click", () => toggleWatchlist(button.dataset.ticker));
  });
}

async function loadWatchlist() {
  const response = await fetch("/api/watchlist");
  if (!response.ok) throw new Error("watchlist request failed");
  const items = await response.json();
  state.watchlist = new Set(items.map((item) => item.ticker));
}

async function toggleWatchlist(ticker) {
  const watched = state.watchlist.has(ticker);
  const response = await fetch(watched ? `/api/watchlist/${ticker}` : "/api/watchlist", {
    method: watched ? "DELETE" : "POST",
    headers: watched ? {} : { "Content-Type": "application/json" },
    body: watched ? undefined : JSON.stringify({ ticker }),
  });
  if (!response.ok) {
    showError();
    return;
  }
  await loadWatchlist();
  render();
}

function showError() {
  elements.error.hidden = false;
  elements.loading.hidden = true;
}

async function loadDashboard() {
  try {
    const [stocksResponse] = await Promise.all([
      fetch("/api/stocks"),
      loadWatchlist(),
    ]);
    if (!stocksResponse.ok) throw new Error("stocks request failed");
    state.stocks = await stocksResponse.json();
    elements.datasetDate.textContent = `Dataset date: ${state.stocks[0]?.data_date || "unavailable"}`;
    elements.loading.hidden = true;
    render();
  } catch (error) {
    showError();
  }
}

elements.search.addEventListener("input", render);
loadDashboard();