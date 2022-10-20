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

    <ul>
          <li><a href="https://www.awdev.my.id/thema/"><i class="fas fa-qrcode"></i>Dashboard</a></li>
          <li><a href="#"><i class="fas fa-link"></i>Shortcuts</a></li>
          <li><a href="https://www.awdev.eu.org"><i class="fas fa-stream"></i>Overview</a></li>
          <li><a href="https://wahyu9kdl.github.io/islami"><i class="fas fa-calendar-week"></i>APP</a></li>
          <li><a href="#"><i class="fas fa-question-circle"></i>About</a></li>
          <li><a href="https://devoloper.awdev.eu.org"><i class="fas fa-sliders-h"></i>Services</a></li>
          <li><a href="#"><i class="fas fa-phone-volume"></i>Contact</a></li>
          <li><a href="#"><i class="fas fa-comments"></i>Feedback</a></li>
        </ul>
        <div class="media_icons">
          <a href="https://web.facebook.com/Awfanspage"><i class="fab fa-facebook-f"></i></a>
          <a href="https://twitter.com/Awfanspage"><i class="fab fa-twitter"></i></a>
          <a href="https://m.awdev.my.id"><i class="fab fa-instagram"></i></a>
          <a href="https://youtube.com/channel/UCyp-Fn_0Ek4_aXIFbcWaq0w"><i class="fab fa-youtube"></i></a>
        </div>
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
        </li>
        <li><a href="https://youtube.com/channel/UCyp-Fn_0Ek4_aXIFbcWaq0w">YOUTUBE</a><ul>
        <li><a href="https://youtube.com/channel/UCyp-Fn_0Ek4_aXIFbcWaq0w">SUBCRIBE</a></li>
        <li><a href="https://www.awdev.my.id/youtube/downloader.html">YOUTUBE DOWNLOADER</a></li>
        </ul>
        </li>
        <li><a href="https://www.awdev.my.id/faq.html">FAQ</a></li>
        <li><a href="https://www.awdev.my.id/privasy.html">PRIVASY</a></li>
        <li><a href="https://www.awdev.my.id/404.html">404</a></li>
        <li><a href="https://www.awdev.my.id/app/htmleditor-2-1.apk">APP</a><ul>
        <li><a href="app/awdev-2-2.aab.zip">awdev-2-2.aab.zip</a></li>
        <li><a href="app/awdev-2-2.apk">awdev-2-2.apk</a></li>
        <li><a href="app/htmleditor-2-1.aab.zip">htmleditor-2-1.aab.zip</a></li>
        <li><a href="app/htmleditor-2-1.apk">htmleditor-2-1.apk</a></li>
        </ul>
        </li>
        <li><a href="LICENSE">License</a></li>
        <li><a href="SECURITY.md">SECURITY</a></li>
        <li><a href="#authors">Authors</a></li>
        <li><a href="#acknowledgements">Acknowledgements</a></li>
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
        
        <center>
        <h3 align="left"><center><h1><span class="multicolortext" >Connect with me:</span></h3>
        <p align="left">
        <a href="https://codepen.io/san3" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/codepen.svg" alt="san3" height="30" width="40" /></a>
        <a href="https://dev.to/wahyu9kdl" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/devto.svg" alt="wahyu9kdl" height="30" width="40" /></a>
        <a href="https://twitter.com/Awfanspage" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="awfanspage" height="30" width="40" /></a>
        <a href="https://www.linkedin.com/in/ahmad-wahyudi-41b6841b6" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="https://www.linkedin.com/in/ahmad-wahyudi-41b6841b6" height="30" width="40" /></a>
        <a href="https://fb.com/awgroupchannel" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="awgroupchannel" height="30" width="40" /></a>
        <a href="https://instagram.com/awfanspage" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="awfanspage" height="30" width="40" /></a>
        <a href=" https://dribbble.com/wahyu9kdl/shots " target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/dribbble.svg" alt="wahyu9kdl" height="30" width="40" /></a>
        <a href="https://wahyu9kdl.medium.com" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/medium.svg" alt="wahyu9kdl" height="30" width="40" /></a>
        <a href="https://m.youtube.com/channel/UC7CRa3nkxakAZx_aRsMwRyA/playlists" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg" alt="aw youtube channel" height="30" width="40" /></a>
        <a href="https://open.spotify.com/show/4UoPUn3e0VhJ6MGOwdsrHV" target="blank"> <img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/rss.svg" alt="http://feedproxy.google.com/~r/blogspot/ghpgr/~3/vyr1fhc7dbi/informasi-cara-mendapatkan-ribuan.html" height="30" width="40" /></a>
        <a href=" https://wahyu9kdl.github.io/wahyu9kdl" ><img align="center" src=" https://camo.githubusercontent.com/5b09aa408358eda7cba977c95dccaf65b070ed679c9be064297a11161058d1f2/68747470733a2f2f312e62702e626c6f6773706f742e636f6d2f2d735749774852616b54744d2f594a7068586a65796f46492f41414141414141414339632f37747230382d4d665f387379524457346c4c30514e7042564431773734772d6841434c63424741735948512f733630302f6c6f676f355f31315f31353330322e706e67 " height="30" width="40" /></a>		
        <a href="https://www.alhikmah.my.id" ><img align="center" src="https://raw.githubusercontent.com/wahyu9kdl/wahyu9kdl/main/logo.png" height="30" width="40" /></a>
        </p>
       </center>
    </div>
    `;
  document.getElementById("root").appendChild(element);
}
