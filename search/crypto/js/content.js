// A function that creates the cards of the coins by going over the array obtained from the api.
// toLocaleString is designed to format the information that comes from the api because the price is displayed
// in a way that is difficult to read and therefore is converted to a currency display format

function creatCryptoCard(jsonObject) {
  let jsonData = jsonObject;

  $("#root").html("");
  $("#root").append(`<div id="divHomePage"></div>`);
  for (var i = 0; i < jsonData.length; i++) {
    $("#divHomePage").append(`<div class="card">
              <div class="imgsymname" title="Select up to 5 coins to get live reports">
                  <div><img src="${jsonData[i].image.small}"></div>
                  <div class="coin-description">
                      <div class="symbolcrypt">${jsonData[i].symbol}</div>
                      <div class="namecrypt">${jsonData[i].name}</div>
                      <div class="">Current Price: ${Number(
                        jsonData[i].market_data.current_price.usd
                      ).toLocaleString(undefined, {
                        style: "currency",
                        currency: "USD",
                      })}</div>
                  </div>
                  <label class="switch swinput">
                      <input onChange="switchToggle(event)" id="i${
                        jsonData[i].symbol
                      }" data-symbol="${jsonData[i].symbol}" data-name="${
      jsonData[i].name
    }" type="checkbox">
                      <span class="slider round"></span>
                  </label>
              </div>
              
              <div><div class="moreinfo" onclick="moreInfo(event)" id="${
                jsonData[i].id
              }">
                  <div class="triangle"></div>Click for more details</div></div>
          </div>
          `);
  }
}

//This function is intended to display additional information about the currency,
//when the clicks on the area of the additional information a copy of the information
//about that currency is sent for local storage. If 2 minutes have not passed (120000 milliseconds)
// new request to api will not send

function moreInfo(e) {
  let coinDescription = document.getElementsByClassName("coin-description");
  coinDescription[coinInfo].parentElement.parentElement.classList.remove(
    "coin-search"
  );
  if (e.target.className === "moreinfo") {
    e.target.innerHTML = `<div class="triangle"></div>Loading data...`;
    e.target.onclick = null;
    let localStorageCoin = JSON.parse(localStorage.getItem(e.target.id));

    let newAjaxCall = true;
    if (localStorageCoin !== null) {
      if (localStorageCoin.date + 120000 >= new Date().getTime()) {
        let currentObj = localStorageCoin;
        newAjaxCall = false;
        e.target.parentElement.innerHTML = `<div class="lessinfo" onclick="moreInfo(event)" id="${
          e.target.id
        }">
          <div class='trianglebas'></div>
          <div class="infowp24">
          <div >
          ${currentObj.eur.toLocaleString(undefined, {
            style: "currency",
            currency: "EUR",
          })}<br>
          ${currentObj.usd.toLocaleString(undefined, {
            style: "currency",
            currency: "USD",
          })}<br>
          ${currentObj.ils.toLocaleString(undefined, {
            style: "currency",
            currency: "ILS",
          })} 
      </div>
              <div class="${
                currentObj.perc24 >= 0 ? "p24p" : "p24m"
              }" title="variation 24h">
                  ${
                    currentObj.perc24 >= 0
                      ? "↑ " + currentObj.perc24
                      : "↓ " + currentObj.perc24
                  }%
              </div>
          </div>
      </div>`;
      }
    }

    if (newAjaxCall) {
      $.ajax({
        url: `https://api.coingecko.com/api/v3/coins/${e.target.id}`,
        success: (coins) => cryptoCurrentData(coins),
        error: (err) => console.error(err),
      });
    }

    function cryptoCurrentData(jsonData) {
      let jsonObject = jsonData;

      let currentObj = {
        date: new Date().getTime(),
        eur: jsonObject.market_data.current_price.eur,
        usd: jsonObject.market_data.current_price.usd,
        ils: jsonObject.market_data.current_price.ils,
        perc24: jsonObject.market_data.price_change_percentage_24h.toFixed(2),
      };

      e.target.parentElement.innerHTML = `<div class="lessinfo" onclick="moreInfo(event)" id="${
        e.target.id
      }">
                  <div class='trianglebas'></div>
                  <div class="infowp24">
                      <div >
                          ${currentObj.eur.toLocaleString(undefined, {
                            style: "currency",
                            currency: "EUR",
                          })}<br>
                          ${currentObj.usd.toLocaleString(undefined, {
                            style: "currency",
                            currency: "USD",
                          })}<br>
                          ${currentObj.ils.toLocaleString(undefined, {
                            style: "currency",
                            currency: "ILS",
                          })} 
                      </div>
                      <div class="${
                        currentObj.perc24 >= 0 ? "p24p" : "p24m"
                      }" title="variation 24h">
                          ${
                            currentObj.perc24 >= 0
                              ? "↑ " + currentObj.perc24
                              : "↓ " + currentObj.perc24
                          }%
                      </div>
                  </div>
              </div>`;

      let savelocalstorage = JSON.stringify(currentObj);
      localStorage.setItem(e.target.id, savelocalstorage);
    }

    //Since we do not know where the user will click we should have tried to catch the
    //correct div that would close the view. Using the closest() method helps to find the closest div and replace
    // the lessinfo class from it and restart it to the initial design
  } else if (e.target.closest(".lessinfo").className === "lessinfo") {
    e.target.closest(
      ".lessinfo"
    ).parentElement.innerHTML = `<div class="moreinfo" onclick="moreInfo(event)" id="${
      e.target.closest(".lessinfo").id
    }">
              <div class="triangle"></div>Click for more details</div>`;
  }
}
