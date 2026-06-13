import urllib.request
import re

base_url = 'https://oxygendx.com/'
pages = [
    'index.html', 'diagnostic.html', 'homecare.html', 'login.html', 
    'tpa.html', 'contact.html', 'blood-work.html', 'breath-alcohol.html', 
    'dna-testing.html', 'urine-test.html', 'styles.css', 'site-motion.js', 
    'site-data.js', 'supabase.js'
]

for page in pages:
    url = base_url + page
    if page == 'index.html':
        url = base_url
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read()
            if b'404 Not Found' in content or b'<title>404' in content:
                print(f"Skipped {page} (404)")
                continue
            with open(page, 'wb') as f:
                f.write(content)
            print(f"Downloaded {page}")
    except Exception as e:
        print(f"Failed {page}: {e}")

# Now find all images in these pages and download them
import glob
assets = set()
pattern = r'(?:src|href)=["\']([^"\'>\s]+\.(?:webp|jpg|jpeg|png|gif|svg|ico|woff2|woff|ttf))(?:[\?][^"\'>\s]+)?["\']'
for html_file in glob.glob('*.html'):
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
        assets.update(re.findall(pattern, html_content))

import os
import urllib.parse
for asset in assets:
    try:
        url = urllib.parse.urljoin(base_url, asset)
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.lstrip('/')
        local_path = os.path.join(*path.split('/'))
        dir_name = os.path.dirname(local_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded asset {asset}")
    except Exception as e:
        print(f"Failed to download {asset}: {e}")

