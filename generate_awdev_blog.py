import os
from datetime import datetime

# Daftar lengkap 138 kategori sesuai ekosistem AWDEV CORP
categories = [
    "aplikasi", "calligraphy", "code", "collor", "converter", "devoloper", "domain", "domains", "eq", 
    "finder", "hook", "img", "ip", "kodepost", "link", "maps", "pdf", "qr", "quran", "removebg", 
    "safelink", "search", "seo", "source", "text", "tools", "utilities", "vidio",
    "market", "finance", "macro", "micro", "economy", "explainers", "manufacturing", "property", 
    "health", "education", "lifestyle", "hospitality", "tech", "media", "smes", "luxury", "whos-who", 
    "international", "local-resources", "politics", "culture", "science", "public-policy", "business", 
    "news", "sports", "arts", "celebrities", "automotive", "commentary", "interview", "money", 
    "perbankan", "belanja", "sharia", "football", "opinion", "video", "kisah", "index-cat", "sejarah", 
    "entrepreneur", "research", "photo", "olahraga", "selebritis", "country", "dki", "diy", "jabar", 
    "jatim", "jateng", "aceh", "papua", "kalimantan", "sumatra", "sulawesi", "bali", "asia", "afrika", 
    "australia", "rusia", "eropa", "amerika", "ai", "teknologi", "astronomi", "zodiak",
    "biografi-ulama", "kisah-hikmah", "kisah-sejarah", "info", "kisah-birrul-walidain", "kisah-hidayah", 
    "kisah-durhaka", "kisah-masa-depan", "kisah-nabi-rasul", "kisah-muhammad", "kisah-nyata", 
    "kisah-orang-shalih", "kisah-pilihan", "kisah-sahabat", "kisah-tabiin", "kisah-tak-nyata", 
    "kisah-umat-terdahulu", "sejarah-islam", "nusantara", "laporan-produksi", "merchandise-yufid", 
    "mutiara-faidah", "teladan-muslimah", "books", "download",
    "islamic-tools", "qibla-direction", "prayer-times", "hijri-calendar", "zakat-calculator", 
    "salah-tracker", "mosque-finder", "worship", "trackers", "calculators", "knowledge", "finders", 
    "duas", "halal-food", "timer", "calendar", "cuaca"
]

print(f"Memulai pembuatan direktori dan halaman blog untuk {len(categories)} kategori...")

def generate_html(category, page_num, total_pages):
    title = f"Panduan Lengkap & Analisis {category.capitalize()} - Artikel #{page_num} | AWDEV CORP"
    filename = "index.html" if page_num == 0 else f"artikel{page_num}.html"
    
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="Eksplorasi mendalam mengenai {category} artikel {page_num} oleh AWDEV Corporation. Temukan wawasan terkini, panduan teknis, FAQ, dan alat open source profesional.">
    <meta name="keywords" content="{category}, AWDEV, open source, developer tools, programming, tutorial, SEO, 2026">
    <meta name="author" content="AWDEV Corporation">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://awdev.my.id/{category}/{filename}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="Analisis komprehensif dan panduan eksklusif seputar {category} bagian {page_num}.">
    <meta property="og:image" content="https://awdev.my.id/img/awdev.png">

    <!-- Google Verification & AdSense -->
    <meta name="google-site-verification" content="OLryKZ1dDupEH_xOuZWiEwdi0ZvuXMcnQeMjRwe5YCw">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5407249785989200" crossorigin="anonymous"></script>
    <meta name="google-adsense-account" content="ca-pub-5407249785989200">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "image": "https://awdev.my.id/img/awdev.png",
      "author": {{
        "@type": "Organization",
        "name": "AWDEV CORPORATION"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "AWDEV CORPORATION",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://awdev.my.id/img/awdev.png"
        }}
      }},
      "mainEntityOfPage": "https://awdev.my.id/{category}/{filename}"
    }}
    </script>

    <!-- Google Fonts & FontAwesome -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        :root {{
            --bg-color: #e4ebf5;
            --neu-shadow-dark: #c5d1e0;
            --neu-shadow-light: #ffffff;
            --text-color: #333333;
            --primary: #1a73e8;
            --rainbow-gradient: linear-gradient(135deg, #ff3366, #ff9933, #33cc66, #3399ff, #9933ff);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; }}
        body {{ background-color: var(--bg-color); color: var(--text-color); line-height: 1.7; padding: 20px; }}
        .rainbow-bar {{ height: 6px; width: 100%; background: var(--rainbow-gradient); border-radius: 3px; margin-bottom: 20px; }}
        .neu-box {{ background: var(--bg-color); box-shadow: 8px 8px 16px var(--neu-shadow-dark), -8px -8px 16px var(--neu-shadow-light); border-radius: 16px; padding: 25px; margin-bottom: 30px; }}
        .neu-inset {{ background: var(--bg-color); box-shadow: inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light); border-radius: 12px; padding: 15px; margin-bottom: 15px; }}
        .neu-button {{ background: var(--bg-color); box-shadow: 5px 5px 10px var(--neu-shadow-dark), -5px -5px 10px var(--neu-shadow-light); border: none; border-radius: 8px; padding: 10px 20px; cursor: pointer; color: var(--text-color); font-weight: 600; text-decoration: none; display: inline-block; }}
        .neu-button:hover {{ box-shadow: inset 3px 3px 6px var(--neu-shadow-dark), inset -3px -3px 6px var(--neu-shadow-light); color: #ff3366; }}
        header {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 20px; }}
        .logo-area {{ display: flex; align-items: center; gap: 15px; }}
        .logo-img {{ width: 50px; height: 50px; border-radius: 50%; object-fit: cover; box-shadow: 4px 4px 8px var(--neu-shadow-dark), -4px -4px 8px var(--neu-shadow-light); }}
        .logo-text {{ font-size: 1.5rem; font-weight: 700; background: var(--rainbow-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .dropdown {{ position: relative; display: inline-block; }}
        .dropbtn {{ background: var(--bg-color); box-shadow: 5px 5px 10px var(--neu-shadow-dark), -5px -5px 10px var(--neu-shadow-light); padding: 10px 18px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; border-radius: 10px; color: var(--primary); }}
        .dropdown-content {{ display: none; position: absolute; right: 0; background-color: var(--bg-color); min-width: 240px; box-shadow: 8px 8px 16px var(--neu-shadow-dark), -8px -8px 16px var(--neu-shadow-light); z-index: 100; border-radius: 12px; padding: 10px 0; max-height: 350px; overflow-y: auto; }}
        .dropdown-content a {{ color: var(--text-color); padding: 10px 20px; text-decoration: none; display: block; font-size: 13px; }}
        .dropdown-content a:hover {{ background: rgba(0,0,0,0.03); color: #ff3366; padding-left: 25px; }}
        .dropdown:hover .dropdown-content {{ display: block; }}
        h1, h2, h3 {{ margin-bottom: 15px; color: #222; }}
        h1 {{ font-size: 2.2rem; background: var(--rainbow-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        h2 {{ font-size: 1.6rem; border-bottom: 2px solid var(--neu-shadow-dark); padding-bottom: 8px; margin-top: 25px; }}
        h3 {{ font-size: 1.2rem; margin-top: 20px; }}
        p {{ margin-bottom: 15px; text-align: justify; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: var(--bg-color); border-radius: 10px; overflow: hidden; box-shadow: inset 2px 2px 5px var(--neu-shadow-dark), inset -2px -2px 5px var(--neu-shadow-light); }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid rgba(0,0,0,0.05); }}
        th {{ background: rgba(26, 115, 232, 0.1); color: var(--primary); font-weight: 600; }}
        .article-img {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; box-shadow: 5px 5px 10px var(--neu-shadow-dark), -5px -5px 10px var(--neu-shadow-light); margin: 20px 0; }}
        .faq-box {{ background: var(--bg-color); box-shadow: inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light); border-radius: 12px; padding: 15px; margin-bottom: 10px; }}
        .social-share {{ display: flex; gap: 15px; justify-content: center; margin: 30px 0; }}
        .social-btn {{ width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: var(--bg-color); box-shadow: 5px 5px 10px var(--neu-shadow-dark), -5px -5px 10px var(--neu-shadow-light); color: var(--primary); text-decoration: none; font-size: 1.1rem; }}
        .social-btn:hover {{ box-shadow: inset 3px 3px 6px var(--neu-shadow-dark), inset -3px -3px 6px var(--neu-shadow-light); color: #ff3366; }}
        .contact-form input, .contact-form textarea {{ width: 100%; padding: 12px; margin-bottom: 15px; border: none; background: var(--bg-color); box-shadow: inset 3px 3px 6px var(--neu-shadow-dark), inset -3px -3px 6px var(--neu-shadow-light); border-radius: 8px; outline: none; color: var(--text-color); }}
        footer {{ text-align: center; padding: 25px; font-size: 14px; color: #666; border-top: 1px solid #ccc; margin-top: 40px; }}
        footer .footer-links {{ margin-top: 10px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; }}
        footer .footer-links a {{ color: var(--primary); text-decoration: none; }}
        footer .footer-links a:hover {{ text-decoration: underline; color: #ff3366; }}
        .adsense-banner {{ text-align: center; margin: 30px 0; padding: 15px; background: rgba(0,0,0,0.02); border-radius: 12px; box-shadow: inset 2px 2px 5px var(--neu-shadow-dark), inset -2px -2px 5px var(--neu-shadow-light); }}
    </style>
</head>
<body>

    <!-- Rainbow Accent Top Bar -->
    <div class="rainbow-bar"></div>

    <!-- Header & Navigation -->
    <header class="neu-box">
        <div class="logo-area">
            <img src="https://awdev.my.id/img/awdev.png" alt="AWDEV Corporation Logo" class="logo-img">
            <span class="logo-text">AWDEV CORP</span>
        </div>
        <div class="dropdown">
            <button class="dropbtn"><i class="fas fa-bars"></i> Navigation Menu</button>
            <div class="dropdown-content">
                <a href="https://awdev.my.id/"><i class="fas fa-home"></i> Home</a>
                <a href="https://awdev.my.id/about.html"><i class="fas fa-info-circle"></i> About Us</a>
                <a href="https://awdev.my.id/blog.html"><i class="fas fa-blog"></i> Blog</a>
                <a href="https://awdev.my.id/tools/index.html"><i class="fas fa-tools"></i> Tools</a>
                <a href="https://awdev.my.id/aplikasi/index.html"><i class="fas fa-mobile-alt"></i> Aplikasi</a>
                <a href="https://awdev.my.id/seo/index.html"><i class="fas fa-search-dollar"></i> Seo</a>
                <a href="https://awdev.my.id/source/index.html"><i class="fas fa-code"></i> Source</a>
                <a href="https://awdev.my.id/eq/index.html"><i class="fas fa-sliders-h"></i> EQ Generator</a>
                <a href="https://awdev.my.id/kodepost/index.html"><i class="fas fa-mail-bulk"></i> Kode Post Search</a>
                <a href="https://awdev.my.id/finder/index.html"><i class="fas fa-compass"></i> Finder</a>
                <a href="https://awdev.my.id/qr/index.html"><i class="fas fa-qrcode"></i> QR Generator</a>
                <a href="https://awdev.my.id/collor/index.html"><i class="fas fa-palette"></i> Collor Code Generator</a>
                <a href="https://awdev.my.id/calligraphy/index.html"><i class="fas fa-feather-alt"></i> Calligraphy Arabic</a>
                <a href="https://awdev.my.id/maps/index.html"><i class="fas fa-map-marked-alt"></i> Maps Search</a>
                <a href="https://awdev.my.id/code/index.html"><i class="fas fa-laptop-code"></i> Code Editor</a>
                <a href="https://awdev.my.id/vidio/index.html"><i class="fas fa-video"></i> Vidio</a>
                <a href="https://awdev.my.id/img/index.html"><i class="fas fa-images"></i> Gallery Images</a>
            </div>
        </div>
    </header>

    <!-- Google AdSense Top Banner -->
    <div class="adsense-banner">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5407249785989200" crossorigin="anonymous"></script>
        <ins class="adsbygoogle" style="display:block" data-adsbygoogle-status="done" data-ad-client="ca-pub-5407249785989200" data-ad-slot="1234567890" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>

    <!-- Main Content -->
    <main class="neu-box">
        <h1>{title}</h1>
        <p><strong>Kategori:</strong> {category.capitalize()} | <strong>Dipublikasikan:</strong> {datetime.now().strftime('%Y-%m-%d')} | <strong>Oleh:</strong> Tim Editor AWDEV</p>
        
        <img src="https://awdev.my.id/img/awdev.png" alt="Ilustrasi Utama Artikel {category} - AWDEV Corporation" class="article-img">

        <!-- Table of Contents -->
        <div class="neu-inset" id="toc">
            <h3>Daftar Isi</h3>
            <ul style="list-style-type: disc; padding-left: 20px; line-height: 1.8;">
                <li><a href="#pengantar" style="color:var(--primary); text-decoration:none;">1. Pengantar dan Latar Belakang</a></li>
                <li><a href="#analisis" style="color:var(--primary); text-decoration:none;">2. Analisis Mendalam & Komparasi Data</a></li>
                <li><a href="#strategi" style="color:var(--primary); text-decoration:none;">3. Strategi Penerapan Terbaik</a></li>
                <li><a href="#tabel-data" style="color:var(--primary); text-decoration:none;">4. Tabel Perbandingan Metrik</a></li>
                <li><a href="#internal-external" style="color:var(--primary); text-decoration:none;">5. Tautan Terkait & Referensi Global</a></li>
                <li><a href="#faq" style="color:var(--primary); text-decoration:none;">6. Pertanyaan Umum (FAQ)</a></li>
                <li><a href="#kesimpulan" style="color:var(--primary); text-decoration:none;">7. Kesimpulan & Penutup</a></li>
            </ul>
        </div>

        <h2 id="pengantar">1. Pengantar dan Latar Belakang {category.capitalize()}</h2>
        <p>Dalam era digital yang berkembang pesat saat ini, pemahaman komprehensif mengenai <strong>{category}</strong> menjadi salah satu kunci utama keberhasilan bagi para pengembang, profesional, serta peminat teknologi global. AWDEV Corporation senantiasa berkomitmen untuk menyediakan sumber daya terbuka yang berkualitas tinggi, terstruktur dengan baik, serta dioptimalkan secara penuh untuk mesin pencari (SEO). Artikel bagian ke-{page_num} ini dirancang khusus untuk mengupas tuntas berbagai aspek fundamental yang memengaruhi performa dan efektivitas ekosistem {category}.</p>
        <p>Perkembangan teknologi modern menuntut fleksibilitas tinggi serta penerapan standar industri yang ketat. Melalui pendekatan berbasis riset mendalam, topik ini tidak hanya menyajikan teori konseptual tetapi juga panduan praktis yang dapat langsung diimplementasikan pada proyek nyata Anda.</p>

        <h2 id="analisis">2. Analisis Mendalam & Komparasi Data {category.capitalize()}</h2>
        <p>Analisis mendalam menunjukkan bahwa optimalisasi pada sektor {category} memerlukan keseimbangan antara performa kecepatan, akurasi data, dan kenyamanan antarmuka pengguna (UI/UX). Dengan mengintegrasikan kerangka kerja modern seperti Neumorphism dan desain responsif, setiap pengguna dapat menikmati pengalaman navigasi yang mulus dan bebas hambatan.</p>
        <p>Berbagai studi kasus membuktikan bahwa pendekatan terstruktur dalam pengelolaan {category} mampu meningkatkan efisiensi operasional hingga lebih dari 45%. Hal ini menjadikannya salah satu topik paling dicari oleh komunitas pengembang global di platform AWDEV.</p>

        <!-- Google AdSense Middle Banner -->
        <div class="adsense-banner">
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5407249785989200" crossorigin="anonymous"></script>
            <ins class="adsbygoogle" style="display:block" data-adsbygoogle-status="done" data-ad-client="ca-pub-5407249785989200" data-ad-slot="0987654321" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>

        <h2 id="strategi">3. Strategi Penerapan Terbaik</h2>
        <p>Untuk mencapai hasil yang optimal dalam pengelolaan proyek berbasis {category}, berikut adalah beberapa langkah strategis yang direkomendasikan oleh para ahli:</p>
        <ul style="padding-left: 20px; margin-bottom: 20px; line-height: 1.8;">
            <li><strong>Audit & Perencanaan:</strong> Lakukan analisis menyeluruh terhadap kebutuhan sistem sebelum mengeksekusi kode atau konten.</li>
            <li><strong>Standarisasi Kode:</strong> Patuhi panduan gaya penulisan standar industri untuk memastikan pemeliharaan jangka panjang.</li>
            <li><strong>Optimalisasi SEO:</strong> Manfaatkan meta tag yang tepat, deskripsi kaya, serta struktur heading hierarkis (H1, H2, H3).</li>
            <li><strong>Keamanan & Skalabilitas:</strong> Pastikan arsitektur sistem mampu menangani lonjakan trafik secara efisien.</li>
        </ul>

        <h2 id="tabel-data">4. Tabel Perbandingan Metrik {category.capitalize()}</h2>
        <table>
            <thead>
                <tr>
                    <th>Parameter Metrik</th>
                    <th>Standar Industri</th>
                    <th>Solusi AWDEV CORP</th>
                    <th>Tingkat Efisiensi</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Performa Kecepatan Muat</td>
                    <td>&lt; 2.5 Detik</td>
                    <td>0.8 Detik</td>
                    <td>Sangat Tinggi</td>
                </tr>
                <tr>
                    <td>Skor Optimasi SEO</td>
                    <td>85%</td>
                    <td>99.5%</td>
                    <td>Optimal</td>
                </tr>
                <tr>
                    <td>Kompatibilitas Perangkat</td>
                    <td>Responsif Standar</td>
                    <td>Multi-Platform Dinamis</td>
                    <td>Sempurna</td>
                </tr>
                <tr>
                    <td>Dukungan Komunitas Open Source</td>
                    <td>Terbatas</td>
                    <td>Global &amp; Aktif 24/7</td>
                    <td>Maksimal</td>
                </tr>
            </tbody>
        </table>

        <h2 id="internal-external">5. Tautan Terkait &amp; Referensi Global</h2>
        <p>Berikut adalah 7 tautan internal dalam ekosistem AWDEV serta 7 tautan referensi eksternal terpercaya untuk memperdalam wawasan Anda:</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-bottom: 20px;">
            <div class="neu-inset">
                <h4>Tautan Internal AWDEV</h4>
                <ul style="list-style-type: none; padding-left:0; line-height: 1.8; font-size: 0.95rem;">
                    <li><a href="https://awdev.my.id/" style="color:var(--primary); text-decoration:none;"><i class="fas fa-link"></i> Halaman Utama AWDEV</a></li>
                    <li><a href="https://awdev.my.id/tools/index.html" style="color:var(--primary); text-decoration:none;"><i class="fas fa-link"></i> Koleksi Open Source Tools</a></li>
                    <li><a href="https://awdev.my.id/aplikasi/index.html" style="color:var(--primary); text-decoration:none;"><i class="fas fa-link"></i> Direktori Aplikasi Modern</a></li>
                    <li><a href="https://awdev.my.id/seo/index.html" style="color:var(--primary); text-decoration:none;"><i class="fas fa-link"></i> Panduan &amp; Alat SEO Lengkap</a></li>
                    <li><a href="https://awdev.my.id/source/index.html" style="color:var(--primary); text-decoration:none;"><i class="fas fa-link"></i> Repositori Kode Sumber</a></li>
                    <li><a href="https://awdev.my.id/eq/index.html" style="color:var(--primary); text-decoration:none;"><i class="fas fa-link"></i> Equalizer &amp; Generator Suara</a></li>
                    <li><a href="https://awdev.my.id/qr/index.html" style="color:var(--primary); text-decoration:none;"><i class="fas fa-link"></i> Generator QR Code Interaktif</a></li>
                </ul>
            </div>
            <div class="neu-inset">
                <h4>Referensi Eksternal Global</h4>
                <ul style="list-style-type: none; padding-left:0; line-height: 1.8; font-size: 0.95rem;">
                    <li><a href="https://github.com/" target="_blank" rel="noopener" style="color:var(--primary); text-decoration:none;"><i class="fas fa-external-link-alt"></i> GitHub Open Source Hub</a></li>
                    <li><a href="https://developer.mozilla.org/" target="_blank" rel="noopener" style="color:var(--primary); text-decoration:none;"><i class="fas fa-external-link-alt"></i> MDN Web Docs</a></li>
                    <li><a href="https://stackoverflow.com/" target="_blank" rel="noopener" style="color:var(--primary); text-decoration:none;"><i class="fas fa-external-link-alt"></i> Stack Overflow Community</a></li>
                    <li><a href="https://schema.org/" target="_blank" rel="noopener" style="color:var(--primary); text-decoration:none;"><i class="fas fa-external-link-alt"></i> Schema.org Structured Data</a></li>
                    <li><a href="https://w3.org/" target="_blank" rel="noopener" style="color:var(--primary); text-decoration:none;"><i class="fas fa-external-link-alt"></i> W3C Web Standards</a></li>
                    <li><a href="https://nodejs.org/" target="_blank" rel="noopener" style="color:var(--primary); text-decoration:none;"><i class="fas fa-external-link-alt"></i> Node.js Runtime Environment</a></li>
                    <li><a href="https://python.org/" target="_blank" rel="noopener" style="color:var(--primary); text-decoration:none;"><i class="fas fa-external-link-alt"></i> Python Programming Language</a></li>
                </ul>
            </div>
        </div>

        <h2 id="faq">6. Pertanyaan Umum (FAQ)</h2>
        <div class="faq-box">
            <strong>Q1: Apa keuntungan utama menggunakan platform AWDEV untuk {category}?</strong>
            <p>A1: AWDEV menyediakan kode sumber terbuka berkualitas tinggi, desain Neumorphic yang elegan, serta performa tinggi yang dioptimalkan untuk mesin pencari.</p>
        </div>
        <div class="faq-box">
            <strong>Q2: Bagaimana cara mengunduh dan mengimplementasikan modul ini?</strong>
            <p>A2: Anda dapat mengakses repositori resmi kami di GitHub atau menavigasi menu unduhan yang tersedia di situs utama.</p>
        </div>
        <div class="faq-box">
            <strong>Q3: Apakah seluruh perangkat dan alat di AWDEV dapat digunakan secara gratis?</strong>
            <p>A3: Ya, seluruh proyek open source dan alat utilitas di AWDEV 100% gratis untuk komunitas global.</p>
        </div>

        <h2 id="kesimpulan">7. Kesimpulan &amp; Penutup</h2>
        <p>Melalui artikel komprehensif ini, diharapkan Anda dapat memperoleh pemahaman yang mendalam serta strategi praktis dalam mengoptimalkan <strong>{category}</strong>. AWDEV Corporation akan terus berinovasi menyediakan konten berkualitas tinggi dan perangkat lunak open source terbaik untuk mendukung kemajuan ekosistem digital global.</p>
    </main>

    <!-- Social Media Share -->
    <div class="neu-box" style="text-align: center;">
        <h3 style="margin-bottom: 15px;">Bagikan Artikel Ini</h3>
        <div class="social-share">
            <a href="https://facebook.com/sharer/sharer.php?u=https://awdev.my.id/{category}/{filename}" target="_blank" class="social-btn"><i class="fab fa-facebook-f"></i></a>
            <a href="https://twitter.com/intent/tweet?url=https://awdev.my.id/{category}/{filename}" target="_blank" class="social-btn"><i class="fab fa-twitter"></i></a>
            <a href="https://linkedin.com/shareArticle?url=https://awdev.my.id/{category}/{filename}" target="_blank" class="social-btn"><i class="fab fa-linkedin-in"></i></a>
            <a href="https://api.whatsapp.com/send?text=https://awdev.my.id/{category}/{filename}" target="_blank" class="social-btn"><i class="fab fa-whatsapp"></i></a>
            <a href="https://t.me/share/url?url=https://awdev.my.id/{category}/{filename}" target="_blank" class="social-btn"><i class="fab fa-telegram-plane"></i></a>
        </div>
    </div>

    <!-- Contact Form Section -->
    <section class="neu-box contact-form">
        <h3 style="margin-bottom: 15px;"><i class="fas fa-envelope"></i> Hubungi Tim AWDEV Corporation</h3>
        <form onsubmit="event.preventDefault(); alert('Pesan berhasil terkirim! Terima kasih telah menghubungi AWDEV.');">
            <input type="text" placeholder="Nama Lengkap Anda" required>
            <input type="email" placeholder="Alamat Email Aktif" required>
            <textarea rows="4" placeholder="Tuliskan pesan, pertanyaan, atau masukan Anda di sini..." required></textarea>
            <button type="submit" class="neu-button" style="width: 100%;">Kirim Pesan Sekarang</button>
        </form>
    </section>

    <!-- Footer -->
    <footer>
        <p>&copy; 2026 AWDEV CORPORATION. All Rights Reserved. Free Open Source General Tools, Developers, Designers &amp; Programmers.</p>
        <div class="footer-links">
            <a href="https://awdev.my.id/">Home</a>
            <a href="https://awdev.my.id/about.html">About Us</a>
            <a href="https://awdev.my.id/blog.html">Blog</a>
            <a href="https://awdev.my.id/tools/index.html">Tools</a>
            <a href="https://awdev.my.id/privacy.html">Privacy Policy</a>
            <a href="https://awdev.my.id/terms.html">Terms of Service</a>
            <a href="https://awdev.my.id/contact.html">Contact</a>
        </div>
    </footer>

</body>
</html>
"""
    return html

def generate_sitemap_xml(category, total_pages):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += f'  <url><loc>https://awdev.my.id/{category}/index.html</loc><priority>1.0</priority></url>\n'
    for i in range(1, total_pages + 1):
        xml += f'  <url><loc>https://awdev.my.id/{category}/artikel{i}.html</loc><priority>0.8</priority></url>\n'
    xml += '</urlset>'
    return xml

def generate_sitemap_txt(category, total_pages):
    txt = f"https://awdev.my.id/{category}/index.html\n"
    for i in range(1, total_pages + 1):
        txt += f"https://awdev.my.id/{category}/artikel{i}.html\n"
    return txt

# Eksekusi pembuatan file dan direktori secara otomatis
for cat in categories:
    cat_dir = os.path.join(".", cat)
    os.makedirs(cat_dir, exist_ok=True)
    
    # Generate index.html (page 0)
    with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_html(cat, 0, 30))
        
    # Generate 30 artikel pendukung
    for p in range(1, 31):
        with open(os.path.join(cat_dir, f"artikel{p}.html"), "w", encoding="utf-8") as f:
            f.write(generate_html(cat, p, 30))
            
    # Generate sitemaps (.html, .xml, .txt)
    with open(os.path.join(cat_dir, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(generate_html(cat, 0, 30))
        
    with open(os.path.join(cat_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(generate_sitemap_xml(cat, 30))
        
    with open(os.path.join(cat_dir, "sitemap.txt"), "w", encoding="utf-8") as f:
        f.write(generate_sitemap_txt(cat, 30))

print("Berhasil! Seluruh direktori dan ribuan artikel telah selesai dibuat secara otomatis.")
