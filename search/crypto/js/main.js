let coinInfo = 0;
let cancelSearch = false;
let checkedm = [];
let clearint;
let dataPoints;
let firstenter = true;

function Load() {
  $.ajax({
    url: `https://api.coingecko.com/api/v3/coins/`,
    success: (coins) => creatCryptoCard(coins),
    error: (err) => console.error(err),
  });
}

window.onload = Load;
window.onunload = function () {
  localStorage.clear();
};

// Adding dynamic content while resizing a window, I used ascii characters to instead icons

function mediaQueryFuncion(x) {
  if (!x.matches) {
    $("#Home").text("Home");
    $("#LiveReports").text("Live Reports");
    $("#About").text("About");
    $("header h1").show();
  } else {
    $("#Home").text("⌂");
    $("#LiveReports").text("🗠");
    $("#About").text("🛈");
    $("header h1").hide();
  }
}

var x = window.matchMedia("(max-width: 791px)");
mediaQueryFuncion(x);
x.addEventListener("change", mediaQueryFuncion);

function changeBtnColor(idbtn) {
  $("nav button").removeClass("btn-on");
  $(idbtn).addClass("btn-on");
  $(idbtn).blur();
  $(idbtn).focus();
}

//A general function that creates an alert window with content according to user actions

function alertError(message) {
  let element = document.createElement("div");
  element.id = "alert-box";
  document.body.appendChild(element, document.body);
  element.innerHTML = `<div id="divalert">${message}
        <div id="btnsalert" class="btnalerterror"><button id="cancel" class="btn-danger" onclick="cancelAlert()">Close</button></div>
    </div>`;
  document.getElementById("cancel").focus();
}

//A function responsible for checking that there are only five coins in the panel
//if the user selects more than five he must remove one.

function switchToggle(e) {
  if (e.target.checked) {
    if (checkedm.length < 5) {
      checkedm.push([
        e.target.id,
        `${e.target.dataset.name} (${e.target.dataset.symbol})`,
      ]);
    } else {
      e.target.checked = false;
      fiveCoinsModal([
        e.target.id,
        `${e.target.dataset.name} (${e.target.dataset.symbol})`,
      ]);
    }
  } else {
    for (i = 0; i < checkedm.length; i++) {
      if (checkedm[i][0] === e.target.id) {
        checkedm.splice(i, 1);
        break;
      }
    }
  }
}

//A function that creates a modal for selecting the coins to display if more than five coins are selected.

function fiveCoinsModal(currence) {
  numselect = 5;
  var element = document.createElement("div");
  element.id = "alert-box";
  document.body.appendChild(element, document.body);
  let fiveCoinHTML = "";
  for (let i = 0; i < checkedm.length; i++) {
    fiveCoinHTML += `<div class="divswi">
        <label class="switch">
            <input type="checkbox" class="swinputalert" onChange="disabledbtn(event)" checked>
            <span class="slider round"></span>
        </label>
        <div><strong>${checkedm[i][1]}</strong></div></div>`;
  }
  element.innerHTML = `<div id="divalert">
        <h4>We can display only 5 Cryptocurrencies at a time</h4>
        <h6>Choose on coin to replace with <strong>${currence[1]}</strong></h6>
        <div id="modal-coins">${fiveCoinHTML}</div>
        <div id="btnsalert">
            <button id="replace" onclick="replaceAlert('${currence[0]}','${currence[1]}')" disabled>Confirm</button>
            <button id="cancel" class="btn-danger" onclick="cancelAlert()">Close</button>
        </div>
    </div>`;
}

//A function that is responsible for preventing the on-screen button from
// being active until a selection is made

function disabledbtn(e) {
  e.target.checked ? numselect++ : numselect--;
  if (numselect === 5) {
    document.getElementById("replace").disabled = true;
  } else {
    document.getElementById("replace").disabled = false;
  }
}

//A function that pushes the user's choice into the array so that the coins are displayed in the life reports

function replaceAlert(currence0, currence1) {
  if (numselect >= 5) {
    return;
  }
  newcheckedm = [];
  let swinputalert = document.querySelectorAll(".swinputalert");

  for (i = 0; i < 5; i++) {
    if (swinputalert[i].checked) {
      newcheckedm.push(checkedm[i]);
    } else {
      document.querySelector(".swinput #" + checkedm[i][0]).checked = false;
    }
  }
  checkedm = newcheckedm;
  checkedm.push([currence0, currence1]);
  document.getElementById(currence0).checked = true;
  cancelAlert();
}

//A function that disables the alert window

function cancelAlert() {
  document.body.removeChild(document.getElementById("alert-box"));
  if (cancelSearch) {
    $("#search").focus();
    cancelSearch = false;
  }
}
