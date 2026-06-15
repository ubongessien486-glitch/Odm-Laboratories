import os
import re

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add loading="lazy" to imgs that don't have eager or lazy
        def add_lazy(match):
            img_tag = match.group(0)
            if 'loading=' not in img_tag:
                img_tag = img_tag.replace('<img ', '<img loading="lazy" decoding="async" ')
            return img_tag

        content = re.sub(r'<img[^>]+>', add_lazy, content)

        # Remove HTML comments (except schema/mobile menu markers if needed)
        # Actually it's safer to skip comment removal to avoid breaking layouts.

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

print("HTML lazy loading added.")

# CSS fixes
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('.mobile-menu {', '.mobile-menu {\n  overflow-y: auto;\n  padding-top: 40px;\n  padding-bottom: 40px;')
css = css.replace('.mobile-menu a {', '.mobile-menu a {\n  margin: 5px 0;')

# Update media queries for better fit
css = css.replace('@media (max-width: 480px) {', '@media (max-width: 480px) {\n  .stats-grid { grid-template-columns: 1fr; }\n  .mobile-menu a { font-size: 18px; padding: 10px 20px; }\n  .contact-grid { grid-template-columns: 1fr; }')

# Minify CSS slightly
css = re.sub(r'\s+', ' ', css)
css = re.sub(r'/\*.*?\*/', '', css)
css = css.replace(' { ', '{').replace(' } ', '}').replace(' ; ', ';')

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS optimized.")
