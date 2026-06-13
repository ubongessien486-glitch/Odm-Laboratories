# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Diagnostic Title & Description
html = html.replace('<title>Oxygen Group | Diagnostic Lab, Home Care &amp; Training</title>', '<title>OMDL Group - Oxygen Medical Diagnostic Lab | Drug & Alcohol Testing</title>')
html = html.replace('Oxygen Group connects medical diagnostic testing, home care services, and professional training programs from one trusted Merrillville, Indiana group.', 'OMDL Group provides 24-hour drug and alcohol testing, DNA testing, comprehensive lab blood work, mobile testing services, and DOT/FMCSA consortium management.')

# Diagnostic canonical URL
html = html.replace('href="https://oxygendx.com/"', 'href="https://oxygendx.com/diagnostic.html"')

# Remove CLIA image from the logo bar
html = re.sub(r'<img[^>]*src="clia-certified\.png"[^>]*>', '', html)

diagnostic_hero = '''<!-- Hero Section -->
    <section class="hero" style="background: linear-gradient(135deg, #001f3f 0%, #003A70 60%, #0f2554 100%);">
        <div class="container hero-content">
            <div class="hero-badge" data-cms="hero.badge">DRUG AND ALCOHOL TEST</div>
            <h1 data-cms="hero.title" style="color: #ffffff; text-shadow: 0 2px 10px rgba(0,0,0,0.8);">BOOK FOR YOUR 24 HOURS DRUGS AND ALCOHOL TEST</h1>
            <p data-cms="hero.subtitle" style="color: #ffffff; text-shadow: 0 2px 8px rgba(0,0,0,0.8);">FAST, RELIABLE AND CONFIDENTIAL TEST. We provide nationwide services with a large collection site network.</p>
            <div class="hero-btns">
                <a href="booking.html" class="btn-primary">
                    Book Now
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </a>
                <a href="about.html" class="btn-outline">Learn More</a>
            </div>
        </div>
    </section>'''

html = re.sub(r'<!-- HERO -->.*?</section>', diagnostic_hero, html, flags=re.DOTALL)

# Remove extra index sections (Divisions, Gateway)
html = re.sub(r'<!-- Divisions Grid -->.*?<!-- Info Section -->', '<!-- Info Section -->', html, flags=re.DOTALL)

with open('diagnostic.html', 'w', encoding='utf-8') as out:
    out.write(html)
print("Diagnostic HTML rewritten cleanly.")
