//These functions are designed to give a user experience of both a mouse click
// on a search icon and a press of the Enter key

$("#search").on("keypress", function (e) {
  if (e.key === "Enter") {
    searchCrypto();
  }
});

$("#formsearch button").on("click", searchCrypto);

//This function is designed to find the relevant currency and bring it to view
//in addition its color also changes so that it is easy to spot

function searchCrypto() {
  $("#search").css("backgroundColor", "white");
  stopSetT();
  $("#divLiveReportsPage").remove();
  $("#divAboutPage").remove();

  changeBtnColor("#Home");
  HomePage();
  let target = $("#search").val().toLowerCase();

  let coinDescription = document.getElementsByClassName("coin-description");

  coinDescription[coinInfo].parentElement.parentElement.classList.remove(
    "coin-search"
  );
  let coinNotFound = true;
  for (i = 0; i < coinDescription.length; i++) {
    if (
      target === coinDescription[i].children[0].innerText.toLowerCase() ||
      target === coinDescription[i].children[1].innerText.toLowerCase()
    ) {
      window.scrollTo(
        0,
        coinDescription[i].parentElement.parentElement.offsetTop - 220
      );

      coinDescription[i].parentElement.parentElement.classList.add(
        "coin-search"
      );

      coinInfo = i;
      coinNotFound = false;

      break;
    }
  }

  //validation for empty string

  if (target === "") {
    alert("Did you forget to to write someting?");
    $("#search").focus();
    $("#search").css("backgroundColor", "pink");
    return;
  }

  //validation unknown coin

  if (coinNotFound) {
    alertError(`<h3>"${target}" is an excellent name for a Cryptocurrency, but it does not exist yet. 
      (or maybe it is just a misspelling). Try again.</h3>`);

    cancelSearch = true;
  }
  $("#formsearch button").focus();
  $("#search").val("");
}
