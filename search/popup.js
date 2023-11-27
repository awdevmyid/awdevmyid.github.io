document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const query = searchInput.value;
    searchAWDev(query);
  });

  function searchAWDev(query) {
    const searchUrl = `https://www.awdev.my.id/search?q=${encodeURIComponent(query)}`;

    chrome.tabs.create({ url: searchUrl }, (tab) => {
      chrome.tabs.executeScript(tab.id, { file: 'contentScript.js' });
    });
  }

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'searchResults') {
      displaySearchResults(message.results);
    }
  });

  function displaySearchResults(results) {
    searchResults.innerHTML = '';

    results.forEach((result) => {
      const resultItem = document.createElement('a');
      resultItem.href = result.url;
      resultItem.target = '_blank';
      resultItem.textContent = result.title;
      resultItem.classList.add('result-item');
      searchResults.appendChild(resultItem);
    });
  }
});
