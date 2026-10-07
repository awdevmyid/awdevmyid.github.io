#!/usr/bin/env python3
"""
AWDEV tools engine - membangun tools yang BENAR-BENAR berfungsi (JavaScript di browser).

Jalankan SETELAH generator.py (atau sendirian):
    python tools.py                 # semua tools
    python tools.py --only islamic  # islamic | general | converter
    python tools.py --list          # hanya hitung & tampilkan jumlah

Output:
  /islamic-tools/<slug>.html   + hub (worship, trackers, calculators, knowledge, finders)
  /tools/<slug>.html           utilitas umum
  /converter/<a>-ke-<b>.html   ratusan konverter satuan (dibangkitkan dari tabel)
  /assets/tools.css, /sitemap-tools.xml (otomatis ditambahkan ke robots.txt)

Menambah tool = tambah satu entri tool(...) di GENERAL / ISLAMIC, atau satu satuan di CONV.
"""
import argparse, json
from datetime import date
import generator as g

e = g.e
OUT = g.OUT

TOOL_CSS = """
.tool label{display:block;font-weight:600;font-size:.85rem;margin-top:8px}
.tool input,.tool select,.tool textarea{width:100%;padding:10px;margin:6px 0;border:0;border-radius:8px;background:var(--bg);box-shadow:inset 4px 4px 8px var(--dark),inset -4px -4px 8px var(--light);outline:0;font-size:1rem}
.tool input[type=checkbox]{width:auto}
.tool .row{display:flex;gap:10px;flex-wrap:wrap}.tool .row>*{flex:1;min-width:140px}
.tool .out{margin-top:12px;padding:14px;border-radius:12px;box-shadow:inset 4px 4px 8px var(--dark),inset -4px -4px 8px var(--light);word-break:break-word}
.tool .big{font-size:1.8rem;font-weight:700}
.tool table{font-size:.95rem}
.tool .btn{margin:4px 4px 4px 0}
.compass{width:200px;height:200px;border-radius:50%;margin:15px auto;box-shadow:8px 8px 16px var(--dark),-8px -8px 16px var(--light);display:flex;align-items:center;justify-content:center}
.needle{font-size:4rem;transition:transform .3s}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.cal div{padding:6px 2px;text-align:center;border-radius:8px;font-size:.9rem}
.cal .today{background:#ff3366;color:#fff}.cal small{display:block;font-size:.65rem;opacity:.7}
.ar{font-size:1.6rem;direction:rtl;text-align:right;line-height:2.2;font-family:'Amiri','Scheherazade New',serif}
.ayah{padding:10px 0;border-bottom:1px solid #ccd5e3}
.tag{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.75rem;color:#fff}
.tag.haram{background:#d32f2f}.tag.syubhat{background:#f57c00}
"""

COMMON = r"""
var $=function(i){return document.getElementById(i)};
function geo(ok){if(!navigator.geolocation){alert('Geolokasi tidak didukung browser ini');return}
navigator.geolocation.getCurrentPosition(function(p){ok(p.coords.latitude,p.coords.longitude)},
function(){alert('Lokasi ditolak / tidak tersedia. Isi koordinat manual.')},{enableHighAccuracy:true,timeout:15000});}
function rad(d){return d*Math.PI/180}
function hav(a,b,c,d){var R=6371,x=rad(c-a),y=rad(d-b),z=Math.sin(x/2)*Math.sin(x/2)+Math.cos(rad(a))*Math.cos(rad(c))*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(z))}
function idr(n){return new Intl.NumberFormat('id-ID',{style:'currency',currency:'IDR',maximumFractionDigits:0}).format(n)}
"""


def tool(slug, title, desc, body, js, steps, faq, groups=(), note="", scripts="", ext=None):
    return dict(slug=slug, title=title, desc=desc, body=body, js=js, steps=steps, faq=faq,
                groups=list(groups), note=note, scripts=scripts, ext=ext or [])


# =============================================================== ISLAMIC TOOLS
ISLAMIC = []

ISLAMIC.append(tool(
    "qibla-direction", "Arah Kiblat (Qibla Direction) Akurat dari Lokasi Anda",
    "Hitung arah kiblat dalam derajat dari utara sejati menggunakan rumus great-circle ke Ka'bah, lengkap dengan kompas ponsel.",
    r"""<div class="row"><button class="btn" id="loc">📍 Pakai lokasi saya</button><button class="btn" id="comp">🧭 Aktifkan kompas ponsel</button></div>
<div class="row"><div><label>Lintang</label><input id="lat" type="number" step="any" placeholder="-6.9667"></div>
<div><label>Bujur</label><input id="lng" type="number" step="any" placeholder="110.4167"></div></div>
<button class="btn" id="go">Hitung</button>
<div class="out" id="out">Isi koordinat atau gunakan lokasi Anda.</div>
<div class="compass"><div class="needle" id="needle">⬆</div></div><p id="hint" class="meta"></p>""",
    r"""
var KA={lat:21.4225,lng:39.8262},q=null;
function bearing(la,ln){var p1=rad(la),p2=rad(KA.lat),dl=rad(KA.lng-ln);
 var y=Math.sin(dl),x=Math.cos(p1)*Math.tan(p2)-Math.sin(p1)*Math.cos(dl);return(Math.atan2(y,x)*180/Math.PI+360)%360}
function show(la,ln){q=bearing(la,ln);$('lat').value=la.toFixed(5);$('lng').value=ln.toFixed(5);
 $('out').innerHTML='Arah kiblat: <span class="big">'+q.toFixed(2)+'°</span> dari utara sejati (searah jarum jam).<br>Jarak ke Ka\'bah ± '+Math.round(hav(la,ln,KA.lat,KA.lng)).toLocaleString('id-ID')+' km.';
 $('needle').style.transform='rotate('+q+'deg)'}
$('loc').onclick=function(){geo(show)};
$('go').onclick=function(){var a=parseFloat($('lat').value),b=parseFloat($('lng').value);if(isNaN(a)||isNaN(b))return alert('Isi lintang & bujur');show(a,b)};
function ori(ev){var h=ev.webkitCompassHeading!=null?ev.webkitCompassHeading:(ev.alpha!=null?360-ev.alpha:null);if(h==null||q==null)return;
 $('needle').style.transform='rotate('+(q-h)+'deg)';$('hint').textContent='Kompas aktif: putar ponsel hingga panah menunjuk ke atas. Jauhkan dari logam/magnet.'}
$('comp').onclick=function(){if(q==null)return alert('Hitung arah kiblat dulu');
 if(window.DeviceOrientationEvent&&DeviceOrientationEvent.requestPermission){DeviceOrientationEvent.requestPermission().then(function(s){if(s==='granted')addEventListener('deviceorientation',ori,true)})}
 else{addEventListener('deviceorientationabsolute',ori,true);addEventListener('deviceorientation',ori,true)}};
""",
    ["Klik 'Pakai lokasi saya' atau isi lintang dan bujur.", "Baca sudut kiblat dari utara sejati.", "Aktifkan kompas ponsel lalu putar badan sampai panah menghadap atas."],
    [("Bagaimana arah kiblat dihitung?", "Dengan rumus bearing great-circle dari koordinat Anda ke Ka'bah (21.4225°N, 39.8262°E)."),
     ("Mengapa kompas ponsel kurang akurat?", "Sensor magnetik terganggu logam dan perangkat elektronik. Kalibrasi dengan gerakan angka 8 dan bandingkan dengan sudut hitungan.")],
    groups=["worship", "finders"], note="Kompas membutuhkan HTTPS dan sensor ponsel. Sudut hitungan adalah acuan utama."))

ISLAMIC.append(tool(
    "prayer-times", "Jadwal Waktu Salat Hari Ini (Subuh, Zuhur, Asar, Magrib, Isya)",
    "Hitung jadwal salat berdasarkan koordinat dan metode (Kemenag RI, MWL, Mesir, Umm al-Qura, ISNA) langsung di browser tanpa server.",
    r"""<div class="row"><div><label>Kota</label><select id="city"></select></div><div><label>Tanggal</label><input type="date" id="dt"></div></div>
<div class="row"><div><label>Lintang</label><input id="lat" type="number" step="any"></div><div><label>Bujur</label><input id="lng" type="number" step="any"></div><div><label>Zona waktu (UTC+)</label><input id="tz" type="number" step="0.5"></div></div>
<div class="row"><div><label>Metode</label><select id="meth"><option value="kemenag">Kemenag RI (Subuh 20°, Isya 18°)</option><option value="mwl">Muslim World League (18°/17°)</option><option value="egypt">Egyptian (19.5°/17.5°)</option><option value="umm">Umm al-Qura (18.5°, Isya +90 mnt)</option><option value="isna">ISNA (15°/15°)</option></select></div>
<div><label>Mazhab Asar</label><select id="asr"><option value="1">Syafi'i / Maliki / Hanbali</option><option value="2">Hanafi</option></select></div>
<div><label>Ihtiyat (menit)</label><input id="ih" type="number" value="2"></div></div>
<button class="btn" id="loc">📍 Lokasi saya</button>
<div class="out" id="out"></div><div class="out" id="next"></div>""",
    r"""
var CITIES={"Jakarta":[-6.2088,106.8456,7],"Semarang":[-6.9667,110.4167,7],"Surabaya":[-7.2575,112.7521,7],"Bandung":[-6.9175,107.6191,7],"Yogyakarta":[-7.7956,110.3695,7],"Medan":[3.5952,98.6722,7],"Makassar":[-5.1477,119.4327,8],"Mekkah":[21.4225,39.8262,3],"Madinah":[24.4672,39.6111,3]};
var METH={kemenag:[20,18,0],mwl:[18,17,0],egypt:[19.5,17.5,0],umm:[18.5,0,90],isna:[15,15,0]};
function S(d){return Math.sin(rad(d))}function C(d){return Math.cos(rad(d))}
function AS(x){return Math.asin(x)*180/Math.PI}function AC(x){return Math.acos(x)*180/Math.PI}
function A2(y,x){return Math.atan2(y,x)*180/Math.PI}function ACOT(x){return Math.atan(1/x)*180/Math.PI}
function fa(a){a=a%360;return a<0?a+360:a}function fh(h){h=h%24;return h<0?h+24:h}
function jd(y,m,d){if(m<=2){y-=1;m+=12}var A=Math.floor(y/100),B=2-A+Math.floor(A/4);return Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))+d+B-1524.5}
function sunPos(j){var D=j-2451545,g=fa(357.529+0.98560028*D),q=fa(280.459+0.98564736*D),L=fa(q+1.915*S(g)+0.020*S(2*g)),e=23.439-0.00000036*D;
 var RA=A2(C(e)*S(L),C(L))/15;return{decl:AS(S(e)*S(L)),eqt:q/15-fh(RA)}}
function fmt(t){if(isNaN(t))return'—';var m=Math.round(fh(t)*60)%1440,h=Math.floor(m/60),n=m%60;return(h<10?'0':'')+h+':'+(n<10?'0':'')+n}
var cur=null,curDate='';
function calc(){
 var lat=parseFloat($('lat').value),lng=parseFloat($('lng').value),tz=parseFloat($('tz').value),d=new Date($('dt').value+'T00:00:00');
 if(isNaN(lat)||isNaN(lng)||isNaN(tz)||isNaN(d.getTime()))return;
 var m=METH[$('meth').value],f=parseInt($('asr').value,10),ih=(parseFloat($('ih').value)||0)/60;
 var j=jd(d.getFullYear(),d.getMonth()+1,d.getDate())-lng/360,shift=tz-lng/15;
 function sp(h){return sunPos(j+h/24)}
 function at(ang,base,ccw){var s=sp(base),noon=12-s.eqt,x=(-S(ang)-S(s.decl)*S(lat))/(C(s.decl)*C(lat));if(x>1||x<-1)return NaN;var v=AC(x)/15;return noon+(ccw?-v:v)}
 var dh=12-sp(12).eqt,sd=sp(15).decl,ax=-ACOT(f+Math.tan(rad(Math.abs(lat-sd))));
 var fajr=at(m[0],5,true)+shift,sr=at(0.833,6,true)+shift,zhr=dh+shift,asr=at(ax,15,false)+shift,mg=at(0.833,18,false)+shift;
 var isha=m[2]?mg+m[2]/60:at(m[1],19,false)+shift;
 cur=[['Imsak',fajr-10/60+ih],['Subuh',fajr+ih],['Terbit',sr-ih],['Zuhur',zhr+ih],['Asar',asr+ih],['Magrib',mg+ih],['Isya',isha+ih]];
 var h='<table><tbody>';cur.forEach(function(r){h+='<tr><td>'+r[0]+'</td><td><b>'+fmt(r[1])+'</b></td></tr>'});
 $('out').innerHTML=h+'</tbody></table><small>Akurasi ± 1–2 menit. Bandingkan dengan jadwal resmi Kemenag/masjid setempat.</small>';tick()}
function tick(){if(!cur)return;var n=new Date(),now=n.getHours()+n.getMinutes()/60+n.getSeconds()/3600;
 if($('dt').value!==n.toISOString().slice(0,0)+[n.getFullYear(),('0'+(n.getMonth()+1)).slice(-2),('0'+n.getDate()).slice(-2)].join('-')){$('next').textContent='';return}
 if(Math.abs(-n.getTimezoneOffset()/60-parseFloat($('tz').value))>0.01){$('next').textContent='';return}
 var list=cur.filter(function(r){return r[0]!='Imsak'&&r[0]!='Terbit'}),nx=null;
 for(var i=0;i<list.length;i++){if(list[i][1]>now){nx=list[i];break}}
 if(!nx){$('next').textContent='Semua waktu salat hari ini telah lewat.';return}
 var s=Math.round((nx[1]-now)*3600),hh=Math.floor(s/3600),mm=Math.floor(s%3600/60),ss=s%60;
 $('next').innerHTML='Menuju <b>'+nx[0]+'</b> ('+fmt(nx[1])+'): <b>'+hh+' j '+mm+' m '+ss+' d</b>'}
var sel=$('city');sel.innerHTML='<option value="">— Lokasi manual —</option>'+Object.keys(CITIES).map(function(k){return'<option>'+k+'</option>'}).join('');
function setCity(){var c=CITIES[sel.value];if(c){$('lat').value=c[0];$('lng').value=c[1];$('tz').value=c[2]}calc()}
sel.onchange=setCity;
['dt','lat','lng','tz','meth','asr','ih'].forEach(function(i){$(i).onchange=calc;$(i).oninput=calc});
$('loc').onclick=function(){geo(function(a,b){sel.value='';$('lat').value=a.toFixed(5);$('lng').value=b.toFixed(5);$('tz').value=-new Date().getTimezoneOffset()/60;calc()})};
var t=new Date();$('dt').value=[t.getFullYear(),('0'+(t.getMonth()+1)).slice(-2),('0'+t.getDate()).slice(-2)].join('-');
sel.value='Jakarta';setCity();setInterval(tick,1000);
""",
    ["Pilih kota atau klik 'Lokasi saya'.", "Pilih metode (Indonesia: Kemenag RI) dan mazhab Asar.", "Baca jadwal; hitung mundur menuju salat berikutnya tampil otomatis."],
    [("Metode mana untuk Indonesia?", "Kemenag RI (Subuh 20°, Isya 18°) dengan ihtiyat 2 menit adalah acuan umum di Indonesia."),
     ("Mengapa beda beberapa menit dengan jadwal masjid?", "Perbedaan sudut, ihtiyat, ketinggian, dan pembulatan. Ikuti jadwal resmi setempat bila ada.")],
    groups=["worship", "finders"], note="Hasil perhitungan astronomis; di lintang tinggi (>48°) Subuh/Isya bisa tidak terdefinisi (—)."))

ISLAMIC.append(tool(
    "hijri-calendar", "Konverter Kalender Hijriah ⇄ Masehi",
    "Konversi tanggal Masehi ke Hijriah dan sebaliknya memakai kalender Umm al-Qura bawaan browser.",
    r"""<h3>Masehi → Hijriah</h3><input type="date" id="g"><div class="out" id="o1"></div>
<h3>Hijriah → Masehi</h3><div class="row"><input id="hd" type="number" min="1" max="30" placeholder="Tanggal"><select id="hm"></select><input id="hy" type="number" placeholder="Tahun H (mis. 1447)"></div>
<button class="btn" id="b2">Konversi</button><div class="out" id="o2"></div>""",
    r"""
var HM=['Muharram','Safar','Rabiul Awal','Rabiul Akhir','Jumadil Awal','Jumadil Akhir','Rajab','Syaban','Ramadan','Syawal','Zulkaidah','Zulhijah'];
var MS=['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'];
var F=new Intl.DateTimeFormat('en-u-ca-islamic-umalqura',{day:'numeric',month:'numeric',year:'numeric',timeZone:'UTC'});
function parts(d){var o={};F.formatToParts(d).forEach(function(x){if(x.type!='literal'&&x.type!='era')o[x.type]=parseInt(x.value,10)});return o}
$('hm').innerHTML=HM.map(function(n,i){return'<option value="'+(i+1)+'">'+n+'</option>'}).join('');
function g2h(){var v=$('g').value;if(!v)return;var p=v.split('-'),d=new Date(Date.UTC(+p[0],+p[1]-1,+p[2])),h=parts(d);
 $('o1').innerHTML='<span class="big">'+h.day+' '+HM[h.month-1]+' '+h.year+' H</span>'}
function h2g(){var y=+$('hy').value,m=+$('hm').value,d=+$('hd').value;if(!y||!d)return;
 var ap=Math.round(y*0.970229+621.574),s=Date.UTC(ap,0,1)-400*864e5;
 for(var i=0;i<900;i++){var t=new Date(s+i*864e5),p=parts(t);if(p.year===y&&p.month===m&&p.day===d){
  $('o2').innerHTML='<span class="big">'+t.getUTCDate()+' '+MS[t.getUTCMonth()]+' '+t.getUTCFullYear()+'</span>';return}}
 $('o2').textContent='Tanggal tidak ditemukan (periksa input).'}
$('g').onchange=g2h;$('b2').onclick=h2g;
var n=new Date();$('g').value=[n.getFullYear(),('0'+(n.getMonth()+1)).slice(-2),('0'+n.getDate()).slice(-2)].join('-');g2h();
var h=parts(new Date(Date.UTC(n.getFullYear(),n.getMonth(),n.getDate())));$('hy').value=h.year;$('hm').value=h.month;$('hd').value=h.day;
""",
    ["Pilih tanggal Masehi untuk melihat tanggal Hijriahnya.", "Atau isi tanggal, bulan, dan tahun Hijriah lalu klik Konversi."],
    [("Mengapa bisa beda satu hari dengan kalender Kemenag?", "Browser memakai kalender Umm al-Qura (Arab Saudi). Indonesia menetapkan awal bulan lewat sidang isbat/rukyat sehingga bisa selisih ±1 hari."),
     ("Apakah butuh internet?", "Tidak. Konversi memakai Intl API bawaan browser.")],
    groups=["trackers", "knowledge"], note="Penetapan awal Ramadan, Syawal, dan Zulhijah di Indonesia mengikuti keputusan resmi pemerintah."))

ISLAMIC.append(tool(
    "calendar", "Kalender Masehi + Hijriah Bulanan",
    "Kalender bulanan yang menampilkan tanggal Masehi dan Hijriah berdampingan.",
    r"""<div class="row"><button class="btn" id="pv">◀ Sebelumnya</button><b id="ttl" style="text-align:center;padding:10px"></b><button class="btn" id="nx">Berikutnya ▶</button></div>
<div class="cal" id="cal"></div>""",
    r"""
var MS=['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'];
var HM=['Muharram','Safar','Rabiul Awal','Rabiul Akhir','Jumadil Awal','Jumadil Akhir','Rajab','Syaban','Ramadan','Syawal','Zulkaidah','Zulhijah'];
var F=new Intl.DateTimeFormat('en-u-ca-islamic-umalqura',{day:'numeric',month:'numeric',year:'numeric',timeZone:'UTC'});
function parts(d){var o={};F.formatToParts(d).forEach(function(x){if(x.type!='literal'&&x.type!='era')o[x.type]=parseInt(x.value,10)});return o}
var n=new Date(),y=n.getFullYear(),m=n.getMonth();
function render(){var f=new Date(Date.UTC(y,m,1)),days=new Date(Date.UTC(y,m+1,0)).getUTCDate(),off=f.getUTCDay(),h='';
 ['Min','Sen','Sel','Rab','Kam','Jum','Sab'].forEach(function(x){h+='<div><b>'+x+'</b></div>'});
 for(var i=0;i<off;i++)h+='<div></div>';
 var a=parts(f),b=parts(new Date(Date.UTC(y,m,days)));
 for(var d=1;d<=days;d++){var p=parts(new Date(Date.UTC(y,m,d))),t=(d==n.getDate()&&m==n.getMonth()&&y==n.getFullYear());
  h+='<div class="'+(t?'today':'')+'">'+d+'<small>'+p.day+' '+HM[p.month-1].slice(0,3)+'</small></div>'}
 $('cal').innerHTML=h;$('ttl').textContent=MS[m]+' '+y+' · '+HM[a.month-1]+' '+a.year+(b.month!=a.month?' – '+HM[b.month-1]+' '+b.year:'')+' H'}
$('pv').onclick=function(){m--;if(m<0){m=11;y--}render()};$('nx').onclick=function(){m++;if(m>11){m=0;y++}render()};render();
""",
    ["Gunakan tombol panah untuk pindah bulan.", "Angka kecil di bawah tanggal adalah tanggal Hijriah."],
    [("Hari ini ditandai bagaimana?", "Hari ini berlatar merah muda-merah."), ("Sumber tanggal Hijriah?", "Kalender Umm al-Qura dari Intl API browser.")],
    groups=["trackers"]))

ISLAMIC.append(tool(
    "zakat-calculator", "Kalkulator Zakat: Mal, Profesi, Emas, dan Fitrah",
    "Hitung zakat maal, zakat penghasilan, zakat emas, dan zakat fitrah dengan nisab setara 85 gram emas.",
    r"""<label>Jenis zakat</label><select id="type"><option value="mal">Zakat Mal (harta)</option><option value="profesi">Zakat Profesi / Penghasilan</option><option value="emas">Zakat Emas</option><option value="fitrah">Zakat Fitrah</option></select>
<label>Harga emas per gram (Rp) — isi harga terbaru</label><input id="gold" type="number" placeholder="mis. harga emas hari ini">
<div id="f-mal"><label>Tabungan / kas</label><input id="m1" type="number" value="0"><label>Investasi / emas / perak (nilai)</label><input id="m2" type="number" value="0"><label>Barang dagangan</label><input id="m3" type="number" value="0"><label>Piutang lancar</label><input id="m4" type="number" value="0"><label>Utang jatuh tempo</label><input id="m5" type="number" value="0"></div>
<div id="f-profesi" style="display:none"><label>Gaji per bulan</label><input id="p1" type="number" value="0"><label>Penghasilan lain per bulan</label><input id="p2" type="number" value="0"><label>Pengurang (kebutuhan pokok/cicilan, opsional)</label><input id="p3" type="number" value="0"></div>
<div id="f-emas" style="display:none"><label>Emas yang dimiliki (gram)</label><input id="e1" type="number" value="0"></div>
<div id="f-fitrah" style="display:none"><label>Jumlah jiwa</label><input id="r1" type="number" value="1"><label>Beras per jiwa (kg)</label><input id="r2" type="number" step="0.1" value="2.5"><label>Harga beras per kg (Rp)</label><input id="r3" type="number" value="0"></div>
<button class="btn" id="go">Hitung Zakat</button><div class="out" id="out"></div>""",
    r"""
function v(i){return parseFloat($(i).value)||0}
var T=$('type');T.onchange=function(){['mal','profesi','emas','fitrah'].forEach(function(k){$('f-'+k).style.display=k==T.value?'block':'none'});$('out').innerHTML=''};
$('go').onclick=function(){var g=v('gold'),nis=85*g,o='';
 if(T.value=='fitrah'){var a=v('r1')*v('r2')*v('r3');o='Zakat fitrah: <span class="big">'+idr(a)+'</span> ('+(v('r1')*v('r2')).toFixed(1)+' kg beras)';}
 else{if(!g)return alert('Isi harga emas per gram');
  if(T.value=='mal'){var n=v('m1')+v('m2')+v('m3')+v('m4')-v('m5');o='Harta bersih: '+idr(n)+'<br>Nisab (85 g emas): '+idr(nis)+'<br>'+(n>=nis?'Zakat 2,5%: <span class="big">'+idr(n*0.025)+'</span><br><small>Wajib bila harta telah dimiliki satu tahun (haul).</small>':'Belum mencapai nisab.');}
  if(T.value=='profesi'){var in_=v('p1')+v('p2')-v('p3'),nb=nis/12;o='Penghasilan bersih/bulan: '+idr(in_)+'<br>Nisab per bulan (85 g ÷ 12): '+idr(nb)+'<br>'+(in_>=nb?'Zakat 2,5%/bulan: <span class="big">'+idr(in_*0.025)+'</span>':'Belum mencapai nisab bulanan.');}
  if(T.value=='emas'){var gm=v('e1');o='Emas: '+gm+' g. Nisab: 85 g<br>'+(gm>=85?'Zakat 2,5%: <span class="big">'+(gm*0.025).toFixed(3)+' gram</span> (≈ '+idr(gm*0.025*g)+')':'Belum mencapai nisab.');}}
 $('out').innerHTML=o};
""",
    ["Pilih jenis zakat.", "Isi harga emas per gram terbaru (dari sumber tepercaya).", "Isi harta/penghasilan lalu klik Hitung Zakat."],
    [("Berapa nisab zakat maal?", "Setara 85 gram emas dan telah dimiliki satu tahun (haul). Zakatnya 2,5%."),
     ("Berapa zakat fitrah?", "Sekitar 2,5 kg beras (atau uang senilai) per jiwa; patokan resmi ditetapkan BAZNAS/Kemenag tiap tahun.")],
    groups=["calculators"], note="Alat bantu estimasi. Untuk kasus khusus, konsultasikan dengan BAZNAS/LAZ resmi atau ulama."))

ISLAMIC.append(tool(
    "salah-tracker", "Salah Tracker: Catat 5 Waktu Salat Harian",
    "Catat salat lima waktu setiap hari, lihat riwayat 7 hari dan rekor beruntun. Data tersimpan hanya di perangkat Anda.",
    r"""<input type="date" id="d"><div id="list"></div><div class="out" id="sum"></div><button class="btn" id="rst">Hapus semua data</button>""",
    r"""
var P=['Subuh','Zuhur','Asar','Magrib','Isya'],K='awdev_salah';
function load(){try{return JSON.parse(localStorage.getItem(K))||{}}catch(x){return{}}}
function save(o){try{localStorage.setItem(K,JSON.stringify(o))}catch(x){}}
function ds(d){return[d.getFullYear(),('0'+(d.getMonth()+1)).slice(-2),('0'+d.getDate()).slice(-2)].join('-')}
function render(){var o=load(),k=$('d').value,a=o[k]||[0,0,0,0,0],h='';
 P.forEach(function(n,i){h+='<label><input type="checkbox" data-i="'+i+'" '+(a[i]?'checked':'')+'> '+n+'</label>'});$('list').innerHTML=h;
 document.querySelectorAll('[data-i]').forEach(function(c){c.onchange=function(){var o=load(),a=o[k]||[0,0,0,0,0];a[+c.dataset.i]=c.checked?1:0;o[k]=a;save(o);sum()}});sum()}
function sum(){var o=load(),t=new Date(),rows='<table><tr><th>Tanggal</th><th>Selesai</th></tr>';
 for(var i=0;i<7;i++){var d=new Date(t.getFullYear(),t.getMonth(),t.getDate()-i),a=o[ds(d)]||[];rows+='<tr><td>'+ds(d)+'</td><td>'+a.reduce(function(x,y){return x+y},0)+' / 5</td></tr>'}
 var st=0;for(var j=0;j<3650;j++){var dd=new Date(t.getFullYear(),t.getMonth(),t.getDate()-j),aa=o[ds(dd)]||[];if(aa.length&&aa.reduce(function(x,y){return x+y},0)==5)st++;else if(j>0||aa.length)break;else break}
 $('sum').innerHTML=rows+'</table>Rekor beruntun (5/5 salat): <b>'+st+' hari</b>'}
$('d').onchange=render;$('d').value=ds(new Date());
$('rst').onclick=function(){if(confirm('Hapus semua data tracker?')){try{localStorage.removeItem(K)}catch(x){}render()}};render();
""",
    ["Pilih tanggal (default hari ini).", "Centang salat yang sudah dikerjakan.", "Lihat ringkasan 7 hari dan rekor beruntun."],
    [("Di mana data disimpan?", "Di localStorage browser Anda. Tidak dikirim ke server dan hilang jika data situs dihapus."), ("Bisa sinkron antar perangkat?", "Tidak, data hanya ada di browser yang dipakai.")],
    groups=["trackers", "worship"]))

ISLAMIC.append(tool(
    "mosque-finder", "Cari Masjid & Musala Terdekat (OpenStreetMap)",
    "Temukan masjid dan musala di sekitar lokasi Anda memakai data OpenStreetMap, lengkap dengan jarak dan tautan peta.",
    r"""<div class="row"><button class="btn" id="loc">📍 Cari di sekitar saya</button><select id="rad"><option value="1000">Radius 1 km</option><option value="2000" selected>Radius 2 km</option><option value="5000">Radius 5 km</option></select></div>
<div class="out" id="out">Klik tombol untuk mencari.</div>""",
    r"""
function go(la,ln){var r=$('rad').value;$('out').textContent='Mencari…';
 var q='[out:json][timeout:25];(node["amenity"="place_of_worship"]["religion"="muslim"](around:'+r+','+la+','+ln+');way["amenity"="place_of_worship"]["religion"="muslim"](around:'+r+','+la+','+ln+'););out center 80;';
 fetch('https://overpass-api.de/api/interpreter',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'data='+encodeURIComponent(q)})
 .then(function(x){return x.json()}).then(function(j){
  var L=j.elements.map(function(z){var a=z.lat||(z.center&&z.center.lat),b=z.lon||(z.center&&z.center.lon);return{n:(z.tags&&(z.tags.name||z.tags['name:id']))||'Masjid/Musala (tanpa nama)',a:a,b:b,d:hav(la,ln,a,b)}}).filter(function(z){return z.a}).sort(function(x,y){return x.d-y.d});
  if(!L.length){$('out').textContent='Tidak ada hasil di radius ini. Perbesar radius (data OSM bisa belum lengkap).';return}
  var h='<ol>';L.slice(0,40).forEach(function(z){h+='<li><b>'+z.n.replace(/</g,'&lt;')+'</b> — '+(z.d<1?Math.round(z.d*1000)+' m':z.d.toFixed(2)+' km')+' · <a target="_blank" rel="noopener" href="https://www.openstreetmap.org/?mlat='+z.a+'&mlon='+z.b+'#map=18/'+z.a+'/'+z.b+'">peta</a></li>'});
  $('out').innerHTML=h+'</ol>'}).catch(function(){$('out').textContent='Gagal mengambil data. Coba lagi beberapa saat.'})}
$('loc').onclick=function(){geo(go)};
""",
    ["Klik 'Cari di sekitar saya' dan izinkan lokasi.", "Pilih radius pencarian.", "Klik 'peta' untuk membuka lokasi."],
    [("Dari mana datanya?", "OpenStreetMap lewat Overpass API; kelengkapan tergantung kontributor lokal."), ("Apakah lokasi saya disimpan?", "Tidak oleh situs ini. Koordinat dikirim ke server Overpass hanya untuk pencarian.")],
    groups=["finders"]))

ISLAMIC.append(tool(
    "quran", "Al-Qur'an Online: Teks Arab & Terjemahan Indonesia",
    "Baca 114 surah dengan teks Arab (Utsmani) dan terjemahan Bahasa Indonesia, dimuat dari Al-Quran Cloud API.",
    r"""<label>Pilih surah</label><select id="s"></select><input id="f" placeholder="Cari nomor ayat atau kata terjemahan…"><div id="out" class="out">Memuat…</div>""",
    r"""
var data=null;
fetch('https://api.alquran.cloud/v1/surah').then(function(r){return r.json()}).then(function(j){
 $('s').innerHTML=j.data.map(function(x){return'<option value="'+x.number+'">'+x.number+'. '+x.englishName+' ('+x.name+') — '+x.numberOfAyahs+' ayat</option>'}).join('');load()}).catch(function(){$('out').textContent='Gagal memuat daftar surah.'});
function load(){$('out').textContent='Memuat…';fetch('https://api.alquran.cloud/v1/surah/'+$('s').value+'/editions/quran-uthmani,id.indonesian')
 .then(function(r){return r.json()}).then(function(j){data=j.data;draw()}).catch(function(){$('out').textContent='Gagal memuat surah.'})}
function draw(){if(!data)return;var q=$('f').value.toLowerCase(),o=$('out');o.innerHTML='';var ar=data[0].ayahs,id=data[1].ayahs;
 ar.forEach(function(a,i){var t=id[i].text;if(q&&String(a.numberInSurah)!==q&&t.toLowerCase().indexOf(q)<0)return;
  var d=document.createElement('div');d.className='ayah';var p=document.createElement('div');p.className='ar';p.textContent=a.text+' ﴿'+a.numberInSurah+'﴾';
  var s=document.createElement('div');s.textContent=a.numberInSurah+'. '+t;d.appendChild(p);d.appendChild(s);o.appendChild(d)})}
$('s').onchange=load;$('f').oninput=draw;
""",
    ["Pilih surah dari daftar.", "Gunakan kotak cari untuk menyaring ayat."],
    [("Dari mana teks Al-Qur'an diambil?", "Dari Al-Quran Cloud API (edisi quran-uthmani dan id.indonesian)."), ("Apakah ini pengganti mushaf?", "Tidak. Gunakan mushaf resmi dan guru yang kompeten untuk belajar tilawah dan hukum bacaan.")],
    groups=["knowledge"], ext=[("Al-Quran Cloud API", "https://alquran.cloud/api"), ("Tanzil", "https://tanzil.net/")]))

DUAS = [
    ("Sebelum makan", "بِسْمِ اللَّهِ", "Dengan nama Allah. (Jika lupa di awal: بِسْمِ اللَّهِ أَوَّلَهُ وَآخِرَهُ)"),
    ("Setelah makan", "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مُسْلِمِينَ", "Segala puji bagi Allah yang telah memberi kami makan dan minum serta menjadikan kami muslim."),
    ("Bangun tidur", "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ", "Segala puji bagi Allah yang menghidupkan kami setelah mematikan kami, dan kepada-Nya kami dibangkitkan."),
    ("Sebelum tidur", "بِاسْمِكَ اللَّهُمَّ أَحْيَا وَبِاسْمِكَ أَمُوتُ", "Dengan nama-Mu ya Allah aku hidup dan dengan nama-Mu aku mati."),
    ("Masuk masjid", "اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ", "Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu."),
    ("Keluar masjid", "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ", "Ya Allah, sungguh aku memohon kepada-Mu sebagian karunia-Mu."),
    ("Keluar rumah", "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", "Dengan nama Allah, aku bertawakal kepada Allah; tiada daya dan kekuatan kecuali dengan pertolongan Allah."),
    ("Naik kendaraan", "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ", "Maha Suci Allah yang menundukkan semua ini bagi kami, padahal kami sebelumnya tidak mampu menguasainya, dan sesungguhnya kepada Tuhan kami kami akan kembali. (QS. Az-Zukhruf: 13-14)"),
    ("Doa sapu jagat", "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", "Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan lindungilah kami dari azab neraka. (QS. Al-Baqarah: 201)"),
]

ISLAMIC.append(tool(
    "duas", "Kumpulan Doa Harian: Teks Arab dan Artinya",
    "Doa-doa harian pilihan (makan, tidur, masuk masjid, bepergian, dan lainnya) dengan teks Arab dan terjemahan Indonesia.",
    r"""<input id="f" placeholder="Cari doa…"><div id="out"></div>""",
    "var D=" + json.dumps(DUAS, ensure_ascii=False) + r""";
function draw(){var q=$('f').value.toLowerCase(),o=$('out');o.innerHTML='';
 D.forEach(function(d){if(q&&(d[0]+d[2]).toLowerCase().indexOf(q)<0)return;var x=document.createElement('div');x.className='ayah';
  var h=document.createElement('h3');h.textContent=d[0];var a=document.createElement('div');a.className='ar';a.textContent=d[1];var t=document.createElement('p');t.textContent=d[2];
  x.appendChild(h);x.appendChild(a);x.appendChild(t);o.appendChild(x)})}
$('f').oninput=draw;draw();
""",
    ["Cari doa dengan kata kunci atau gulir daftar.", "Baca teks Arab dan artinya."],
    [("Apakah teks doa sudah diverifikasi?", "Teks diambil dari doa yang masyhur; tetap rujuk kitab Hisnul Muslim atau ustaz tepercaya untuk takhrij dan lafaz."), ("Ada transliterasi Latin?", "Belum, agar tidak ada kekeliruan lafaz. Belajarlah membaca langsung dari guru.")],
    groups=["knowledge", "worship"]))

HALAL = [
    ("babi", "haram", "Babi/turunannya haram."), ("pork", "haram", "Pork = babi."), ("lard", "haram", "Lard = lemak babi."),
    ("bacon", "haram", "Bacon umumnya dari babi."), ("ham", "haram", "Ham umumnya dari babi."), ("wine", "haram", "Wine mengandung alkohol khamr."),
    ("arak", "haram", "Minuman beralkohol."), ("bir", "haram", "Minuman beralkohol."), ("beer", "haram", "Minuman beralkohol."),
    ("gelatin", "syubhat", "Bisa dari babi/sapi/ikan; cek sumber & sertifikat halal."),
    ("rennet", "syubhat", "Enzim keju; bisa dari hewan tidak disembelih."), ("pepsin", "syubhat", "Sering dari lambung babi."),
    ("e120", "syubhat", "Carmine/pewarna dari serangga cochineal; ulama berbeda pendapat."), ("carmine", "syubhat", "Pewarna dari serangga cochineal; ulama berbeda pendapat."),
    ("e441", "syubhat", "Gelatin."), ("e904", "syubhat", "Shellac, dari serangga lac."), ("e542", "syubhat", "Bone phosphate, bisa dari tulang hewan."),
    ("e471", "syubhat", "Emulsifier; sumber lemak bisa hewani."), ("e472", "syubhat", "Emulsifier; sumber lemak bisa hewani."), ("e920", "syubhat", "L-cysteine, bisa dari bulu/rambut."),
    ("alkohol", "syubhat", "Periksa asal & kadar; etanol dari khamr bermasalah."), ("ethanol", "syubhat", "Periksa asal & kadar."), ("vanilla extract", "syubhat", "Ekstrak biasa memakai alkohol."),
    ("enzim", "syubhat", "Periksa sumber enzim."), ("enzyme", "syubhat", "Periksa sumber enzim."), ("mono and diglycerides", "syubhat", "Sumber lemak bisa hewani."),
]
ISLAMIC.append(tool(
    "halal-food", "Cek Bahan Makanan: Titik Kritis Halal",
    "Tempel daftar komposisi produk untuk menandai bahan yang haram atau syubhat (perlu dicek). Bukan pengganti sertifikat halal.",
    r"""<textarea id="t" rows="6" placeholder="Tempel komposisi: mis. sugar, gelatin, E471, natural flavour…"></textarea><button class="btn" id="go">Periksa</button><div class="out" id="out"></div>
<p><a href="https://cekbpjph.halal.go.id/" target="_blank" rel="noopener">Cek status sertifikat halal resmi (BPJPH)</a></p>""",
    "var H=" + json.dumps(HALAL, ensure_ascii=False) + r""";
$('go').onclick=function(){var t=$('t').value.toLowerCase(),r=[];H.forEach(function(h){if(t.indexOf(h[0])>=0)r.push(h)});
 var o=$('out');if(!t.trim()){o.textContent='Isi komposisi dulu.';return}
 if(!r.length){o.textContent='Tidak ditemukan kata kunci kritis dalam database sederhana ini. Tetap periksa logo/sertifikat halal resmi.';return}
 o.innerHTML='<ul>'+r.map(function(h){return'<li><b>'+h[0]+'</b> <span class="tag '+h[1]+'">'+h[1]+'</span> — '+h[2]+'</li>'}).join('')+'</ul>'};
""",
    ["Salin daftar komposisi dari kemasan.", "Klik Periksa dan lihat bahan bertanda haram/syubhat.", "Konfirmasi ke BPJPH atau MUI untuk kepastian."],
    [("Apakah hasil ini penentu halal?", "Tidak. Ini hanya penanda titik kritis. Status halal ditetapkan lembaga resmi lewat sertifikasi."), ("Mengapa 'syubhat'?", "Bahan bisa berasal dari sumber halal maupun tidak; perlu verifikasi produsen.")],
    groups=["knowledge", "finders"], note="Database kata kunci sederhana, bukan fatwa."))

ISLAMIC.append(tool(
    "timer", "Timer, Stopwatch & Penghitung Tasbih",
    "Timer hitung mundur dengan bunyi alarm, stopwatch, dan penghitung dzikir yang menyimpan hitungan di perangkat.",
    r"""<h3>Timer</h3><div class="row"><input id="tm" type="number" min="0" value="5" placeholder="Menit"><input id="ts" type="number" min="0" max="59" value="0" placeholder="Detik"></div>
<div class="big" id="td">05:00</div><button class="btn" id="tg">Mulai</button><button class="btn" id="tr">Reset</button>
<h3>Stopwatch</h3><div class="big" id="sd">00:00.0</div><button class="btn" id="sg">Mulai</button><button class="btn" id="sr">Reset</button>
<h3>Tasbih</h3><div class="big" id="cn">0</div><div class="row"><button class="btn" id="cp">+1</button><button class="btn" id="cr">Reset</button></div><label>Target</label><input id="ct" type="number" value="33">""",
    r"""
function p2(n){return(n<10?'0':'')+n}
var left=300,ti=null;function drawT(){$('td').textContent=p2(Math.floor(left/60))+':'+p2(left%60)}
function beep(){try{var a=new (window.AudioContext||window.webkitAudioContext)(),o=a.createOscillator();o.connect(a.destination);o.frequency.value=880;o.start();setTimeout(function(){o.stop()},800)}catch(x){}}
function setT(){left=(parseInt($('tm').value)||0)*60+(parseInt($('ts').value)||0);drawT()}
$('tm').oninput=$('ts').oninput=function(){if(!ti)setT()};
$('tg').onclick=function(){if(ti){clearInterval(ti);ti=null;$('tg').textContent='Lanjut';return}if(left<=0)setT();$('tg').textContent='Jeda';
 ti=setInterval(function(){left--;drawT();if(left<=0){clearInterval(ti);ti=null;$('tg').textContent='Mulai';beep();alert('Waktu habis!')}},1000)};
$('tr').onclick=function(){clearInterval(ti);ti=null;$('tg').textContent='Mulai';setT()};
var st=0,si=null,s0=0;function drawS(){var t=st+(si?Date.now()-s0:0),m=Math.floor(t/60000),s=Math.floor(t%60000/1000),d=Math.floor(t%1000/100);$('sd').textContent=p2(m)+':'+p2(s)+'.'+d}
$('sg').onclick=function(){if(si){st+=Date.now()-s0;clearInterval(si);si=null;$('sg').textContent='Lanjut'}else{s0=Date.now();si=setInterval(drawS,100);$('sg').textContent='Jeda'}};
$('sr').onclick=function(){clearInterval(si);si=null;st=0;$('sg').textContent='Mulai';drawS()};
var K='awdev_tasbih',c=0;try{c=parseInt(localStorage.getItem(K))||0}catch(x){}
function drawC(){$('cn').textContent=c}function sv(){try{localStorage.setItem(K,c)}catch(x){}}
$('cp').onclick=function(){c++;sv();drawC();if(navigator.vibrate)navigator.vibrate(c==(parseInt($('ct').value)||0)?[200,100,200]:20)};
$('cr').onclick=function(){c=0;sv();drawC()};drawC();setT();
""",
    ["Isi menit/detik lalu klik Mulai untuk timer.", "Gunakan stopwatch untuk mencatat durasi.", "Tekan +1 pada tasbih; hitungan tersimpan otomatis."],
    [("Apakah alarm berbunyi saat tab di latar belakang?", "Browser dapat menunda timer di tab tidak aktif. Biarkan tab terbuka untuk hasil terbaik."), ("Tasbih tersimpan?", "Ya, di localStorage perangkat Anda.")],
    groups=["worship", "trackers"]))

ISLAMIC.append(tool(
    "cuaca", "Cuaca Hari Ini & Prakiraan 7 Hari (Open-Meteo)",
    "Cek cuaca saat ini dan prakiraan 7 hari untuk kota mana pun atau lokasi Anda, data dari Open-Meteo.",
    r"""<div class="row"><input id="q" placeholder="Nama kota, mis. Semarang"><button class="btn" id="s">Cari</button><button class="btn" id="loc">📍 Lokasi saya</button></div><div class="out" id="out">Cari kota atau gunakan lokasi Anda.</div>""",
    r"""
var WC={0:'Cerah',1:'Cerah berawan',2:'Berawan sebagian',3:'Berawan',45:'Kabut',48:'Kabut beku',51:'Gerimis ringan',53:'Gerimis',55:'Gerimis lebat',61:'Hujan ringan',63:'Hujan sedang',65:'Hujan lebat',80:'Hujan lokal ringan',81:'Hujan lokal',82:'Hujan lokal lebat',95:'Badai petir',96:'Badai petir + es',99:'Badai petir + es lebat'};
function W(c){return WC[c]||'Kode '+c}
function go(la,ln,name){$('out').textContent='Memuat…';
 fetch('https://api.open-meteo.com/v1/forecast?latitude='+la+'&longitude='+ln+'&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=7')
 .then(function(r){return r.json()}).then(function(j){var c=j.current,d=j.daily,h='<h3>'+name+'</h3><div class="big">'+Math.round(c.temperature_2m)+'°C · '+W(c.weather_code)+'</div><p>Terasa '+Math.round(c.apparent_temperature)+'°C · Kelembapan '+c.relative_humidity_2m+'% · Angin '+c.wind_speed_10m+' km/j · Hujan '+c.precipitation+' mm</p><table><tr><th>Tanggal</th><th>Cuaca</th><th>Min–Maks</th><th>Hujan</th></tr>';
  d.time.forEach(function(t,i){h+='<tr><td>'+t+'</td><td>'+W(d.weather_code[i])+'</td><td>'+Math.round(d.temperature_2m_min[i])+'–'+Math.round(d.temperature_2m_max[i])+'°C</td><td>'+(d.precipitation_probability_max[i]||0)+'%</td></tr>'});
  $('out').innerHTML=h+'</table>'}).catch(function(){$('out').textContent='Gagal memuat cuaca.'})}
$('s').onclick=function(){var q=$('q').value.trim();if(!q)return;
 fetch('https://geocoding-api.open-meteo.com/v1/search?name='+encodeURIComponent(q)+'&count=1&language=id').then(function(r){return r.json()}).then(function(j){
  if(!j.results||!j.results.length){$('out').textContent='Kota tidak ditemukan.';return}var r=j.results[0];go(r.latitude,r.longitude,r.name+', '+(r.country||''))}).catch(function(){$('out').textContent='Gagal mencari kota.'})};
$('loc').onclick=function(){geo(function(a,b){go(a,b,'Lokasi Anda')})};
""",
    ["Ketik nama kota lalu klik Cari, atau pakai lokasi Anda.", "Baca kondisi saat ini dan prakiraan 7 hari."],
    [("Sumber data cuaca?", "Open-Meteo (open-meteo.com), layanan gratis tanpa API key."), ("Seberapa akurat?", "Model prakiraan global; untuk peringatan resmi rujuk BMKG.")],
    groups=["finders"], ext=[("BMKG", "https://www.bmkg.go.id/"), ("Open-Meteo", "https://open-meteo.com/")]))

HUBS = {
    "worship": ("Worship (Ibadah)", "Tools ibadah: kiblat, waktu salat, doa, tasbih."),
    "trackers": ("Trackers", "Pelacak ibadah dan kalender."),
    "calculators": ("Calculators", "Kalkulator zakat dan perhitungan syariah."),
    "knowledge": ("Knowledge", "Al-Qur'an, doa, kalender Hijriah, dan pengetahuan halal."),
    "finders": ("Finders", "Pencari masjid, arah kiblat, cuaca, dan bahan halal."),
}
ALIASES = {"qibla": "qibla-direction", "zakat": "zakat-calculator"}

# =============================================================== GENERAL TOOLS
GENERAL = []

GENERAL.append(tool("word-counter", "Penghitung Kata & Karakter Online",
    "Hitung jumlah kata, karakter, kalimat, paragraf, dan estimasi waktu baca secara langsung.",
    r'<textarea id="t" rows="8" placeholder="Tempel teks…"></textarea><div class="out" id="o"></div>',
    r"""var t=$('t');function u(){var s=t.value,w=(s.trim().match(/\S+/g)||[]).length;
$('o').innerHTML='Kata: <b>'+w+'</b> · Karakter: <b>'+s.length+'</b> · Tanpa spasi: <b>'+s.replace(/\s/g,'').length+'</b> · Kalimat: <b>'+(s.match(/[^.!?]+[.!?]+/g)||[]).length+'</b> · Paragraf: <b>'+s.split(/\n\s*\n/).filter(function(x){return x.trim()}).length+'</b> · Waktu baca: <b>'+(w?Math.max(1,Math.ceil(w/200)):0)+' menit</b>'}t.oninput=u;u();""",
    ["Tempel atau ketik teks.", "Hasil terhitung otomatis."],
    [("Bagaimana waktu baca dihitung?", "Kata dibagi 200 kata per menit."), ("Apakah teks dikirim ke server?", "Tidak, semua berjalan di browser.")], groups=["text"]))

GENERAL.append(tool("case-converter", "Konverter Huruf Besar/Kecil (Case Converter)",
    "Ubah teks menjadi HURUF BESAR, huruf kecil, Title Case, atau Sentence case.",
    r'<textarea id="t" rows="6"></textarea><button class="btn" data-m="u">UPPER</button><button class="btn" data-m="l">lower</button><button class="btn" data-m="t">Title Case</button><button class="btn" data-m="s">Sentence case</button>',
    r"""var t=$('t');document.querySelectorAll('[data-m]').forEach(function(b){b.onclick=function(){var s=t.value,m=b.dataset.m;
t.value=m=='u'?s.toUpperCase():m=='l'?s.toLowerCase():m=='t'?s.toLowerCase().replace(/(^|\s)(\S)/g,function(x,a,c){return a+c.toUpperCase()}):s.toLowerCase().replace(/(^\s*|[.!?]\s+)([a-z])/g,function(x,a,c){return a+c.toUpperCase()})}})""",
    ["Tempel teks.", "Klik format yang diinginkan."],
    [("Apa itu Title Case?", "Huruf pertama setiap kata dikapitalkan."), ("Apakah mendukung huruf beraksen?", "Ya, memakai fungsi bawaan JavaScript.")], groups=["text"]))

GENERAL.append(tool("slug-generator", "Slug Generator untuk URL SEO",
    "Ubah judul menjadi slug URL yang bersih dan ramah SEO.",
    r'<input id="t" placeholder="Judul artikel…"><div class="out" id="o"></div>',
    r"""$('t').oninput=function(){$('o').textContent=this.value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'')}""",
    ["Ketik judul.", "Salin slug hasil."],
    [("Mengapa slug penting untuk SEO?", "URL singkat dan deskriptif lebih mudah dipahami pengguna dan mesin pencari."), ("Tanda baca dihapus?", "Ya, diganti tanda hubung.")], groups=["seo"]))

GENERAL.append(tool("base64-encoder", "Base64 Encode & Decode",
    "Enkode teks ke Base64 atau dekode kembali, mendukung karakter Unicode.",
    r'<textarea id="t" rows="5"></textarea><button class="btn" id="e">Encode</button><button class="btn" id="d">Decode</button><div class="out" id="o"></div>',
    r"""$('e').onclick=function(){$('o').textContent=btoa(unescape(encodeURIComponent($('t').value)))};
$('d').onclick=function(){try{$('o').textContent=decodeURIComponent(escape(atob($('t').value.trim())))}catch(x){$('o').textContent='Input Base64 tidak valid'}}""",
    ["Tempel teks atau string Base64.", "Klik Encode atau Decode."],
    [("Apakah Base64 enkripsi?", "Bukan. Base64 hanya pengkodean, bukan keamanan."), ("Mengapa ukuran bertambah?", "Base64 menambah ukuran sekitar 33%.")], groups=["developer"]))

GENERAL.append(tool("url-encoder", "URL Encode & Decode",
    "Enkode atau dekode string URL (percent-encoding).",
    r'<textarea id="t" rows="4"></textarea><button class="btn" id="e">Encode</button><button class="btn" id="d">Decode</button><div class="out" id="o"></div>',
    r"""$('e').onclick=function(){$('o').textContent=encodeURIComponent($('t').value)};$('d').onclick=function(){try{$('o').textContent=decodeURIComponent($('t').value)}catch(x){$('o').textContent='Input tidak valid'}}""",
    ["Tempel teks/URL.", "Pilih Encode atau Decode."],
    [("Kapan perlu URL encoding?", "Saat parameter query berisi spasi atau karakter khusus."), ("Beda encodeURI dan encodeURIComponent?", "Tool ini memakai encodeURIComponent yang mengenkode hampir semua karakter khusus.")], groups=["developer"]))

GENERAL.append(tool("json-formatter", "JSON Formatter & Validator",
    "Rapikan (pretty print), minify, dan validasi JSON beserta pesan error.",
    r'<textarea id="t" rows="10" placeholder=\'{"nama":"AWDEV"}\'></textarea><button class="btn" id="f">Format</button><button class="btn" id="m">Minify</button><div class="out" id="o"></div>',
    r"""function run(ind){try{var j=JSON.parse($('t').value);$('t').value=JSON.stringify(j,null,ind);$('o').textContent='✅ JSON valid'}catch(x){$('o').textContent='❌ '+x.message}}
$('f').onclick=function(){run(2)};$('m').onclick=function(){run(0)}""",
    ["Tempel JSON.", "Klik Format atau Minify."],
    [("Mengapa JSON saya tidak valid?", "Penyebab umum: koma berlebih, kutip tunggal, atau key tanpa kutip ganda."), ("Apakah data dikirim ke server?", "Tidak.")], groups=["developer"]))

GENERAL.append(tool("password-generator", "Generator Password Acak yang Kuat",
    "Buat password acak aman memakai crypto.getRandomValues, dengan panjang dan jenis karakter yang bisa diatur.",
    r"""<label>Panjang: <b id="lv">16</b></label><input type="range" id="len" min="8" max="64" value="16">
<label><input type="checkbox" id="u" checked> Huruf besar</label><label><input type="checkbox" id="l" checked> Huruf kecil</label><label><input type="checkbox" id="n" checked> Angka</label><label><input type="checkbox" id="s" checked> Simbol</label>
<button class="btn" id="g">Buat Password</button><div class="out big" id="o" style="font-size:1.2rem"></div>""",
    r"""function gen(){var set='';if($('u').checked)set+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';if($('l').checked)set+='abcdefghijklmnopqrstuvwxyz';if($('n').checked)set+='0123456789';if($('s').checked)set+='!@#$%^&*()-_=+[]{};:,.?';
if(!set){$('o').textContent='Pilih minimal satu jenis karakter';return}var n=+$('len').value,a=new Uint32Array(n);crypto.getRandomValues(a);var r='';for(var i=0;i<n;i++)r+=set[a[i]%set.length];$('o').textContent=r}
$('len').oninput=function(){$('lv').textContent=this.value};$('g').onclick=gen;gen();""",
    ["Atur panjang dan jenis karakter.", "Klik Buat Password dan salin hasilnya."],
    [("Seberapa panjang password aman?", "Minimal 12–16 karakter acak; lebih panjang lebih baik."), ("Apakah password disimpan?", "Tidak, dibuat di browser Anda saja.")], groups=["developer"]))

GENERAL.append(tool("color-converter", "Konverter Warna HEX ⇄ RGB ⇄ HSL",
    "Konversi kode warna HEX ke RGB dan HSL dengan pemilih warna interaktif.",
    r'<input type="color" id="p" value="#1a73e8"><input id="h" value="#1a73e8"><div class="out" id="o"></div>',
    r"""function h2r(h){h=h.replace('#','');if(h.length==3)h=h.split('').map(function(c){return c+c}).join('');var n=parseInt(h,16);return[(n>>16)&255,(n>>8)&255,n&255]}
function r2l(r,g,b){r/=255;g/=255;b/=255;var mx=Math.max(r,g,b),mn=Math.min(r,g,b),h=0,s=0,l=(mx+mn)/2;if(mx!=mn){var d=mx-mn;s=l>.5?d/(2-mx-mn):d/(mx+mn);h=mx==r?(g-b)/d+(g<b?6:0):mx==g?(b-r)/d+2:(r-g)/d+4;h*=60}return[Math.round(h),Math.round(s*100),Math.round(l*100)]}
function u(v){if(!/^#?([0-9a-f]{3}|[0-9a-f]{6})$/i.test(v)){$('o').textContent='HEX tidak valid';return}var c=h2r(v),l=r2l(c[0],c[1],c[2]);$('o').innerHTML='<div style="height:50px;border-radius:8px;background:'+v+'"></div>RGB: <b>rgb('+c.join(', ')+')</b><br>HSL: <b>hsl('+l[0]+', '+l[1]+'%, '+l[2]+'%)</b>'}
$('p').oninput=function(){$('h').value=this.value;u(this.value)};$('h').oninput=function(){u(this.value)};u('#1a73e8')""",
    ["Pilih warna atau ketik kode HEX.", "Salin nilai RGB/HSL."],
    [("Apa itu HSL?", "Hue, Saturation, Lightness: cara menyatakan warna yang lebih intuitif."), ("HEX 3 digit didukung?", "Ya, misalnya #fff.")], groups=["design"]))

GENERAL.append(tool("uuid-generator", "UUID v4 Generator",
    "Buat satu atau banyak UUID versi 4 acak.",
    r'<label>Jumlah</label><input id="n" type="number" value="5" min="1" max="100"><button class="btn" id="g">Generate</button><textarea id="o" rows="8" readonly></textarea>',
    r"""function gen(){var n=Math.min(100,Math.max(1,+$('n').value||1)),r=[];for(var i=0;i<n;i++)r.push(crypto.randomUUID());$('o').value=r.join('\n')}$('g').onclick=gen;gen()""",
    ["Isi jumlah UUID.", "Klik Generate dan salin."],
    [("Apakah UUID unik?", "Peluang bentrok UUID v4 sangat kecil secara praktis."), ("Bisa untuk primary key?", "Bisa, namun perhatikan performa indeks pada database besar.")], groups=["developer"]))

GENERAL.append(tool("hash-generator", "Generator Hash SHA-1, SHA-256, SHA-512",
    "Hitung hash SHA dari teks memakai Web Crypto API di browser.",
    r'<textarea id="t" rows="4"></textarea><div class="out" id="o"></div>',
    r"""async function H(a,s){var b=await crypto.subtle.digest(a,new TextEncoder().encode(s));return Array.from(new Uint8Array(b)).map(function(x){return x.toString(16).padStart(2,'0')}).join('')}
$('t').oninput=async function(){var s=this.value;$('o').innerHTML='SHA-1:<br><code>'+await H('SHA-1',s)+'</code><br>SHA-256:<br><code>'+await H('SHA-256',s)+'</code><br>SHA-512:<br><code>'+await H('SHA-512',s)+'</code>'};$('t').oninput.call($('t'))""",
    ["Ketik teks.", "Hash tampil otomatis."],
    [("Apakah hash bisa dibalik?", "Tidak, hash adalah fungsi satu arah."), ("Aman untuk password?", "Jangan simpan password dengan SHA polos; gunakan bcrypt/argon2.")], groups=["developer"]))

GENERAL.append(tool("timestamp-converter", "Konverter Unix Timestamp ⇄ Tanggal",
    "Ubah Unix timestamp (detik/milidetik) menjadi tanggal dan sebaliknya.",
    r'<input id="ts" placeholder="Unix timestamp"><div class="out" id="o1"></div><input type="datetime-local" id="dt"><div class="out" id="o2"></div><button class="btn" id="now">Sekarang</button>',
    r"""$('ts').oninput=function(){var v=+this.value;if(!v){$('o1').textContent='';return}var d=new Date(v<1e12?v*1000:v);$('o1').textContent=isNaN(d)?'Tidak valid':d.toString()+' | UTC: '+d.toISOString()};
$('dt').oninput=function(){var d=new Date(this.value);$('o2').textContent=isNaN(d)?'':'Detik: '+Math.floor(d/1000)+' | Milidetik: '+d.getTime()};
$('now').onclick=function(){$('ts').value=Math.floor(Date.now()/1000);$('ts').oninput()}""",
    ["Isi timestamp atau pilih tanggal.", "Lihat hasil konversi."],
    [("Detik atau milidetik?", "Tool menebak: angka di bawah 1e12 dianggap detik."), ("Zona waktu?", "Ditampilkan lokal dan UTC.")], groups=["developer"]))

GENERAL.append(tool("age-calculator", "Kalkulator Umur Tepat (Tahun, Bulan, Hari)",
    "Hitung umur dari tanggal lahir dan hari menuju ulang tahun berikutnya.",
    r'<label>Tanggal lahir</label><input type="date" id="b"><div class="out" id="o"></div>',
    r"""$('b').oninput=function(){var b=new Date(this.value),n=new Date();if(isNaN(b)||b>n){$('o').textContent='Tanggal tidak valid';return}
var y=n.getFullYear()-b.getFullYear(),m=n.getMonth()-b.getMonth(),d=n.getDate()-b.getDate();if(d<0){m--;d+=new Date(n.getFullYear(),n.getMonth(),0).getDate()}if(m<0){y--;m+=12}
var nx=new Date(n.getFullYear(),b.getMonth(),b.getDate());if(nx<=n)nx.setFullYear(n.getFullYear()+1);
$('o').innerHTML='Umur: <span class="big">'+y+' tahun '+m+' bulan '+d+' hari</span><br>Ulang tahun berikutnya: '+Math.ceil((nx-n)/864e5)+' hari lagi'}""",
    ["Pilih tanggal lahir."], [("Apakah memperhitungkan tahun kabisat?", "Ya, memakai objek Date."), ("Hari lahir?", "Tidak ditampilkan di versi ini.")], groups=["calculator"]))

GENERAL.append(tool("bmi-calculator", "Kalkulator BMI (Indeks Massa Tubuh)",
    "Hitung BMI dari berat dan tinggi badan beserta kategori menurut WHO.",
    r'<div class="row"><input id="w" type="number" placeholder="Berat (kg)"><input id="h" type="number" placeholder="Tinggi (cm)"></div><button class="btn" id="g">Hitung</button><div class="out" id="o"></div>',
    r"""$('g').onclick=function(){var w=+$('w').value,h=+$('h').value/100;if(!w||!h)return;var b=w/(h*h),c=b<18.5?'Kurus':b<25?'Normal':b<30?'Kelebihan berat':'Obesitas';$('o').innerHTML='BMI: <span class="big">'+b.toFixed(1)+'</span> — '+c}""",
    ["Isi berat dan tinggi.", "Klik Hitung."],
    [("Batas BMI normal?", "18,5–24,9 menurut WHO (kategori Asia dapat berbeda)."), ("Apakah ini diagnosis?", "Bukan. BMI tidak membedakan massa otot dan lemak; konsultasikan ke tenaga kesehatan.")], groups=["calculator"]))

GENERAL.append(tool("percentage-calculator", "Kalkulator Persen",
    "Hitung X% dari Y, X adalah berapa persen dari Y, dan perubahan persentase.",
    r"""<div class="row"><input id="a1" type="number" placeholder="X"><input id="b1" type="number" placeholder="Y"></div><button class="btn" id="g1">X% dari Y</button><button class="btn" id="g2">X adalah …% dari Y</button><button class="btn" id="g3">Perubahan X → Y</button><div class="out" id="o"></div>""",
    r"""var a=function(){return +$('a1').value},b=function(){return +$('b1').value};
$('g1').onclick=function(){$('o').textContent=a()+'% dari '+b()+' = '+(a()/100*b())};
$('g2').onclick=function(){$('o').textContent=b()?a()+' adalah '+(a()/b()*100).toFixed(2)+'% dari '+b():'Y tidak boleh 0'};
$('g3').onclick=function(){$('o').textContent=a()?'Perubahan dari '+a()+' ke '+b()+': '+((b()-a())/Math.abs(a())*100).toFixed(2)+'%':'X tidak boleh 0'}""",
    ["Isi X dan Y.", "Pilih jenis perhitungan."], [("Rumus persen?", "Persen = bagian ÷ total × 100."), ("Kenaikan atau penurunan?", "Tanda minus berarti turun.")], groups=["calculator"]))

GENERAL.append(tool("kpr-calculator", "Kalkulator Cicilan KPR & Pinjaman",
    "Simulasi cicilan bulanan KPR atau kredit anuitas dari harga, uang muka, bunga, dan tenor.",
    r"""<label>Harga properti / pinjaman (Rp)</label><input id="p" type="number" value="500000000"><label>Uang muka (%)</label><input id="d" type="number" value="20"><label>Bunga per tahun (%)</label><input id="r" type="number" step="0.01" value="9"><label>Tenor (tahun)</label><input id="y" type="number" value="15"><button class="btn" id="g">Hitung</button><div class="out" id="o"></div>""",
    r"""$('g').onclick=function(){var P=+$('p').value*(1-(+$('d').value)/100),r=(+$('r').value)/1200,n=(+$('y').value)*12;if(!P||!n)return;var m=r?P*r/(1-Math.pow(1+r,-n)):P/n;
$('o').innerHTML='Pokok pinjaman: '+idr(P)+'<br>Cicilan/bulan: <span class="big">'+idr(m)+'</span><br>Total bayar: '+idr(m*n)+'<br>Total bunga: '+idr(m*n-P)+'<br><small>Simulasi bunga tetap (anuitas). Bunga KPR floating dan biaya admin berbeda per bank.</small>'}""",
    ["Isi harga, uang muka, bunga, dan tenor.", "Klik Hitung."],
    [("Rumus cicilan?", "Anuitas: M = P·r / (1 − (1+r)^−n)."), ("Apakah termasuk asuransi/provisi?", "Tidak.")], groups=["calculator", "finance"]))

GENERAL.append(tool("qr-generator", "QR Code Generator Gratis",
    "Buat QR code dari teks atau URL dan unduh sebagai gambar.",
    r'<input id="t" placeholder="https://awdev.my.id"><button class="btn" id="g">Buat QR</button><div id="q" style="margin:15px 0"></div><a class="btn" id="dl" style="display:none" download="qr.png">Unduh PNG</a>',
    r"""$('g').onclick=function(){var v=$('t').value.trim();if(!v)return;$('q').innerHTML='';new QRCode($('q'),{text:v,width:256,height:256});
setTimeout(function(){var c=$('q').querySelector('canvas'),i=$('q').querySelector('img'),s=(i&&i.src)||(c&&c.toDataURL());if(s){$('dl').href=s;$('dl').style.display='inline-block'}},300)}""",
    ["Ketik teks atau URL.", "Klik Buat QR lalu unduh."],
    [("Apakah QR kedaluwarsa?", "QR statis tidak kedaluwarsa."), ("Ukuran data?", "Semakin panjang teks, semakin padat QR.")], groups=["design"],
    scripts='<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>'))

# =============================================================== CONVERTERS
DISPLAY = {"mmhg": "mmHg", "btu": "BTU", "psi": "PSI", "hz": "Hz", "khz": "kHz", "mhz": "MHz", "ghz": "GHz",
           "galon-as": "Galon (AS)", "quart-as": "Quart (AS)", "cangkir-as": "Cangkir (AS)", "ons-inggris": "Ons (Inggris)", "pon": "Pon (lb)"}
CONV = {
    "Panjang": [("meter", "m", 1), ("kilometer", "km", 1000), ("sentimeter", "cm", .01), ("milimeter", "mm", .001), ("mil", "mi", 1609.344), ("yard", "yd", .9144), ("kaki", "ft", .3048), ("inci", "in", .0254), ("mil-laut", "nmi", 1852)],
    "Massa": [("kilogram", "kg", 1), ("gram", "g", .001), ("miligram", "mg", 1e-6), ("ton", "t", 1000), ("pon", "lb", .45359237), ("ons-inggris", "oz", .028349523125), ("kuintal", "kuintal", 100)],
    "Volume": [("liter", "L", 1), ("mililiter", "mL", .001), ("meter-kubik", "m³", 1000), ("galon-as", "gal", 3.785411784), ("quart-as", "qt", .946352946), ("cangkir-as", "cup", .2365882365), ("sendok-makan", "tbsp", .01478676478), ("sendok-teh", "tsp", .004928921594)],
    "Luas": [("meter-persegi", "m²", 1), ("kilometer-persegi", "km²", 1e6), ("hektare", "ha", 1e4), ("are", "are", 100), ("acre", "ac", 4046.8564224), ("kaki-persegi", "ft²", .09290304), ("inci-persegi", "in²", .00064516), ("mil-persegi", "mi²", 2589988.110336)],
    "Kecepatan": [("meter-per-detik", "m/s", 1), ("kilometer-per-jam", "km/j", 1 / 3.6), ("mil-per-jam", "mph", .44704), ("knot", "kn", 1852 / 3600), ("kaki-per-detik", "ft/s", .3048)],
    "Data": [("byte", "B", 1), ("kilobyte", "KB", 1024), ("megabyte", "MB", 1024 ** 2), ("gigabyte", "GB", 1024 ** 3), ("terabyte", "TB", 1024 ** 4), ("petabyte", "PB", 1024 ** 5), ("bit", "bit", .125)],
    "Waktu": [("detik", "s", 1), ("menit", "mnt", 60), ("jam", "jam", 3600), ("hari", "hari", 86400), ("minggu", "mgg", 604800), ("tahun", "thn", 31557600)],
    "Energi": [("joule", "J", 1), ("kilojoule", "kJ", 1000), ("kalori", "cal", 4.184), ("kilokalori", "kcal", 4184), ("kilowatt-jam", "kWh", 3.6e6), ("btu", "BTU", 1055.05585262)],
    "Tekanan": [("pascal", "Pa", 1), ("kilopascal", "kPa", 1000), ("bar", "bar", 1e5), ("atmosfer", "atm", 101325), ("psi", "psi", 6894.757293168), ("mmhg", "mmHg", 133.322387415)],
    "Daya": [("watt", "W", 1), ("kilowatt", "kW", 1000), ("tenaga-kuda", "hp", 745.69987158227)],
    "Sudut": [("derajat", "°", 1), ("radian", "rad", 57.29577951308232), ("gradian", "grad", .9), ("putaran", "rev", 360)],
    "Frekuensi": [("hertz", "Hz", 1), ("kilohertz", "kHz", 1e3), ("megahertz", "MHz", 1e6), ("gigahertz", "GHz", 1e9)],
}
TEMPS = [("celsius", "°C"), ("fahrenheit", "°F"), ("kelvin", "K")]


def disp(slug):
    return DISPLAY.get(slug, slug.replace("-", " ").title())


def temp_conv(v, a, b):
    c = v if a == "celsius" else (v - 32) * 5 / 9 if a == "fahrenheit" else v - 273.15
    return c if b == "celsius" else c * 9 / 5 + 32 if b == "fahrenheit" else c + 273.15


def num(x):
    return f"{x:.10g}"


def build_converters():
    pages, seen = [], set()
    for cat, units in CONV.items():
        for a in units:
            for b in units:
                if a is b:
                    continue
                slug = f"{a[0]}-ke-{b[0]}"
                assert slug not in seen, slug
                seen.add(slug)
                pages.append(dict(kind="lin", cat=cat, a=a, b=b, slug=slug,
                                  fa=a[2], fb=b[2], ratio=a[2] / b[2]))
    for a in TEMPS:
        for b in TEMPS:
            if a is b:
                continue
            slug = f"{a[0]}-ke-{b[0]}"
            assert slug not in seen, slug
            seen.add(slug)
            pages.append(dict(kind="temp", cat="Suhu", a=(a[0], a[1], 0), b=(b[0], b[1], 0), slug=slug))
    return pages


def conv_tool(p, siblings):
    an, bn = disp(p["a"][0]), disp(p["b"][0])
    title = f"Konversi {an} ke {bn} ({p['a'][1]} ke {p['b'][1]})"
    if p["kind"] == "lin":
        ratio = p["ratio"]
        rows = [(v, v * ratio) for v in (1, 5, 10, 25, 50, 100, 500, 1000)]
        formula = f"1 {an} = {num(ratio)} {bn}. Rumus: {bn} = {an} × {num(ratio)}."
        js = ("var R=%r;function f(x){return Number(x.toPrecision(12)).toLocaleString('id-ID',{maximumSignificantDigits:12})}"
              "function u(){var v=parseFloat($('v').value.replace(',','.'));$('o').innerHTML=isNaN(v)?'':'<span class=\"big\">'+f(v*R)+'</span> %s'}"
              "$('v').oninput=u;u();") % (ratio, e(p["b"][1]))
        faq1 = (f"1 {an} berapa {bn}?", f"1 {an} sama dengan {num(ratio)} {bn}.")
    else:
        rows = [(v, temp_conv(v, p["a"][0], p["b"][0])) for v in (-40, 0, 20, 37, 100)]
        formulas = {("celsius", "fahrenheit"): "°F = °C × 9/5 + 32", ("fahrenheit", "celsius"): "°C = (°F − 32) × 5/9",
                    ("celsius", "kelvin"): "K = °C + 273,15", ("kelvin", "celsius"): "°C = K − 273,15",
                    ("fahrenheit", "kelvin"): "K = (°F − 32) × 5/9 + 273,15", ("kelvin", "fahrenheit"): "°F = (K − 273,15) × 9/5 + 32"}
        formula = "Rumus: " + formulas[(p["a"][0], p["b"][0])]
        js = ("function cv(v,a,b){var c=a=='celsius'?v:a=='fahrenheit'?(v-32)*5/9:v-273.15;return b=='celsius'?c:b=='fahrenheit'?c*9/5+32:c+273.15}"
              "function u(){var v=parseFloat($('v').value.replace(',','.'));$('o').innerHTML=isNaN(v)?'':'<span class=\"big\">'+Number(cv(v,'%s','%s').toPrecision(10)).toLocaleString('id-ID')+'</span> %s'}"
              "$('v').oninput=u;u();") % (p["a"][0], p["b"][0], e(p["b"][1]))
        faq1 = (f"Berapa 100 {an} dalam {bn}?", f"100 {p['a'][1]} = {num(temp_conv(100, p['a'][0], p['b'][0]))} {p['b'][1]}.")
    table = ("<h2>Tabel Konversi</h2><table><thead><tr><th>" + e(an) + " (" + e(p["a"][1]) + ")</th><th>" + e(bn) + " (" + e(p["b"][1]) +
             ")</th></tr></thead><tbody>" + "".join(f"<tr><td>{num(x)}</td><td>{num(y)}</td></tr>" for x, y in rows) + "</tbody></table>")
    return dict(
        slug=p["slug"], title=title,
        desc=f"Konversi {an.lower()} ke {bn.lower()} online: kalkulator instan, rumus, dan tabel nilai umum.",
        body=f'<label>Nilai dalam {e(an)} ({e(p["a"][1])})</label><input id="v" type="text" inputmode="decimal" value="1"><div class="out" id="o"></div>'
             f'<p><a href="/converter/{p["b"][0]}-ke-{p["a"][0]}.html">⇄ Balik: {e(bn)} ke {e(an)}</a></p>',
        js=js, steps=[f"Masukkan nilai dalam {an}.", f"Hasil dalam {bn} tampil otomatis.", "Klik tautan balik untuk konversi sebaliknya."],
        faq=[faq1, ("Apakah hasilnya presisi?", "Ya, dihitung dengan faktor konversi standar dan dibulatkan 12 angka signifikan.")],
        groups=["converter"], note=formula, scripts="", ext=[], extra=table, cat=p["cat"])


# =============================================================== RENDER
def render_tool(t, dir_, index_label, related):
    path = f"/{dir_}/{t['slug']}.html"
    a = {"cat": dir_, "n": t["slug"], "path": path, "title": t["title"]}
    steps = "".join(f"<li>{e(s)}</li>" for s in t["steps"])
    faq_html = "".join(f'<div class="faq-item"><div class="faq-q">{e(q)} <i class="fas fa-chevron-down"></i></div><div class="faq-a">{e(an)}</div></div>' for q, an in t["faq"])
    rel = related[:7]
    rel_html = "<ul>" + "".join(f'<li><a href="{r[1]}">{e(r[0])}</a></li>' for r in rel) + "</ul>"
    ext, seen = [], set()
    for n, u in t["ext"] + g.EXTERNAL_LINKS:
        if u not in seen:
            seen.add(u)
            ext.append((n, u))
    ext_html = "<ul>" + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(n)}</a></li>' for n, u in ext[:7]) + "</ul>"
    crumbs = [("Home", "/"), (index_label, f"/{dir_}/index.html"), (t["title"], path)]
    ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"], "description": t["desc"],
           "url": g.url(path), "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "IDR"}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": g.url(u)} for i, (n, u) in enumerate(crumbs)]},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": an}} for q, an in t["faq"]]}]
    extra_head = '<link rel="stylesheet" href="/assets/tools.css">' + "".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    note = f'<p class="meta">ℹ️ {e(t["note"])}</p>' if t.get("note") else ""
    page = g.head(t["title"], t["desc"], path, g.SITE["logo"], False, extra_head)
    page += f"""<main><article class="box">
<nav class="meta"><a href="/">Home</a> / <a href="/{dir_}/index.html">{e(index_label)}</a> / {e(t['title'])}</nav>
<h1 class="rtext">{e(t['title'])}</h1><p>{e(t['desc'])}</p>{g.ad_banner()}
<section class="inset tool">{t['body']}</section>{note}
<h2>Cara Menggunakan</h2><ol>{steps}</ol>{t.get('extra', '')}
<h2>FAQ</h2>{faq_html}
<div class="grid"><div class="card"><h4>Tools Terkait</h4>{rel_html}</div><div class="card"><h4>Referensi Eksternal</h4>{ext_html}</div></div>
</article>{g.share_html(a)}{g.contact_html()}{g.disqus_html(a)}</main>
{t['scripts']}<script>(function(){{{COMMON}{t['js']}}})();</script>"""
    return page + g.footer_html()


def render_hub(path, title, desc, items, intro=""):
    cards = "".join(f'<div class="card"><h4><a href="{u}">{e(n)}</a></h4><p style="font-size:.85rem">{e(d)}</p></div>' for n, u, d in items)
    page = g.head(title, desc, path, g.SITE["logo"], False, '<link rel="stylesheet" href="/assets/tools.css">')
    page += f'<main><section class="box"><h1 class="rtext">{e(title)}</h1><p>{e(desc)}</p>{intro}</section>{g.ad_banner()}<section class="box"><div class="grid">{cards}</div></section>{g.share_html({"path": path, "title": title})}{g.contact_html()}</main>'
    return page + g.footer_html()


def write(path, content):
    f = OUT / path.lstrip("/")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["islamic", "general", "converter"])
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    conv = build_converters()
    total = len(ISLAMIC) + len(GENERAL) + len(conv)
    print(f"Tools terdaftar: {len(ISLAMIC)} islamic + {len(GENERAL)} umum + {len(conv)} konverter = {total}")
    if args.list:
        return
    urls, today = [], date.today().isoformat()
    write("/assets/tools.css", TOOL_CSS.strip())

    if args.only in (None, "islamic"):
        items = [(t["title"], f"/islamic-tools/{t['slug']}.html", t["desc"]) for t in ISLAMIC]
        for t in ISLAMIC:
            rel = [(x["title"], f"/islamic-tools/{x['slug']}.html") for x in ISLAMIC if x is not t]
            write(f"/islamic-tools/{t['slug']}.html", render_tool(t, "islamic-tools", "Islamic Tools", rel))
            urls.append(f"/islamic-tools/{t['slug']}.html")
        write("/islamic-tools/index.html", render_hub("/islamic-tools/index.html", "Islamic Tools: Kiblat, Waktu Salat, Zakat & Lainnya",
                                                      "Kumpulan alat ibadah yang berjalan di browser.", items,
                                                      '<p>' + " · ".join(f'<a href="/islamic-tools/{k}.html">{e(v[0])}</a>' for k, v in HUBS.items()) + '</p>'))
        urls.append("/islamic-tools/index.html")
        for k, (name, desc) in HUBS.items():
            its = [(t["title"], f"/islamic-tools/{t['slug']}.html", t["desc"]) for t in ISLAMIC if k in t["groups"]]
            write(f"/islamic-tools/{k}.html", render_hub(f"/islamic-tools/{k}.html", f"Islamic Tools - {name}", desc, its))
            urls.append(f"/islamic-tools/{k}.html")
        for al, real in ALIASES.items():
            tgt = g.url(f"/islamic-tools/{real}.html")
            write(f"/islamic-tools/{al}.html", f'<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><title>Redirect</title><link rel="canonical" href="{tgt}"><meta http-equiv="refresh" content="0;url=/islamic-tools/{real}.html"><meta name="robots" content="noindex"></head><body><a href="/islamic-tools/{real}.html">Lanjut</a></body></html>')

    if args.only in (None, "general"):
        for t in GENERAL:
            rel = [(x["title"], f"/tools/{x['slug']}.html") for x in GENERAL if x is not t and set(x["groups"]) & set(t["groups"])]
            rel += [(x["title"], f"/tools/{x['slug']}.html") for x in GENERAL if x is not t and (x["title"], f"/tools/{x['slug']}.html") not in rel]
            write(f"/tools/{t['slug']}.html", render_tool(t, "tools", "Tools", rel))
            urls.append(f"/tools/{t['slug']}.html")
        items = [(t["title"], f"/tools/{t['slug']}.html", t["desc"]) for t in GENERAL]
        items += [("Islamic Tools", "/islamic-tools/index.html", "Kiblat, waktu salat, zakat, Al-Qur'an."), ("Converter Satuan", "/converter/index.html", "Ratusan konverter satuan.")]
        write("/tools/index.html", render_hub("/tools/index.html", "Tools Gratis untuk Developer, Desainer & Umum", "Utilitas online gratis yang berjalan di browser.", items))
        urls.append("/tools/index.html")

    if args.only in (None, "converter"):
        by_cat = {}
        for p in conv:
            t = conv_tool(p, None)
            same = [(disp(x["b"][0]), f"/converter/{x['slug']}.html") for x in conv if x["cat"] == p["cat"] and x["a"][0] == p["a"][0] and x is not p]
            rel = [(f"{disp(x['a'][0])} ke {disp(x['b'][0])}", u) for x, (_, u) in zip([x for x in conv if x["cat"] == p["cat"] and x["a"][0] == p["a"][0] and x is not p], same)]
            write(f"/converter/{p['slug']}.html", render_tool(t, "converter", "Converter", rel))
            urls.append(f"/converter/{p['slug']}.html")
            by_cat.setdefault(p["cat"], []).append((f"{disp(p['a'][0])} ke {disp(p['b'][0])}", f"/converter/{p['slug']}.html", f"{p['a'][1]} → {p['b'][1]}"))
        body = "".join(f'<section class="box"><h2>{e(c)}</h2><div class="grid">' + "".join(f'<div class="card"><a href="{u}">{e(n)}</a></div>' for n, u, _ in its) + '</div></section>' for c, its in by_cat.items())
        page = g.head("Converter Satuan Online", f"{len(conv)} konverter satuan: panjang, massa, suhu, volume, dan lainnya.", "/converter/index.html", g.SITE["logo"], False, '<link rel="stylesheet" href="/assets/tools.css">')
        page += f'<main><section class="box"><h1 class="rtext">Converter Satuan Online</h1><p>{len(conv)} konverter satuan gratis.</p></section>{g.ad_banner()}{body}</main>'
        write("/converter/index.html", page + g.footer_html())
        urls.append("/converter/index.html")

    sm = "".join(f"<url><loc>{g.url(u)}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    write("/sitemap-tools.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + sm + "</urlset>")
    robots = OUT / "robots.txt"
    line = f"Sitemap: {g.url('/sitemap-tools.xml')}\n"
    txt = robots.read_text(encoding="utf-8") if robots.exists() else "User-agent: *\nAllow: /\n"
    if "sitemap-tools.xml" not in txt:
        robots.write_text(txt.rstrip("\n") + "\n" + line, encoding="utf-8")
    print(f"Selesai: {len(urls)} halaman ditulis, sitemap-tools.xml dibuat.")


if __name__ == "__main__":
    main()
