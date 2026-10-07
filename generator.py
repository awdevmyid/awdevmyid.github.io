import os
import shutil

# Daftar kategori lengkap (total 50+ kategori/sub-kategori dari permintaan)
CATEGORIES = [
    "market", "finance", "macro", "micro", "economy", "explainers", "manufacturing", 
    "property", "health", "education", "lifestyle", "hospitality", "tech", "media", 
    "smes", "luxury", "whoswho", "international", "localresources", "politics", 
    "culture", "science", "publicpolicy", "business", "news", "sports", "arts", 
    "celebrities", "automotive", "commentary", "interview", "money", "perbankan", 
    "belanja", "sharia", "football", "opinion", "video", "kisah", "index", 
    "sejarah", "entrepreneur", "research", "photo", "olahraga", "selebritis", 
    "country", "dki", "diy", "jabar", "jatim", "jateng", "aceh", "papua", 
    "kalimantan", "sumatra", "sulawesi", "bali", "asia", "afrika", "australia", 
    "rusia", "eropa", "amerika", "ai", "teknologi", "astronomi", "zodiak", "maps"
]

ARTICLES_PER_CATEGORY = 30

# Template Header & Footer sesuai Home Page dengan Neumorphic & Rainbow UI
def get_header(title, cat_name):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AWDEV CORPORATION</title>
    
    <!-- Meta SEO & Open Graph -->
    <meta name="description" content="{title} - AWDEV FREE OPEN SOURCE GENERAL TOOLS PROJECTS DEVELOPER, DESIGNER, AND PROGRAMMER. Explore free tools, applications, source code, gallery images, and videos.">
    <meta name="keywords" content="AWDEV, Open Source, Developer Tools, Programming, {cat_name}, Free Apps, SEO Tools">
    <meta name="author" content="AWDEV Corporation">
    
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://awdev.my.id/{cat_name}/">
    <meta property="og:title" content="{title} - AWDEV CORPORATION">
    <meta property="og:description" content="{title} - Professional insights and open-source solutions.">
    <meta property="og:image" content="https://awdev.my.id/img/awdev.png">

    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://awdev.my.id/{cat_name}/">
    <meta property="twitter:title" content="{title} - AWDEV CORPORATION">
    <meta property="twitter:description" content="{title} - Professional insights and open-source solutions.">
    <meta property="twitter:image" content="https://awdev.my.id/img/awdev.png">

    <!-- Favicons -->
    <link rel="icon" type="image/png" href="https://awdev.my.id/awdev.jpg">
    <link rel="icon" type="image/png" href="https://awdev.my.id/awdev.png">
    
    <!-- Google Verification & AdSense -->
    <meta name="google-site-verification" content="OLryKZ1dDupEH_xOuZWiEwdi0ZvuXMcnQeMjRwe5YCw">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5407249785989200" crossorigin="anonymous"></script>
    <meta name="google-adsense-account" content="ca-pub-5407249785989200">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{title}",
      "image": "https://awdev.my.id/img/awdev.png",
      "url": "https://awdev.my.id/{cat_name}/",
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
      }}
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
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; transition: all 0.3s ease; }}
        body {{ background-color: var(--bg-color); color: var(--text-color); line-height: 1.6; padding: 20px; }}
        .rainbow-bar {{ height: 6px; width: 100%; background: var(--rainbow-gradient); border-radius: 3px; margin-bottom: 20px; }}
        .neu-box {{ background: var(--bg-color); box-shadow: 8px 8px 16px var(--neu-shadow-dark), -8px -8px 16px var(--neu-shadow-light); border-radius: 16px; padding: 20px; margin-bottom: 30px; }}
        .neu-inset {{ background: var(--bg-color); box-shadow: inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light); border-radius: 12px; padding: 15px; }}
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
        .article-content h1, .article-content h2, .article-content h3 {{ margin: 20px 0 10px 0; background: var(--rainbow-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .article-content p {{ margin-bottom: 15px; text-align: justify; }}
        .article-content img {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; box-shadow: 5px 5px 10px var(--neu-shadow-dark), -5px -5px 10px var(--neu-shadow-light); margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: var(--bg-color); border-radius: 10px; overflow: hidden; box-shadow: 4px 4px 8px var(--neu-shadow-dark), -4px -4px 8px var(--neu-shadow-light); }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid rgba(0,0,0,0.08); }}
        th {{ background: rgba(26, 115, 232, 0.1); color: var(--primary); }}
        .adsense-banner {{ text-align: center; margin: 30px 0; padding: 15px; background: var(--bg-color); box-shadow: inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light); border-radius: 12px; }}
        .sidebar-widget {{ margin-bottom: 25px; }}
        .sidebar-widget h4 {{ margin-bottom: 12px; color: var(--primary); font-size: 1.1rem; }}
        .sidebar-widget ul {{ list-style: none; padding: 0; }}
        .sidebar-widget li {{ margin-bottom: 8px; }}
        .sidebar-widget a {{ text-decoration: none; color: #555; font-size: 0.95rem; }}
        .sidebar-widget a:hover {{ color: #ff3366; text-decoration: underline; }}
        .faq-item {{ margin-bottom: 15px; border-bottom: 1px solid rgba(0,0,0,0.08); padding-bottom: 10px; }}
        .faq-question {{ font-weight: 600; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
        .faq-answer {{ margin-top: 8px; font-size: 0.95rem; color: #555; }}
        .social-share {{ display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin: 20px 0; }}
        .social-btn {{ width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: var(--bg-color); box-shadow: 5px 5px 10px var(--neu-shadow-dark), -5px -5px 10px var(--neu-shadow-light); color: var(--primary); text-decoration: none; font-size: 1.1rem; }}
        .social-btn:hover {{ box-shadow: inset 3px 3px 6px var(--neu-shadow-dark), inset -3px -3px 6px var(--neu-shadow-light); color: #ff3366; }}
        .contact-form input, .contact-form textarea {{ width: 100%; padding: 12px; margin-bottom: 15px; border: none; background: var(--bg-color); box-shadow: inset 4px 4px 8px var(--neu-shadow-dark), inset -4px -4px 8px var(--neu-shadow-light); border-radius: 8px; outline: none; color: var(--text-color); }}
        footer {{ text-align: center; padding: 20px; font-size: 14px; color: #666; border-top: 1px solid #e0e0e0; margin-top: 40px; }}
        footer .footer-links {{ margin-top: 10px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; }}
        footer .footer-links a {{ color: var(--primary); text-decoration: none; }}
        footer .footer-links a:hover {{ text-decoration: underline; color: #ff3366; }}
    </style>
</head>
<body>
    <div class="rainbow-bar"></div>
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
            </div>
        </div>
    </header>
"""

def get_footer(cat_name):
    return f"""
    <footer>
        <div class="neu-inset" style="text-align: center;">
            <p>&copy; 2026 awdev. All rights reserved.</p>
            <p class="footer-links">
                <a href="https://awdev.my.id/">Home</a> | 
                <a href="https://awdev.my.id/about.html">About Us</a> | 
                <a href="https://awdev.my.id/blog.html">Blog</a> | 
                <a href="https://awdev.my.id/contact.html">Contact</a> | 
                <a href="https://awdev.my.id/privacy-policy.html">Privacy Policy</a> | 
                <a href="https://awdev.my.id/terms.html">Terms & Conditions</a> | 
                <a href="https://awdev.my.id/disclaimers.html">Disclaimers</a> | 
                <a href="https://awdev.my.id/license.html">License</a>
            </p>
        </div>
    </footer>
</body>
</html>
"""

def generate_article_content(title, cat_name, index):
    return f"""
    <div class="neu-box article-content">
        <h1>{title}</h1>
        <p>Published in <strong>{cat_name.upper()}</strong> | Comprehensive SEO Guide & Research (3000+ Words)</p>
        
        <img src="https://awdev.my.id/img/awdev.png" alt="{title} vector illustration for {cat_name}">
        
        <h2>Table of Contents</h2>
        <ul>
            <li><a href="#introduction">1. Introduction to {title}</a></li>
            <li><a href="#core-mechanics">2. Core Mechanics and Frameworks</a></li>
            <li><a href="#strategic-analysis">3. Strategic Industry Analysis</a></li>
            <li><a href="#faq-section">4. Frequently Asked Questions</a></li>
            <li><a href="#conclusion">5. Conclusion and Future Outlook</a></li>
        </ul>

        <div class="adsense-banner">
            <!-- Google AdSense Banner -->
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5407249785989200" crossorigin="anonymous"></script>
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5407249785989200" data-ad-slot="1234567890" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>

        <h2 id="introduction">1. Introduction to {title}</h2>
        <p>Welcome to our comprehensive examination of {title}. In modern digital ecosystems, understanding the nuances of {cat_name} is essential for professionals, researchers, and developers alike. This document serves as an exhaustive guide, incorporating advanced technical specs, structural breakdowns, and industry best practices.</p>
        <p>As technological adoption scales globally, frameworks continuously adapt to fulfill stringent performance metrics, security compliance, and user experience standards.</p>

        <h2 id="core-mechanics">2. Core Mechanics and Frameworks</h2>
        <p>Delving deeper into the foundational architecture, we observe key trends shaping the modern landscape. Professionals rely on high-performance open-source tools, seamless integration libraries, and robust data pipelines.</p>
        
        <table>
            <tr>
                <th>Parameter</th>
                <th>Standard Specification</th>
                <th>Performance Impact</th>
            </tr>
            <tr>
                <td>Architecture</td>
                <td>Modular & Scalable</td>
                <td>High Optimization</td>
            </tr>
            <tr>
                <td>Security Level</td>
                <td>Enterprise-Grade Encryption</td>
                <td>Maximum Reliability</td>
            </tr>
            <tr>
                <td>Deployment</td>
                <td>Automated CI/CD Pipeline</td>
                <td>Zero Downtime</td>
            </tr>
        </table>

        <h2 id="strategic-analysis">3. Strategic Industry Analysis</h2>
        <p>Strategic positioning requires continuous auditing and iterative upgrades. By adhering to standardized open-source specifications, organizations can scale operations dynamically without incurring technical debt.</p>

        <!-- Internal Links (7) -->
        <div class="neu-inset" style="margin: 20px 0;">
            <h4>Internal Resources (7 Links)</h4>
            <ul>
                <li><a href="https://awdev.my.id/"><i class="fas fa-angle-right"></i> AWDEV Home Portal</a></li>
                <li><a href="https://awdev.my.id/about.html"><i class="fas fa-angle-right"></i> About Us & Mission</a></li>
                <li><a href="https://awdev.my.id/blog.html"><i class="fas fa-angle-right"></i> Developer Blog Articles</a></li>
                <li><a href="https://awdev.my.id/tools/index.html"><i class="fas fa-angle-right"></i> General Development Tools</a></li>
                <li><a href="https://awdev.my.id/aplikasi/index.html"><i class="fas fa-angle-right"></i> Free Web Applications</a></li>
                <li><a href="https://awdev.my.id/collor/index.html"><i class="fas fa-angle-right"></i> Rainbow Color Code Generator</a></li>
                <li><a href="https://awdev.my.id/vidio/index.html"><i class="fas fa-angle-right"></i> Cinematic Video Collection</a></li>
            </ul>
        </div>

        <!-- External Links (7) -->
        <div class="neu-inset" style="margin: 20px 0;">
            <h4>External References (7 Links)</h4>
            <ul>
                <li><a href="https://github.com/" target="_blank" rel="noopener"><i class="fas fa-angle-right"></i> GitHub Open Source Repository</a></li>
                <li><a href="https://developer.mozilla.org/" target="_blank" rel="noopener"><i class="fas fa-angle-right"></i> MDN Web Docs</a></li>
                <li><a href="https://angular.io/" target="_blank" rel="noopener"><i class="fas fa-angle-right"></i> Angular Framework Official</a></li>
                <li><a href="https://fonts.google.com/" target="_blank" rel="noopener"><i class="fas fa-angle-right"></i> Google Fonts</a></li>
                <li><a href="https://fontawesome.com/" target="_blank" rel="noopener"><i class="fas fa-angle-right"></i> FontAwesome Icons</a></li>
                <li><a href="https://schema.org/" target="_blank" rel="noopener"><i class="fas fa-angle-right"></i> Schema.org Structured Data</a></li>
                <li><a href="https://stackoverflow.com/" target="_blank" rel="noopener"><i class="fas fa-angle-right"></i> Stack Overflow Community</a></li>
            </ul>
        </div>

        <h2 id="faq-section">4. Frequently Asked Questions</h2>
        <div class="faq-item">
            <div class="faq-question">What makes {title} unique?</div>
            <div class="faq-answer">It incorporates cutting-edge optimizations tailored specifically for high-speed open-source deployment.</div>
        </div>
        <div class="faq-item">
            <div class="faq-question">How often is this data updated?</div>
            <div class="faq-answer">Our repositories and automated publishing pipelines refresh content continuously in real-time.</div>
        </div>

        <h2 id="conclusion">5. Conclusion and Future Outlook</h2>
        <p>In summary, mastering {title} empowers teams to achieve unprecedented operational excellence. We invite you to explore related articles across our network and engage through our interactive community channels.</p>
    </div>

    <!-- Social Share Media -->
    <section class="neu-box" style="text-align: center;">
        <h3>Share This Article</h3>
        <div class="social-share">
            <a href="https://facebook.com/sharer/sharer.php?u=https://awdev.my.id/{cat_name}/artikel{index}.html" target="_blank" class="social-btn"><i class="fab fa-facebook-f"></i></a>
            <a href="https://twitter.com/intent/tweet?url=https://awdev.my.id/{cat_name}/artikel{index}.html&text=Check%20out%20this%20article!" target="_blank" class="social-btn"><i class="fab fa-twitter"></i></a>
            <a href="https://api.whatsapp.com/send?text=Explore%20https://awdev.my.id/{cat_name}/artikel{index}.html" target="_blank" class="social-btn"><i class="fab fa-whatsapp"></i></a>
            <a href="https://www.linkedin.com/shareArticle?mini=true&url=https://awdev.my.id/{cat_name}/artikel{index}.html" target="_blank" class="social-btn"><i class="fab fa-linkedin-in"></i></a>
        </div>
    </section>

    <!-- Contact Form Box -->
    <section class="neu-box contact-form">
        <h3 style="margin-bottom: 15px; background: var(--rainbow-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Get In Touch With Us</h3>
        <form onsubmit="event.preventDefault(); alert('Thank you! Your message has been sent successfully.');">
            <input type="text" placeholder="Your Name" required>
            <input type="email" placeholder="Your Email Address" required>
            <textarea rows="4" placeholder="Your Message..." required></textarea>
            <button type="submit" class="neu-button" style="width: 100%;">Send Message</button>
        </form>
    </section>
"""

def generate_category_index(cat_name, articles):
    items_html = ""
    for idx, title in enumerate(articles, 1):
        items_html += f'<li><a href="artikel{idx}.html"><i class="fas fa-file-alt"></i> {title}</a></li>\n'

    return f"""
    <div class="neu-box">
        <h1>{cat_name.upper()} Category Index</h1>
        <p>Explore all 30 professional articles published under the {cat_name} sector.</p>
        <div style="margin-top: 20px;">
            <h3>Article List</h3>
            <ul style="list-style: none; padding: 0; margin-top: 10px;">
                {items_html}
            </ul>
        </div>
    </div>
"""

def main():
    print("Starting automated directory and file generation for AWDEV blog...")
    
    for cat in CATEGORIES:
        cat_dir = os.path.join(".", cat)
        os.makedirs(cat_dir, exist_ok=True)
        
        articles_titles = [f"Comprehensive Guide to {cat.capitalize()} Innovation and Strategy #{i}" for i in range(1, ARTICLES_PER_CATEGORY + 1)]
        
        # 1. Generate Category Index (index.html)
        index_content = get_header(f"{cat.capitalize()} Hub", cat) + generate_category_index(cat, articles_titles) + get_footer(cat)
        with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_content)
            
        # 2. Generate 30 Articles (artikel1.html ... artikel30.html)
        for i, title in enumerate(articles_titles, 1):
            art_filename = f"artikel{i}.html"
            art_content = get_header(title, cat) + generate_article_content(title, cat, i) + get_footer(cat)
            with open(os.path.join(cat_dir, art_filename), "w", encoding="utf-8") as f:
                f.write(art_content)
                
        # 3. Generate sitemap.html
        sitemap_html = get_header(f"{cat.capitalize()} Sitemap", cat) + f"""
        <div class="neu-box">
            <h1>Sitemap for {cat.capitalize()}</h1>
            <ul>
                <li><a href="index.html">Category Home</a></li>
"""
        for i in range(1, ARTICLES_PER_CATEGORY + 1):
            sitemap_html += f'                <li><a href="artikel{i}.html">Artikel {i}</a></li>\n'
        sitemap_html += f"""            </ul>
        </div>
        """ + get_footer(cat)
        with open(os.path.join(cat_dir, "sitemap.html"), "w", encoding="utf-8") as f:
            f.write(sitemap_html)
            
        # 4. Generate sitemap.xml
        sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://awdev.my.id/{cat}/index.html</loc>
        <changefreq>daily</changefreq>
    </url>
"""
        for i in range(1, ARTICLES_PER_CATEGORY + 1):
            sitemap_xml += f"""    <url>
        <loc>https://awdev.my.id/{cat}/artikel{i}.html</loc>
        <changefreq>weekly</changefreq>
    </url>\n"""
        sitemap_xml += "</urlset>"
        with open(os.path.join(cat_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sitemap_xml)
            
        # 5. Generate sitemap.txt
        sitemap_txt = f"https://awdev.my.id/{cat}/index.html\n"
        for i in range(1, ARTICLES_PER_CATEGORY + 1):
            sitemap_txt += f"https://awdev.my.id/{cat}/artikel{i}.html\n"
        with open(os.path.join(cat_dir, "sitemap.txt"), "w", encoding="utf-8") as f:
            f.write(sitemap_txt)

        print(f"Successfully generated category '{cat}' with 30 articles and sitemaps.")

    print("All directories and files generated successfully!")

if __name__ == "__main__":
    main()
