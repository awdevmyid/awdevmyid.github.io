#!/usr/bin/env python3
"""
AWDEV static blog generator  (untuk GitHub Pages: awdevmyid.github.io)

Struktur output per kategori:
  /<kategori>/index.html, artikel1..N.html, sitemap.html, sitemap.xml, sitemap.txt
Global: /sitemap.xml, /robots.txt, /assets/style.css, /assets/app.js

Isi artikel dibaca dari:  content/<kategori>/artikelN.json
Halaman tanpa file JSON dibuat sebagai DRAFT: noindex + tidak masuk sitemap
(supaya tidak ada halaman kosong/tipis yang diindeks Google).

Pemakaian:
  python generator.py --scaffold            # buat kerangka JSON untuk diisi
  python generator.py                       # generate semua halaman
  python generator.py --only property       # satu kategori saja
  python generator.py --pages 30 --push     # generate lalu git commit + push
"""
import argparse, hashlib, html, json, subprocess
from datetime import date
from pathlib import Path

# ----------------------------------------------------------------- CONFIG
SITE = {
    "base_url": "https://awdevmyid.github.io",
    "name": "AWDEV CORPORATION",
    "brand": "AWDEV CORP",
    "logo": "https://awdev.my.id/img/awdev.png",
    "favicon": "https://awdev.my.id/favicon.png",
    "adsense_client": "ca-pub-5407249785989200",
    "adsense_slot": "0000000000",  # ganti dengan ad slot ID banner Anda
    "gsc_verification": "OLryKZ1dDupEH_xOuZWiEwdi0ZvuXMcnQeMjRwe5YCw",
    "disqus": "awdevgithub",
    "email": "support@awdev.my.id",
    "year": date.today().year,
}

CATEGORIES = [
    "aplikasi", "calligraphy", "code", "collor", "converter", "devoloper", "domain",
    "domains", "eq", "finder", "hook", "img", "ip", "kodepost", "link", "maps", "pdf",
    "qr", "quran", "removebg", "safelink", "search", "seo", "source", "text", "tools",
    "utilities", "vidio",
    "market", "finance", "macro", "micro", "economy", "explainers", "manufacturing",
    "property", "health", "education", "lifestyle", "hospitality", "tech", "media",
    "smes", "luxury", "politics", "culture", "science", "public-policy", "business",
    "news", "sports", "arts", "celebrities", "automotive", "commentary", "interview",
    "money", "perbankan", "belanja", "sharia", "football", "opinion", "video", "kisah",
    "sejarah", "entrepreneur", "research", "photo", "olahraga", "selebritis",
    "dki", "diy", "jabar", "jatim", "jateng", "aceh", "papua", "kalimantan", "sumatra",
    "sulawesi", "bali", "asia", "afrika", "australia", "rusia", "eropa", "amerika",
    "ai", "teknologi", "astronomi", "zodiak",
    "islamic", "biografi-ulama", "kisah-hikmah", "kisah-sejarah", "info",
    "kisah-birrul-walidain", "kisah-hidayah-islam", "kisah-kaum-durhaka",
    "kisah-masa-depan", "kisah-nabi-dan-rasul", "kisah-nabi-muhammad", "kisah-nyata",
    "kisah-orang-shalih", "kisah-pilihan", "kisah-sahabat-nabi", "kisah-tabiin",
    "kisah-tak-nyata", "kisah-umat-terdahulu", "sejarah-islam", "nusantara",
    "laporan-produksi", "merchandise-yufid", "mutiara-faidah", "teladan-muslimah",
    "books", "download",
    "islamic-tools", "qibla", "prayer-times", "hijri-calendar", "zakat-calculator",
    "salah-tracker", "mosque-finder", "worship", "trackers", "calculators",
    "knowledge", "finders", "duas", "halal-food", "timer", "calendar", "cuaca",
]

NAV = [
    ("Home", "/"), ("About", "/about.html"), ("Blog", "/blog.html"),
    ("Tools", "/tools/index.html"), ("Aplikasi", "/aplikasi/index.html"),
    ("SEO", "/seo/index.html"), ("Source", "/source/index.html"),
    ("QR", "/qr/index.html"), ("Color", "/collor/index.html"),
    ("Maps", "/maps/index.html"), ("Video", "/vidio/index.html"),
]

EXTERNAL_LINKS = [
    ("GitHub", "https://github.com/"),
    ("MDN Web Docs", "https://developer.mozilla.org/"),
    ("Google Search Central", "https://developers.google.com/search"),
    ("W3C", "https://www.w3.org/"),
    ("Schema.org", "https://schema.org/"),
    ("Wikipedia", "https://id.wikipedia.org/"),
    ("Stack Overflow", "https://stackoverflow.com/"),
]

FOOTER_LINKS = [
    ("Home", "/"), ("About Us", "/about.html"), ("Blog", "/blog.html"),
    ("Contact", "/contact.html"), ("Privacy Policy", "/privacy-policy.html"),
    ("Terms & Conditions", "/terms.html"), ("Disclaimers", "/disclaimers.html"),
    ("License", "/license.html"),
]

ROOT = Path(__file__).parent
OUT = ROOT            # tulis langsung ke root repo agar URL sesuai root
CONTENT = ROOT / "content"


# ----------------------------------------------------------------- HELPERS
def e(s):
    return html.escape(str(s), quote=True)


def label(slug):
    return slug.replace("-", " ").title()


def url(path):
    return SITE["base_url"] + path


def hash_rank(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def load_article(cat, n):
    f = CONTENT / cat / f"artikel{n}.json"
    if f.exists():
        d = json.loads(f.read_text(encoding="utf-8"))
        d["draft"] = False
    else:
        d = {
            "title": f"{label(cat)} - Artikel {n} (draft)",
            "description": f"Draft artikel {n} kategori {label(cat)}.",
            "date": "2026-01-01",
            "image": SITE["logo"],
            "image_alt": f"Ilustrasi {label(cat)}",
            "intro": "Artikel ini belum ditulis.",
            "sections": [],
            "faq": [],
            "conclusion": "",
            "draft": True,
        }
    d["n"] = n
    d["cat"] = cat
    d["path"] = f"/{cat}/artikel{n}.html"
    d.setdefault("date", "2026-01-01")
    d.setdefault("image", SITE["logo"])
    d.setdefault("image_alt", d["title"])
    d.setdefault("description", d["title"])
    return d


def word_count(a):
    txt = a.get("intro", "") + a.get("conclusion", "")
    for s in a.get("sections", []):
        txt += " ".join(s.get("paragraphs", []))
        for sub in s.get("subsections", []):
            txt += " ".join(sub.get("paragraphs", []))
    return len(txt.split())


# ----------------------------------------------------------------- ASSETS
CSS = """
:root{--bg:#e4ebf5;--dark:#c5d1e0;--light:#fff;--text:#333;--primary:#1a73e8;
--rainbow:linear-gradient(135deg,#ff3366,#ff9933,#33cc66,#3399ff,#9933ff)}
*{box-sizing:border-box;margin:0;padding:0;font-family:'Poppins',sans-serif}
body{background:var(--bg);color:var(--text);line-height:1.7;padding:20px;max-width:1100px;margin:auto}
a{color:#ff3366}
.rainbow-bar{height:6px;background:var(--rainbow);border-radius:3px;margin-bottom:20px}
.rtext{background:var(--rainbow);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.box{background:var(--bg);box-shadow:8px 8px 16px var(--dark),-8px -8px 16px var(--light);border-radius:16px;padding:20px;margin-bottom:30px}
.inset{background:var(--bg);box-shadow:inset 4px 4px 8px var(--dark),inset -4px -4px 8px var(--light);border-radius:12px;padding:15px}
.btn{background:var(--bg);box-shadow:5px 5px 10px var(--dark),-5px -5px 10px var(--light);border:0;border-radius:8px;padding:10px 20px;cursor:pointer;color:var(--text);font-weight:600;text-decoration:none;display:inline-block}
.btn:hover{box-shadow:inset 3px 3px 6px var(--dark),inset -3px -3px 6px var(--light);color:#ff3366}
header.box{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
.logo-area{display:flex;align-items:center;gap:15px;text-decoration:none}
.logo-img{width:50px;height:50px;border-radius:50%;object-fit:cover}
.logo-text{font-size:1.5rem;font-weight:700}
.dropdown{position:relative}
.dropbtn{background:var(--bg);box-shadow:5px 5px 10px var(--dark),-5px -5px 10px var(--light);padding:10px 18px;border:0;border-radius:10px;color:var(--primary);font-weight:600;cursor:pointer}
.dropdown-content{display:none;position:absolute;right:0;background:var(--bg);min-width:230px;box-shadow:8px 8px 16px var(--dark);z-index:100;border-radius:12px;padding:10px 0;max-height:350px;overflow-y:auto}
.dropdown:hover .dropdown-content,.dropdown.open .dropdown-content{display:block}
.dropdown-content a{display:block;padding:9px 20px;color:var(--text);text-decoration:none;font-size:13px}
.dropdown-content a:hover{color:#ff3366}
h1{font-size:2rem;margin-bottom:10px}h2{margin:25px 0 10px}h3{margin:18px 0 8px;color:var(--primary)}
p{margin-bottom:14px;text-align:justify}
.hero img,.article img{max-width:100%;border-radius:12px;margin:10px 0}
.meta{font-size:.85rem;color:#666;margin-bottom:10px}
.toc ol{padding-left:22px}.toc li{margin-bottom:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:15px}
.card{padding:15px;border-radius:10px;box-shadow:5px 5px 10px var(--dark),-5px -5px 10px var(--light)}
.card img{width:100%;height:150px;object-fit:cover;border-radius:8px}
.card h4{margin:8px 0}.card a{text-decoration:none}
.labels a,.archive a{display:inline-block;margin:4px;padding:6px 14px;border-radius:20px;background:var(--bg);box-shadow:3px 3px 6px var(--dark),-3px -3px 6px var(--light);text-decoration:none;font-size:.85rem}
.faq-item{margin-bottom:12px}.faq-q{font-weight:600;cursor:pointer;display:flex;justify-content:space-between}
.faq-a{display:none;margin-top:8px;color:#555}.faq-item.active .faq-a{display:block}
.share{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.share a{padding:10px 16px;border-radius:25px;text-decoration:none;font-weight:600;background:var(--bg);box-shadow:5px 5px 10px var(--dark),-5px -5px 10px var(--light)}
.contact input,.contact textarea{width:100%;padding:12px;margin-bottom:12px;border:0;border-radius:8px;background:var(--bg);box-shadow:inset 4px 4px 8px var(--dark),inset -4px -4px 8px var(--light);outline:0}
.ad{text-align:center;min-height:90px;margin:20px 0}
table{width:100%;border-collapse:collapse;margin:14px 0}th,td{padding:10px;border-bottom:1px solid #ccd5e3;text-align:left}
footer{text-align:center;margin-top:40px;font-size:14px;color:#666}
footer .links{display:flex;flex-wrap:wrap;gap:15px;justify-content:center;margin-top:10px}
footer a{color:var(--primary);text-decoration:none}
@media(max-width:768px){h1{font-size:1.6rem}}
"""

JS = """
document.querySelectorAll('.faq-q').forEach(function(q){
  q.addEventListener('click',function(){q.parentElement.classList.toggle('active');});
});
var dd=document.querySelector('.dropdown');
if(dd){dd.querySelector('.dropbtn').addEventListener('click',function(){dd.classList.toggle('open');});}
"""


# ----------------------------------------------------------------- BLOCKS
def head(title, desc, path, image, noindex=False, extra=""):
    canon = url(path)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else \
             '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f"""<!DOCTYPE html>
<html lang="id"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} | {e(SITE['name'])}</title>
<meta name="description" content="{e(desc[:160])}">
<meta name="author" content="{e(SITE['name'])}">
{robots}
<link rel="canonical" href="{e(canon)}">
<meta property="og:type" content="article"><meta property="og:url" content="{e(canon)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc[:160])}">
<meta property="og:image" content="{e(image)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc[:160])}"><meta name="twitter:image" content="{e(image)}">
<link rel="icon" type="image/png" href="{e(SITE['favicon'])}">
<meta name="google-site-verification" content="{SITE['gsc_verification']}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={SITE['adsense_client']}" crossorigin="anonymous"></script>
<meta name="google-adsense-account" content="{SITE['adsense_client']}">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="/assets/style.css">
{extra}
</head><body>
<div class="rainbow-bar"></div>
{header_html()}
"""


def header_html():
    links = "".join(f'<a href="{p}">{e(n)}</a>' for n, p in NAV)
    return f"""<header class="box">
<a class="logo-area" href="/"><img class="logo-img" src="{e(SITE['logo'])}" alt="Logo {e(SITE['name'])}">
<span class="logo-text rtext">{e(SITE['brand'])}</span></a>
<div class="dropdown"><button class="dropbtn" type="button"><i class="fas fa-bars"></i> Navigation Menu</button>
<div class="dropdown-content">{links}</div></div></header>"""


def footer_html():
    links = " | ".join(f'<a href="{p}">{e(n)}</a>' for n, p in FOOTER_LINKS)
    return f"""<footer><div class="inset"><p>&copy; {SITE['year']} awdev. All rights reserved.</p>
<p class="links">{links}</p></div></footer>
<script src="/assets/app.js"></script></body></html>"""


def ad_banner():
    return f"""<div class="ad"><ins class="adsbygoogle" style="display:block"
data-ad-client="{SITE['adsense_client']}" data-ad-slot="{SITE['adsense_slot']}"
data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>"""


def share_html(a):
    u, t = url(a["path"]), e(a["title"])
    return f"""<section class="box"><h3>Bagikan Artikel</h3><div class="share">
<a href="https://facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener"><i class="fab fa-facebook-f"></i> Facebook</a>
<a href="https://twitter.com/intent/tweet?url={u}&text={t}" target="_blank" rel="noopener"><i class="fab fa-twitter"></i> Twitter</a>
<a href="https://api.whatsapp.com/send?text={t}%20{u}" target="_blank" rel="noopener"><i class="fab fa-whatsapp"></i> WhatsApp</a>
<a href="https://www.linkedin.com/shareArticle?mini=true&url={u}" target="_blank" rel="noopener"><i class="fab fa-linkedin-in"></i> LinkedIn</a>
<a href="https://t.me/share/url?url={u}&text={t}" target="_blank" rel="noopener"><i class="fab fa-telegram"></i> Telegram</a>
</div></section>"""


def contact_html():
    return f"""<section class="box contact"><h3 class="rtext">Hubungi Kami</h3>
<form action="mailto:{e(SITE['email'])}" method="post" enctype="text/plain">
<input type="text" name="nama" placeholder="Nama Anda" required>
<input type="email" name="email" placeholder="Email Anda" required>
<textarea name="pesan" rows="4" placeholder="Pesan Anda..." required></textarea>
<button class="btn" type="submit" style="width:100%">Kirim Pesan</button></form></section>"""


def disqus_html(a):
    return f"""<section class="box"><div id="disqus_thread"></div>
<script>var disqus_config=function(){{this.page.url="{url(a['path'])}";this.page.identifier="{a['cat']}-{a['n']}";}};
(function(){{var d=document,s=d.createElement('script');s.src='https://{SITE['disqus']}.disqus.com/embed.js';
s.setAttribute('data-timestamp',+new Date());(d.head||d.body).appendChild(s);}})();</script></section>"""


def card(a):
    return (f'<div class="card"><img src="{e(a["image"])}" alt="{e(a["image_alt"])}" loading="lazy">'
            f'<h4><a href="{a["path"]}">{e(a["title"])}</a></h4>'
            f'<div class="meta">{e(a["date"])}</div></div>')


def article_lists(a, arts):
    real = [x for x in arts if not x["draft"]] or arts
    newest = sorted(real, key=lambda x: x["date"], reverse=True)[:5]
    oldest = sorted(real, key=lambda x: x["date"])[:5]
    popular = sorted(real, key=lambda x: (-x.get("views", 0), hash_rank(x["path"])))[:5]
    news = newest[:3]
    def block(title, items):
        return f'<section class="box"><h3>{title}</h3><div class="grid">{"".join(card(x) for x in items)}</div></section>'
    years = sorted({x["date"][:4] for x in real}, reverse=True)
    archive = "".join(f'<a href="/{a["cat"]}/sitemap.html#{y}">{y}</a>' for y in years)
    labels = "".join(f'<a href="/{c}/index.html">{e(label(c))}</a>' for c in CATEGORIES[:24])
    return (block("News Artikel", news) + block("Artikel Populer", popular) +
            block("Artikel Terbaru", newest) + block("Artikel Terlama", oldest) +
            f'<section class="box labels"><h3>Label</h3>{labels}</section>'
            f'<section class="box archive"><h3>Archive</h3>{archive}</section>')


def internal_links(a, arts):
    links = [("Beranda AWDEV", "/"), (f"Kategori {label(a['cat'])}", f"/{a['cat']}/index.html"),
             ("Sitemap Kategori", f"/{a['cat']}/sitemap.html"), ("Blog", "/blog.html"),
             ("Tools", "/tools/index.html")]
    others = [x for x in arts if x["n"] != a["n"]][:2]
    links += [(x["title"], x["path"]) for x in others]
    links = links[:7]
    i = 1
    while len(links) < 7:
        links.append((f"Kategori {label(CATEGORIES[i])}", f"/{CATEGORIES[i]}/index.html")); i += 1
    return "<ul>" + "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links) + "</ul>"


def external_links():
    return "<ul>" + "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener">{e(n)}</a></li>'
        for n, u in EXTERNAL_LINKS[:7]) + "</ul>"


# ----------------------------------------------------------------- PAGES
def render_article(a, arts):
    toc, body = [], []
    for i, s in enumerate(a.get("sections", []), 1):
        sid = f"sec-{i}"
        toc.append(f'<li><a href="#{sid}">{e(s["h2"])}</a></li>')
        part = f'<h2 id="{sid}">{e(s["h2"])}</h2>'
        if s.get("image"):
            part += f'<img src="{e(s["image"])}" alt="{e(s.get("image_alt", s["h2"]))}" loading="lazy">'
        part += "".join(f"<p>{e(p)}</p>" for p in s.get("paragraphs", []))
        for sub in s.get("subsections", []):
            part += f'<h3>{e(sub["h3"])}</h3>' + "".join(f"<p>{e(p)}</p>" for p in sub.get("paragraphs", []))
        if s.get("table"):
            t = s["table"]
            part += ("<table><thead><tr>" + "".join(f"<th>{e(h)}</th>" for h in t["headers"]) +
                     "</tr></thead><tbody>" +
                     "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in t["rows"]) +
                     "</tbody></table>")
        body.append(part)
        if i == 2:
            body.append(ad_banner())

    faq = a.get("faq", [])
    faq_html = "".join(f'<div class="faq-item"><div class="faq-q">{e(q["q"])} <i class="fas fa-chevron-down"></i></div>'
                       f'<div class="faq-a">{e(q["a"])}</div></div>' for q in faq)
    toc_extra = ('<li><a href="#faq">FAQ</a></li>' if faq else "") + \
                ('<li><a href="#kesimpulan">Kesimpulan</a></li>' if a.get("conclusion") else "")

    schema = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"],
              "description": a["description"], "image": a["image"], "datePublished": a["date"],
              "dateModified": a.get("modified", a["date"]),
              "author": {"@type": "Organization", "name": SITE["name"]},
              "publisher": {"@type": "Organization", "name": SITE["name"],
                            "logo": {"@type": "ImageObject", "url": SITE["logo"]}},
              "mainEntityOfPage": url(a["path"])}
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
    if faq:
        ld += '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in faq]},
            ensure_ascii=False) + "</script>"

    draft_note = '<div class="inset"><b>DRAFT:</b> isi artikel belum ditulis (noindex).</div>' if a["draft"] else ""
    page = head(a["title"], a["description"], a["path"], a["image"], a["draft"], ld)
    page += f"""<main><article class="box article">
<nav class="meta"><a href="/">Home</a> / <a href="/{a['cat']}/index.html">{e(label(a['cat']))}</a> / Artikel {a['n']}</nav>
<h1 class="rtext">{e(a['title'])}</h1>
<div class="meta">Dipublikasikan {e(a['date'])} &middot; {word_count(a)} kata</div>
{draft_note}
<img src="{e(a['image'])}" alt="{e(a['image_alt'])}">
<p>{e(a.get('intro', ''))}</p>
{ad_banner()}
<section class="inset toc"><h3>Daftar Isi</h3><ol>{"".join(toc)}{toc_extra}</ol></section>
{"".join(body)}
{f'<h2 id="faq">FAQ</h2>{faq_html}' if faq else ''}
{f'<h2 id="kesimpulan">Kesimpulan</h2><p>{e(a["conclusion"])}</p>' if a.get('conclusion') else ''}
<div class="grid"><div class="card"><h4>Internal Links</h4>{internal_links(a, arts)}</div>
<div class="card"><h4>Referensi Eksternal</h4>{external_links()}</div></div>
</article>
{share_html(a)}
{article_lists(a, arts)}
{contact_html()}
{disqus_html(a)}
</main>
"""
    return page + footer_html()


def render_index(cat, arts):
    path = f"/{cat}/index.html"
    title = f"{label(cat)} - Artikel & Panduan"
    desc = f"Kumpulan artikel {label(cat)} dari {SITE['name']}."
    a = {"cat": cat, "n": 0, "path": path, "title": title}
    real = [x for x in arts if not x["draft"]]
    page = head(title, desc, path, SITE["logo"], noindex=not real)
    page += f"""<main><section class="box"><h1 class="rtext">{e(label(cat))}</h1><p>{e(desc)}</p>
<a class="btn" href="/{cat}/sitemap.html">Sitemap</a></section>{ad_banner()}
<section class="box"><h2>Semua Artikel</h2><div class="grid">{"".join(card(x) for x in arts)}</div></section>
{share_html(a)}{contact_html()}</main>"""
    return page + footer_html()


def render_sitemap_html(cat, arts):
    path = f"/{cat}/sitemap.html"
    title = f"Sitemap {label(cat)}"
    items = "".join(f'<li><a href="{x["path"]}">{e(x["title"])}</a></li>' for x in arts)
    page = head(title, title, path, SITE["logo"])
    page += f'<main><section class="box"><h1 class="rtext">{e(title)}</h1><ul>{items}</ul></section></main>'
    return page + footer_html()


def sitemap_xml(urls):
    rows = "".join(f"<url><loc>{e(u)}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{rows}</urlset>')


# ----------------------------------------------------------------- MAIN
def scaffold(cats, pages):
    for cat in cats:
        d = CONTENT / cat
        d.mkdir(parents=True, exist_ok=True)
        for n in range(1, pages + 1):
            f = d / f"artikel{n}.json"
            if f.exists():
                continue
            f.write_text(json.dumps({
                "title": "", "description": "", "date": date.today().isoformat(),
                "image": "", "image_alt": "", "intro": "",
                "sections": [{"h2": "", "paragraphs": [""],
                              "subsections": [{"h3": "", "paragraphs": [""]}],
                              "table": {"headers": [], "rows": []}}],
                "faq": [{"q": "", "a": ""}], "conclusion": ""
            }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scaffold dibuat di {CONTENT}")


def build(cats, pages):
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "style.css").write_text(CSS.strip(), encoding="utf-8")
    (OUT / "assets" / "app.js").write_text(JS.strip(), encoding="utf-8")
    all_urls, drafts = [], 0
    for cat in cats:
        arts = [load_article(cat, n) for n in range(1, pages + 1)]
        d = OUT / cat
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render_index(cat, arts), encoding="utf-8")
        for a in arts:
            (d / f"artikel{a['n']}.html").write_text(render_article(a, arts), encoding="utf-8")
        (d / "sitemap.html").write_text(render_sitemap_html(cat, arts), encoding="utf-8")
        live = [(url(x["path"]), x["date"]) for x in arts if not x["draft"]]
        drafts += sum(1 for x in arts if x["draft"])
        cat_urls = [(url(f"/{cat}/index.html"), date.today().isoformat())] + live
        (d / "sitemap.xml").write_text(sitemap_xml(cat_urls), encoding="utf-8")
        (d / "sitemap.txt").write_text("\n".join(u for u, _ in cat_urls), encoding="utf-8")
        all_urls += cat_urls
    (OUT / "sitemap.xml").write_text(sitemap_xml(all_urls), encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {url('/sitemap.xml')}\n", encoding="utf-8")
    print(f"Selesai: {len(cats)} kategori, {len(all_urls)} URL di sitemap, {drafts} halaman draft (noindex).")


def push(msg):
    for cmd in (["git", "add", "-A"], ["git", "commit", "-m", msg], ["git", "push", "origin", "HEAD"]):
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode and cmd[1] != "commit":
            raise SystemExit(f"Gagal: {' '.join(cmd)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=30, help="jumlah artikel per kategori")
    ap.add_argument("--only", help="satu kategori saja (slug)")
    ap.add_argument("--scaffold", action="store_true", help="buat kerangka JSON")
    ap.add_argument("--push", action="store_true", help="git add/commit/push setelah build")
    args = ap.parse_args()
    cats = [args.only] if args.only else CATEGORIES
    if args.scaffold:
        scaffold(cats, args.pages)
    else:
        build(cats, args.pages)
        if args.push:
            push("Generate blog pages")
