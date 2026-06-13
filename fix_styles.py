import urllib.request
import re

url = 'https://oxygendx.com/styles.css'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
css = urllib.request.urlopen(req).read().decode('utf-8')

new_footer_css = """/* ─── FOOTER ─── */
footer {
  background: var(--navy-dark);
  color: rgba(255,255,255,0.8);
  padding: 60px 0 0;
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 40px;
  padding-bottom: 48px;
}
@media (max-width: 900px) { .footer-grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 600px) { .footer-grid { grid-template-columns: 1fr; } }
.footer-brand img {
  height: 56px;
  width: auto !important;
  max-width: 220px;
  object-fit: contain;
  object-position: left center;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.96);
  padding: 10px 14px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.footer-brand p { font-size: 15px; line-height: 1.6; color: rgba(255,255,255,0.9); max-width: 320px; }
.footer-col h4 { font-size: 15px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: var(--white); margin-bottom: 20px; }
.footer-col ul { display: flex; flex-direction: column; gap: 14px; }
.footer-col ul a { font-size: 15px; color: rgba(255,255,255,0.9); transition: color 0.2s; }
.footer-col ul a:hover { color: var(--teal); }
.footer-contact-item { display: flex; align-items: flex-start; gap: 12px; font-size: 15px; color: rgba(255,255,255,0.9); margin-bottom: 14px; line-height: 1.5; }
.footer-contact-item span:first-child { color: var(--teal); flex-shrink: 0; margin-top: 3px; font-size: 16px; }
.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.12);
  padding: 24px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 14px;
  color: rgba(255,255,255,0.7);
}

/* ─── MOBILE RESPONSIVE ─── */"""

# Replace the block
pattern = r'/\* ─── FOOTER ─── \*/.*?/\* ─── MOBILE RESPONSIVE ─── \*/'
css = re.sub(pattern, new_footer_css, css, flags=re.DOTALL)

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("SUCCESS: styles.css rewritten cleanly.")
