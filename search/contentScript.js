const results = [];

document.querySelectorAll('.search-results .result').forEach((result) => {
  const title = result.querySelector('.result-title').textContent;
  const url = result.querySelector('.result-url').textContent;
  results.push({ title, url });
});

chrome.runtime.sendMessage({ type: 'searchResults', results });
