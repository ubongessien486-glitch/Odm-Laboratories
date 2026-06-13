import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('diagnostic.html', 'r', encoding='utf-8') as f:
    diag_html = f.read()

# Grab Service 0 and Service 1 from index.html
match = re.search(r'(<!-- Service 0 \(New Employment Testing\) -->.*?<!-- Service 2 -->)', index_html, re.DOTALL)
if match:
    # Everything up to, but not including, <!-- Service 2 -->
    extracted = match.group(1).replace('<!-- Service 2 -->', '')
    
    # Insert it right before <!-- Service 2 --> in diagnostic.html
    new_diag = diag_html.replace('<!-- Service 2 -->', extracted + '<!-- Service 2 -->')
    
    with open('diagnostic.html', 'w', encoding='utf-8') as out:
        out.write(new_diag)
    print("Success inserting services")
else:
    print("Could not find services in index")
