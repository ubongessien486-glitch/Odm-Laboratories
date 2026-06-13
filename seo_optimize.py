import os
import re

dir_path = r'C:\Users\LENOVO\.gemini\antigravity-ide\scratch\oxygendx'
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

# JSON-LD Schema for LocalBusiness
schema_markup = """
    <!-- JSON-LD LocalBusiness Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "MedicalOrganization",
      "name": "Oxygen Group",
      "url": "https://oxygendx.com",
      "logo": "https://oxygendx.com/oxygen-group-logo.svg",
      "description": "Medical diagnostic testing, home care services, and professional training programs in Merrillville, Indiana.",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Merrillville",
        "addressRegion": "IN",
        "addressCountry": "US"
      },
      "telephone": "+12193060674"
    }
    </script>
"""

for file in html_files:
    file_path = os.path.join(dir_path, file)
    
    # Try reading as utf-8, fallback to windows-1252
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='windows-1252') as f:
            html = f.read()

    # Extract title and description
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    desc_match = re.search(r'<meta name="description" content="(.*?)">', html, re.IGNORECASE | re.DOTALL)
    
    title = title_match.group(1).strip() if title_match else 'Oxygen Group'
    desc = desc_match.group(1).strip() if desc_match else 'Oxygen Group connects medical diagnostic testing and home care services.'
    
    # Check if OG tags already exist
    if 'property="og:title"' not in html:
        og_tags = f"""
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://oxygendx.com/{file}">
    <meta property="og:image" content="https://oxygendx.com/oxygen-group-logo.svg">
    <meta name="twitter:card" content="summary_large_image">
"""
        # Insert OG tags before </head>
        html = re.sub(r'(</head>)', og_tags + r'\1', html, flags=re.IGNORECASE)
        
    # Inject JSON-LD only on index.html
    if file == 'index.html' and 'application/ld+json' not in html:
        html = re.sub(r'(</head>)', schema_markup + r'\1', html, flags=re.IGNORECASE)
        
    # Add loading="lazy" to imgs that don't have it, ignoring hero-bg.webp
    def img_replacer(match):
        img_tag = match.group(0)
        if 'loading=' in img_tag or 'hero-bg' in img_tag or 'logo' in img_tag:
            return img_tag
        return img_tag.replace('<img ', '<img loading="lazy" decoding="async" ')
        
    html = re.sub(r'<img [^>]+>', img_replacer, html)
    
    # Write back as UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("SEO and performance optimization complete.")
