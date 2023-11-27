//The functions in this file are intended to create dynamic content of the pages when the user selects one of the relevant buttons

$("nav button").click(SetPage);

function SetPage(event) {
  const btn = event.target.id;
  if (btn === "LiveReports" && checkedm.length === 0) {
    alertError("<h2>Please select at least one coin</h2>");

    $("#divHomePage").show();
    $("#divLiveReportsPage").remove();
    $("#divAboutPage").remove();
    changeBtnColor("#Home");
    return;
  }
  actions = { HomePage, LiveReportsPage, AboutPage };

  stopSetT();
  $("#divLiveReportsPage").remove();
  $("#divAboutPage").remove();

  actions[btn + "Page"]();

  changeBtnColor("#" + btn);

  window.scrollTo(0, 0);
}

function HomePage() {
  $("#divHomePage").show();
}

function LiveReportsPage() {
  $("#divHomePage").hide();
  liveReportsFunc();
}

function AboutPage() {
  $("#divHomePage").hide();
  var element = document.createElement("div");
  element.id = "divAboutPage";
  element.innerHTML = `<h1>About the project</h1>
    <div id="imgandauthor">
      
                <div class="imgiglobal" style="background-image:url(imgs/profile.jpg)"></div>
            </div>
        </div>

  
        <div id="theauthor">
            <div class="firstinfoaut">
                <div class="infoauthor"><div class="winfoauthor"><i class="fa fa-user" aria-hidden="true"></i></div><div class="xinfoauthor">AWDEV</div></div>
                <div class="infoauthor"><div class="winfoauthor"><i class="fa fa-map-marker" aria-hidden="true"></i></div><div class="xinfoauthor">INDONESIA</div></div>
            </div>
            <div class="secondinfoaut">
                <div class="infoauthor"><div class="winfoauthor"><i class="fa fa-btc" aria-hidden="true"></i></div><div class="xinfoauthor"><pre>0xFDd2b5bA05C21B1fD387F53ffC001acA512d6877</pre></div></div>
                <div class="infoauthor"><div class="winfoauthor"><i class="fa fa-envelope" aria-hidden="true"></i></div><div class="xinfoauthor">cs@awdev.my.id</div></div>
            </div>
        </div>
    </div>
    <div id="aboutproject">
        <div id="titleabpr">JQuery-Ajax API Project</div><br>
        <div id="lgsused">
            <div>Technology used in the project</div>
            <div class="about-info">HTML</div>
            <div class="about-info">CSS3</div>
            <div class="about-info">JavaScript</div>
            <div class="about-info">JQuery&Ajax</div>
         
        </div><br>

        <div id="lgsused">
            <div>Libraries used in the project</div>
       
            <div class="about-info">Bootstrap</div>
            <div class="about-info">Font Awsome</div>
            <div class="about-info">Pace.js</div>
            <div class="about-info">Canvas.js</div>
            
        </div><br>
        <div class="titleapi">CoinGecko API</div>
        <div>CoinGecko provides data for live pricing, trading volume, tickers, exchanges, historical data, coin info & images, developer & community stats, events, global markets, and CoinGecko Beam coins & exchanges status updates directly.</div><br>
        <div class="titleapi">CryptoCompare API</div>
        <div>CryptoCompare is the independent global cryptocurrency market data provider, giving institutional and retail investors access to real-time, high-quality, reliable market and pricing data. A central authority for clear and concise information, CryptoCompare offers unrivalled breadth, scope and depth of data, bridging the gap between the crypto asset and traditional financial markets.</div><br>
<div>


       <p>
        <div id="imgandauthor">
        
        <div class="imgiglobal" style="background-image:url(https://www.awdev.my.id/favicon.png)"></div>
        </p>
        <p></a></p>
        <h3 align="center">AWDEV CORPORATION</h3>
        
        <p align="center">
        AWDEV FREE OPPEN SOURCE GENERAL TO PROJECTS DEVOLOPER , DESIGNER , AND PROGRAMER  <br/>
        Note This Project Is Still @AWDEV
        <br/>
        <br/>
        <a href="https://www.awdev.my.id"><strong>View Demo »</strong></a>
        <br/>
        <br/>
        <a href="https://www.awdev.my.id/GitHub-Finder/index.html">Github Finder</a>
        .
        <a href="https://www.awdev.my.id/home.html ">Page Projects</a>
        .
        <a href="https://www.awdev.my.id/android/vc/index.html">Visual Code</a>
        .
        <a href="https://www.awdev.my.id/youtube/downloader.html">Youtube Downloader</a>
        .
        <a href="https://www.awdev.my.id/thema">Templates</a><br>  </p>
        </p>
        
        
        
        <h2 id="table-of-contents">Table Of Contents</h2>
        <ul>
        <li><a href="https://www.awdev.my.id">HOME PAGE</a></li>
        <li><a href="https://www.awdev.my.id/home.html">The Project</a></li>
        <li><a href="https://www.awdev.my.id/GitHub-Finder/index.html">Github Finder</a></li>
        <li><a href="https://www.awdev.my.id/android">Android</a><ul>
        <li><a href="https://www.awdev.my.id/android/auto">AUTO</a></li>
        <li><a href="https://www.awdev.my.id/android/auto/convert.html">Converter</a></li>
        <li><a href="https://www.awdev.my.id/android/auto/rools.html">Rools</a></li>
        <li><a href="https://www.awdev.my.id/android/kodepost">Kode Post</a></li>
        <li><a href="https://www.awdev.my.id/android/screen/index.html">Screenshot</a></li>
        <li><a href="https://www.awdev.my.id/android/vc/index.html">Visual Code</a></li>
        <li><a href="https://www.awdev.my.id/android/character.html">Character</a></li>
        <li><a href="https://www.awdev.my.id/android/index.html">Android Asset</a></li>
        </ul>
        </li>
        <li><a href="https://www.awdev.my.id/thema">Thema</a><ul>
        <li><a href="https://www.awdev.my.id/thema/amp/v1.html">AMP 1 ⚡</a></li>
        <li><a href="https://www.awdev.my.id/thema/amp/v2.html">AMP 2 ⚡</a></li>
        <li><a href="https://www.awdev.my.id/thema/arsha/index.html">ARSHA</a></li>
        <li><a href="https://www.awdev.my.id/thema/atom/index.html">ATOM</a></li>
        <li><a href="https://www.awdev.my.id/thema/landing/index.html">LANDING</a></li>
        <li><a href="https://www.awdev.my.id/thema/mobile/index.html">MOBILE</a></li>
        <li><a href="https://www.awdev.my.id/thema/mobile/amp.html">⚡ AMP MOBILE</a></li>
        <li><a href="https://www.awdev.my.id/thema/pages/dashboard.html">ADMIN DASHBOARD</a></li>
        <li><a href="https://www.awdev.my.id/thema/pages/sign-in.html">SIGN IN</a></li>
        <li><a href="https://www.awdev.my.id/thema/pages/sign-up.html">SIGN UP</a></li>
        <li><a href="https://www.awdev.my.id/thema/pages/virtual-reality.html">VIRTUAL REALITY</a></li>
        <li><a href="https://www.awdev.my.id/thema/pages/billing.html">BILLING</a></li>
        <li><a href="https://www.awdev.my.id/thema/rtl.html">RTL</a></li>
        <li><a href="https://www.awdev.my.id/thema/index.html">Index</a></li>
        </ul>
        </li>
        <li><a href="https://www.awdev.my.id/file">FILE</a><ul>
        <li><a href="https://www.awdev.my.id/file/index.html">NFT AWDEV COLLECTION</a></li>
        </ul>
        </li>
        <li><a href="https://www.awdev.my.id/ar/">AR ( Augmented Reality )</a><ul>
        <li><a href="https://www.awdev.my.id/ar/index.html">WEB AR VIEWVER</a></li>
        <li><a href="https://www.awdev.my.id/ar/nft.html">WEB AR NFT</a></li>
        </ul>
        </li>
        <li><a href="https://www.awdev.my.id/vr/">VR ( Virtual Reality )</a><ul>
        <li><a href="https://www.awdev.my.id/vr/examples/">excample</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/littleplanet_image.html">littleplanet image</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panomoment_linking.html">panomoment linking</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_basic.html">panorama basic</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_camera.html">panorama camera</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_cube.html">panorama cube</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_googlestreetview.html">panorama googlestreetview</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_image.html">panorama image</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_infospot.html">panorama infospot</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_infospot_focus.html">panorama infospot focus</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_interactive.html">panorama interactive</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_linking.html">panorama linking</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_loading_progress.html">panorama loading progress</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_memoryleak_test.html">panorama memoryleak test</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_reticle.html">panorama reticle</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_simple_gallery.html">panorama simple gallery</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_stereo_image.html">panorama stereo image</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_stereo_video.html">panorama stereo vidio</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_storytelling.html">panorama storytelling</a></li>
        <li><a href="https://www.awdev.my.id/vr/examples/panorama_video.html">panorama video</a></li>
        </ul>
        </li>
        <li><a href="https://qr.awdev.my.id">QR ( Quick Response )</a><ul>
        <li><a href="https://qr.awdev.my.id/v3">View Web QR</a></li>
        </ul>
        
        
        <!-- Adsense -->
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5295583488737876"
        crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
        style="display:block"
        data-ad-format="autorelaxed"
        data-ad-client="ca-pub-5295583488737876"
        data-ad-slot="1958340468"></ins>
        <script>
        (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
        
        <!-- And Adsense -->
        </div>
        <div
  class="DePayButton"
  title="Pay"
  integration="882ccd43-679f-4311-859c-6f2752abea93"
  blockchains='["ethereum"]'
></div>
<script src="https://integrate.depay.com/buttons/v12.js"></script>
<noscript><a href="https://www.awdev.my.id">Web3 Payments</a> are only supported with JavaScript enabled.</noscript>
<script>DePayButtons.init({document: document});</script>
        
       </center>
    </div>
    `;
  document.getElementById("root").appendChild(element);
}
