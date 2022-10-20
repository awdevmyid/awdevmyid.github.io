//The created array contains information about five currencies, after we have all the information about the
//currencies we send a request to the api of cryptocompare and display the data using canvasjs

function liveReportsFunc() {
  let curstr = "";
  for (i = 0; i < checkedm.length; i++) {
    if (i > 0) {
      curstr += ",";
    }
    curstr += checkedm[i][0].slice(1);
  }

  updateData();

  function updateData() {
    $.ajax({
      url: `https://min-api.cryptocompare.com/data/pricemulti?fsyms=${curstr.toUpperCase()}&tsyms=USD`,
      success: (coins) => addData(coins),
      error: (err) =>
        alertError(
          `<h2>SORRY, problem with the live reports</h2><h2><strong>${err}</strong></h2>`
        ),
    });
  }

  function addData(cryptocompareObj) {
    let jsonObj = cryptocompareObj;

    if (jsonObj.Response === "Error") {
      alertError(
        `<h2>Sorry, we have a problem with live reports</h2><h2><strong>Error</strong></h2>`
      );
      return;
    }

    let arrobj = Object.values(jsonObj);

    if (firstenter) {
      let elt = document.createElement("div");
      elt.id = "divLiveReportsPage";
      elt.innerHTML =
        '<h1 id="live">Live Reports</h1><div><button id="clear-selection-live" onClick="clearSelection()">Clear Selection</button></div></div><div id="chartContainer" style="height: 400px; width: 100%;">';
      document.getElementById("root").appendChild(elt);

      let arrprop = Object.getOwnPropertyNames(jsonObj);
      dataPoints = [arrprop.length];

      let strnotfound = "";
      if (arrprop.length != checkedm.length) {
        let mnotfound = [];
        let positionmnf = 0;
        for (i = 0; i < checkedm.length; i++) {
          if (
            !arrprop[i - positionmnf] ||
            checkedm[i][0].slice(1).toUpperCase() !==
              arrprop[i - positionmnf].toUpperCase()
          ) {
            mnotfound.push(checkedm[i][0].slice(1).toUpperCase());
            positionmnf++;
          }
        }
        strnotfound = `[${mnotfound.join(", ").toUpperCase()} Not Found]`;
      }

      let options = {
        exportEnabled: true,
        animationEnabled: true,
        title: {
          text: `${arrprop.join(", ").toUpperCase()} TO USD($) ${strnotfound}`,
        },
        subtitles: [
          {
            text: "Live reports from cryptocompare API",
          },
        ],
        axisX: {
          title: "",
        },
        axisY: {
          titleFontColor: "#4F81BC",
          lineColor: "#4F81BC",
          labelFontColor: "#4F81BC",
          tickColor: "#4F81BC",
          includeZero: false,
        },
        toolTip: {
          shared: true,
        },
        legend: {
          cursor: "pointer",
          itemclick: toggleDataSeries,
        },
        data: [],
      };

      $("#chartContainer").CanvasJSChart(options);

      for (i = 0; i < arrobj.length; i++) {
        dataPoints[i] = [];
        options.data.push({
          type: "spline",
          name: arrprop[i],
          showInLegend: true,

          dataPoints: dataPoints[i],
        });
      }
      firstenter = false;
    }

    for (i = 0; i < arrobj.length; i++) {
      dataPoints[i].push({ x: new Date(), y: arrobj[i].USD });
    }

    //If the user cancels his choice, we should make sure that the function of the render
    //of canvasjs will not continue to try to create content, so there is validation that the container
    //is not undefined

    if ($("#chartContainer").CanvasJSChart() !== undefined) {
      $("#chartContainer").CanvasJSChart().render();
      clearint = setTimeout(updateData, 2000);
    }
  }

  function toggleDataSeries(e) {
    if (typeof e.dataSeries.visible === "undefined" || e.dataSeries.visible) {
      e.dataSeries.visible = false;
    } else {
      e.dataSeries.visible = true;
    }
    e.chart.render();
  }
}

function stopSetT() {
  if (!clearint) {
    return;
  }
  clearInterval(clearint);
  firstenter = true;
}

//A function I built because I saw that it was not easy to find the coins the user selected and remove the
//selection from them. This function cancels all the user's selection and returns him to the home screen

function clearSelection() {
  let switchButtons = document.querySelectorAll('input[type="checkbox"]');
  switchButtons.forEach((button) => (button.checked = false));
  $("#divHomePage").show();
  $("#divLiveReportsPage").remove();
  $("#divAboutPage").remove();
  changeBtnColor("#Home");
  checkedm.length = 0;
  return;
}
