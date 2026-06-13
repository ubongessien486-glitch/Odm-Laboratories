import os
import re

nav_pattern = re.compile(r'(<li><a href="services\.html"(?: class="active")?>Services.*?</a></li>)')
mobile_pattern = re.compile(r'(<a href="services\.html"(?: class="active")?>Services.*?</a>)')

for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            if '<ul class="nav-links">' in content or 'mobile-menu' in content:
                content = nav_pattern.sub(r'\1\n                <li><a href="employment-testing.html">Employment Testing</a></li>', content)
                content = mobile_pattern.sub(r'\1\n        <a href="employment-testing.html">Employment Testing</a>', content)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(content)
                    print(f"Updated {filepath}")
