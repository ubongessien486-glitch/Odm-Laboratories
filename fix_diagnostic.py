import sys
with open('diagnostic.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('
          <a href="drug-free-workplace.html" style="background-color: #ffc439; color: #001f3f; padding: 5px 10px; border-radius: 5px; font-weight: bold;">Non-DOT Pricing List</a>', '')
content = content.replace('
                        <li><a href="drug-free-workplace.html" style="background-color: #ffc439; color: #001f3f; padding: 5px 10px; border-radius: 5px; font-weight: bold;">Non-DOT Pricing List</a></li>', '')

with open('diagnostic.html', 'w', encoding='utf-8') as f:
    f.write(content)
