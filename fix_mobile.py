import os
import re

with open('drug-free-workplace.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix grid overflowing on mobile
content = content.replace('minmax(280px, 1fr)', 'minmax(240px, 1fr)')
content = content.replace('minmax(250px, 1fr)', 'minmax(220px, 1fr)')

# Add media query for better mobile card formatting and grid wrapping
mobile_fixes = '''
        /* MOBILE VIEW FIXES */
        @media (max-width: 480px) {
            .vibes-grid { grid-template-columns: 1fr; }
            .vibes-list { grid-template-columns: 1fr; }
            .dfwp-price-card__bottom { flex-wrap: wrap; flex-direction: column; text-align: center; align-items: stretch !important; gap: 12px !important; }
            .dfwp-pay-btn, .dfwp-inquiry-btn { width: 100% !important; text-align: center; justify-content: center; }
            .dfwp-why-grid { grid-template-columns: 1fr; }
            .vibes-title { font-size: 26px !important; }
            .dfwp-hero h1 { font-size: 28px !important; }
        }
'''

content = content.replace('/* MOBILE VIEW FIXES */', mobile_fixes)

# Clean up redundant stylesheet links
content = content.replace('<link rel="stylesheet" href="styles.css?v=5"><link rel="stylesheet" href="styles.css?v=5">', '')

with open('drug-free-workplace.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('minmax(280px, 1fr)', 'minmax(240px, 1fr)')
css = css.replace('minmax(300px, 1fr)', 'minmax(240px, 1fr)')

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Fixed mobile view overflowing and layouts.")
